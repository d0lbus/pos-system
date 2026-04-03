# Dashboard and Reports Module Specification

## 1. Module Purpose

The Dashboard and Reports module is responsible for giving the minimart a clear operational and financial overview of the system’s data. It transforms records from Sales, Products, Inventory, Expenses, GCash, Money In / Money Out, and Offline Sync into readable summaries, alerts, filtered views, and exportable reports.

This module helps users answer practical business questions such as:
- How much did the store sell today?
- Which products are low in stock?
- How much money came in and went out?
- How much is currently in GCash versus physical cash?
- What expenses were recorded in a date range?
- Which sales were refunded, voided, or still pending sync?

The dashboard should focus on fast visibility, while the reporting layer should focus on deeper filtering, review, and export.

---

## 2. Module Goals

- provide a useful operational dashboard
- present financial and inventory summaries clearly
- support date-based and category-based filtering
- provide separate reporting views for key business areas
- keep cash and GCash summaries distinct
- support exportable reports
- support printable reports even without receipt printing
- include visibility into important operational states such as low stock and sync status

---

## 3. Scope of This Module

### In Scope
- dashboard summary cards
- dashboard alerts and highlights
- sales reports
- inventory reports
- expense reports
- money flow reports
- GCash reports
- action/history reporting where useful
- date range filtering
- cashier filtering
- category filtering
- payment method filtering
- transaction type filtering
- export support
- printable reports

### Out of Scope
- receipt printing
- advanced business intelligence dashboards
- predictive analytics
- supplier analytics
- multi-store roll-up reporting
- external accounting platform export integrations in version 1

---

## 4. Core Concepts

### Dashboard
The dashboard is the quick overview screen for the business. It should prioritize the most important real-time or recent operational information.

### Reports
Reports are more detailed, filterable, and review-oriented views of the system’s stored records.

### Summary vs Detail
The dashboard should answer “what is happening now or recently,” while reports should answer “what happened over a chosen period or category.”

### Separation of Financial Contexts
The reporting layer must keep distinctions clear between:
- cash sales and GCash sales
- GCash balances and register cash
- operational expenses and other money-out activity
- synced versus pending-sync operational data where shown

---

## 5. Dashboard Overview

The dashboard should be a high-visibility summary screen for Admin and should present the most relevant business indicators.

### Suggested Dashboard Priorities
- today’s sales summary
- total expenses summary
- total money in summary
- total money out summary
- low-stock alerts
- separate cash and GCash visibility
- recent transactions or activity highlights
- offline/sync status indicators if relevant

### Role Direction
- Admin should have access to the full dashboard
- Cashier access to dashboard views can be restricted or simplified based on final permission rules

---

## 6. Dashboard Summary Cards

The user asked for typical dashboard fields, so version 1 should support common operational summary cards.

### Suggested Core Cards
- Today’s Sales
- Today’s Expenses
- Total Money In
- Total Money Out
- Cash Sales Total
- GCash Sales Total
- Current Register Cash Indicator if modeled clearly
- GCash Balance Summary
- Low-Stock Product Count
- Pending Sync Count if relevant

### Important Rule
Dashboard totals should remain understandable and should avoid misleading double counting, especially where Sales, GCash, and Money Flow overlap.

---

## 7. Dashboard Alerts and Highlights

The dashboard should surface important operational issues.

### Suggested Alerts/Highlights
- low-stock products
- recently refunded or voided sales
- pending sync records
- failed sync records if available
- unusual recent money-out activity if later needed
- recent GCash activity summary

### Primary Goal
Help Admin quickly identify issues that need attention.

---

## 8. Main Report Groups

The system should support separate report groups for the major modules.

### 8.1 Sales Reports
Should support views such as:
- sales by date range
- sales by cashier
- sales by payment method
- refunded sales
- voided sales
- edited sales
- product-level sales summaries

### 8.2 Inventory Reports
Should support views such as:
- current stock report
- low-stock report
- inventory movement history
- damaged item report
- lost item report
- stock adjustments report

