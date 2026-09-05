# 供货项目盈亏、关店风险与合同报价

Use this reference for wholesale/supply projects involving return rates, reusable returns, abrupt store closure, contract-duration pricing, working capital, order-volume scenarios, target profit, deposits, or shipping/after-sales fees.

## Confirm Before Calculating

Confirm these inputs; mark missing items `需确认` instead of inventing them:

- `C`: supplier-borne all-in production cost per newly made garment.
- `D`: gross shipped orders per day, per product.
- `r`: eventual return rate as a decimal.
- `H`: guaranteed or evaluated cooperation days.
- `L`: days from shipment until a return is unpacked and reusable.
- `T`: days from placing a production order until goods can ship.
- `i`: annual capital/opportunity-cost rate.
- `m`: desired true profit per finally retained sale.
- Returned-goods reuse rate during cooperation and terminal salvage value.
- Who bears accessories, outbound/return shipping, packing, after-sales, overweight, tax, platform, fixed, and bad-debt costs.
- Whether committed factory orders can be cancelled when cooperation stops.

Do not hardcode old product costs, rates, order volumes, contract terms, deposits, or service prices. The latest user correction wins.

## Select The Correct Loss Model

### Reusable-return tail model

Use this model when returned goods are reusable during cooperation but become unsellable to the supplier after the buyer/store abruptly stops. Earlier returns circulate into later shipments; only closing return stock and uncancellable production are stranded.

Do not use `C / (1-r)` here. That formula treats every return as a permanent loss and materially overstates a longer contract's unit floor.

### Permanent-loss model

Use `P_break_even = C / (1-r)` only when every returned unit is permanently unusable, unrecoverable, or charged as a full product loss. Then `risk markup = C*r/(1-r)`.

## Reusable-Return Formulas

Assume steady daily demand, daily rolling replenishment, 100% reuse during cooperation, zero terminal salvage, and uncancellable production:

```text
retained units N        = D * (1-r) * H
return-loop stock Qr    = D * r * L
committed production Qp = D * (1-r) * T
closing stock Q         = Qr + Qp
closing exposure E      = Q * C
capital cost K          = E * i * H / 365
break-even price Pb     = C + (E + K + other supplier costs) / N
quoted price P          = Pb + m
project profit          = N * (P-C) - E - K - other supplier costs
```

Without fixed or per-shipment supplier costs, `D` cancels from the unit-price formula:

```text
Pb = C + C * [rL + (1-r)T] / [(1-r)H] * (1 + iH/365)
```

Therefore order volume normally scales closing exposure, working capital, and total profit, but not the per-unit floor. This cancellation is invalid when stock was prepared for a prior peak, demand drops after production is committed, minimum production batches apply, or fixed costs are material. In those cases use actual committed stock and actual retained sales.

## Cost Classification

- Include an accessory in `C` only when the supplier bears it on newly produced/stranded garments.
- Keep reimbursed or buyer-supplied accessories outside `C` and show them separately.
- If the supplier bears a service cost `s` on every gross shipment and it is not separately reimbursed, add `s/(1-r)` to the retained-sale quote.
- Keep separately billed shipping/after-sales and overweight charges outside the goods quote.
- Add fixed costs as `fixed_cost/N`.
- A markup over garment cost is not all true profit: first allocate closing exposure, capital cost, and supplier-borne variable/fixed costs. Only the remainder is true profit.

## Contract And Demand Scenarios

- Price against the shortest cooperation period the supplier must survive, not an optimistic duration.
- If quoting against a longer period, state that early termination can create an unamortized deficit.
- Calculate an early-termination deposit or buyout from actual return-loop stock, uncancellable production, and other committed inventory; do not invent the deposit amount without order-volume facts.
- For demand scenarios, show unit quote, retained units, closing stock, capital required, and total profit at each daily-order level.
- If daily demand is volatile, distinguish average demand from peak/committed demand. Use peak or actual committed quantities for downside exposure.

## Calculation Procedure

1. List confirmed facts and `需确认` items.
2. Choose the reusable-tail or permanent-loss model explicitly.
3. Use the conservative end of a user-provided cycle range, while also showing the range when useful.
4. Calculate the pure break-even price before target profit.
5. Add capital cost, supplier-borne services, fixed costs, and desired true profit separately.
6. Show a reconciliation proving that accumulated margin covers closing exposure and capital cost.
7. State whether the result assumes the contract reaches its full term.
8. For business copy, separate goods price, optional accessories, shipping/after-sales, overweight, return cap, deposit, and early-termination treatment.

## Deterministic Calculator

Use `scripts/supply_project_pricing.py` for repeat calculations. Pass return rate as `0.4` or `40`. Treat `--service-cost-per-shipment` as a supplier-borne, unreimbursed gross-shipment cost; omit it when billed separately.

Example:

```powershell
python scripts/supply_project_pricing.py --cost 52 --daily-orders 500 --return-rate 40 --contract-days 180 --return-days 10 --production-days 5 --annual-capital-rate 3 --target-profit 10
```

Before quoting, round the minimum upward, not downward, and identify any commercial buffer created by rounding.
