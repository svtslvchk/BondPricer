from datetime import date

from bond_pricer.models import Bond, YieldCurve
from bond_pricer.pricing import calculate_dirty_price
from bond_pricer.yield_to_maturity import calculate_ytm
from bond_pricer.duration import modified_duration


def main() -> None:
    settlement_date = date(2024, 7, 1)

    bond = Bond(
        issue_date=date(2024, 1, 1),
        maturity_date=date(2029, 1, 1),
        face_value=1000,
        annual_coupon_rate=0.05,
        payments_per_year=2,
    )

    curve = YieldCurve(
        points={
            0.5: 0.0763,
            1.0: 0.0782,
            2.0: 0.0832,
            3.0: 0.0865,
            4.0: 0.0885,
            5.0: 0.0901,
        }
    )

    dirty_price = calculate_dirty_price(
        bond,
        settlement_date,
        curve,
        credit_spread=0.01,
    )
    ytm = calculate_ytm(bond, settlement_date, dirty_price)
    duration = modified_duration(bond, settlement_date, ytm)

    print(f"Грязная цена:             {dirty_price:.2f} рублей")
    print(f"YTM:                      {ytm:.4%}")
    print(f"Модифицированная дюрация: {duration:.4f}")


if __name__ == "__main__":
    main()