### 8.3 Expense Reports
Should support views such as:
- expense list by date range
- expense totals by category
- expense totals over time
- expense detail review

### 8.4 Money In / Money Out Reports
Should support views such as:
- money-in report
- money-out report
- cash movement report
- transfer-related report
- opening/closing cash summaries

### 8.5 GCash Reports
Should support views such as:
- GCash transaction history
- GCash sales payment report
- GCash cash-in report
- GCash cash-out report
- per-account filtered reporting

### 8.6 Sync/Operational State Reporting
Where useful, reporting should support:
- pending sync sales
- failed sync records
- synced versus unsynced counts in a date range

---

## 9. Filtering Requirements

The user confirmed that filtering should be supported broadly.

### Required Filter Directions
Reports should support filters such as:
- date range
- cashier
- category
- payment method
- transaction type
- product
- GCash account
- sync status where relevant

### Practical Rule
Only show filters that make sense for the selected report type.

Examples:
- inventory reports should emphasize product/category/date
- sales reports should emphasize cashier/payment method/date
- GCash reports should emphasize account/type/date/reference

---

## 10. Export and Print Requirements

The user confirmed that report export is required and printable reports should be supported.

### Required Directions
- export support: yes
- printable reports: yes

### Format Direction
The exact export formats were not locked, but the system should be designed to support practical formats such as:
- CSV
- Excel-compatible output
- PDF or print-friendly layout later if needed

### Version 1 Recommendation
A practical first implementation may start with simpler export paths and printable report views, then expand later.

---

## 11. Sales Report Details

### Key Metrics
Sales reporting should support:
- total sales amount
- number of sales
- sales by cashier
- sales by payment method
- refunded totals
- voided totals
- top-selling products if useful later

### Historical Clarity
Sales-related reports should preserve distinctions between:
- completed sales
- refunded sales
- voided sales
- edited sales where relevant

### Payment Context
Reports must clearly distinguish:
- cash sales
- GCash sales

---

## 12. Inventory Report Details

### Key Metrics
Inventory reports should support:
- current stock by product
- low-stock products
- stock movement count and volume by date range
- damaged quantities
- lost quantities
- adjustment records

### Historical Rule
Archived products must still be resolvable in inventory reporting when linked to historical data.

---

## 13. Expense Report Details

### Key Metrics
Expense reports should support:
- total expenses by date range
- expense count
- expense totals by category
- expense detail list

### Reminder Distinction
If recurring reminders appear in report-related views, they must not be confused with real posted expenses.

---

## 14. Money Flow Report Details

### Key Metrics
Money In / Money Out reporting should support:
- total money in
- total money out
- totals by type/category
- transfer-related views
- opening/closing cash visibility if modeled separately

### Financial Clarity Rule
The module must avoid misleading totals caused by counting the same business event twice across sales, GCash, and money movement layers.

---

## 15. GCash Report Details

### Key Metrics
GCash reporting should support:
- per-account transaction history
- total GCash sales payments
- total GCash cash-ins
- total GCash cash-outs
- reference-number-aware history browsing
- fee-related details where useful

### Separation Rule
GCash reports must remain clearly separate from generic cash movement reports, even though linked financial interpretations may still exist elsewhere.

---

## 16. Offline and Sync Visibility

Because offline selling is part of version 1, reporting and dashboard behavior should consider sync state where relevant.

### Dashboard Uses
The dashboard may show:
- pending sync count
- failed sync count
- last sync-related activity if later added

### Report Uses
Operational reporting may support:
- list of unsynced sales
- sync status filter on sales history

### Important Rule
The UI should not make unsynced records look identical to fully synced backend-confirmed records when sync status matters operationally.

---

## 17. User Access and Permissions

### Admin
Admin should have access to:
- full dashboard
- all report groups
- filters and exports
- printable views

### Cashier
Cashier access should be restricted based on final business rules.

Possible version 1 direction:
- limited or no access to full reporting
- sales-related views only if needed for operational use

The exact permission matrix can be refined later in the Auth and Access module.

---

## 18. UI Requirements

