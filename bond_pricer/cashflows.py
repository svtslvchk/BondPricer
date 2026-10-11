from calendar import monthrange
from datetime import date

from .exceptions import InvalidScheduleError
from .models import Bond, CashFlow


def add_months(value: date, months: int) -> date:
    """Adding calendar months to a date"""
    total_months = value.year * 12 + value.month - 1 + months
    year, month_index = divmod(total_months, 12)
    month = month_index + 1
    last_day = monthrange(year, month)[1]

    return date(year, month, min(value.day, last_day))


def generate_cash_flows(bond: Bond) -> list[CashFlow]:
    """Generate all coupon and principal payments for a bond."""
    flows: list[CashFlow] = []
    payment_date = add_months(bond.issue_date, bond.period_months)

    while payment_date < bond.maturity_date:
        flows.append(
            CashFlow(
                payment_date=payment_date,
                amount=bond.coupon_amount,
            )
        )
        payment_date = add_months(payment_date, bond.period_months)

    if payment_date != bond.maturity_date:
        raise InvalidScheduleError(
            "Maturity date must fall on a coupon payment date"
        )

    flows.append(
        CashFlow(
            payment_date=bond.maturity_date,
            amount=bond.coupon_amount + bond.face_value,
            includes_principal=True,
        )
    )
    return flows


def get_future_cash_flows(
    bond: Bond,
    settlement_date: date,
    *,
    include_on_settlement: bool = False,
) -> list[CashFlow]:
    """Return payments after settlement, excluding an already paid coupon."""
    if settlement_date < bond.issue_date:
        raise ValueError("Settlement date cannot precede issue date")

    if settlement_date >= bond.maturity_date:
        return []

    all_flows = generate_cash_flows(bond)

    if include_on_settlement:
        return [
            flow
            for flow in all_flows
            if flow.payment_date >= settlement_date
        ]

    return [
        flow
        for flow in all_flows
        if flow.payment_date > settlement_date
    ]
