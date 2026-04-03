# Money In / Money Out Module Specification

## 1. Module Purpose

The Money In / Money Out module is responsible for tracking financial movement across the minimart beyond simple transaction lists. It provides a central ledger-like layer that records how money enters and leaves the business, while keeping distinctions clear between:
- sales-related money movement
- expense-related money movement
- register cash movement
- GCash-related movement
- transfers between register cash and GCash accounts
- opening and closing cash records

This module helps the business monitor actual financial flow in a more organized way than relying only on sales history, expense lists, or GCash logs separately.

---

## 2. Module Goals

- track incoming and outgoing money clearly
- separate cash-on-hand and GCash-related balances
- automatically create money movement records from sales and expenses where applicable
- support manual financial entries for typical business cases
- support daily opening and closing cash records
- support transfers between register cash and GCash accounts
- provide history, filtering, and reporting for money movement
- remain auditable and understandable for store operations

---

## 3. Scope of This Module

### In Scope
- record incoming money
- record outgoing money
- auto-create records from sales
- auto-create records from expenses
- track register cash separately
- track transfers between register and GCash where relevant
- support opening cash entry
- support closing cash entry
- support optional notes
- provide money movement history
- integrate with reports and dashboard summaries

### Out of Scope
- full accounting system behavior
- external bank integration
- advanced general ledger accounting
- supplier payable tracking
- tax accounting
- multi-store financial separation

---

## 4. Core Concepts

### Money In
Represents money entering the business or a tracked internal financial area.

### Money Out
Represents money leaving the business or a tracked internal financial area.

### Register Cash
Represents physical cash handled inside store operations.

### GCash Movement Linkage
GCash transactions may create related money movement entries, but GCash remains separately tracked as its own wallet/account layer.

### Opening and Closing Cash
The system should support daily cash opening and closing records to help monitor the register’s cash state.

---

## 5. Main Use Cases

### 5.1 Sales-Driven Money In
When a sale is completed, the system should create money-in records that reflect the sale according to the selected payment method.

### 5.2 Expense-Driven Money Out
When an expense is recorded, the system should create a money-out entry automatically.

### 5.3 Manual Cash Movement
Admin should be able to record additional typical cash-in or cash-out entries when needed.

### 5.4 Register and GCash Transfer Tracking
The system should support explicit tracking when value moves between register cash and a GCash account.

### 5.5 Daily Cash Monitoring
The system should support opening cash and closing cash records for the register.

---

## 6. Supported Movement Categories

The exact final list can be refined later, but version 1 should support typical financial movement categories such as:

### Money In Categories
- SALE_CASH
- SALE_GCASH
- OWNER_CASH_IN if needed
- MISCELLANEOUS_IN
- TRANSFER_FROM_GCASH if relevant to register view
- OPENING_CASH

### Money Out Categories
- EXPENSE
- GCash-related transfer out where relevant
- MISCELLANEOUS_OUT
- WITHDRAWAL if used later
- CLOSING_CASH record context if modeled as a movement or daily summary event

### Important Note
The final implementation may use separate transaction types, entry types, and source links, but the module must preserve the business meaning of why money moved.

---

## 7. Automatic Record Generation Rules

### From Sales
The system should automatically create money movement records when a sale is completed.

#### Cash Sale
A cash sale should increase register-related money-in records.

#### GCash Sale
A GCash sale should create a money-in entry that remains linked to GCash-related movement, while still preserving separation between:
- cash-on-hand
- GCash balance

### From Expenses
An expense should automatically create a money-out entry.

### From GCash Transactions
Certain GCash cash-in, cash-out, or transfer events should create linked money movement records when relevant.

---

## 8. Manual Entry Flow

### Purpose
The module must allow manual money-in and money-out entries for common business cases that are not purely sales or expenses.

### Flow
1. Authorized user opens money movement entry.
2. User selects entry direction: IN or OUT.
3. User selects a category/type.
4. User enters amount.
5. User optionally adds a note.
6. User selects related source context if needed.
7. System saves the record.
8. System updates related balances if applicable.
9. System writes audit records.

