"""Regression tests for the refactored analytics module."""

import pytest

from analytics import build_analytics_report, calculate_growth


def test_growth_is_calculated_as_percentage():
    assert calculate_growth(120, 100) == 20.0


def test_growth_with_zero_previous_value_is_zero():
    assert calculate_growth(120, 0) == 0.0


def test_growth_supports_negative_values():
    assert calculate_growth(80, 100) == -20.0


def test_report_calculates_revenue_tax_and_average():
    report = build_analytics_report([
        {"id": 1, "amount": 100, "tax_rate": 0.2, "status": "paid"},
        {"id": 2, "amount": 50, "tax_rate": 0.1, "status": "paid"},
    ])
    assert report["total_revenue"] == 150
    assert report["total_tax"] == 25
    assert report["average_order"] == 75
    assert len(report["processed"]) == 2


def test_report_applies_discount_before_tax():
    report = build_analytics_report(
        [{"id": 1, "amount": 100, "discount": 10, "tax_rate": 0.2, "status": "paid"}],
        apply_discount=True,
    )
    assert report["total_revenue"] == 90
    assert report["total_discount"] == 10
    assert report["total_tax"] == 18


def test_report_does_not_apply_discount_when_disabled():
    report = build_analytics_report(
        [{"id": 1, "amount": 100, "discount": 10, "tax_rate": 0.2, "status": "paid"}]
    )
    assert report["total_revenue"] == 100
    assert report["total_discount"] == 0


def test_cancelled_orders_are_separated_and_excluded_from_totals():
    cancelled = {"id": 2, "amount": 75, "status": "cancelled"}
    report = build_analytics_report([
        {"id": 1, "amount": 100, "tax_rate": 0.2, "status": "paid"},
        cancelled,
    ])
    assert report["cancelled"] == [cancelled]
    assert report["processed"][0]["id"] == 1
    assert report["total_revenue"] == 100
    assert report["total_tax"] == 20


def test_cancelled_orders_can_be_included_in_processed_list():
    cancelled = {"id": 2, "amount": 75, "status": "cancelled"}
    report = build_analytics_report([cancelled], include_cancelled=True)
    assert report["processed"] == [cancelled]
    assert report["cancelled"] == [cancelled]
    assert report["average_order"] == 0


def test_empty_report_has_zero_totals_and_average():
    report = build_analytics_report([])
    assert report == {
        "processed": [],
        "cancelled": [],
        "total_revenue": 0.0,
        "total_discount": 0.0,
        "total_tax": 0.0,
        "average_order": 0.0,
    }


@pytest.mark.parametrize(
    ("amount", "tax_rate", "expected_tax"),
    [(0, 0.2, 0), (25, 0, 0), (100, 0.05, 5)],
)
def test_tax_edge_cases(amount, tax_rate, expected_tax):
    report = build_analytics_report([
        {"id": 1, "amount": amount, "tax_rate": tax_rate, "status": "paid"}
    ])
    assert report["total_tax"] == expected_tax
