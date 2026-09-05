# 款号映射与错误库

Use this reference whenever a task involves style-code normalization, ambiguous handwriting, known user corrections, or previously learned failure modes.

## Style Mapping Rules

Apply only when the user has confirmed the mapping or the current task explicitly provides it. If a mapping conflicts with new user instructions, use the newest user instruction.

| Raw / Alias | Canonical |
|---|---|
| `328` | `0328` |
| `8328` | `0328` |
| `0328蓝色` / `0328蓝` | `0328` |
| `329` | `0329` |
| `8329` | `0329` |
| `8336` | `8836` |
| `格子裙里布` | `8338` |
| `工装裤` | `8339` |
| `0325` | `0326` when the cost table has no `0325` block and context matches |

## Known Handwriting / OCR Pitfalls

- `8809` can be misread as `8807`; if the cost table has `8809` but no `8807`, verify context before using `8807`.
- `8856` total `556` can be misread as `526`; verify by color/size detail sum and user correction.
- Handwritten `#` after a style code is not part of the style code.
- If a row is marked `返修`, do not merge it into normal style costs/quantities.

## General Error-Prevention Rules

- Re-read live Tencent Docs before deciding a style/row/date is absent.
- Do not overwrite formula/summary rows.
- Do not repeat completed follow-ups; track only current unresolved items.
- Preserve the latest user correction over older notes.
- Do not hard-code inventory or cost values from memory.
- If a Tencent Docs write fails mid-batch, re-read target cells before retrying.
- Do not silently create new categories or row meanings in the cost table; follow existing table classifications or ask.

## Cost Table Specific User Corrections

- For 2026-07-23 cost write, `8856` 洗水费 and 扣子/辅料 were confirmed to count into `8856` 面料费.
- Remaining misc should go to row 5 `前期杂费` when following prior misc classification.
- Misc folder items that are 工装裤 fabric/lining should be split to `8339` 面料 fee.

## Output Discipline

- Say `需确认` for unclear values.
- Expose discrepancies rather than hiding them.
- If the user allows a tolerance, state whether the difference is within tolerance.
- After writing, report exact cells and readback values.
