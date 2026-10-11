from datetime import date

from .cashflows import get_future_cash_flows
from .models import Bond, CashFlow
from .pricing import year_fraction
from .exceptions import YieldCalculationError


def price_from_yield(
    cash_flows: list[CashFlow],
    settlement_date: date,
    annual_yield: float,
    payments_per_year: int,
) -> float:
    """Calculate price using one annual yield with periodic compounding."""
    if payments_per_year <= 0:
        raise YieldCalculationError("Payments per year must be positive")

    if annual_yield <= -payments_per_year:
        raise YieldCalculationError("Yield is too low for the selected frequency")

    price = 0.0
    periodic_rate = annual_yield / payments_per_year

    for cash_flow in cash_flows:
        time_years = year_fraction(
            settlement_date,
            cash_flow.payment_date,
        )
        periods = payments_per_year * time_years
        price += cash_flow.amount / (1 + periodic_rate) ** periods

    return price


def calculate_ytm(
    bond: Bond,
    settlement_date: date,
    target_price: float,
    *,
    lower_bound: float = -0.99,
    upper_bound: float = 1.0,
    tolerance: float = 1e-12,
    max_iterations: int = 200,
) -> float:
    """Find YTM using the bisection method."""
    if target_price <= 0:
        raise YieldCalculationError("Target price must be positive")

    cash_flows = get_future_cash_flows(bond, settlement_date)
    if not cash_flows:
        raise YieldCalculationError("No future cash flows available")

    lower_bound = max(lower_bound, -bond.payments_per_year + 1e-12)

    lower_price = price_from_yield(
        cash_flows,
        settlement_date,
        lower_bound,
        bond.payments_per_year,
    )
    upper_price = price_from_yield(
        cash_flows,
        settlement_date,
        upper_bound,
        bond.payments_per_year,
    )

    if not lower_price >= target_price >= upper_price:
        raise YieldCalculationError(
            "Target price is outside the selected yield search range"
        )

    for _ in range(max_iterations):
        middle = (lower_bound + upper_bound) / 2
        middle_price = price_from_yield(
            cash_flows,
            settlement_date,
            middle,
            bond.payments_per_year,
        )

        if abs(middle_price - target_price) <= tolerance:
            return middle

        if middle_price > target_price:
            lower_bound = middle
        else:
            upper_bound = middle

    return (lower_bound + upper_bound) / 2
