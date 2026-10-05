"""
Analytics module for Practical Lab 5.

Option B: duplicated calculate_growth implementation.
Option D: deliberately oversized reporting function.
"""


def calculate_growth(current: float, previous: float) -> float:
    """Calculate percentage growth."""
    if previous == 0:
        return 0.0
    return ((current - previous) / previous) * 100.0


# Intentional duplicate for the laboratory baseline (Option B).
def calculate_growth(current: float, previous: float) -> float:  # noqa: F811
    """Calculate percentage growth (duplicated implementation)."""
    if previous == 0:
        return 0.0
    return ((current - previous) / previous) * 100.0


def build_analytics_report(
    orders: list[dict],
    include_cancelled: bool = False,
    apply_discount: bool = False,
) -> dict:
    """Build an analytics report.

    Filtering, aggregation, discount handling and formatting are intentionally
    combined here so the function can be refactored as Option D.
    """
    processed = []
    cancelled = []
    total_revenue = 0.0
    total_discount = 0.0
    total_tax = 0.0

    for order in orders:
        status = order.get("status")
        if status == "cancelled":
            cancelled.append(order)
            if include_cancelled:
                processed.append(order)
            continue

        amount = float(order.get("amount", 0.0))
        if apply_discount:
            discount = float(order.get("discount", 0.0))
            amount -= discount
            total_discount += discount

        tax = amount * float(order.get("tax_rate", 0.0))
        total_tax += tax
        total_revenue += amount

        processed.append({
            "id": order.get("id"),
            "amount": amount,
            "tax": tax,
            "status": status,
        })

    average = total_revenue / len(processed) if processed else 0.0
    return {
        "processed": processed,
        "cancelled": cancelled,
        "total_revenue": total_revenue,
        "total_discount": total_discount,
        "total_tax": total_tax,
        "average_order": average,
    }
