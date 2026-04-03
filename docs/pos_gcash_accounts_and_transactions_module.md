# GCash Accounts and Transactions Module Specification

## 1. Module Purpose

The GCash Accounts and Transactions module is responsible for managing all GCash-related activity in the POS system. It handles GCash as both:
- a payment method used in sales
- a separately tracked digital wallet balance

This module must support one or more GCash accounts, record GCash cash-in and cash-out activity, preserve reference numbers and transaction details, support OCR-assisted data entry from screenshots or photos, and keep GCash history clearly separated from normal cash activity.

This module is important because the business does not use a direct GCash payment gateway in version 1. Instead, it records real-world GCash transactions manually, with OCR assistance when useful.

---

## 2. Module Goals

- support one or more GCash accounts
- track GCash balances separately from cash on hand
- record GCash sales payments
- record GCash cash-in and cash-out transactions
- support transaction fee handling per entry
- preserve reference numbers and transaction details
- provide separate GCash history and reporting
- support OCR-assisted extraction from screenshots or photos
- integrate cleanly with sales, money flow, reports, and audit logs

---

## 3. Scope of This Module

### In Scope
- create and manage multiple GCash accounts
- record GCash payment transactions from sales
- record GCash cash-in transactions
- record GCash cash-out transactions
- store GCash reference numbers
- store transaction amount and fee-related details
- track account balances
- support OCR-assisted GCash transaction entry
- maintain separate GCash history views
- feed GCash records into reports and money movement tracking
- support transfers involving register cash and GCash where applicable

### Out of Scope
- direct GCash payment gateway integration
- automatic real-time sync with GCash platform APIs
- bank integration
- multi-store wallet separation
- advanced reconciliation with external financial platforms

---

## 4. Core Concepts

### GCash as Payment Method
A sale can use GCash as its payment method. When this happens, the sale is recorded in the Sales module and a related GCash record must also be created.

### GCash as Wallet Balance
Each GCash account has its own running balance. GCash transactions should affect that balance according to the transaction type and fee behavior.

### Multiple Account Support
The system must support multiple GCash accounts. Each account should be identifiable and manageable independently.

### Separate History Requirement
GCash transactions must have their own history and reporting views rather than being mixed only into general sales or general cash flow lists.

---

## 5. GCash Account Management

### Account Purpose
A GCash account record represents one real-world GCash wallet/account used by the business.

### Account Capabilities
Admin should be able to:
- create a GCash account
- edit account details
- activate or deactivate an account
- view account balance
- view account transaction history

### Suggested Account Fields
Each GCash account should support:
- account name
- account number or identifier
- current balance
- status
- created/updated timestamps

### Status Direction
Possible account statuses may include:
- ACTIVE
- INACTIVE
- ARCHIVED if needed later

For version 1, active/inactive handling is enough.

---

## 6. Supported GCash Transaction Types

The module must support at least the following transaction types:
- SALE_PAYMENT
- CASH_IN
- CASH_OUT
- TRANSFER_IN if needed for register-to-GCash or related movement
- TRANSFER_OUT if needed for GCash-to-register or related movement
- ADJUSTMENT if future correction flow is needed

### Required Confirmed Types for Version 1
At minimum, the system must clearly support:
- GCash sale payment recording
- GCash cash in
- GCash cash out

---

## 7. GCash Sales Payment Flow

### Purpose
This flow records a sale that was paid using GCash.

### Flow
1. User completes a sale in the Sales / POS module.
2. User selects GCash as payment method.
3. User selects the relevant GCash account.
4. System creates the sale record.
5. System creates a related GCash transaction record.
6. System updates the selected GCash account balance according to finalized business rules.
7. System writes financial and audit records.

### Business Rule
GCash sales should increase the selected GCash account balance unless future business exceptions require a different rule.

---

## 8. GCash Cash-In Flow

### Purpose
This flow records a real-world GCash cash-in event.

### Example Business Case
A customer gives cash, and the store sends value into a GCash account. Depending on the real transaction setup:
- the main amount may enter the GCash account
- a fee may go to the register
- the fee may already be deducted from the transaction
- the fee may already be included in the transaction amount

### Flow
1. User opens GCash transaction entry.
2. User selects CASH_IN.
3. User selects the GCash account.
4. User enters or confirms the amount.
5. User records fee handling mode.
6. User enters or confirms the reference number.
7. System updates GCash account balance and related money flow records.
8. System stores the transaction.
9. System writes audit records.

---

