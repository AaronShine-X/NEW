# 生产与收货表

Use this reference when the user asks about 做货、收货、填表格、生产计划、排单、未到货、反向同步库存, or writing production/receipt data to Tencent Docs.

## Target Tables

- Tencent Docs workbook: read from private config key `workbook`.
- Default production/receipt sheet: read from private config key `sheets.production_receipt`.
- Optional legacy production sheet: read from private config key `sheets.legacy_production`; use only when explicitly requested.
- Inventory sheet for cross-checks: read from private config key `sheets.inventory`.
- Public skill files must not contain real Tencent Docs workbook names, sheet names, sheet IDs, or account-specific routes.

## Default Production/Receipt Table Layout

MCP indexes are 0-based.

| Index | Excel | Field | Rule |
|---:|---|---|---|
| 0 | A | 图片 | Usually leave unchanged |
| 1 | B | 退货率 | Read only unless asked |
| 2 | C | 生产周期 | Read only |
| 3 | D | 标题 | Product title |
| 4 | E | 每条件数 | Pieces per fabric roll/condition |
| 5 | F | 总数 | Planned total |
| 6 | G | 未到货数量 | Formula-owned/read-only. Preserve existing formulas; never write, clear, or manually fill this column. |
| 7 | H | 款号 | Style code |
| 8 | I | 颜色 | Color |
| 9 | J | 尺码 | Size |
| 10 | K | 空列 | Separator; leave unchanged |


## Formula Protection

- In the configured default production/receipt sheet, the unreceived-quantity column is formula-owned.
- Never write values or formulas into column G. Never clear column G while preparing a write range.
- For production plans, write only the paired date `做货数量` detail cells.
- For receipts, write only the paired date `到货` detail cells.
- After any write, re-read column G as verification only. If a G formula/value is wrong, report the exact row/cell and ask before any repair.

## Date Columns

- Row 1 is the date row, for example `2026/05/28`.
- Row 2 is the user-maintained daily summary/formula row. Never overwrite it.
- Each date uses two columns:
  - first column = 到货
  - second column = 做货数量
- If today's date column is missing, ask before inserting; do not insert silently.

## Writing Production Plans

1. Confirm date using the current Asia/Shanghai date unless the user specifies another date.
2. Find the date in row 1 and identify the paired `做货数量` column.
3. Find rows by `H=款号`, `I=颜色`, `J=尺码`.
4. If the user omits color and only one color exists for the style, use it; if multiple colors exist, ask.
5. Write only detail rows in the `做货数量` column.
6. Do not write the date summary row 2.
7. Never update `G=未到货数量`. Treat G as formula-owned/read-only; after writing the paired date column, re-read G only to verify the formula result. If formulas do not update or look wrong, report it and ask before any repair.
8. If `F=总数` is not formula-driven and should reflect the section total, update it only within the target style block.
9. Read back the target block and row 2 summary after writing.

### Adding A Missing Style Block

Use this only when the user has approved a production plan but the style has no existing rows in the configured default production/receipt sheet.

1. Re-read the entire current sheet identity columns to confirm the style is absent; do not treat this as proof that no off-sheet or unrecorded in-transit stock exists.
2. Re-read the target date pair, row 2 summary, merged-cell ranges, and candidate rows. Prefer the first contiguous blank rows already carrying the table's protected per-row formulas. If suitable blank rows do not exist or adding rows would be required, stop and ask before inserting rows.
3. The approved quantities authorize the necessary identity block for those quantities. Populate only the fields needed to identify and calculate it: title when confirmed from inventory, per-roll yield when confirmed, style, color, sizes, the paired date `做货数量` cells, and the block total formula when the live neighboring pattern requires it. Leave unknown return rate and production cycle blank.
4. Never write or replace G. Preserve any other pre-existing row formulas. Do not merge cells unless the live template requires it; unmerged continuation rows may leave repeated style/color fields blank when the neighboring pattern does so.
5. Match the live cell type for the style code. Numeric-only codes may need `NUMBER`; preserve leading-zero or mixed codes as `STRING`. If a numeric-looking string fails readback, retry that one empty cell as `NUMBER`; never rewrite cells that already match.
6. A successful API response is not completion. Re-read identity cells, each quantity, protected G formulas and computed values, block total, date, row 2 summary, and a sheet-wide style search for duplicates.
7. If a batch write reports success but readback is unchanged, retry only cells still empty or incorrect with single-cell writes. After any partial/network failure, re-read first; stop on unexpected non-empty values rather than overwriting them.

