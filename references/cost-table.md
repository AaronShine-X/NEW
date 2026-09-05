# 成本表

Use this reference when the user asks about 成本计算、成本表、面料费、布料费、加工费、缩水、辅料、杂费、扣子、洗水费、工厂出货数量, or requests writing extracted payment/image costs into Tencent Docs.

## Target Table

- Read the target workbook and cost-table sheet from private config key `sheets.cost`.
- Public skill files must not contain real Tencent Docs workbook names, sheet names, sheet IDs, or account-specific routes.
- Always re-read live sheet info before writing. Do not rely only on remembered row/column positions.

## Live Layout Rules

- Row/column indexes in Tencent Docs MCP are 0-based. User-facing rows/columns are Excel-style.
- Row 1 contains date headers such as `7/23`.
- Current live layout observed on 2026-07-23:
  - `E列` = 货号
  - `I列` = 项目
  - 第 5 行 = `前期杂费`
- Older notes may say D/H are 货号/项目. Treat those as historical only; always re-read the live header row and left columns.
- Rows 2-4 are summary/formula rows. Never overwrite them with manual detail values.
- If a target date column is missing:
  - First check whether there is an existing blank reserved date column before the latest date. If the blank column already has summary formulas in rows 2-4 and empty detail cells, prefer using it.
  - If no safe blank column exists, ask before inserting a date column.
  - After inserting a date column, re-read row 1 and formula rows before writing detail values.

## Cost Item Routing

- 面料/布料费: write to the row in the style block where `项目=面料` or `项目=布料`.
- 加工费/缩水/辅料: write to the row where `项目=加工费+缩水`, unless user gives a specific separate row.
- 工厂出货数量: write only to the row where `项目=数量`.
- 前期杂费: write to row 5 (`前期杂费`) when the user says to follow prior miscellaneous-cost classification.
- `8856返修` / `8856返袖口`: write to the dedicated `8856返修` row, not normal `8856`.

## User-Specific Cost Classification

- `8856`:
  - User confirmed `8856 面料洗水费` and `8856 扣子/辅料` both count into normal `8856` 面料费.
  - 2026-07-23 example: `7642.5 + 11828 = 19470.5`, written to `8856` 面料 row.
- 杂项:
  - Do not invent new I-column categories for remaining miscellaneous costs.
  - If user says follow prior misc classification, write remaining misc amount directly to row 5 `前期杂费`.
  - 2026-07-23 example: misc folder total `2195`; split `8339` fabric `819`; remaining misc `1376` written to row 5.
- 工装裤:
  - `工装裤=8339`.
  - Fabric/lining items in misc folders that clearly belong to 工装裤 should be split out to `8339` 面料 row, not kept in row 5 misc.

## Image/Payment Extraction Rules

1. For fabric/payment screenshots, extract the original merchant amount before discounts, not the discounted paid amount.
2. If red-label style text exists, prefer that style code.
3. Extract every image into a detail table first:
   `图片编号 | 日期 | 原始款号/项目 | 映射货号 | 数量 | 单价 | 金额 | 备注`.
4. Merge by mapped style and item type.
5. Reconcile detail totals with folder names, user-stated totals, or image totals.
6. If a value is back-solved or uncertain, mark `需确认`; do not silently treat it as confirmed.
7. If the user allows a small difference, apply only that tolerance. Do not hide larger discrepancies.

## Write Preview Required

Before writing, show a preview containing at least:

| 货号/项目 | 店铺归属 | 填写位置 | 项目行 | 拟填金额 |
|---|---|---|---|---:|

Also include:

- Target file and sheet.
- Target date column.
- Current target cell value. If non-empty, ask whether to overwrite or append.
- Detail sum, source/folder total, and difference.
- Any uncertain extraction items.

## Write Rules

1. Write only after the user explicitly approves writing.
2. Use `sheet.set_cell_value` with `value_type=NUMBER` for numeric amounts.
3. Pass integers as integers, e.g. `860`, not `860.0`.
4. If preserving an existing value and adding the new amount, write a formula such as `=14616+49929`; do not overwrite.
5. After writing, re-read target cells and rows 2-4 for the date column.
6. Report the final written cells and readback values.
7. If an API call interrupts mid-batch, re-read first and only fill missing cells. Do not blindly rerun the full batch.

## Confirmed Historical Row Hints

These hints are useful for sanity checks only. Re-read before using.

- `8836/8336`: historically around rows 93-95.
- `6601`: historically around rows 96-98.
- `8339`: present near the bottom as of 2026-07-23.
- `8856`: normal block present near row 30 as of 2026-07-23.

## 2026-07-23 Verified Write Example

Date column used: `K列 = 7/23`, an existing blank reserved column before `7/18`.

Readback after writing:

| Cell | Meaning | Value |
|---|---|---:|
| K5 | 前期杂费 | 1376 |
| K30 | 8856 面料费 | 19470.5 |
| K66 | 0328 面料费 | 6102 |
| K69 | 8335 面料费 | 6879 |
| K84 | 0329 面料费 | 1316 |
| K90 | 8338 面料费 | 375 |
| K93 | 8836/8336 面料费 | 17600 |
| K96 | 6601 面料费 | 18492 |
| K99 | 8339 面料费 | 819 |

Detail sum and row 2 date summary both read back as `72429.5`.
