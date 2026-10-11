from datetime import date

from bond_pricer.models import Bond
from bond_pricer.prices import (
    accrued_interest,
    clean_to_dirty_price,
    dirty_to_clean_price,
    get_coupon_period,
)


def make_bond() -> Bond:
    return Bond(
        issue_date=date(2024, 1, 1),
        maturity_date=date(2029, 1, 1),
        face_value=1000,
        annual_coupon_rate=0.05,
        payments_per_year=2,
    )


def test_coupon_period_on_coupon_date() -> None:
    previous_date, next_date = get_coupon_period(
        make_bond(),
        date(2024, 7, 1),
    )

    assert previous_date == date(2024, 7, 1)
    assert next_date == date(2025, 1, 1)


def test_accrued_interest_is_zero_on_coupon_date() -> None:
    assert accrued_interest(make_bond(), date(2024, 7, 1)) == 0


def test_accrued_interest_between_coupon_dates() -> None:
    accrued = accrued_interest(make_bond(), date(2024, 10, 1))

    assert 12 < accrued < 13


def test_price_conversion() -> None:
    assert dirty_to_clean_price(850, 12.5) == 837.5
    assert clean_to_dirty_price(837.5, 12.5) == 850