## 9. GCash Cash-Out Flow

### Purpose
This flow records a real-world GCash cash-out event.

### Flow
1. User opens GCash transaction entry.
2. User selects CASH_OUT.
3. User selects the GCash account.
4. User enters or confirms the amount.
5. User records fee handling mode if needed.
6. User enters or confirms the reference number.
7. System updates the selected GCash account balance.
8. System creates corresponding money flow records.
9. System stores the transaction.
10. System writes audit records.

---

## 10. Transaction Fee Handling

Fee behavior in GCash transactions can vary depending on the real-world case.

### Confirmed Business Rule
Fee handling must be a **manual choice per entry**.

### Supported Fee Cases
The system should support cases where:
- fee is deducted from the transaction
- fee is included in the transaction
- fee goes to the register

### Design Direction
Each GCash transaction should store enough detail to explain:
- the main transaction amount
- whether a fee exists
- the fee amount if present
- how the fee was handled

### Importance
This is necessary to avoid incorrect balance computation and incorrect financial reporting.

---

## 11. OCR-Assisted GCash Entry

This module is connected to OCR because GCash entries may be based on screenshots or transaction photos.

### OCR Use Cases
OCR should help extract likely values such as:
- reference number
- amount
- visible account clue
- date/time if visible
- fee clue if readable

### OCR Flow
1. User opens GCash entry.
2. User uploads or captures a screenshot/photo.
3. Backend runs OCR.
4. System extracts likely values.
5. Suggested values are shown in editable fields.
6. User confirms or corrects the data.
7. User saves the transaction.

### Rule
OCR is assistance only. Final transaction submission must depend on user confirmation.

---

## 12. Main Features

### 12.1 GCash Account List
Admin should be able to view all GCash accounts with:
- account name
- account number/identifier
- current balance
- status
- action buttons

### 12.2 GCash Account Detail View
The account detail view should show:
- account information
- current balance
- recent transactions
- filtered transaction history
- summary totals where useful

### 12.3 GCash Transaction Entry
Users should be able to create GCash transactions by:
- selecting account
- selecting transaction type
- entering amount
- entering reference number
- setting fee handling
- adding optional note
- using OCR assistance where needed

### 12.4 GCash Transaction History
The module must have a separate GCash history area with filters such as:
- date range
- account
- transaction type
- reference number
- user who recorded it if needed

### 12.5 Balance Tracking
Each transaction should update the relevant GCash account balance consistently according to transaction rules.

---

## 13. Business Rules

### Account Rules
- multiple GCash accounts are supported
- only active accounts should normally be used for new transactions
- account balances must remain traceable

### Transaction Rules
- every GCash transaction should belong to one account
- every GCash transaction should have a type
- reference number should be stored
- notes are optional unless future business rules change
- OCR should assist, not auto-finalize

### Sales Integration Rules
- GCash sale payments must create GCash-related transaction records
- sales paid by GCash must appear in both sales context and GCash context

### Fee Rules
- fee mode is manual per entry
- the chosen fee handling must affect how balances and money movement are interpreted

---

## 14. Integration with Sales / POS Module

The Sales / POS module and GCash module are tightly connected.

### Relationship Rules
- when a sale uses GCash payment, this module must record the GCash side of that payment
- the selected GCash account must be stored for the transaction
- sale and GCash history should remain linkable
- refunds or reversals involving GCash should remain auditable and connected to the original sale where applicable

### Reporting Link
Sales reports and GCash reports should remain consistent with each other.

---

## 15. Integration with Money In / Money Out Module

GCash behavior must also connect to the broader financial tracking system.

### Relationship Rules
- GCash cash in and cash out should create corresponding money movement records where relevant
- transfers between register cash and GCash should remain visible in financial history
- GCash balances must remain separate from cash-on-hand balances

### Importance
This separation is necessary because the business wants both:
- overall money tracking
- separate GCash-specific wallet tracking

---

## 16. Integration with Reports Module

The GCash module should provide dedicated reporting support.

### Reporting Uses
- GCash transaction history report
- GCash cash-in report
- GCash cash-out report
- GCash sales payment report
- per-account balance history views if supported later
- fee-related reporting if useful

### Filter Direction
Reports should support filters such as:
- date range
- account
- transaction type
- reference number
- user if needed

---

## 17. User Access and Permissions

### Admin
Admin should be able to:
- create and manage GCash accounts
- record GCash transactions
- review balances and histories
- use OCR-assisted GCash recording
- view GCash reports

