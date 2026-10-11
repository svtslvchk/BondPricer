# Bond Pricer

## Структура проекта

```text
bond_pricer/
├── models.py              # модели Bond, CashFlow, YieldCurve
├── exceptions.py          # специализированные ошибки
├── cashflows.py           # генерация денежных потоков
├── prices.py              # НКД, чистая/грязная цена
├── yield_curve.py         # интерполяция ставок и кредитный спред
├── pricing.py             # дисконтирование и расчёт цены
├── yield_to_maturity.py   # поиск YTM бинарным поиском
└── duration.py            # дюрация Маколея и модифицированная дюрация

tests/
├── test_models.py
├── test_cashflows.py
├── test_prices.py
├── test_yield_curve.py
├── test_pricing.py
├── test_yield_to_maturity.py
└── test_duration.py

main.py                    # полный пример расчёта
```

## Основные понятия

- `Bond` — параметры облигации: номинал, купон, даты и частота выплат.
- `CashFlow` — отдельный будущий платёж.
- `YieldCurve` — ставки рынка для разных сроков.
- `accrued_interest` — накопленный купонный доход.
- `dirty price` — цена с НКД.
- `clean price` — цена без НКД.
- `YTM` — годовая доходность инвестора при удержании до погашения.
- `modified duration` — чувствительность цены к изменению доходности.

## Исключения

- `BondValidationError` — неверные параметры облигации или денежного потока.
- `InvalidScheduleError` — дата погашения не совпадает с купонной датой.
- `YieldCurveError` — невозможно получить ставку из кривой.
- `PricingError` — ошибка расчёта цены или НКД.
- `YieldCalculationError` — невозможно найти YTM.

Каждая ошибка выбрасывается в модуле, которому она относится.

## Подготовка и активация окружения

```bash
python3 -m venv venv
source venv/bin/activate
```

## Установка зависимостей

```bash
pip install -r requirements.txt
```

## Запуск демонстрации

```bash
python demo.py
```

## Запуск тестов

```bash
pytest
```
