# 库存、订单、补货分析

Use this reference when the user asks about 小红书订单统计、库存分析、查库存、补货建议、库存预警、近七天消耗、退货率, or SKU-level demand planning.

## Data Sources

- Order export: local `.xlsx`, sheet `包裹详情`.
- Tencent Docs workbook: read from private config key `workbook`.
- Inventory sheet: read from private config key `sheets.inventory`.
- Production/receipt sheet: read from private config key `sheets.production_receipt`.

## Hard Rules

- Always read live Tencent Docs for inventory, production, receipt, shipment, and return-to-inventory values.
- Memory or old chat context can provide boundaries only, not reusable figures.
- If a field is absent, unclear, range-based, ratio-only, or fabric-roll-only, use `需确认`; do not invent exact garment quantities.
- Use the configured available-stock column in the inventory sheet, not total inventory unless the user asks otherwise.
- Different colors must be analyzed separately.

## Inventory Sheet Layout

MCP indexes are 0-based.

| Index | Excel | Field |
|---:|---|---|
| 2 | C | 标题 |
| 5 | F | 款号 |
| 6 | G | 颜色 |
| 7 | H | 尺码 |
| 8 | I | 库存数/总库存 |
| 9 | J | 实时总数/可发库存 |

Rows are often structured as product header row plus same-color size continuation rows. Re-read around the block before deciding a style or size is missing.

## Order Statistics

1. Read the order `.xlsx`, usually sheet `包裹详情`.
2. If several products exist, default to the product with the most orders unless the user specifies a product.
3. Clean SKU specifications by removing bracketed campaign text.
4. Group by color and size.
5. Sort sizes as `XS -> S -> M -> L -> XL`.
6. Output `颜色 | 尺码 | 件数`.

## Matching Orders To Inventory

Priority:

1. If merchant code exists, match code to inventory style; pad to 4 digits when needed, e.g. `328 -> 0328`.
2. If no code exists, match product name to inventory title using simplified core keywords.
3. If uncertain, list possible matches and mark `需确认`.

## Shortage Calculation

Use:

`缺口 = 订单数 - 实时库存`

- Positive result = shortage.
- Negative result = surplus.
- Search only the relevant inventory sheet unless the user asks otherwise.

## Recent Shipment Consumption

When analyzing recent consumption:

1. Use the most recent 7 complete shipment days unless the user asks to include today.
2. Shipment columns can be grouped as `发货 / 到货 / 退货转库存`.
3. 发货 values are often negative; use absolute value.
4. Daily net shipment:
   `max(abs(发货) - 退货转库存, 0)`.
5. Do not count arrivals as consumption.
6. If today is incomplete, exclude it or label it as incomplete.
7. Label this metric `逐日截零净消耗`. It may exceed `7天发货总量－7天退货转库存总量` because days with net returns are clipped to zero. Keep gross shipments, returned-to-stock, and this metric separate; do not call same-window returns a cohort return rate or deduct them again from current J stock.

## Replenishment Forecast

For a production quantity or size allocation, read `production-advice.md`. It defines demand versus net consumption, stockout bias, fixed-roll allocation, and rounding validation. Use current J, formula-owned G, recent complete days, and the user's latest explicit constraints. Do not reuse a past recommendation as a current answer.

## Output Style

- Put SKU-level facts first.
- Use tables over prose.
- Give clear actions: produce, chase arrival, pause, or confirm data.
- If delivery to WeChat/Feishu fails, say `未发送` and provide copyable text.
