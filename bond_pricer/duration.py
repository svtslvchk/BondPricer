from datetime import date

from .cashflows import get_future_cash_flows
from .models import Bond
from .pricing import year_fraction
from .yield_to_maturity import price_from_yield


def macaulay_duration(
    bond: Bond,
    settlement_date: date,
    annual_yield: float,
) -> float:
    """Calculate Macaulay duration in years."""
    cash_flows = get_future_cash_flows(bond, settlement_date)
    if not cash_flows:
        raise ValueError("No future cash flows available")

    price = price_from_yield(
        cash_flows,
        settlement_date,
        annual_yield,
        bond.payments_per_year,
    )

    weighted_present_value = 0.0
    periodic_rate = annual_yield / bond.payments_per_year

    for cash_flow in cash_flows:
        time_years = year_fraction(
            settlement_date,
            cash_flow.payment_date,
        )
        periods = bond.payments_per_year * time_years
        present_value = cash_flow.amount / (1 + periodic_rate) ** periods
        weighted_present_value += time_years * present_value

    return weighted_present_value / price


def modified_duration(
    bond: Bond,
    settlement_date: date,
    annual_yield: float,
) -> float:
    """Calculate modified duration in years."""
    macaulay = macaulay_duration(
        bond,
        settlement_date,
        annual_yield,
    )

    return macaulay / (1 + annual_yield / bond.payments_per_year)
