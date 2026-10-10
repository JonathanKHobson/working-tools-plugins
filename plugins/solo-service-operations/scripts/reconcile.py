#!/usr/bin/env python3
"""Check explicit invoice allocations; read one JSON file, write JSON to stdout."""
import argparse
from datetime import date
from decimal import Decimal, InvalidOperation, localcontext
import json
import re
import sys


def text(row, key):
    value = row.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{key} must be a nonempty string")
    return value


def amount(row):
    value = text(row, "amount")
    if not re.fullmatch(r"[0-9]+(?:\.[0-9]+)?", value) or len(value) > 24:
        raise ValueError("amount must be a positive decimal string, at most 24 characters")
    try:
        result = Decimal(value)
    except InvalidOperation as exc:
        raise ValueError("invalid amount") from exc
    if result <= 0:
        raise ValueError("amount must be positive; credits/refunds need separate source review")
    return result


def currency(row):
    value = text(row, "currency")
    if not re.fullmatch(r"[A-Z]{3}", value):
        raise ValueError("currency must be a three-letter uppercase code")
    return value


def _reconcile(data):
    as_of = date.fromisoformat(text(data, "as_of"))
    invoices, paid, payment_ids, exceptions = {}, {}, set(), []
    unapplied_by_currency = {}
    for row in data["invoices"]:
        iid = text(row, "invoice_id")
        if iid in invoices:
            raise ValueError(f"duplicate invoice ID: {iid}")
        invoices[iid] = {"invoice_id": iid, "customer_id": text(row, "customer_id"),
                         "currency": currency(row), "amount": amount(row),
                         "source_ref": text(row, "source_ref")}
        paid[iid] = Decimal(0)
    for row in data["payments"]:
        pid = text(row, "payment_id")
        if pid in payment_ids:
            raise ValueError(f"duplicate payment ID: {pid}")
        payment_ids.add(pid)
        total, cur = amount(row), currency(row)
        customer, source = text(row, "customer_id"), text(row, "source_ref")
        status = text(row, "status")
        if status not in {"settled", "pending", "failed", "reversed"}:
            raise ValueError(f"unknown payment status: {status}")
        allocations = row.get("allocations", [])
        if not isinstance(allocations, list):
            raise ValueError("allocations must be a list")
        parsed = [(text(a, "invoice_id"), amount(a)) for a in allocations]
        if len({i for i, _ in parsed}) != len(parsed):
            raise ValueError(f"duplicate allocation for payment: {pid}")
        if sum((a for _, a in parsed), Decimal(0)) > total:
            raise ValueError(f"allocations exceed payment: {pid}")
        def flag(reason, value=total, invoice_id=None):
            exceptions.append({"payment_id": pid, "invoice_id": invoice_id,
                               "reason": reason, "amount": format(value, "f"), "additive": False,
                               "currency": cur, "source_ref": source})
        if status != "settled":
            flag("not_settled:" + status)
            continue
        settled_on = date.fromisoformat(text(row, "settled_on"))
        if settled_on > as_of:
            flag("after_cutoff")
            continue
        applied = Decimal(0)
        for iid, value in parsed:
            invoice = invoices.get(iid)
            reason = ("unknown_invoice" if invoice is None else
                      "currency_mismatch" if invoice["currency"] != cur else
                      "customer_mismatch" if invoice["customer_id"] != customer else None)
            if reason:
                flag(reason, value, iid)
            else:
                paid[iid] += value
                applied += value
        # This total includes invalid allocation amounts; exceptions are not additive.
        if applied < total:
            flag("total_unapplied", total - applied)
            unapplied_by_currency[cur] = unapplied_by_currency.get(cur, Decimal(0)) + total - applied
    rows = []
    for iid, row in invoices.items():
        remaining = row["amount"] - paid[iid]
        state = ("open" if paid[iid] == 0 else "partial" if remaining > 0 else
                 "matched-paid" if remaining == 0 else "overpaid")
        rows.append({**row, "amount": format(row["amount"], "f"),
                     "settled_allocated": format(paid[iid], "f"),
                     "remaining": format(remaining, "f"), "status": state})
    return {"as_of": as_of.isoformat(), "basis": "supplied explicit settled allocations only",
            "invoices": rows, "exceptions": exceptions,
            "unapplied_settled_by_currency": {cur: format(value, "f") for cur, value in sorted(unapplied_by_currency.items())},
            "exceptions_note": "Reason details and total_unapplied overlap; do not sum all exception rows."}


def reconcile(data):
    if not isinstance(data, dict) or not all(isinstance(data.get(k), list) for k in ("invoices", "payments")):
        raise ValueError("input requires invoices and payments arrays")
    if len(data["invoices"]) + len(data["payments"]) > 10000:
        raise ValueError("input exceeds the 10000-record review limit")
    if sum(len(p.get("allocations", [])) for p in data["payments"]) > 50000:
        raise ValueError("input exceeds the 50000-allocation review limit")
    with localcontext() as context:
        context.prec = 64
        return _reconcile(data)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", help="Prepared private JSON input; input is never modified")
    args = parser.parse_args()
    try:
        with open(args.input, encoding="utf-8") as stream:
            data = json.load(stream)
        if not isinstance(data, dict) or not all(isinstance(data.get(k), list) for k in ("invoices", "payments")):
            raise ValueError("input requires invoices and payments arrays")
        print(json.dumps(reconcile(data), indent=2))
    except (OSError, ValueError, KeyError, TypeError, AttributeError) as exc:
        print(f"Invalid reconciliation input: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
