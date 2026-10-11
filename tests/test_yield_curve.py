import pytest

from bond_pricer.models import YieldCurve
from bond_pricer.yield_curve import (
    rate_at, rate_with_spread
)


def make_curve() -> YieldCurve:
    return YieldCurve(
        points={
            1.0: 0.0782,
            2.0: 0.0832,
            3.0: 0.0865,
            4.0: 0.0885,
            5.0: 0.0901,
        }
    )


def test_exact_curve_point() -> None:
    assert rate_at(make_curve(), 2.0) == 0.0832


def test_linear_interpolation() -> None:
    assert rate_at(make_curve(), 1.5) == pytest.approx(0.0807)


def test_credit_spread_is_added_to_rate() -> None:
    rate = rate_with_spread(make_curve(), 1.5, 0.01)

    assert rate == pytest.approx(0.0907)


def test_term_outside_curve_is_rejected() -> None:
    with pytest.raises(ValueError):
        rate_at(make_curve(), 0.5)