Example of the verified recovery pattern: a batch request may return `error: ""` while none of its cells persist. Single-cell writes followed by readback can recover the missing targets. This observation does not justify blind retries or changing G.

## Correcting Production Quantities From Images

Use this workflow when the user sends a quantity/cutting-bed image and the text includes `修正数量`, `修正一下数量`, or `修正做货数量`.

1. Treat the phrase as explicit approval to correct the existing production quantities; do not stop for a preview unless a row, date, colour, size, or number is unclear.
2. Parse the image into `款号/颜色/尺码/数量`. Text in the user message overrides OCR or handwriting interpretation. For example, if the image is ambiguous but the user says `青色S是29`, use `29`.
3. Map handwritten colour aliases to the table's live colour names by re-reading the relevant production/receipt rows and, if needed, the inventory sheet. For example, `绿` can map to `军绿`; `青` can map to `藏青` / `藏青色` only after confirming the table rows.
4. Preserve the table's standard size order (`XS/S/M/L/XL`) even when the image columns are ordered differently, such as `S/M/XS`.
5. Re-read row 1 and row 2 to find the date and paired `做货数量` column. If the correction is clearly for a previous write, correct that existing date column rather than today's column.
6. Re-read the existing style block and update only already-existing detail cells in the target `做货数量` column. Do not create new rows for a correction unless the user explicitly says the current rows are missing.
7. Never write column G (`未到货数量`) or row 2. After writing, re-read G only as verification.
8. After writing, read back the corrected detail rows and the date summary row. Report exact cells, values before/after when available, detail total, and summary readback.

## Writing Receipts

1. Use the paired `到货` column under the target date.
2. Write only receipt details, never the paired plan column.
3. Re-read `G=未到货数量` and row 2 after writing, but do not write to G. Preserve existing G formulas even when the displayed value looks wrong.

## Filling Old-Format Production Rows

Only use this section when the user explicitly asks for old-format row writing.

- Ask the user which row to start from before writing.
- Clear only the intended target range before filling.
- Do not merge cells unless the current target template requires it and the user expects that format.
- Fill repeated rows in standard format:
  - A = half-width space
  - B = style code on the first row of a group
  - C = date on the first row of a date subgroup
  - D = color on the first row of a color subgroup
  - E = size every row, sorted XS/S/M/L/XL
  - F = cutting ratio every row
  - G = plan quantity every row
  - H = 0 initially
  - I = `未出货`
  - J = backend backorder
  - K = `G-J`, required

## Production Ratio Principles

- For new 做货建议 and size allocation, read `production-advice.md`; distinguish demand share, combined inventory share, and this batch's cutting ratio.
- The following F/G meanings apply only to the old-format rows described above: F is cutting ratio; G is planned quantity and may differ from the ratio. In the configured default production/receipt sheet, the configured total column is section total and the configured unreceived column is formula-owned/read-only.
- Historical receipt ratios show previous supply choices, not customer demand. They may inform cutting feasibility; infer demand from orders/shipments with stockout and return checks.
- Known parameters:
  - `0331`: 102 pieces/roll, ratio `1:1:1`
  - `0332`: 140 pieces/roll, ratio `1:1:1`
  - `0333`: 110 pieces/roll, ratio `2:2:1`
  - `0335`: 140 pieces/roll, 米白 `1:2:1`, 深灰 `2:3:3`
  - `0328`: about 180 pieces/roll, 黑 `1:5:3`, 深灰 `1:6:2`

## Production Scheduling

- Default scheduling mode: backward scheduling from due date.
- Consider priority, delivery date, recent sales, fabric sharing, and production cycle.
- Colors must be analyzed separately; do not merge different colors for size planning.
- Use real order data and live inventory when available. Mark assumptions clearly.

## Reverse Sync To Inventory

Only perform reverse sync when the user explicitly asks.

Map the configured production/receipt sheet to the configured inventory sheet:

| Production/receipt sheet | Inventory sheet |
|---|---|
| H 款号 | F 款号 |
| I 颜色 | G 颜色 |
| J 尺码 | H 尺码 |

Before syncing, confirm row range and target styles. After syncing, re-read target inventory rows.
