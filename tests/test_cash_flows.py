from datetime import date

from bond_pricer.cashflows import (
    add_months,
    generate_cash_flows,
    get_future_cash_flows,
)
from bond_pricer.models import Bond


def make_bond() -> Bond:
    return Bond(
        issue_date=date(2024, 1, 1),
        maturity_date=date(2029, 1, 1),
        face_value=1000,
        annual_coupon_rate=0.05,
        payments_per_year=2,
    )


def test_add_months() -> None:
    assert add_months(date(2024, 1, 1), 6) == date(2024, 7, 1)


def test_full_schedule_contains_ten_payments() -> None:
    flows = generate_cash_flows(make_bond())

    assert len(flows) == 10
    assert flows[0].payment_date == date(2024, 7, 1)
    assert flows[0].amount == 25


def test_last_payment_contains_coupon_and_principal() -> None:
    last_flow = generate_cash_flows(make_bond())[-1]

    assert last_flow.payment_date == date(2029, 1, 1)
    assert last_flow.amount == 1025
    assert last_flow.includes_principal is True


def test_future_schedule_excludes_coupon_on_settlement_date() -> None:
    flows = get_future_cash_flows(
        make_bond(),
        settlement_date=date(2024, 7, 1),
    )

    assert len(flows) == 9
    assert flows[0].payment_date == date(2025, 1, 1)


def test_future_schedule_can_include_payment_on_settlement_date() -> None:
    flows = get_future_cash_flows(
        make_bond(),
        settlement_date=date(2024, 7, 1),
        include_on_settlement=True,
    )

    assert len(flows) == 10
    assert flows[0].payment_date == date(2024, 7, 1)
