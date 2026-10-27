#!/usr/bin/env python3
"""Unit economics for founder-cfo. Standard library only, no network.

Takes one JSON file describing the business and prints the numbers a CFO would
check before a single dollar is spent: what one unit earns, the real margin at
the volume you plan, how many units a day you need to break even, what year 1
looks like month by month, and how long it takes to earn the startup money back.

    python3 unit_economics.py founder/numbers.json
    python3 unit_economics.py founder/numbers.json --out founder/cfo.md
    python3 unit_economics.py founder/numbers.json --json
    python3 unit_economics.py founder/numbers.json --price 7.00 --volume 0.8

The input (see example.json in this folder):

    business          name, for the report
    unit              what you sell one of: "cup", "order", "client-month"
    price             price per unit, before tax
    variable          [{label, cost}]  cost of ONE unit: ingredients, packaging,
                      shipping, card fees, a per-unit commission
    fixed_monthly     [{label, cost}]  costs you pay every month whatever you sell:
                      rent, salaries, software, insurance
    startup           [{label, cost}]  one-off spend before you open
    days_per_month    selling days in a month (default 30)
    capacity_per_day  the most units a day you can physically sell (optional)
    plan_per_day      the volume you plan for once you are up and running
    ramp_per_day      12 numbers: units a day in each month of year 1
                      (optional; default = plan_per_day every month)

Every number in the report comes from that file. Nothing is looked up or
guessed. If a field is missing the tool says so instead of filling it in.

--price and --volume run a what-if without editing the file: --price replaces
the price, --volume scales every volume (0.8 = 20 percent fewer sales).
"""

import argparse
import json
import math
import sys


class NumbersError(ValueError):
    pass


def _money(v):
    sign = "-" if v < 0 else ""
    return "%s$%s" % (sign, "{:,.2f}".format(abs(v)))


def _whole(v):
    sign = "-" if v < 0 else ""
    return "%s$%s" % (sign, "{:,.0f}".format(abs(round(v))))


def _number(value, field, positive=False):
    if isinstance(value, bool):
        raise NumbersError("%s must be a finite number" % field)
    try:
        out = float(value)
    except (TypeError, ValueError):
        raise NumbersError("%s must be a finite number" % field)
    if not math.isfinite(out) or out < 0 or (positive and out == 0):
        raise NumbersError("%s must be finite and %s" % (field, "above zero" if positive else "nonnegative"))
    return out


def _sum(items, field):
    total = 0.0
    if items is not None and not isinstance(items, list):
        raise NumbersError("%s must be a list" % field)
    for i, it in enumerate(items or []):
        if not isinstance(it, dict) or "cost" not in it:
            raise NumbersError("%s[%d] needs a 'cost'" % (field, i))
        try:
            total += _number(it["cost"], "%s[%d].cost" % (field, i))
        except (TypeError, ValueError):
            raise NumbersError("%s[%d].cost is not a number: %r" % (field, i, it["cost"]))
    return total


def load(path):
    try:
        with open(path, encoding="utf-8") as fh:
            return json.load(fh)
    except FileNotFoundError:
        raise NumbersError("no such file: %s" % path)
    except json.JSONDecodeError as e:
        raise NumbersError("%s is not valid JSON: %s" % (path, e))


