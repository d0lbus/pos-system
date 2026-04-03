# Reporting Query Specification

## 1. Document Purpose

This document defines what each report should mean, what it should count, what filters it should support, and how reporting logic should avoid ambiguity or double counting.

It is intended to guide:
- report service logic
- backend query design
- dashboard summary logic
- export endpoint behavior
- frontend report UI expectations

This is especially important because the system contains overlapping financial areas such as:
- sales
- GCash transactions
- money in / money out
- offline sync states

---

## 2. Reporting Principles

- every report must have a clear business meaning
- one business event should not be counted twice in the same report meaning
- reports must distinguish source records from linked records
- cash and GCash contexts must remain separate where appropriate
- refunds and voids must not inflate normal completed-sales metrics
- recurring expense reminders must not be mistaken for real expenses
- unsynced offline records must be handled intentionally, not accidentally mixed in

---

## 3. Report Families

The reporting layer should support these main families:
- dashboard summaries
- sales reports
- inventory reports
- expense reports
- money flow reports
- GCash reports
- sync/operational state reports

---

## 4. Dashboard Summary Query Rules

Dashboard summaries should be quick operational aggregates, not overly heavy detail reports.

### Suggested Dashboard Metrics
- today’s sales total
- today’s expense total
- total money in for selected period
- total money out for selected period
- cash sales total
- GCash sales total
- low-stock count
- GCash balance summary
- pending sync count
- failed sync count if available

### Important Counting Rules
- today’s sales total should represent completed/recognized sales according to final sales status rules
- refunded/voided sales should not silently behave like normal successful sales totals
- GCash balance summary should come from GCash account state, not from naive summing of unrelated records alone
- pending sync count should count local/backend-tracked sync states intentionally, not guessed implicitly

---

## 5. Sales Report Meaning

Sales reports answer questions about sales performance and transaction activity.

### Base Sales Report Should Mean
A filtered view of sale records, their totals, payment methods, actors, and action context.

### Core Metrics
- number of sales
- total sales amount
- sales by payment method
- sales by cashier
- refunded sales count/amount
- voided sales count/amount
- edited sale count if shown

### Important Counting Rules
- completed sales should be separated from refunded/voided contexts
- if a report is labeled “completed sales total,” it should not include refunded/voided values as if they were unchanged successful sales
- if a report is labeled “all sales records,” then action/status context must be visible so totals are not misread

---

## 6. Sales Report Filters

Suggested filters:
- date range
- cashier
- payment method
- sale status/action type
- product
- sync status where relevant

### Filter Behavior Notes
- payment method should distinguish CASH vs GCASH
- sync status filter should be available only if the operational screen/report includes sync-aware records
- product filters may work through joins with sale items

---

## 7. Inventory Report Meaning

Inventory reports answer questions about stock state and stock movement.

### Core Inventory Reports
- current stock report
- low-stock report
- inventory movement history report
- damaged items report
- lost items report
- stock adjustment report

### Important Counting Rules
- current stock report should reflect current trusted stock values
- movement reports should summarize movement records by type and date range
- archived products must still resolve correctly in historical movement reports

---

## 8. Inventory Report Filters

Suggested filters:
- date range
- product
- category
- movement type
- product status where meaningful

### Filter Behavior Notes
- low-stock report may not need date filters unless presented as snapshot over time later
- movement history should support movement type filters like DAMAGED or LOST

---

## 9. Expense Report Meaning

Expense reports answer questions about recorded business costs.

### Core Expense Reports
- expense list by date range
- expense total by category
- expense total over time
- expense detail review

### Important Counting Rules
- only real posted expenses should count toward expense totals
- recurring reminders should not count as real expenses unless an actual expense record was posted
- soft-deleted expenses must be handled intentionally according to report mode

### Recommended Default Behavior
Default expense reports should exclude soft-deleted expenses unless there is a filter to include them for audit/admin review.

---

## 10. Expense Report Filters

Suggested filters:
- date range
- category
- deleted state
- created by if useful later

---

## 11. Money Flow Report Meaning

Money flow reports answer questions about broader cash movement in and out of the business.

### Core Money Flow Reports
- money-in report
- money-out report
- transfer-related report
- opening/closing cash report
- movement list with filters

### Important Counting Rules
- cashflow reports should use cashflow entries as their source records
- these reports should not be labeled as “sales totals” unless they are specifically designed to do so
- linked sales or GCash references should explain source context, but the primary source of count/sum here is the cashflow entry itself

### Critical Double-Counting Warning
Do not combine sales totals and cashflow totals in one metric unless the report explicitly defines that behavior. Sales and cashflow often reflect the same business event from different perspectives.

---

## 12. Money Flow Report Filters

Suggested filters:
- date range
- direction (IN/OUT)
- movement type
- source module
- related GCash account where relevant
- recorded by if needed

---

## 13. GCash Report Meaning

GCash reports answer questions about GCash-specific wallet/account activity.

### Core GCash Reports
- GCash transaction history
- GCash sales payment report
- GCash cash-in report
- GCash cash-out report
- per-account transaction report

