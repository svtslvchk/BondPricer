from datetime import date

import pytest

from bond_pricer.models import Bond
from bond_pricer.duration import modified_duration


def test_modified_duration_is_positive_and_reasonable() -> None:
    bond = Bond(
        issue_date=date(2024, 1, 1),
        maturity_date=date(2029, 1, 1),
        face_value=1000,
        annual_coupon_rate=0.05,
        payments_per_year=2,
    )

    duration = modified_duration(
        bond=bond,
        settlement_date=date(2024, 7, 1),
        annual_yield=0.096535,
    )

    assert duration == pytest.approx(3.85, abs=0.1)