def analyse(spec, price=None, volume=1.0):
    """Return a dict of every number in the report. Pure function, easy to test."""
    if not isinstance(spec, dict):
        raise NumbersError("numbers must be a JSON object")
    volume = _number(volume, "volume")
    if "price" not in spec and price is None:
        raise NumbersError("'price' is missing")
    p = _number(price if price is not None else spec["price"], "price", positive=True)
    if p <= 0:
        raise NumbersError("price must be above zero")
    days = _number(spec.get("days_per_month", 30), "days_per_month", positive=True)
    var = _sum(spec.get("variable"), "variable")
    fixed = _sum(spec.get("fixed_monthly"), "fixed_monthly")
    startup = _sum(spec.get("startup"), "startup")

    if "plan_per_day" not in spec and "ramp_per_day" not in spec:
        raise NumbersError("give 'plan_per_day' or 'ramp_per_day' (12 numbers)")
    plan = _number(spec.get("plan_per_day", 0), "plan_per_day") * volume
    ramp = spec.get("ramp_per_day")
    if ramp is None:
        ramp = [plan] * 12
    else:
        if not isinstance(ramp, list):
            raise NumbersError("ramp_per_day must be a list of 12 numbers")
        if len(ramp) != 12:
            raise NumbersError("'ramp_per_day' needs 12 numbers, one per month (got %d)" % len(ramp))
        ramp = [_number(v, "ramp_per_day") * volume for v in ramp]
    if not plan:
        plan = ramp[-1]

    contribution = p - var
    contribution_pct = contribution / p
    breakeven_day = math.inf if contribution <= 0 else fixed / (contribution * days)
    plan_units_month = plan * days
    margin_at_plan = (contribution - (fixed / plan_units_month if plan_units_month else math.inf)) / p

    months = []
    cumulative = -startup
    payback_month = None
    for m, per_day in enumerate(ramp, start=1):
        units = per_day * days
        revenue = units * p
        variable_cost = units * var
        profit = revenue - variable_cost - fixed
        cumulative += profit
        if payback_month is None and cumulative >= 0:
            payback_month = m
        months.append({"month": m, "per_day": per_day, "units": units, "revenue": revenue,
                       "variable": variable_cost, "fixed": fixed, "profit": profit,
                       "cumulative": cumulative})
    year_profit = sum(m["profit"] for m in months)
    year_revenue = sum(m["revenue"] for m in months)
    # the cash you need: startup plus the deepest hole the monthly losses dig
    lowest = min([-startup] + [m["cumulative"] for m in months])
    cash_needed = -lowest

    capacity = spec.get("capacity_per_day")
    if capacity is not None:
        capacity = _number(capacity, "capacity_per_day")
    flags = []
    if contribution <= 0:
        flags.append("Each unit loses money before rent and salaries: the price is below the variable cost.")
    if capacity is not None and breakeven_day > float(capacity):
        flags.append("Break-even needs %.0f %ss a day but capacity is %s." % (breakeven_day, spec.get("unit", "unit"), capacity))
    if capacity is not None and plan > float(capacity):
        flags.append("The plan (%.0f a day) is above capacity (%s)." % (plan, capacity))
    if year_profit < 0:
        flags.append("Year 1 loses money on operations (%s)." % _whole(year_profit))
    if payback_month is None:
        flags.append("The startup spend is not earned back within year 1.")

    return {
        "business": spec.get("business", ""), "unit": spec.get("unit", "unit"),
        "price": p, "variable_per_unit": var, "contribution": contribution,
        "contribution_pct": contribution_pct, "fixed_monthly": fixed, "startup": startup,
        "plan_per_day": plan, "margin_at_plan": margin_at_plan, "breakeven_per_day": breakeven_day,
        "capacity_per_day": capacity, "year1_revenue": year_revenue, "year1_profit": year_profit,
        "year1_after_startup": year_profit - startup, "payback_month": payback_month,
        "cash_needed": cash_needed, "months": months, "flags": flags,
        "variable_items": spec.get("variable", []), "fixed_items": spec.get("fixed_monthly", []),
        "startup_items": spec.get("startup", []),
    }


def sensitivity(spec):
    """The three what-ifs every plan should survive."""
    base = analyse(spec)
    rows = [("Base plan", base)]
    rows.append(("Price -10%", analyse(spec, price=base["price"] * 0.9)))
    rows.append(("Volume -20%", analyse(spec, volume=0.8)))
    worse = json.loads(json.dumps(spec))
    for it in worse.get("variable", []):
        it["cost"] = float(it["cost"]) * 1.15
    rows.append(("Unit costs +15%", analyse(worse)))
    return rows