### Important Counting Rules
- GCash reports should use GCash transactions as the primary source
- GCash balance summaries should reflect account balance state, not naive recomputation unless intentionally designed that way
- GCash reports should stay distinct from ordinary cashflow reports even if linked entries exist

### Fee Handling Note
Where fee details are shown, the report should display fee amount and fee mode clearly to avoid interpretation mistakes.

---

## 14. GCash Report Filters

Suggested filters:
- date range
- GCash account
- transaction type
- reference number
- related sale presence if useful

---

## 15. Sync and Operational State Report Meaning

These reports answer questions about offline-created operational records and sync behavior.

### Core Sync Reports
- pending sync sales
- failed sync sales
- sync status counts

### Important Counting Rules
- sync reports should be based on sync state records or sync-aware sale states, not assumptions
- a synced record should not remain counted as pending
- failed sync records should remain visible until resolved or cleared intentionally

---

## 16. Sync Report Filters

Suggested filters:
- date range
- sync state
- cashier/user
- record type if later expanded beyond sales

---

## 17. Report Source-of-Truth Mapping

This section defines which table/entity is the primary reporting source for each report family.

### Source Mapping
- sales reports -> `sales` + `sale_items` + `sale_action_histories`
- inventory reports -> `products` + `inventory_movements`
- expense reports -> `expenses`
- money flow reports -> `cashflow_entries`
- GCash reports -> `gcash_transactions` + `gcash_accounts`
- sync reports -> `offline_sync_records` and/or sync-aware sale data depending on final implementation
- dashboard summaries -> derived from multiple source-specific summary queries

### Principle
A report should not switch its source-of-truth casually. Its primary table(s) should match the report’s meaning.

---

## 18. Dashboard vs Report Query Difference

### Dashboard Queries
- small number of summary metrics
- fast, focused, operational
- limited aggregation

### Report Queries
- deeper filtering
- pagination or export-friendly result sets
- more detailed breakdowns

### Design Principle
Do not overload dashboard endpoints with full report logic.

---

## 19. Refund and Void Handling in Reporting

This is one of the most important reporting rules.

### Recommended Direction
Use either:
- clear sale status fields
- or sale action history-aware logic

so reports can distinguish:
- completed sales
- refunded sales
- voided sales

### Practical Rule
If a report says “completed sales total,” refunded/voided entries must not inflate that number.

### Optional Additional Report Views
- refunded totals report
- voided sales report
- net sales summary later if defined explicitly

---

## 20. Soft Delete and Archive Handling in Reporting

### Products
Archived products should still appear in historical reports through linked references.

### Expenses
Soft-deleted expenses should generally be excluded from normal business totals unless the report is explicitly an audit/admin view.

### Users
Inactive users should still resolve correctly in historical reports where they were the actor.

---

## 21. Export Query Direction

Export endpoints should reuse the same report logic as on-screen reports where possible.

### Principle
Do not create separate business rules for export that disagree with on-screen reporting.

### Practical Direction
- on-screen filters should map directly to export filters
- exported data columns should align with the report’s meaning
- export should not silently include hidden/excluded states unless chosen by filters

---

## 22. Suggested Report Output Shapes

### Summary-Oriented Response
Useful for dashboard and report headers:
- totals
- counts
- grouped subtotals

### Detail-Oriented Response
Useful for report tables:
- list of records
- pagination metadata where needed
- applied filters summary

### Export-Oriented Response
Useful for file generation:
- normalized row data
- stable column order
- report title/context metadata if desired

---

## 23. Query Layer Direction

The reporting layer should probably use dedicated report service functions and repository queries rather than reusing raw CRUD list endpoints.

### Why
Reporting usually needs:
- joins
- aggregations
- status-aware counting
- cross-table rules
- grouped summaries

### Suggested Structure
- `report_service.py` defines report business meaning
- `report_repository.py` performs optimized queries

---

## 24. Performance Considerations

### Potential Heavy Areas
- sales reports joined with sale items and filters
- inventory movement history over large date ranges
- GCash reports with fee detail and account filters
- export queries over broad date ranges

### Practical Mitigations
- add useful indexes
- paginate on-screen detail reports
- keep dashboard queries aggregated and narrow
- optimize export paths separately if needed

---

## 25. Risks and Considerations

### Risk: Double Counting Sales and Cashflow
Mitigation:
- keep report meanings explicit
- use source-of-truth mapping
- avoid mixed-total shortcuts

### Risk: Confusing GCash Balance with GCash Income
Mitigation:
- separate balance views from transaction totals
- label reports clearly

### Risk: Refunded Sales Misreported as Normal Sales
Mitigation:
- use sale action/status-aware logic
- expose refund/void filters and metrics clearly

### Risk: Soft-Deleted Expenses Accidentally Included
Mitigation:
- default to excluding deleted expenses in normal reports
- add explicit include-deleted filter only for admin review use

---

## 26. Success Criteria

This reporting query specification is successful if it:
- defines what each report means
- defines what each report should count
- defines how filters should behave
- reduces ambiguity across sales, GCash, and cashflow reporting
- is concrete enough to guide backend report service and repository implementation