---

## 9. Opening and Closing Cash

### Opening Cash
The system should support recording the register’s opening cash for the day.

### Closing Cash
The system should support recording the register’s closing cash for the day.

### Purpose
These records help:
- monitor daily cash handling
- compare expected and actual register cash
- improve operational visibility

### Design Direction
Opening and closing cash may be modeled either as:
- specific money movement categories
- or dedicated daily cash session records linked to money movement

The final implementation detail can be decided later, but version 1 must support the business behavior itself.

---

## 10. Register Cash and GCash Separation

A core requirement of this system is that cash and GCash must not be treated as the same balance.

### Required Separation
The module must clearly distinguish between:
- physical register cash
- GCash wallet balances

### Practical Meaning
- cash sales affect register cash
- GCash sales affect the selected GCash account
- transfers between them should be explicitly recorded
- reports should be able to show them separately

---

## 11. Transfer Tracking

The system should support transfers between register cash and GCash where relevant.

### Example Cases
- cash moved from register to GCash cash-in activity
- value moved from GCash back into physical cash context

### Transfer Rules
- transfer records should remain understandable in history
- the source and destination context should be clear
- linked records should not make balances look duplicated

This is especially important because GCash fee handling can complicate the true financial effect of some transactions.

---

## 12. Main Features

### 12.1 Money Movement List
The module should provide a full history list for money-in and money-out entries.

Suggested content:
- date/time
- direction
- category/type
- amount
- source link if applicable
- related account or context
- note if present
- recorded by

### 12.2 Manual Entry Form
Authorized users should be able to create manual IN or OUT entries.

### 12.3 Opening / Closing Cash Entry
The module should support easy creation of opening and closing cash records.

### 12.4 Filtered History View
Users should be able to filter by:
- date range
- direction
- category/type
- related module/source
- user
- payment context where useful

### 12.5 Summary Views
The module should support summary totals such as:
- total money in
- total money out
- cash-related totals
- GCash-related totals where relevant

---

## 13. Business Rules

### Entry Rules
- every money movement must have a direction: IN or OUT
- every money movement should have a type/category
- amount must be valid and positive
- note is optional

### Auto-Creation Rules
- sales should auto-create money movement entries
- expenses should auto-create money movement entries
- linked entries should remain traceable to their source record

### Separation Rules
- register cash and GCash balances must remain separate
- linked transfers should not be confused with ordinary income or ordinary expense

### Audit Rules
- important financial movement must remain traceable
- user and timestamp should be captured for entries

---

## 14. Integration with Sales / POS Module

The Sales / POS module feeds this module automatically.

### Relationship Rules
- completed sales must create money-in records
- payment method affects the interpretation of the money movement
- sale-linked entries should remain connected to the originating sale
- refunds or void-related reversals should also be reflected consistently when finalized business logic requires it

---

## 15. Integration with Expenses Module

The Expenses module feeds this module automatically.

### Relationship Rules
- every expense should create a related money-out record
- expense-linked money movement should remain traceable to the original expense
- deleting or soft-deleting an expense should preserve understandable financial history behavior according to finalized rules

---

## 16. Integration with GCash Accounts and Transactions Module

This module must work closely with the GCash module without replacing it.

### Relationship Rules
- GCash has its own wallet/account tracking
- money movement records may reflect the broader financial effect of GCash events
- the system must avoid double-counting balances across cash and GCash layers
- transfer-related flows must remain explicit and understandable

---

## 17. Integration with Reports and Dashboard

The Money In / Money Out module is a major source for operational summaries.

### Dashboard Uses
The dashboard may display:
- total money in
- total money out
- cash on hand indicators
- GCash-related indicators where appropriate
- daily financial overview

### Report Uses
The reporting layer should support:
- money-in report
- money-out report
- cash movement report
- transfer report
- opening/closing cash summaries
- date-based financial summaries

---

## 18. User Access and Permissions

### Admin
Admin should be able to:
- view money movement history
- create manual money-in entries
- create manual money-out entries
- record opening cash
- record closing cash
- review filtered summaries and reports

