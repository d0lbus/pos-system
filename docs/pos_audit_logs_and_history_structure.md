# Audit Logs and History Structure

## 1. Document Purpose

This document defines how the POS system should preserve traceability across important actions, with a focus on:
- centralized audit logs
- module-specific history records
- actor attribution
- timestamps and change context
- operational review and accountability

This is not just about one generic log table. It defines how central audit logging and domain-specific history should work together.

---

## 2. Logging Principles

- important business actions must be attributable
- domain-specific history should live near the domain when necessary
- centralized audit should complement, not replace, domain history
- logs should be understandable by Admins
- logs should preserve who, what, when, and where
- logs should not be so verbose that they become useless noise

---

## 3. Two Logging Layers

## 3.1 Domain-Specific History
Some modules need their own dedicated history because the business meaning is specific.

Examples:
- sale action history
- inventory movement history

## 3.2 Central Audit Log
A broader audit log should capture important actions across modules in a standard structure.

Examples:
- user creation/update
- product archive/update
- expense deletion
- GCash transaction recording
- manual cashflow entry

### Design Principle
Use domain history where the business event is part of the module’s core data story, and use central audit logs for broader administrative traceability.

---

## 4. Core Logged Questions

The system should be able to answer:
- who performed the action?
- what action was performed?
- when did it happen?
- which record or module was affected?
- what changed or what was the context?

---

## 5. Central Audit Log Scope

The central audit log should record important actions across major modules.

### Strong Candidates for Central Audit Logging
- user creation
- user update
- user activation/deactivation
- PIN reset/change
- product creation
- product update
- product archive/deactivate
- category creation/update
- manual inventory actions
- expense creation/update/delete
- manual money-in/out entries
- opening/closing cash entries
- GCash account creation/update/status change
- GCash transaction creation
- major sale actions if centralized duplication is desired
- sync failures/retries where useful

### Important Note
Not every row view or harmless screen visit needs to become an audit record in version 1.

---

## 6. Domain History Areas

## 6.1 Sales History
The Sales module needs dedicated history because edit/void/refund behavior is core business logic.

### Sales History Must Preserve
- sale creation
- sale edit
- sale void
- sale refund
- stock restored or not restored during refund
- actor
- timestamp
- change summary

### Recommended Structure
Use `sale_action_histories` as the primary domain history table for sale lifecycle events.

## 6.2 Inventory History
Inventory movement is itself a domain history record.

### Inventory History Must Preserve
- stock in
- stock out
- adjustment
- damaged
- lost
- sale deduction
- refund restore
- actor
- timestamp
- stock before and after

### Recommended Structure
Use `inventory_movements` as both the operational stock history and the domain log of stock-changing actions.

---

## 7. Central Audit Log Structure Direction

### Suggested Core Fields
- `id`
- `actor_user_id`
- `module_name`
- `action_name`
- `target_record_type`
- `target_record_id`
- `metadata`
- `created_at`

### Field Meaning
- `actor_user_id`: who performed the action
- `module_name`: broad module context such as SALES, PRODUCTS, USERS
- `action_name`: operation such as CREATE, UPDATE, ARCHIVE, RESET_PIN
- `target_record_type`: entity type affected
- `target_record_id`: exact record affected
- `metadata`: compact contextual summary

---

## 8. Metadata Direction

Metadata should remain useful but not bloated.

### Good Metadata Examples
- changed fields summary
- old status to new status
- relevant reference number
- note that stock was restored or not restored
- source module context

### Avoid
- storing huge raw snapshots unnecessarily in every audit record
- duplicating entire business records when a summary is enough

### Practical Approach
Use compact JSON-like metadata when the action needs extra explanation.

---

## 9. Actor Attribution Rules

Every important action should preserve the acting user.

### Required Actor Areas
- sales actions
- inventory actions
- expense actions
- user/admin actions
- cashflow actions
- GCash actions
- sync handling where triggered by a user-facing process

### Important Rule
If an action is system-triggered rather than manually performed, the log design may later support a system actor or clear metadata note.

---

## 10. Timestamp Rules

Every important log or history record should store when the action happened.

### Required Timestamp Areas
- sale creation and sale actions
- inventory movements
- expense create/edit/delete
- cashflow entries
- GCash transactions
- user management actions
- audit log records
- sync attempt outcomes where logged

### Practical Rule
Use timestamps consistently across modules so logs can be correlated during review.

---

## 11. Module-by-Module Logging Direction

## 11.1 Auth and User Management
### Log Through Central Audit
- user created
- user updated
- user activated/deactivated
- PIN reset/change

### Optional Later Auth Events
- login success
- logout
- failed login attempts

Version 1 does not need heavy auth event logging unless desired later.

