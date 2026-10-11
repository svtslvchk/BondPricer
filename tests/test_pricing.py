from datetime import date

import pytest

from bond_pricer.models import Bond
from bond_pricer.pricing import (
    calculate_dirty_price,
    discount_factor,
    year_fraction,
)
from bond_pricer.yield_curve import YieldCurve


def make_bond() -> Bond:
    return Bond(
        issue_date=date(2024, 1, 1),
        maturity_date=date(2029, 1, 1),
        face_value=1000,
        annual_coupon_rate=0.05,
        payments_per_year=2,
    )


def make_curve() -> YieldCurve:
    return YieldCurve(
        points={
            0.5: 0.0763,
            1.0: 0.0782,
            2.0: 0.0832,
            3.0: 0.0865,
            4.0: 0.0885,
            5.0: 0.0901,
        }
    )


def test_year_fraction_uses_actual_365() -> None:
    assert year_fraction(date(2024, 7, 1), date(2025, 1, 1)) == pytest.approx(
        184 / 365
    )


def test_discount_factor_is_less_than_one_for_positive_rate() -> None:
    assert discount_factor(0.1, 1) == pytest.approx(1 / 1.1)


def test_dirty_price_is_below_nominal_when_market_rates_are_higher() -> None:
    price = calculate_dirty_price(
        bond=make_bond(),
        settlement_date=date(2024, 7, 1),
        curve=make_curve(),
        credit_spread=0.01,
    )

    assert 820 < price < 850
