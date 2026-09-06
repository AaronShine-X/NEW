---
name: jushuitan-order-monitor
description: Use Microsoft Edge to inspect and conditionally process exception orders in a Jushuitan order-management page, submit return-order reviews, and monitor a configured supplier's available amount. Use for recurring Jushuitan order checks; keep store-specific names and thresholds in private local configuration.
---

# Jushuitan Order Monitor

Use the current Microsoft Edge session and the private local configuration to inspect a Jushuitan order-management page. This skill is intentionally separate from Xiaohongshu inventory, Tencent Docs, production, and cost-table workflows.

## Private configuration

Read the local, ignored configuration file `config/jushuitan-order-monitor.local.json` before acting. It should define:

- `bookmark_name`: the verified Edge bookmark for the Jushuitan order page.
- `product_name`: the exact product-name history value to search.
- `supplier_name`: the exact supplier to monitor.
- `alert_threshold`: the strict lower bound for the available amount.
- `alert_message`: the exact message to send when the amount is below the threshold.
- `timezone`: the timezone used for the daily-run guard, normally `Asia/Shanghai`.

Never commit the local configuration, credentials, cookies, account identifiers, screenshots, or real business data.

## Daily order check

1. Use Microsoft Edge. If Edge is closed, start Edge and connect to the new Edge tab; do not substitute Chrome.
2. From the verified bookmark, enter the order-management page, then open the left-side order-management entry. If the current page is already verified, do not navigate unnecessarily.
3. In the product-name field, select the exact configured value from the browser's saved/history values when available. If the history value cannot be verified, stop. A visible exact field value is acceptable only when the search results also clearly show the configured product.
4. Search and wait until the results are fully loaded. Read each result's product and status. Only rows whose product matches the configured product and whose status is explicitly `异常` are in scope.
5. If there are no matching exception rows, make no order changes. This is still a completed daily check.
6. Select every matching exception row. Before clicking `取消异常`, show the pending rows and wait for explicit user confirmation.
7. After cancellation, re-read the page and verify the rows are still selected and the exception status has been cleared. Before clicking the actual observed review-submission action (normally `审核推单`), show the pending rows again and wait for explicit confirmation.
8. Submit the review and verify a clear success result, such as a changed status, push time, or `已推送至供应商` message. Do not claim success from a click alone.

If an order had already been pushed, follow the page's explicit rollback branch only when the page presents it: use `撤回推单`, inspect the confirmation text, and require explicit confirmation before confirming any `撤回订单优先在线退款` choice. Do not infer that branch from a missing or ambiguous button.

## Supplier amount check

Enter the supplier section and open the configured supplier list. Find the exact configured supplier and read its available amount. When the amount is strictly below `alert_threshold`, send exactly the configured `alert_message`; otherwise remain quiet. Never click an online-recharge or other funding action.

Run the supplier check on the first valid run and after every five valid daily order checks, then reset the valid-check counter. A run counts only after the search results have been completely read. A failed run, an unresolved page, or a run paused for confirmation does not count. A second run on the same local calendar date does not repeat the order check.

## Scheduling and stopping

The daily guard uses the configured timezone. If the workflow is scheduled, use one run per calendar day and preserve the state needed for the five-check counter in the current task or its permitted local automation state.

Stop and ask the user to intervene if Edge, the page, login, permissions, CAPTCHA, the bookmark, the configured history value, the supplier identity, or an action button cannot be verified. Also stop if multiple rows or targets cannot be distinguished safely. Keep the task quiet when there is no exception order and no amount alert.

## Reporting

Report only meaningful outcomes:

- no exception rows found;
- rows awaiting confirmation, including their visible identifiers;
- cancellation and review submission verified;
- supplier amount and whether the threshold alert was triggered;
- a precise blocker and the user action required.
