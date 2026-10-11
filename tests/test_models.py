from datetime import date

import pytest

from bond_pricer.exceptions import BondValidationError
from bond_pricer.models import Bond, CashFlow


def make_bond() -> Bond:
    return Bond(
        issue_date=date(2024, 1, 1),
        maturity_date=date(2029, 1, 1),
        face_value=1000,
        annual_coupon_rate=0.05,
        payments_per_year=2,
    )


def test_coupon_amount_is_calculated_per_period() -> None:
    assert make_bond().coupon_amount == 25


def test_bond_rejects_non_positive_face_value() -> None:
    with pytest.raises(BondValidationError):
        Bond(
            issue_date=date(2024, 1, 1),
            maturity_date=date(2029, 1, 1),
            face_value=0,
            annual_coupon_rate=0.05,
            payments_per_year=2,
        )


def test_cash_flow_rejects_negative_amount() -> None:
    with pytest.raises(BondValidationError):
        CashFlow(payment_date=date(2025, 1, 1), amount=-1)