### Dashboard Screen
Suggested UI sections:
- summary cards row(s)
- low-stock alert area
- recent transactions/activity area
- GCash summary area
- sync status area if relevant

### Reports Area
Suggested report UI structure:
- left-side report navigation or tab navigation
- filter bar
- summary metrics section
- table/list/chart area if later needed
- export/print actions

### UX Priorities
- easy to scan
- not overloaded with unnecessary metrics
- clear separation of modules and report types
- responsive layout on tablet and desktop

---

## 19. Data Source Integration

The Dashboard and Reports module depends on many source modules.

### Major Source Modules
- Sales / POS
- Products
- Inventory
- Expenses
- Money In / Money Out
- GCash Accounts and Transactions
- Offline Mode and Sync
- Audit/history records where useful

### Important Design Principle
The reporting layer should use source-linked and traceable data rather than vague aggregated values with unclear origins.

---

## 20. Validation and Data Integrity Considerations

### Reporting Accuracy Rules
- reports should only count records according to their intended business meaning
- refunded and voided records should not inflate normal completed sales totals
- recurring reminders should not be mistaken for actual expenses
- GCash totals and cash totals must remain distinct

### Historical Integrity
Archived products and old records should still appear correctly in historical report contexts.

---

## 21. Data Design Direction

The reporting layer may use:
- direct filtered queries
- derived summary endpoints
- reusable reporting service logic

### Possible Dashboard Summary Inputs
- sales totals
- low-stock counts
- expense totals
- money-in totals
- money-out totals
- GCash balances
- pending sync counts

### Possible Report-Oriented Structures
Depending on implementation, the backend may provide:
- report query endpoints
- summary endpoints
- export endpoints

The final architecture can be detailed later in the API and backend technical structure documents.

---

## 22. API Direction

### Possible Endpoint Groups
- dashboard
- reports/sales
- reports/inventory
- reports/expenses
- reports/cashflow
- reports/gcash
- reports/sync
- exports

### Example Endpoint Direction
- get dashboard summary
- get sales report
- get inventory report
- get expense report
- get cashflow report
- get GCash report
- export selected report

Exact endpoint naming can be finalized later in the API-specific canvas.

---

## 23. Logging and Audit Considerations

The reporting layer itself may not need separate business logs for normal viewing, but export actions and certain admin-only report actions may later be tracked if the business wants greater auditability.

### Possible Future Tracking
- export action log
- printable report generation log
- admin report access audit if needed later

Version 1 does not require heavy report access logging unless implemented as part of broader audit policy.

---

## 24. Risks and Considerations

### Risk: Double Counting Across Modules
Because sales, GCash, and money movement are related, poorly designed reporting can show misleading totals.

Mitigation:
- define report purpose clearly
- separate wallet balance views from income/outflow views
- use linked source-aware calculations

### Risk: Too Much Information on Dashboard
If the dashboard is overloaded, it becomes less useful.

Mitigation:
- prioritize key summary cards and alerts
- keep deeper detail in reports instead of dashboard cards

### Risk: Unsynced Records Misleading the User
Offline records may make summaries confusing if sync state is ignored.

Mitigation:
- expose sync-aware context where needed
- distinguish pending and confirmed data when operationally important

---

## 25. Version 1 Success Criteria for This Module

This module is successful in version 1 if it can:
- provide a useful dashboard overview
- show typical operational summary cards
- clearly separate cash and GCash contexts
- show low-stock and sync-related operational alerts
- provide filterable reports for sales, inventory, expenses, cash flow, and GCash
- support exportable and printable report workflows
- integrate correctly with all core operational modules

---

## 26. Suggested Future Enhancements

Possible later enhancements include:
- richer charts and trend visualizations
- top-selling product panels
- deeper profitability analysis
- advanced export formats
- scheduled report generation
- more advanced sync analytics

---

## 27. Next Related Module Documents

After this module, the most connected documents to create are:
- Auth and Access Module
- System Architecture and Technical Structure Module
- Reporting API and Query Specification
- Data Model / ERD Overview

