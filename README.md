# Ecommerce Inventory Operations Assistant

Ecommerce Inventory Operations Assistant is a Codex skill for Xiaohongshu commerce operations. It connects order analysis, live inventory, replenishment decisions, production planning, receipt tracking, cost-table writes, supply-project pricing, and Tencent Docs readback verification.

The skill trigger name inside Codex remains `小红`.

## What It Does

- Order and SKU analysis: clean Xiaohongshu order exports, group by color and size, and compare demand with live available stock.
- Inventory and replenishment: read live Tencent Docs inventory, separate available stock, in-transit quantity, recent consumption, and uncertain items before recommending replenishment.
- Production and receipts: prepare production-plan or receipt writes, protect formula-owned columns and summary rows, and verify by reading the sheet back after writes.
- Cost-table workflow: extract and merge fabric, processing, shrinkage, accessories, button, washing, miscellaneous, and factory-shipment costs from screenshots or payment records, preview them, and write only after approval.
- Supply-project pricing: calculate reusable-return exposure, closure tail risk, capital cost, break-even price, and target-profit quote.
- Error prevention: preserve confirmed style-code mappings, handwriting/OCR pitfalls, and Tencent Docs write boundaries.

## Repository Layout

```text
.
|-- SKILL.md
|-- INSTALL.md
|-- config/
|   `-- tencent-docs.example.json
|-- references/
|   |-- cost-table.md
|   |-- inventory-orders.md
|   |-- mappings-errors.md
|   |-- production-advice.md
|   |-- production-table.md
|   `-- supply-project-profit.md
`-- scripts/
    `-- supply_project_pricing.py
```

`SKILL.md` is the Codex entry point. It contains shared rules and task routing. Detailed workflow instructions live in `references/` and are loaded only when relevant.

## Main Workflows

### Inventory, Orders, And Replenishment

Use `references/inventory-orders.md` for Xiaohongshu order exports, SKU statistics, live inventory checks, shortage calculations, recent seven-complete-day consumption, and replenishment forecasts.

Key rules:

- Use live Tencent Docs data; do not reuse old quantities as current facts.
- Use the live available-stock column in the configured inventory sheet as the stock basis.
- Analyze different colors separately.
- Mark unclear fields, quantities, rows, columns, or mappings as `需确认`.

### Production Planning And Receipt Writes

Use `references/production-table.md` for production plans, receipt writes, quantity corrections from images, missing style blocks, old-format production rows, and reverse sync to inventory.

The configured production/receipt sheet includes a formula-owned unreceived-quantity column. It must not be written, cleared, or manually repaired unless the user explicitly approves.

### Production Advice And Size Allocation

Use `references/production-advice.md` to decide how many pieces to make and how to allocate color and size quantities, including fixed-roll constraints, integer rounding, round-ten execution choices, and stockout replenishment.

This workflow separates actual demand, recent fulfilled shipments, current stock, confirmed in-transit quantities, stockout bias, and the user's latest constraints. Instructions such as "only one roll", "only S and M", or "only khaki" are hard limits.

### Cost Table

Use `references/cost-table.md` for cost-table writes, fabric costs, processing costs, shrinkage, accessories, miscellaneous costs, buttons, washing fees, factory shipment quantities, and payment screenshot extraction.

Before writing, provide an auditable preview with source totals, mapped style codes, target date column, target rows, current target-cell values, and unresolved items. After writing, read back target cells and summary/formula rows.

### Supply-Project Pricing

Use `references/supply-project-profit.md` and `scripts/supply_project_pricing.py` for wholesale or supply projects involving return rates, reusable returns, sudden store closure, contract duration, capital cost, deposits, break-even pricing, and target profit.

Example:

```powershell
python scripts/supply_project_pricing.py --cost 52 --daily-orders 500 --return-rate 40 --contract-days 180 --return-days 10 --production-days 5 --annual-capital-rate 3 --target-profit 10
```

The script prints JSON with gross shipments, retained units, return-loop stock, committed production, closing-stock exposure, capital cost, break-even price, quoted price, and expected project profit.

## Tencent Docs Configuration

