from datetime import date

from .cashflows import generate_cash_flows
from .models import Bond
from .exceptions import PricingError


def get_coupon_period(
    bond: Bond,
    settlement_date: date,
) -> tuple[date, date]:
    """Return the previous and next coupon dates around settlement."""
    if settlement_date < bond.issue_date:
        raise PricingError("Settlement date cannot precede issue date")

    if settlement_date >= bond.maturity_date:
        raise PricingError("Settlement date must precede maturity date")

    coupon_dates = [bond.issue_date]
    coupon_dates.extend(
        flow.payment_date for flow in generate_cash_flows(bond)
    )

    previous_date = coupon_dates[0]
    for coupon_date in coupon_dates[1:]:
        if coupon_date > settlement_date:
            return previous_date, coupon_date
        previous_date = coupon_date

    raise PricingError("Could not determine coupon period")


def accrued_interest(
    bond: Bond,
    settlement_date: date,
) -> float:
    """Calculate accrued coupon using a simple Actual/Actual fraction."""
    previous_date, next_date = get_coupon_period(
        bond,
        settlement_date,
    )

    elapsed_days = (settlement_date - previous_date).days
    period_days = (next_date - previous_date).days

    if period_days <= 0:
        raise PricingError("Coupon period must be positive")

    return bond.coupon_amount * elapsed_days / period_days


def dirty_to_clean_price(
    dirty_price: float,
    accrued_coupon: float,
) -> float:
    """Convert dirty price to clean price."""
    return dirty_price - accrued_coupon


def clean_to_dirty_price(
    clean_price: float,
    accrued_coupon: float,
) -> float:
    """Convert clean price to dirty price."""
    return clean_price + accrued_coupon