### Cashier
Cashier should be able to:
- record GCash sale-related entries as allowed
- use GCash payment selection during sales
- use OCR-assisted GCash entry where business rules allow
- access GCash-related screens only if included in cashier permissions

The exact final permission matrix can be refined later in the Auth and Access module.

---

## 18. UI Requirements

### GCash Account List Screen
Suggested UI elements:
- account list/table
- balance column
- status column
- account identifier column
- create/edit actions
- account detail action

### GCash Transaction Entry Screen
Suggested fields:
- account selector
- transaction type selector
- amount
- fee amount if applicable
- fee handling mode
- reference number
- optional note
- OCR upload/capture area
- extracted field preview if OCR is used

### GCash Transaction History Screen
Suggested UI elements:
- filter controls
- transaction list/table
- type badges
- amount display
- fee display
- reference number
- account reference
- timestamp

### UX Priorities
- minimize confusion around fee handling
- make account selection obvious
- keep OCR-assisted entry simple and editable
- remain responsive on tablet and desktop

---

## 19. Validation Rules

### Account Validation
- account name must not be empty
- account identifier/number must not be empty
- inactive accounts should not be used for new operational entries unless explicitly allowed later

### Transaction Validation
- account selection is required
- transaction type is required
- amount must be valid and positive
- reference number should be stored
- fee mode selection should be explicit when fee exists
- OCR-derived values must still pass normal validation rules

### Balance Safety Direction
The implementation should prevent obviously invalid balance updates unless future business rules explicitly allow negative wallet balances.

---

## 20. Data Design Direction

### GCash Account Entity
Suggested fields:
- id
- name
- account_identifier
- current_balance
- status
- created_at
- updated_at
- created_by if needed
- updated_by if needed

### GCash Transaction Entity
Suggested fields:
- id
- gcash_account_id
- transaction_type
- amount
- fee_amount nullable
- fee_mode nullable
- reference_number
- note nullable
- related_sale_id nullable
- related_cashflow_entry_id nullable
- created_by
- created_at
- updated_at if needed

### Possible Fee Mode Values
Possible values may include:
- DEDUCTED
- INCLUDED
- TO_REGISTER

Exact enum naming can be finalized later.

---

## 21. API Direction

### Possible Endpoint Groups
- gcash/accounts
- gcash/transactions
- gcash/ocr

### Example Endpoint Direction
- create GCash account
- get GCash accounts
- update GCash account
- get account details
- create GCash transaction
- get GCash transaction history
- OCR extract GCash transaction details

Exact endpoint naming can be finalized later in the API-specific canvas.

---

## 22. Logging and Audit Requirements

The following must be traceable:
- GCash account creation
- GCash account updates
- GCash transaction creation
- fee handling choice per transaction
- linked sale references where applicable
- user who recorded the transaction
- timestamps for all GCash actions

This is critical because GCash records affect:
- wallet balances
- financial reports
- sales consistency
- audit trust

---

## 23. Risks and Considerations

### Risk: Incorrect Fee Interpretation
If fee handling is misunderstood, GCash balances and financial records may become inaccurate.

Mitigation:
- make fee mode explicit per entry
- show clear field labels
- keep fee amount and fee treatment separately stored

### Risk: Wrong OCR Extraction
OCR may misread reference numbers, amounts, or account clues.

Mitigation:
- use editable prefills only
- require user confirmation
- preserve manual entry fallback

### Risk: Confusion Between Cash and GCash Histories
If GCash is mixed too heavily with other records, operational review becomes harder.

Mitigation:
- keep separate GCash history screens/reports
- still link GCash to wider money flow where needed

---

## 24. Version 1 Success Criteria for This Module

This module is successful in version 1 if it can:
- support multiple GCash accounts
- track current balance per account
- record GCash sales payments
- record GCash cash in and cash out transactions
- store reference numbers and fee handling details
- support OCR-assisted entry from screenshots or photos
- keep a separate GCash history and reporting view
- integrate correctly with Sales, Money Flow, and Reports

---

## 25. Suggested Future Enhancements

Possible later enhancements include:
- automated reconciliation helpers
- richer transfer workflows between accounts and register
- balance snapshots over time
- advanced fee analytics
- external platform integration if ever needed
- improved OCR extraction confidence and formatting

---

## 26. Next Related Module Documents

After this module, the most connected documents to create are:
- Money In / Money Out Module
- Expenses Module
- Offline Mode and Sync Module
- Auth and Access Module
- GCash API and Data Model Module