### Cashier
Cashier access should be limited unless a specific flow requires it.

Cashier may interact with this module indirectly through:
- sales creation
- GCash transaction recording tied to sales or allowed operational actions

Direct access to manual financial entry screens should remain controlled.

---

## 19. UI Requirements

### Money Movement List Screen
Suggested UI elements:
- date range filter
- direction filter
- category/type filter
- amount column
- source reference column
- note column
- recorded by column
- quick summary cards

### Manual Entry Form
Suggested fields:
- direction
- category/type
- amount
- optional note
- related source context if needed

### Opening / Closing Cash Screen
Suggested fields:
- session/date context
- amount
- optional note
- submit action

### UX Priorities
- clear distinction between IN and OUT
- clear distinction between cash and GCash context
- readable financial history
- responsive layout for tablet and desktop

---

## 20. Validation Rules

### Entry Validation
- direction is required
- category/type is required
- amount must be positive
- note is optional

### Source Validation
- linked source references should point to valid source records when used
- transfer-related entries should preserve source/destination meaning clearly

### Balance Safety Direction
The implementation should prevent obviously invalid financial state updates where practical, especially when actions affect tracked balances.

---

## 21. Data Design Direction

### Core Money Movement Entity
Suggested fields:
- id
- direction
- movement_type
- amount
- note nullable
- source_module nullable
- source_record_id nullable
- related_gcash_account_id nullable
- recorded_by
- created_at
- updated_at if needed

### Optional Daily Cash Session Entity
If opening/closing cash is modeled separately, possible fields may include:
- id
- date
- opening_cash
- closing_cash
- created_by
- created_at
- updated_at

The final design can decide whether this stays inside the money movement entity or uses a separate daily cash session structure.

---

## 22. API Direction

### Possible Endpoint Groups
- cashflow
- cashflow/opening-closing
- cashflow/transfers

### Example Endpoint Direction
- get money movement list
- create money-in entry
- create money-out entry
- record opening cash
- record closing cash
- get summary totals
- get transfer history

Exact endpoint naming can be finalized later in the API-specific canvas.

---

## 23. Logging and Audit Requirements

The following must be traceable:
- manual money-in entries
- manual money-out entries
- auto-created entries from sales
- auto-created entries from expenses
- opening cash entries
- closing cash entries
- transfer-related entries
- user and timestamp for all important financial records

This is necessary because the module affects:
- daily operations
- financial trust
- report accuracy
- reconciliation across system areas

---

## 24. Risks and Considerations

### Risk: Double Counting Between Sales, GCash, and Cash Flow
If financial records are not linked carefully, the system may display misleading totals.

Mitigation:
- keep source links explicit
- separate wallet balance tracking from general movement display
- clarify report logic for totals

### Risk: Confusion Around Opening and Closing Cash
If these are not modeled clearly, cash handling becomes hard to review.

Mitigation:
- keep daily cash handling explicit
- provide dedicated UI or strongly labeled categories

### Risk: Overly Generic Manual Entries
If manual entries are too vague, later reporting becomes harder to trust.

Mitigation:
- require type/category selection
- allow optional notes
- preserve user and timestamp

---

## 25. Version 1 Success Criteria for This Module

This module is successful in version 1 if it can:
- record money in and money out clearly
- auto-create entries from sales and expenses
- keep register cash separate from GCash balances
- support transfers between register and GCash contexts
- support opening and closing cash recording
- provide searchable and filterable history
- integrate correctly with Sales, Expenses, GCash, Reports, and Dashboard

---

## 26. Suggested Future Enhancements

Possible later enhancements include:
- richer reconciliation workflows
- variance detection between expected and actual cash
- financial approval workflows
- more structured owner cash-in/withdrawal categories
- stronger analytics and trend reporting

---

## 27. Next Related Module Documents

After this module, the most connected documents to create are:
- Expenses Module
- Offline Mode and Sync Module
- Dashboard and Reports Module
- Auth and Access Module
- Money Flow API and Data Model Module

