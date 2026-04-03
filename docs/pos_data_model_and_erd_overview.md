# Data Model and ERD Overview

## 1. Document Purpose

This document defines the high-level data model direction of the POS system and translates the approved business modules into database entities and relationships.

It is intended to guide:
- SQLAlchemy model design
- MySQL table design
- relationship mapping
- audit/history structure
- reporting-friendly data organization
- offline sync record structure

This is an **ERD-oriented overview**, not yet the final field-by-field implementation schema.

---

## 2. Data Modeling Principles

### 2.1 Source-of-Truth Principles
- the backend database is the main long-term source of truth
- frontend offline records are temporary operational records until synchronized
- historical records should remain resolvable even when related entities are archived or soft deleted

### 2.2 Auditability Principles
- stock-changing actions must be traceable
- sale-changing actions must be traceable
- financial records must be traceable
- user attribution should be preserved where practical

### 2.3 Historical Integrity Principles
- products may be archived, but old sales and inventory records must still resolve correctly
- expenses may be soft deleted, but financial meaning should remain understandable
- sale actions such as refund and void must preserve history, not overwrite it

### 2.4 Simplicity Principles
- version 1 should avoid unnecessary over-normalization
- the design should remain clear and practical for a single-store minimart
- relationships should support reporting without becoming hard to maintain

---

## 3. Major Entity Groups

The system can be divided into these main data groups:

### 3.1 Access and Identity
- User

### 3.2 Product and Catalog
- Category
- Product

### 3.3 Inventory
- InventoryMovement

### 3.4 Sales
- Sale
- SaleItem
- SaleActionHistory

### 3.5 Expenses
- Expense

### 3.6 Financial Movement
- CashflowEntry

### 3.7 GCash
- GCashAccount
- GCashTransaction

### 3.8 Audit and System Records
- AuditLog
- OfflineSyncRecord

---

## 4. Core Entity Overview

## 4.1 User
Represents a system user who can log in and perform actions.

### Main Purpose
- authentication
- role-based access
- action attribution

### Key Fields Direction
- id
- full_name or display_name
- role
- pin_hash
- status
- created_at
- updated_at

### Main Relationships
- one user can create many sales
- one user can perform many sale actions
- one user can perform many inventory movements
- one user can create many expenses
- one user can create many cashflow entries
- one user can create many GCash transactions
- one user can create many audit logs

---

## 4.2 Category
Represents a product category used for organization and filtering.

### Main Purpose
- organize products
- support filtering
- support reporting

### Key Fields Direction
- id
- name
- created_at
- updated_at

### Main Relationships
- one category has many products

---

## 4.3 Product
Represents one sellable product variant.

### Main Purpose
- store product identity
- store pricing
- store stock
- serve as source for sales, OCR matching, and inventory

### Key Fields Direction
- id
- name
- brand
- category_id
- price
- cost
- stock
- low_stock_threshold
- image_path
- status
- created_by nullable if tracked
- updated_by nullable if tracked
- created_at
- updated_at
- archived_at nullable

### Main Relationships
- one product belongs to one category
- one product has many inventory movements
- one product has many sale items

### Important Notes
- one product record represents one variant
- no barcode or serial number fields are required in version 1
- archived products must remain valid references in old records

---

## 4.4 InventoryMovement
Represents one stock-changing event for a product.

### Main Purpose
- preserve stock movement history
- explain stock changes over time

### Key Fields Direction
- id
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

### Main Relationships
- one inventory movement belongs to one product
- one inventory movement may belong to one sale
- one inventory movement may relate to one sale action history record
- one inventory movement belongs to one user as actor

### Important Notes
Movement types should support at least:
- STOCK_IN
- STOCK_OUT
- ADJUSTMENT
- DAMAGED
- LOST
- SALE_DEDUCTION
- REFUND_RESTORE

---

## 4.5 Sale
Represents a finalized or otherwise tracked sale record.

### Main Purpose
- store transaction-level sales information
- connect items, payment method, and sales history

### Key Fields Direction
- id
- reference_number
- payment_method
- total_amount
- status
- created_by
- created_at
- updated_at
- synced_at nullable
- sync_state nullable if stored server-side

### Main Relationships
- one sale has many sale items
- one sale has many sale action history records
- one sale may have many inventory movements
- one sale may have many related cashflow entries depending on design
- one sale may have many related GCash transactions depending on design
- one sale belongs to one user as creator

### Important Notes
Sale status can remain simple in version 1, but the design must still support:
- normal completed sale
- later refund/void/edit history through related action records

---

## 4.6 SaleItem
Represents one product line inside a sale.

### Main Purpose
- preserve which products were sold in which quantity and price

### Key Fields Direction
- id
- sale_id
- product_id
- quantity
- unit_price
- line_total
- created_at

### Main Relationships
- one sale item belongs to one sale
- one sale item belongs to one product

---

## 4.7 SaleActionHistory
Represents a post-sale or tracked action taken on a sale.

### Main Purpose
- preserve edit/void/refund history
- preserve actor and timestamps
- support traceability

