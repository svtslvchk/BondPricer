from datetime import date

import pytest

from bond_pricer.models import Bond, YieldCurve
from bond_pricer.cashflows import get_future_cash_flows
from bond_pricer.yield_to_maturity import price_from_yield
from bond_pricer.pricing import calculate_dirty_price
from bond_pricer.yield_to_maturity import calculate_ytm


def make_bond() -> Bond:
    return Bond(
        issue_date=date(2024, 1, 1),
        maturity_date=date(2029, 1, 1),
        face_value=1000,
        annual_coupon_rate=0.05,
        payments_per_year=2,
    )


def make_price() -> float:
    curve = YieldCurve(
        points={
            0.5: 0.0763,
            1.0: 0.0782,
            2.0: 0.0832,
            3.0: 0.0865,
            4.0: 0.0885,
            5.0: 0.0901,
        }
    )
    return calculate_dirty_price(
        make_bond(),
        date(2024, 7, 1),
        curve,
        credit_spread=0.01,
    )


def test_price_decreases_when_yield_increases() -> None:
    flows = get_future_cash_flows(make_bond(), date(2024, 7, 1))
    low_yield_price = price_from_yield(
        flows,
        date(2024, 7, 1),
        annual_yield=0.05,
        payments_per_year=2,
    )
    high_yield_price = price_from_yield(
        flows,
        date(2024, 7, 1),
        annual_yield=0.10,
        payments_per_year=2,
    )

    assert high_yield_price < low_yield_price


def test_ytm_reproduces_target_price() -> None:
    bond = make_bond()
    settlement_date = date(2024, 7, 1)
    target_price = make_price()
    ytm = calculate_ytm(bond, settlement_date, target_price)

    reproduced_price = price_from_yield(
        get_future_cash_flows(bond, settlement_date),
        settlement_date,
        ytm,
        bond.payments_per_year,
    )

    assert reproduced_price == pytest.approx(target_price)
    assert ytm == pytest.approx(0.096, abs=0.002)
