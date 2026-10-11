from datetime import date

from .cashflows import get_future_cash_flows
from .models import Bond, CashFlow, YieldCurve
from .yield_curve import rate_with_spread
from .exceptions import PricingError


def year_fraction(start_date: date, end_date: date) -> float:
    """Calculate a simple Actual/365 year fraction."""
    if end_date < start_date:
        raise PricingError("End date cannot precede start date")

    return (end_date - start_date).days / 365.0


def discount_factor(rate: float, time_years: float) -> float:
    """Calculate a discount factor using annual effective compounding."""
    if rate <= -1:
        raise PricingError("Discount rate must be greater than -100%")

    if time_years < 0:
        raise PricingError("Time to payment cannot be negative")

    return 1 / (1 + rate) ** time_years


def present_value(
    cash_flow: CashFlow,
    settlement_date: date,
    rate: float,
) -> float:
    """Calculate the present value of one future cash flow."""
    time_years = year_fraction(
        settlement_date,
        cash_flow.payment_date,
    )
    return cash_flow.amount * discount_factor(rate, time_years)


def calculate_dirty_price(
    bond: Bond,
    settlement_date: date,
    curve: YieldCurve,
    credit_spread: float = 0.0,
) -> float:
    """Calculate dirty price by discounting future cash flows."""
    future_flows = get_future_cash_flows(
        bond,
        settlement_date,
    )

    if not future_flows:
        raise PricingError("No future cash flows available")

    price = 0.0

    for cash_flow in future_flows:
        time_years = year_fraction(
            settlement_date,
            cash_flow.payment_date,
        )
        rate = rate_with_spread(curve, time_years, credit_spread)
        price += present_value(cash_flow, settlement_date, rate)

    return price