This skill can connect to a user's private Tencent Docs workbook, but this public README does not include specific workbook names, sheet names, sheet IDs, or account-related details.

Only the generic table roles need to be configured locally or in the target environment:

| Role | Purpose |
|---|---|
| Inventory sheet | Live stock and SKU inventory |
| Production and receipt sheet | Production plans, receipts, and unreceived quantities |
| Cost table | Cost entries, payment extraction, and reconciliation |
| Optional legacy production sheet | Old-format production rows, only when explicitly requested |

Specific IDs and sheet names should stay in the private environment only. Before acting, the skill still re-reads live headers, dates, rows, columns, formulas, and target cells.

## Installation

Clone or download this repository, then place its contents in the Codex skills directory:

```text
~/.codex/skills/小红/
```

Required layout:

```text
~/.codex/skills/小红/
|-- SKILL.md
|-- config/
|-- references/
`-- scripts/
```

Tencent Docs tooling and credentials must be configured separately in the target Codex environment. Do not commit tokens, cookies, account data, specific document IDs, or other credentials to this repository.

To connect real Tencent Docs, copy `config/tencent-docs.example.json` to `config/tencent-docs.local.json` and fill in the private workbook and sheet configuration locally. `config/*.local.json` is ignored by Git.

## Safety Boundaries

- Preview before any Tencent Docs write unless the skill's explicit image-correction workflow applies.
- Write only after clear user approval.
- After each write, read back target cells, formula rows, and summary rows.
- Never overwrite formula-owned columns, formula rows, or summary rows.
- The user's latest correction overrides older memory and older rules.
- Do not commit `.bak` backups, real credentials, cookies, account screenshots, or sensitive raw data.

## Project Name

`Ecommerce Inventory Operations Assistant` describes the skill's practical role: it connects demand, inventory, production, cost, and pricing into a repeatable commerce operations workflow.

---

# 电商库存运营助手

电商库存运营助手是一个面向小红书电商运营的 Codex skill，用来串联订单统计、实时库存、补货判断、做货计划、收货回写、成本表填写、供货报价和腾讯文档回读验证。

Codex 内部的 skill 触发名仍然保留为 `小红`。

## 功能概览

- 订单与 SKU 分析：清洗小红书订单导出，按颜色和尺码统计，并与实时可发库存对比。
- 库存与补货判断：读取腾讯文档实时库存，区分可发库存、在途数量、近期消耗和不确定项，再给出补货建议。
- 做货与收货：准备生产计划或收货写入，保护公式列和汇总行，并在写入后回读验证。
- 成本表工作流：从截图或付款记录中归纳面料、加工、缩水、辅料、扣子、洗水、杂费和工厂出货数量，先预览再写入。
- 供货项目报价：计算可复用退货、关店尾货风险、资金成本、保本价和目标利润报价。
- 错误预防：保留已确认的款号映射、手写/OCR 易错点和腾讯文档写入边界。

## 目录结构

```text
.
|-- SKILL.md
|-- INSTALL.md
|-- config/
|   `-- tencent-docs.example.json
|-- references/
|   |-- cost-table.md
|   |-- inventory-orders.md
|   |-- mappings-errors.md
|   |-- production-advice.md
|   |-- production-table.md
|   `-- supply-project-profit.md
`-- scripts/
    `-- supply_project_pricing.py
```

`SKILL.md` 是 Codex 加载的入口文件，包含通用规则和任务路由。具体场景的细节放在 `references/` 中，只有相关任务才需要读取。

## 主要工作流

### 库存、订单与补货

使用 `references/inventory-orders.md` 处理小红书订单导出、SKU 统计、实时库存检查、缺口计算、近七个完整日消耗和补货预测。

关键口径：

- 使用腾讯文档实时数据，不复用旧数量作为当前事实。
- 用指定库存表中的实时可发库存列作为库存口径。
- 不同颜色分开分析。
- 不清楚的字段、数量、行列或映射标为 `需确认`。

### 做货、收货与排单

使用 `references/production-table.md` 处理做货计划、收货写入、图片修正数量、缺失款式区块、旧格式生产行和反向同步库存。

默认生产/收货表中存在公式负责的未到货数量列，不能写入、清空或手动修复，除非用户明确批准。

### 做货建议与配码

使用 `references/production-advice.md` 判断要做多少件、怎么分配颜色和尺码，以及固定条数、整数化、整十取整、断码补货等问题。

这个工作流会区分真实需求、近期已发货、当前库存、已确认在途、断码偏差和用户最新约束。比如“只做一条”“只做 S 和 M”“只做卡其色”都属于硬限制。

### 成本表

使用 `references/cost-table.md` 处理成本表、面料费、布料费、加工费、缩水、辅料、杂费、扣子、洗水费、工厂出货数量以及付款截图提取。

写入前必须提供可审计预览，包括来源合计、映射款号、目标日期列、目标行、当前单元格值和待确认项。写入后必须回读目标单元格和汇总/公式行。

### 供货报价与盈亏

使用 `references/supply-project-profit.md` 和 `scripts/supply_project_pricing.py` 处理供货项目的退货率、可复用退货、突然关店、合同周期、资金成本、押金、保本价和目标利润。

示例：

```powershell
python scripts/supply_project_pricing.py --cost 52 --daily-orders 500 --return-rate 40 --contract-days 180 --return-days 10 --production-days 5 --annual-capital-rate 3 --target-profit 10
```

脚本会输出 JSON，包含发货量、留存销量、退货循环库存、未完成生产、关店尾货敞口、资金成本、保本价、报价和项目利润。

## 腾讯文档配置

这个 skill 支持连接用户自己的腾讯文档工作簿，但公开 README 不包含具体工作簿名、表名、sheet ID 或账号相关信息。

需要在本地或目标环境中配置的只是通用表角色：

| 表角色 | 用途 |
|---|---|
| 库存表 | 实时库存和 SKU 库存 |
| 生产/收货表 | 做货计划、收货和未到货数量 |
| 成本表 | 成本录入、付款提取和金额核对 |
| 可选旧版生产表 | 旧格式生产行，仅在用户明确要求时使用 |

具体 ID 和表名只应保存在私有环境中。实际操作前仍要重新读取实时表头、日期、行列、公式和目标单元格。

## 安装

克隆或下载本仓库后，把内容放入 Codex 技能目录：

```text
~/.codex/skills/小红/
```

需要保留的目录结构：

```text
~/.codex/skills/小红/
|-- SKILL.md
|-- config/
|-- references/
`-- scripts/
```

腾讯文档工具和凭据需要在目标 Codex 环境中单独配置。不要把 token、cookie、账号信息、具体文档 ID 或其他凭据提交到本仓库。

需要连接真实腾讯文档时，可以复制 `config/tencent-docs.example.json` 为 `config/tencent-docs.local.json`，再在本地填写私有工作簿和表配置。`config/*.local.json` 不会被提交。

## 安全边界

- 写入腾讯文档前先预览，除非 skill 中明确的图片修正数量流程适用。
- 只有用户明确批准后才写表。
- 每次写入后回读目标单元格、公式行和汇总行。
- 不覆盖公式列、公式行或汇总行。
- 用户最新纠正优先于旧记忆和旧规则。
- 不提交 `.bak` 备份文件、真实凭据、cookie、账号截图或敏感原始数据。

## 项目名称

`电商库存运营助手` 概括的是这个 skill 的实际作用：围绕电商库存，把需求、库存、做货、成本和报价连接成一套可重复执行的运营流程。

## Related Skill

`jushuitan-order-monitor/SKILL.md` is a separate Microsoft Edge and Jushuitan skill for exception-order checks, review submission, and configured supplier-amount monitoring. Keep product names, supplier names, bookmarks, thresholds, and account details in the ignored local configuration; do not commit real business data. Install it separately under `~/.codex/skills/jushuitan-order-monitor/`.

---

## 相关 Skill

`jushuitan-order-monitor/SKILL.md` 是独立的 Microsoft Edge 聚水潭 Skill，用于异常订单检查、审核推送和指定供应商可用金额监控。商品名、供应商名、书签、阈值和账号信息应保存在 Git 忽略的本地配置中，不要提交真实业务数据。需要使用时，单独安装到 `~/.codex/skills/jushuitan-order-monitor/`。