### Key Fields Direction
- id
- sale_id
- action_type
- performed_by
- action_note nullable
- metadata_summary nullable
- created_at

### Main Relationships
- one sale action history record belongs to one sale
- one sale action history record belongs to one user as actor
- one sale action history record may relate to many inventory movements if stock was affected

### Supported Action Concepts
- CREATED
- EDITED
- VOIDED
- REFUNDED
- STOCK_RESTORED
- STOCK_NOT_RESTORED

---

## 4.8 Expense
Represents one store expense record.

### Main Purpose
- record outgoing business costs
- support expense reporting
- create money-out records

### Key Fields Direction
- id
- title
- category
- amount
- date
- note nullable
- attachment_path nullable
- recurring_enabled
- recurring_rule nullable
- deleted_at nullable
- created_by
- updated_by
- created_at
- updated_at

### Main Relationships
- one expense belongs to one user as creator
- one expense may link to one or more cashflow entries depending on implementation design

### Important Notes
- recurring support is reminder-only in version 1
- soft delete should preserve historical meaning

---

## 4.9 CashflowEntry
Represents one money-in or money-out event in the wider financial movement layer.

### Main Purpose
- track operational financial flow
- unify sales-driven, expense-driven, manual, and transfer-related money movement

### Key Fields Direction
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
- updated_at

### Main Relationships
- one cashflow entry may belong to one user as actor
- one cashflow entry may reference one sale
- one cashflow entry may reference one expense
- one cashflow entry may reference one GCash transaction
- one cashflow entry may reference one GCash account where relevant

### Important Notes
This table should be designed carefully to avoid double counting in reporting. The meaning of each entry must remain clear through source references and movement types.

---

## 4.10 GCashAccount
Represents one tracked business GCash wallet/account.

### Main Purpose
- track one GCash wallet’s balance and identity
- support multiple accounts

### Key Fields Direction
- id
- name
- account_identifier
- current_balance
- status
- created_at
- updated_at
- created_by nullable
- updated_by nullable

### Main Relationships
- one GCash account has many GCash transactions
- one GCash account may relate to many cashflow entries

---

## 4.11 GCashTransaction
Represents one GCash-related business event.

### Main Purpose
- record GCash sale payments
- record cash-in and cash-out
- preserve fee handling and reference numbers

### Key Fields Direction
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
- updated_at

### Main Relationships
- one GCash transaction belongs to one GCash account
- one GCash transaction may belong to one sale
- one GCash transaction may reference one cashflow entry depending on design
- one GCash transaction belongs to one user as actor

### Important Notes
Fee handling must support at least:
- DEDUCTED
- INCLUDED
- TO_REGISTER

---

## 4.12 AuditLog
Represents a generalized log of important system actions.

### Main Purpose
- preserve admin and operational traceability
- centralize important action history where broader logging is needed

### Key Fields Direction
- id
- actor_user_id
- module_name
- action_name
- target_record_type
- target_record_id
- metadata nullable
- created_at

### Main Relationships
- one audit log belongs to one user as actor

### Important Notes
Some modules also maintain their own domain history tables, such as SaleActionHistory and InventoryMovement. AuditLog should complement those, not replace them.

---

## 4.13 OfflineSyncRecord
Represents a sync-tracking record for frontend-originated offline data.

### Main Purpose
- support sync state tracking
- preserve submitted payload context where needed
- support retry and failure handling

### Key Fields Direction
- id
- local_reference
- record_type
- payload_snapshot
- sync_state
- error_message nullable
- retry_count
- created_at
- updated_at
- synced_at nullable

### Main Relationships
- may later link to final backend-created records where needed

### Important Notes
Version 1 mainly needs this concept for offline sales, but the design can remain extensible.

---

## 5. Relationship Summary

## 5.1 User Relationships
- User 1 -> many Sales
- User 1 -> many SaleActionHistories
- User 1 -> many InventoryMovements
- User 1 -> many Expenses
- User 1 -> many CashflowEntries
- User 1 -> many GCashTransactions
- User 1 -> many AuditLogs

## 5.2 Catalog Relationships
- Category 1 -> many Products
- Product 1 -> many InventoryMovements
- Product 1 -> many SaleItems

## 5.3 Sales Relationships
- Sale 1 -> many SaleItems
- Sale 1 -> many SaleActionHistories
- Sale 1 -> many InventoryMovements where sale-related
- Sale 1 -> many CashflowEntries where sale-related if chosen
- Sale 1 -> many GCashTransactions where GCash-related

## 5.4 Expense Relationships
- Expense 1 -> one or more CashflowEntries depending on implementation direction

## 5.5 Financial Relationships
- GCashAccount 1 -> many GCashTransactions
- GCashAccount 1 -> many CashflowEntries where relevant
- GCashTransaction may relate to Sale
- CashflowEntry may point to Sale, Expense, or GCashTransaction through source references

---

## 6. Relationship Diagram Direction

A simplified ERD direction can be understood like this:

