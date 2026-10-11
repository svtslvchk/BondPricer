from dataclasses import dataclass
from datetime import date
from typing import Mapping

from .exceptions import BondValidationError


@dataclass(frozen=True)
class CashFlow:
    """A single payment made by the bond."""

    payment_date: date
    amount: float
    includes_principal: bool = False

    def __post_init__(self) -> None:
        if self.amount < 0:
            raise BondValidationError("Cash flow amount cannot be negative")


@dataclass(frozen=True)
class Bond:
    """A fixed-rate coupon bond."""

    issue_date: date
    maturity_date: date
    face_value: float
    annual_coupon_rate: float
    payments_per_year: int

    def __post_init__(self) -> None:
        if self.maturity_date <= self.issue_date:
            raise BondValidationError(
                "Maturity date must be later than issue date"
            )

        if self.face_value <= 0:
            raise BondValidationError("Face value must be positive")

        if self.annual_coupon_rate < 0:
            raise BondValidationError(
                "Annual coupon rate cannot be negative"
            )

        if self.payments_per_year <= 0:
            raise BondValidationError(
                "Payments per year must be positive"
            )

        if 12 % self.payments_per_year != 0:
            raise BondValidationError(
                "Payments per year must divide 12 without a remainder"
            )

    @property
    def period_months(self) -> int:
        return 12 // self.payments_per_year

    @property
    def coupon_amount(self) -> float:
        return (
            self.face_value
            * self.annual_coupon_rate
            / self.payments_per_year
        )


@dataclass(frozen=True)
class YieldCurve:
    """Zero-coupon yield curve represented by term-to-rate points."""

    points: Mapping[float, float]

    def __post_init__(self) -> None:
        if len(self.points) < 2:
            raise BondValidationError(
                "Yield curve must contain at least two points"
            )

        for term, rate in self.points.items():
            if term <= 0:
                raise BondValidationError("Curve terms must be positive")
            if rate <= -1:
                raise BondValidationError(
                    "Curve rates must be greater than -100%"
                )

    @property
    def terms(self) -> tuple[float, ...]:
        return tuple(sorted(self.points))