## 11.2 Products
### Log Through Central Audit
- product created
- product updated
- product archived/deactivated
- product image changed if important

## 11.3 Categories
### Log Through Central Audit
- category created
- category updated

## 11.4 Inventory
### Log Through Domain History
- every inventory movement is already a history record

### Optional Central Audit Also
- major stock adjustments can also be logged centrally if desired for broader audit visibility

## 11.5 Sales
### Log Through Domain History
- sale created
- sale edited
- sale voided
- sale refunded
- restore-stock choice

### Optional Central Audit Also
- central audit may capture major sale action summaries for easier admin-wide review

## 11.6 Expenses
### Log Through Central Audit
- expense created
- expense updated
- expense soft deleted
- recurring reminder config changed if meaningful

## 11.7 Money In / Money Out
### Log Through Central Audit
- manual money-in entry created
- manual money-out entry created
- opening cash recorded
- closing cash recorded

## 11.8 GCash
### Log Through Central Audit
- account created
- account updated
- account status changed
- transaction created
- fee mode recorded as context in metadata if useful

## 11.9 Offline Sync
### Possible Logging Areas
- sync retry triggered
- sync failed
- sync succeeded for previously failed record if meaningful

Version 1 can keep sync logging focused and practical rather than over-detailed.

---

## 12. Sale Action History Structure Direction

### Table/Entity
`sale_action_histories`

### Required Fields
- sale_id
- action_type
- performed_by
- action_note nullable
- metadata_summary nullable
- created_at

### Main Use
This should be the authoritative history for the sale lifecycle.

### Good Metadata Examples
- changed total from X to Y
- refund processed
- stock restored = true/false

---

## 13. Inventory Movement as History Direction

### Table/Entity
`inventory_movements`

### Required Fields
- product_id
- movement_type
- quantity
- previous_stock
- new_stock
- note nullable
- related_sale_id nullable
- related_sale_action_id nullable
- performed_by
- created_at

### Main Use
This should be the authoritative history for stock changes.

---

## 14. Log Retrieval Direction

### Audit Log Retrieval
Admin should be able to review logs through filters such as:
- module
- action
- actor
- date range

### Domain History Retrieval
- sales history is retrieved through sale detail or sales history views
- inventory history is retrieved through inventory/product movement views

### Practical Rule
Do not force Admin to use one giant mixed log for everything. Domain histories should still be accessible from their natural module context.

---

## 15. Retention and Deletion Direction

### Audit Logs
Should generally not be deletable in ordinary workflows.

### Domain Histories
Should remain preserved as part of business record integrity.

### Practical Principle
If the system preserves a record for operational truth, its history should remain preserved too.

---

## 16. Logging Service Direction

A central `audit_service` should be used to standardize central audit log creation.

### Responsibilities
- create audit log entry
- normalize module/action names
- accept metadata payload
- keep formatting consistent

### Benefits
- avoids scattered ad hoc logging
- makes audit behavior more maintainable
- keeps module services cleaner

---

## 17. Naming Direction for Module and Action Values

### Module Name Examples
- AUTH
- USERS
- PRODUCTS
- CATEGORIES
- INVENTORY
- SALES
- EXPENSES
- CASHFLOW
- GCASH
- SYNC

### Action Name Examples
- CREATE
- UPDATE
- ARCHIVE
- ACTIVATE
- DEACTIVATE
- RESET_PIN
- STOCK_IN
- STOCK_OUT
- ADJUST
- DAMAGE
- LOST
- VOID
- REFUND
- RECORD_OPENING_CASH
- RECORD_CLOSING_CASH

### Principle
Use predictable names so filtering and review remain easy.

---

## 18. UI Implications

### Admin Audit View
If exposed in UI, the audit log screen should support:
- filters
- module/action badges
- actor info
- timestamps
- target record summary

### Module-Specific History Views
- Sales detail view should show sale action history
- Inventory detail view should show movement history
- GCash/history modules already expose their own domain records

---

## 19. Risks and Considerations

### Risk: Too Little Logging
Important actions may become impossible to trace.

Mitigation:
- log all sensitive business changes
- preserve actor and timestamp consistently

### Risk: Too Much Logging
Noise may make logs unreadable.

Mitigation:
- focus version 1 on meaningful business actions
- avoid logging every harmless UI event

### Risk: Confusing Mixed Histories
If domain history and audit logs are not clearly separated, admin review becomes harder.

Mitigation:
- keep domain histories in their modules
- use central audit for cross-module accountability

---

## 20. Success Criteria

This logging and history structure is successful if it:
- clearly separates central audit from domain history
- preserves sale lifecycle history well
- preserves stock change history well
- attributes important actions to users
- is concrete enough to implement the audit service and history tables
- supports later admin review and troubleshooting

