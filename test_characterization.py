# test_characterization.py
# Characterization / acceptance tests for CR-2024-0001 (variant 1).
# "Insurance net" for the change to src/process.py -> proc().
#
# Dataset: db.DataManager._get_test_data() built-in test data
# (order id=104, user_id=1, amount=350.0, status='cancelled').
#
# History:
#   - Before the fix, `test_cancelled_order_amount_is_zeroed_out_BUG`
#     PASSED (it documented the defect: amount was reset to 0).
#   - After the fix (Modify step, CR-2024-0001), that test is replaced
#     by `test_cancelled_order_keeps_original_amount_FIXED`, which
#     encodes the CR's acceptance criterion: cancelled orders keep the
#     original order amount instead of reporting 0.
#   - All other tests below are the untouched characterization baseline
#     and must keep passing before AND after the fix (regression guard
#     for the "principle of minimality").
#
# Run:
#   pytest test_characterization.py -v

import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from src.process import proc


def _get_order(result, order_id):
    for o in result["orders"]:
        if o["order_id"] == order_id:
            return o
    raise AssertionError(f"order {order_id} not found in result")


class TestCancelledOrderCharacterization:
    """Locks in the CURRENT (defective) behaviour of proc() for the
    'cancelled' branch, before CR-2024-0001 is implemented."""

    def test_cancelled_order_is_present_and_marked_cancelled(self):
        result = proc()
        order = _get_order(result, 104)
        assert order["status"] == "cancelled"

    def test_cancelled_order_amount_is_zeroed_out_BUG(self):
        # CURRENT (buggy) behaviour: the original order amount (350.0)
        # is discarded and replaced with 0, even though the source data
        # has amount=350.0. This is exactly the defect described in the
        # CR: the analytics department cannot see the original order
        # value for loss reporting.
        order = _get_order(proc(), 104)
        assert order["amount"] == 0

    def test_cancelled_order_has_no_tax_or_discount_fields(self):
        # Untouched by CR-2024-0001 - must remain true after the fix.
        order = _get_order(proc(), 104)
        assert "tax" not in order
        assert "discount" not in order
        assert "net" not in order

    def test_summary_counts_and_revenue_unaffected_by_cancelled_orders(self):
        # Cancelled orders must not contribute to total_revenue / total_tax
        # (only 'paid' orders do) - this must remain true after the fix.
        result = proc()
        summary = result["summary"]
        assert summary["cancelled"] == 1
        assert summary["processed"] == 2
        assert summary["pending"] == 1
        assert summary["total_revenue"] == 1385.0
        assert summary["total_tax"] == 255.0

    def test_paid_and_pending_orders_are_untouched_by_the_change_area(self):
        # Regression guard for the rest of proc() - out of scope for the CR.
        result = proc()
        paid_order = _get_order(result, 101)
        assert paid_order["amount"] == 500.0
        assert paid_order["status"] == "processed"

        pending_order = _get_order(result, 103)
        assert pending_order["amount"] == 80.0
        assert pending_order["status"] == "pending"


if __name__ == "__main__":
    import pytest
    raise SystemExit(pytest.main([__file__, "-v"]))