def report(spec, a):
    u = a["unit"]
    L = []
    L.append("# Unit economics: %s" % (a["business"] or "your business"))
    L.append("")
    L.append("Conditional scenario from the input file. No demand, costs or viability are independently verified; omitted costs remain omitted.")
    L.append("")
    L.append("## One %s" % u)
    L.append("")
    L.append("| line | per %s |" % u)
    L.append("| --- | ---: |")
    L.append("| Price | %s |" % _money(a["price"]))
    for it in a["variable_items"]:
        L.append("| %s | -%s |" % (it.get("label", "cost"), _money(float(it["cost"]))))
    L.append("| **Contribution** (what each %s leaves to pay the fixed costs) | **%s** (%.0f%%) |"
             % (u, _money(a["contribution"]), a["contribution_pct"] * 100))
    L.append("")
    L.append("## The margin that matters")
    L.append("")
    L.append("Fixed costs: %s a month (%s)." % (_whole(a["fixed_monthly"]), ", ".join(
        "%s %s" % (it.get("label", "cost"), _whole(float(it["cost"]))) for it in a["fixed_items"]) or "none given"))
    L.append("")
    be = a["breakeven_per_day"]
    L.append("- **Break-even: %s %ss a day.** Below that you lose money every month." % (
        "never (each unit loses money)" if math.isinf(be) else "{:,.0f}".format(math.ceil(be)), u))
    L.append("- **Profit margin at your plan** (%s a day): **%.0f%%** of every sale, after the entered variable and fixed costs." % (
        "{:,.0f}".format(a["plan_per_day"]), a["margin_at_plan"] * 100))
    if a["capacity_per_day"] is not None:
        L.append("- Capacity: %s a day." % a["capacity_per_day"])
    L.append("")
    L.append("## Year 1, month by month")
    L.append("")
    L.append("| month | %ss a day | revenue | profit | cumulative (after %s startup) |" % (u, _whole(a["startup"])))
    L.append("| ---: | ---: | ---: | ---: | ---: |")
    for m in a["months"]:
        L.append("| %d | %s | %s | %s | %s |" % (m["month"], "{:,.0f}".format(m["per_day"]), _whole(m["revenue"]),
                                             _whole(m["profit"]), _whole(m["cumulative"])))
    L.append("")
    L.append("- **Year 1 operating profit: %s** on %s of revenue." % (_whole(a["year1_profit"]), _whole(a["year1_revenue"])))
    L.append("- After the %s startup spend: %s." % (_whole(a["startup"]), _whole(a["year1_after_startup"])))
    L.append("- Startup money earned back: %s." % ("month %d" % a["payback_month"] if a["payback_month"] else "not within year 1"))
    L.append("- Cash you need before it pays for itself: **%s**." % _whole(a["cash_needed"]))
    L.append("")
    L.append("## What if")
    L.append("")
    L.append("| scenario | margin at plan | break-even a day | year 1 profit |")
    L.append("| --- | ---: | ---: | ---: |")
    for name, s in sensitivity(spec):
        be = s["breakeven_per_day"]
        L.append("| %s | %.0f%% | %s | %s |" % (name, s["margin_at_plan"] * 100,
                                              "never" if math.isinf(be) else "{:,.0f}".format(math.ceil(be)),
                                              _whole(s["year1_profit"])))
    L.append("")
    if a["flags"]:
        L.append("## Red flags")
        L.append("")
        for f in a["flags"]:
            L.append("- %s" % f)
    else:
        L.append("No red flags in these numbers. They are only as good as the inputs: check every cost against a real quote.")
    return "\n".join(L) + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("numbers", help="the business's numbers.json")
    ap.add_argument("--out", help="write the report here (markdown)")
    ap.add_argument("--json", action="store_true", help="print the numbers as JSON")
    ap.add_argument("--price", type=float, help="what-if price")
    ap.add_argument("--volume", type=float, default=1.0, help="what-if volume multiplier")
    args = ap.parse_args(argv)
    try:
        spec = load(args.numbers)
        if args.price is not None:
            spec = dict(spec, price=args.price)
        if args.volume != 1.0:
            spec = dict(spec)
            if "plan_per_day" in spec:
                spec["plan_per_day"] = _number(spec["plan_per_day"], "plan_per_day") * _number(args.volume, "volume")
            if "ramp_per_day" in spec:
                spec["ramp_per_day"] = [_number(v, "ramp_per_day") * _number(args.volume, "volume") for v in spec["ramp_per_day"]]
        a = analyse(spec)
    except NumbersError as e:
        print("error: %s" % e, file=sys.stderr)
        return 2
    if args.json:
        out = {k: v for k, v in a.items() if not k.endswith("_items")}
        out["breakeven_per_day"] = None if math.isinf(out["breakeven_per_day"]) else out["breakeven_per_day"]
        print(json.dumps(out, indent=1))
        return 0
    text = report(spec, a)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as fh:
            fh.write(text)
        print("wrote %s" % args.out)
    else:
        sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