```text
User
 ├──< Sale
 │      ├──< SaleItem >── Product >── Category
 │      └──< SaleActionHistory
 │
 ├──< InventoryMovement >── Product
 ├──< Expense
 ├──< CashflowEntry
 ├──< GCashTransaction >── GCashAccount
 └──< AuditLog

Product ──< InventoryMovement
Product ──< SaleItem

Sale ──< InventoryMovement
Sale ──< GCashTransaction
Sale ──< CashflowEntry (optional source-linked)

Expense ──< CashflowEntry (source-linked)
GCashAccount ──< CashflowEntry (where relevant)

OfflineSyncRecord (sync-tracking support entity)
```

This is only a conceptual diagram, not yet the final normalized schema diagram.

---

## 7. Suggested Foreign Key Direction

### Core Foreign Keys
- products.category_id -> categories.id
- inventory_movements.product_id -> products.id
- inventory_movements.performed_by -> users.id
- inventory_movements.related_sale_id -> sales.id nullable
- inventory_movements.related_sale_action_id -> sale_action_histories.id nullable

- sales.created_by -> users.id
- sale_items.sale_id -> sales.id
- sale_items.product_id -> products.id
- sale_action_histories.sale_id -> sales.id
- sale_action_histories.performed_by -> users.id

- expenses.created_by -> users.id
- expenses.updated_by -> users.id nullable

- cashflow_entries.recorded_by -> users.id
- cashflow_entries.related_gcash_account_id -> gcash_accounts.id nullable

- gcash_transactions.gcash_account_id -> gcash_accounts.id
- gcash_transactions.related_sale_id -> sales.id nullable
- gcash_transactions.created_by -> users.id
- gcash_transactions.related_cashflow_entry_id -> cashflow_entries.id nullable

- audit_logs.actor_user_id -> users.id

---

## 8. Soft Delete and Archive Direction

## 8.1 Product Archive
Products should use archive/inactive behavior instead of hard delete.

### Reason
- sales history must still resolve product references
- inventory history must still resolve product references

## 8.2 Expense Soft Delete
Expenses should use soft delete.

### Reason
- money-out meaning should remain understandable
- audit trail should remain intact

## 8.3 User Status
Users should use active/inactive status rather than hard delete for operational safety.

---

## 9. Status and Enum Direction

The final schema will likely use enum-like fields or constrained strings for clarity.

### Suggested Areas for Enums
- user.role
- user.status
- product.status
- inventory_movement.movement_type
- sale.payment_method
- sale.status if used
- sale_action_history.action_type
- cashflow_entry.direction
- cashflow_entry.movement_type
- gcash_account.status
- gcash_transaction.transaction_type
- gcash_transaction.fee_mode
- offline_sync_record.sync_state

### Important Principle
Enum usage should improve clarity, not complicate development unnecessarily.

---

## 10. Reporting Implications of the Data Model

The data model must support clean reporting without forcing fragile query logic.

### Reporting-Sensitive Design Areas
- sales totals must distinguish completed vs refunded/voided contexts
- cashflow entries must not cause double counting when combined with sale and GCash records
- low-stock reporting must rely on trusted product stock values and/or movement history
- archived products must still be reportable in historical contexts
- sync state may matter in operational reporting for offline-created sales

### Practical Principle
Where a record has financial meaning in more than one module, source references must remain explicit.

---

## 11. Offline Data Model Considerations

Frontend offline records are temporary, but the backend data model should still support sync-aware logic.

### Important Concepts
- local reference identifiers
- payload snapshot support for troubleshooting or replay where useful
- sync state values
- timestamps for creation and sync

### Version 1 Focus
Version 1 mainly needs this for offline-created sales, not full offline support for every table.

---

## 12. Image and File Data Considerations

The data model must support file references for:
- product images
- expense attachments
- OCR inputs temporarily if needed

### Practical Direction
Persistent records should store file paths or file references, not the raw binary content directly inside main business tables.

### Main Areas
- Product.image_path
- Expense.attachment_path

---

## 13. Recommended Next Schema Step

This ERD overview should be followed by a more concrete schema document that defines:
- exact SQLAlchemy model classes
- exact field types
- nullable vs non-nullable rules
- indexes
- unique constraints
- enum implementation choice
- relationship loading strategy

---

## 14. Suggested Table List for Version 1

The initial version should likely include at least these tables:
- users
- categories
- products
- inventory_movements
- sales
- sale_items
- sale_action_histories
- expenses
- cashflow_entries
- gcash_accounts
- gcash_transactions
- audit_logs
- offline_sync_records

---

## 15. Version 1 Data Model Success Criteria

The data model is successful in version 1 if it can:
- represent all confirmed business modules
- preserve historical relationships cleanly
- support sales, inventory, GCash, expenses, and money movement together
- support auditability
- support OCR-assisted workflows without requiring barcode structures
- support offline sales sync tracking
- support reporting without major ambiguity

---

## 16. Recommended Next Technical Documents

After this document, the strongest next documents to create are:
- SQLAlchemy Model Specification
- API Structure and Endpoint Specification
- Frontend Route and Screen Structure
- Audit Logs and History Structure
- Local Offline Data Strategy

