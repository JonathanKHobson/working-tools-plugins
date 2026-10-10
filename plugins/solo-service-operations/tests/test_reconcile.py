import copy
import importlib.util
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location("reconcile", Path(__file__).parents[1] / "scripts/reconcile.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class ReconciliationTests(unittest.TestCase):
    def setUp(self):
        self.invoice = {"invoice_id": "I1", "customer_id": "C1", "amount": "600.00", "currency": "USD", "source_ref": "fixture-invoice:1"}
        self.payment = {"payment_id": "P1", "customer_id": "C1", "amount": "250.00", "currency": "USD", "source_ref": "fixture-bank:1", "status": "settled", "settled_on": "2026-09-30", "allocations": [{"invoice_id": "I1", "amount": "250.00"}]}
        self.data = {"as_of": "2026-10-01", "invoices": [self.invoice], "payments": [self.payment]}

    def run_case(self):
        return module.reconcile(copy.deepcopy(self.data))

    def test_partial_and_multiple_payments(self):
        result = self.run_case()["invoices"][0]
        self.assertEqual((result["status"], result["remaining"]), ("partial", "350.00"))
        p2 = copy.deepcopy(self.payment)
        p2.update(payment_id="P2", amount="350.00", allocations=[{"invoice_id": "I1", "amount": "350.00"}])
        self.data["payments"].append(p2)
        self.assertEqual(self.run_case()["invoices"][0]["status"], "matched-paid")

    def test_pending_and_future_not_counted(self):
        for changes in [{"status": "pending"}, {"settled_on": "2026-10-02"}, {"status": "reversed"}]:
            original = copy.deepcopy(self.payment)
            self.payment.update(changes)
            self.assertEqual(self.run_case()["invoices"][0]["remaining"], "600.00")
            self.payment.clear(); self.payment.update(original)

    def test_identity_and_currency_mismatches_unapplied(self):
        for key, value in [("customer_id", "C2"), ("currency", "EUR")]:
            original = self.payment[key]; self.payment[key] = value
            result = self.run_case()
            self.assertEqual(result["invoices"][0]["status"], "open")
            self.assertEqual(result["exceptions"][-1]["amount"], "250.00")
            self.payment[key] = original

    def test_no_allocation_and_unknown_invoice(self):
        for allocations in [[], [{"invoice_id": "unknown", "amount": "250.00"}]]:
            self.payment["allocations"] = allocations
            self.assertEqual(self.run_case()["invoices"][0]["status"], "open")

    def test_overpayment_visible(self):
        self.payment.update(amount="650", allocations=[{"invoice_id": "I1", "amount": "650"}])
        result = self.run_case()["invoices"][0]
        self.assertEqual((result["status"], result["remaining"]), ("overpaid", "-50.00"))

    def test_duplicate_source_ids_fail(self):
        self.data["payments"].append(copy.deepcopy(self.payment))
        with self.assertRaises(ValueError): self.run_case()
        self.data["payments"].pop()
        self.data["invoices"].append(copy.deepcopy(self.invoice))
        with self.assertRaises(ValueError): self.run_case()

    def test_overallocation_and_duplicate_allocations_fail(self):
        for allocations in [[{"invoice_id":"I1", "amount":"251"}], [{"invoice_id":"I1", "amount":"100"}, {"invoice_id":"I1", "amount":"100"}]]:
            self.payment["allocations"] = allocations
            with self.assertRaises(ValueError): self.run_case()

    def test_invalid_money_fails(self):
        for value in ["NaN", "Infinity", "-1", "0", "1e3", 250.0]:
            self.payment["amount"] = value
            with self.assertRaises(ValueError): self.run_case()

    def test_exact_decimal_and_split_allocations(self):
        self.invoice["amount"] = "0.30"
        i2 = dict(self.invoice, invoice_id="I2", amount="0.20")
        self.data["invoices"].append(i2)
        self.payment.update(amount="0.50", allocations=[{"invoice_id":"I1", "amount":"0.30"}, {"invoice_id":"I2", "amount":"0.20"}])
        self.assertTrue(all(i["status"] == "matched-paid" for i in self.run_case()["invoices"]))

    def test_wide_decimal_range_preserves_small_allocation(self):
        self.invoice["amount"] = "100000000000000000000000"
        self.payment.update(amount="0.000000000000000000001", allocations=[{"invoice_id":"I1", "amount":"0.000000000000000000001"}])
        self.assertEqual(self.run_case()["invoices"][0]["remaining"], "99999999999999999999999.999999999999999999999")

    def test_unapplied_summary_does_not_double_count_or_mix_currency(self):
        self.payment["allocations"] = [{"invoice_id": "unknown", "amount": "250.00"}]
        self.data["payments"].append(dict(self.payment, payment_id="P2", currency="EUR", amount="40", allocations=[]))
        self.data["payments"].append(dict(self.payment, payment_id="P3", status="pending"))
        result = self.run_case()
        self.assertEqual(result["unapplied_settled_by_currency"], {"USD": "250.00", "EUR": "40"})
        self.assertTrue(all(x["additive"] is False for x in result["exceptions"]))

    def test_input_untouched(self):
        original = copy.deepcopy(self.data)
        module.reconcile(self.data)
        self.assertEqual(self.data, original)


if __name__ == "__main__":
    unittest.main()
