#!/usr/bin/env python3
"""Calculate reusable-return supply-project pricing."""

from __future__ import annotations

import argparse
import json


def as_rate(value: float, name: str) -> float:
    rate = value / 100 if value > 1 else value
    if not 0 <= rate < 1:
        raise argparse.ArgumentTypeError(f"{name} must be in [0, 1) or [0, 100)")
    return rate


def nonnegative(value: float, name: str) -> float:
    if value < 0:
        raise argparse.ArgumentTypeError(f"{name} must be nonnegative")
    return value


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Price a supply project where returns are reusable until closure."
    )
    parser.add_argument("--cost", type=float, required=True)
    parser.add_argument("--daily-orders", type=float, required=True)
    parser.add_argument("--return-rate", type=float, required=True)
    parser.add_argument("--contract-days", type=float, required=True)
    parser.add_argument("--return-days", type=float, required=True)
    parser.add_argument("--production-days", type=float, required=True)
    parser.add_argument("--annual-capital-rate", type=float, default=0)
    parser.add_argument("--target-profit", type=float, default=0)
    parser.add_argument("--service-cost-per-shipment", type=float, default=0)
    parser.add_argument("--fixed-cost", type=float, default=0)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    cost = nonnegative(args.cost, "cost")
    daily_orders = nonnegative(args.daily_orders, "daily-orders")
    return_rate = as_rate(args.return_rate, "return-rate")
    contract_days = nonnegative(args.contract_days, "contract-days")
    return_days = nonnegative(args.return_days, "return-days")
    production_days = nonnegative(args.production_days, "production-days")
    capital_rate = as_rate(args.annual_capital_rate, "annual-capital-rate")
    target_profit = nonnegative(args.target_profit, "target-profit")
    service_cost = nonnegative(
        args.service_cost_per_shipment, "service-cost-per-shipment"
    )
    fixed_cost = nonnegative(args.fixed_cost, "fixed-cost")

    if daily_orders == 0 or contract_days == 0:
        raise SystemExit("daily-orders and contract-days must be greater than zero")

    retained_units = daily_orders * (1 - return_rate) * contract_days
    return_stock = daily_orders * return_rate * return_days
    committed_production = daily_orders * (1 - return_rate) * production_days
    closing_stock = return_stock + committed_production
    closing_exposure = closing_stock * cost
    capital_cost = closing_exposure * capital_rate * contract_days / 365
    gross_shipments = daily_orders * contract_days
    supplier_service_cost = gross_shipments * service_cost
    other_costs = capital_cost + supplier_service_cost + fixed_cost
    break_even_price = cost + (closing_exposure + other_costs) / retained_units
    quoted_price = break_even_price + target_profit
    expected_profit = (
        retained_units * (quoted_price - cost)
        - closing_exposure
        - other_costs
    )

    result = {
        "inputs": {
            "cost": cost,
            "daily_orders": daily_orders,
            "return_rate": return_rate,
            "contract_days": contract_days,
            "return_days": return_days,
            "production_days": production_days,
            "annual_capital_rate": capital_rate,
            "target_profit_per_retained_sale": target_profit,
            "supplier_service_cost_per_gross_shipment": service_cost,
            "fixed_cost": fixed_cost,
        },
        "volume": {
            "gross_shipments": gross_shipments,
            "retained_units": retained_units,
            "return_loop_stock": return_stock,
            "committed_production": committed_production,
            "closing_stock": closing_stock,
        },
        "costs": {
            "closing_exposure": closing_exposure,
            "capital_cost": capital_cost,
            "supplier_service_cost": supplier_service_cost,
            "fixed_cost": fixed_cost,
        },
        "pricing": {
            "break_even_price": break_even_price,
            "quoted_price": quoted_price,
            "expected_project_profit": expected_profit,
        },
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
