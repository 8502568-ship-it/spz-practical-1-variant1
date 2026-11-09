"""Sales analytics helpers with a backwards-compatible public API."""

ZERO = 0.0
PERCENT_MULTIPLIER = 100.0
CANCELLED_STATUS = "cancelled"


def calculate_growth(current: float, previous: float) -> float:
    """Return percentage growth; return zero when the previous value is zero."""
    if previous == ZERO:
        return ZERO
    return ((current - previous) / previous) * PERCENT_MULTIPLIER


def _calculate_discount(order: dict, apply_discount: bool) -> float:
    """Return the discount for an order when discount processing is enabled."""
    if not apply_discount:
        return ZERO
    return float(order.get("discount", ZERO))


def _calculate_order_amount(order: dict, discount: float) -> float:
    """Return the order amount after applying its discount."""
    return float(order.get("amount", ZERO)) - discount


def _calculate_tax(amount: float, tax_rate: float) -> float:
    """Calculate tax for an order amount."""
    return amount * float(tax_rate)


def _build_processed_order(order: dict, apply_discount: bool) -> tuple[dict, float, float]:
    """Build the normalized report row and return its discount and tax."""
    discount = _calculate_discount(order, apply_discount)
    amount = _calculate_order_amount(order, discount)
    tax = _calculate_tax(amount, order.get("tax_rate", ZERO))
    processed_order = {
        "id": order.get("id"),
        "amount": amount,
        "tax": tax,
        "status": order.get("status"),
    }
    return processed_order, discount, tax


def _build_summary(
    processed: list[dict],
    cancelled: list[dict],
    total_revenue: float,
    total_discount: float,
    total_tax: float,
) -> dict:
    """Assemble the public analytics report."""
    average = total_revenue / len(processed) if processed else ZERO
    return {
        "processed": processed,
        "cancelled": cancelled,
        "total_revenue": total_revenue,
        "total_discount": total_discount,
        "total_tax": total_tax,
        "average_order": average,
    }


def build_analytics_report(
    orders: list[dict],
    include_cancelled: bool = False,
    apply_discount: bool = False,
) -> dict:
    """Build a report while keeping filtering, calculations and formatting separate."""
    processed = []
    cancelled = []
    total_revenue = ZERO
    total_discount = ZERO
    total_tax = ZERO

    for order in orders:
        if order.get("status") == CANCELLED_STATUS:
            cancelled.append(order)
            if include_cancelled:
                processed.append(order)
            continue

        processed_order, discount, tax = _build_processed_order(order, apply_discount)
        processed.append(processed_order)
        total_discount += discount
        total_tax += tax
        total_revenue += processed_order["amount"]

    return _build_summary(
        processed,
        cancelled,
        total_revenue,
        total_discount,
        total_tax,
    )
