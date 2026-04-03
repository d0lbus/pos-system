# SQLAlchemy Model Specification

## 1. Document Purpose

This document translates the approved data model into concrete SQLAlchemy-oriented model guidance for FastAPI + SQLAlchemy + MySQL.

It is not yet the final code, but it is intended to be specific enough to guide:
- model class creation
- relationship mapping
- enum strategy
- nullable rules
- archive/soft delete behavior
- index and uniqueness direction

---

## 2. Modeling Principles

- use explicit primary keys
- use clear foreign keys for linked records
- preserve historical references
- prefer archive/soft delete over destructive deletion where needed
- keep enum-like fields consistent across models
- keep financial and stock events auditable
- avoid overloading one table with too many unrelated responsibilities

---

## 3. Shared Base Model Direction

A reusable base mixin may provide common fields where practical.

### Common Field Direction
- `id`
- `created_at`
- `updated_at`

### Optional Mixins
- `TimestampMixin`
- `SoftDeleteMixin`
- `StatusMixin`
- `ActorMixin` where useful but not required globally

---

## 4. Enum Direction

The final implementation can use SQLAlchemy Enum or constrained strings.

### Suggested Enum Areas
- `UserRole`
- `UserStatus`
- `ProductStatus`
- `InventoryMovementType`
- `SalePaymentMethod`
- `SaleStatus`
- `SaleActionType`
- `CashflowDirection`
- `CashflowType`
- `GCashAccountStatus`
- `GCashTransactionType`
- `GCashFeeMode`
- `SyncState`

### Recommended Practical Direction
For clarity and maintainability, use enum definitions in Python and store string values consistently.

---

## 5. User Model

### Table Name
`users`

### Field Direction
- `id`: integer PK
- `full_name`: string, required
- `role`: enum/string, required
- `pin_hash`: string, required
- `status`: enum/string, required
- `created_at`: datetime
- `updated_at`: datetime

### Relationships
- `sales_created`
- `sale_actions_performed`
- `inventory_movements_performed`
- `expenses_created`
- `cashflow_entries_recorded`
- `gcash_transactions_created`
- `audit_logs_created`

### Constraints Direction
- no unique requirement on full name
- role must be valid
- inactive user should not be allowed to authenticate

---

## 6. Category Model

### Table Name
`categories`

### Field Direction
- `id`: integer PK
- `name`: string, required
- `created_at`: datetime
- `updated_at`: datetime

### Relationships
- `products`

### Constraints Direction
- category name should generally be unique for clean operations

---

## 7. Product Model

### Table Name
`products`

### Field Direction
- `id`: integer PK
- `name`: string, required
- `brand`: string, required or strongly expected by schema layer
- `category_id`: FK -> categories.id, required
- `price`: decimal/numeric, required
- `cost`: decimal/numeric, required
- `stock`: integer, required
- `low_stock_threshold`: integer, nullable or required by final rule
- `image_path`: string, nullable
- `status`: enum/string, required
- `created_by`: FK -> users.id, nullable if tracking creation actor
- `updated_by`: FK -> users.id, nullable
- `created_at`: datetime
- `updated_at`: datetime
- `archived_at`: datetime, nullable

### Relationships
- `category`
- `inventory_movements`
- `sale_items`

### Constraints Direction
- price must be non-negative
- cost must be non-negative
- stock must be whole number
- archived products must remain referenceable in old records

### Index Direction
Useful indexes may include:
- category_id
- status
- name
- brand

---

## 8. InventoryMovement Model

### Table Name
`inventory_movements`

### Field Direction
- `id`: integer PK
- `product_id`: FK -> products.id, required
- `movement_type`: enum/string, required
- `quantity`: integer, required
- `previous_stock`: integer, required
- `new_stock`: integer, required
- `note`: text/string, nullable
- `related_sale_id`: FK -> sales.id, nullable
- `related_sale_action_id`: FK -> sale_action_histories.id, nullable
- `performed_by`: FK -> users.id, required
- `created_at`: datetime

### Relationships
- `product`
- `sale`
- `sale_action_history`
- `actor`

### Constraints Direction
- quantity must be positive
- movement_type must be valid
- previous_stock/new_stock should reflect actual change semantics

### Index Direction
Useful indexes may include:
- product_id
- movement_type
- created_at
- related_sale_id

---

## 9. Sale Model

### Table Name
`sales`

### Field Direction
- `id`: integer PK
- `reference_number`: string, required
- `payment_method`: enum/string, required
- `total_amount`: decimal/numeric, required
- `status`: enum/string, required
- `created_by`: FK -> users.id, required
- `created_at`: datetime
- `updated_at`: datetime
- `synced_at`: datetime, nullable
- `sync_state`: enum/string, nullable if tracked server-side

### Relationships
- `items`
- `actions`
- `inventory_movements`
- `gcash_transactions`
- `creator`

### Constraints Direction
- reference_number should be unique
- payment_method must be valid
- total_amount must be non-negative

### Index Direction
Useful indexes may include:
- reference_number unique
- created_at
- payment_method
- status
- created_by

---

## 10. SaleItem Model

### Table Name
`sale_items`

### Field Direction
- `id`: integer PK
- `sale_id`: FK -> sales.id, required
- `product_id`: FK -> products.id, required
- `quantity`: integer, required
- `unit_price`: decimal/numeric, required
- `line_total`: decimal/numeric, required
- `created_at`: datetime

### Relationships
- `sale`
- `product`

### Constraints Direction
- quantity must be positive whole number
- unit_price must be non-negative
- line_total must match quantity × price in business logic

### Index Direction
Useful indexes may include:
- sale_id
- product_id

---

## 11. SaleActionHistory Model

### Table Name
`sale_action_histories`

### Field Direction
- `id`: integer PK
- `sale_id`: FK -> sales.id, required
- `action_type`: enum/string, required
- `performed_by`: FK -> users.id, required
- `action_note`: text/string, nullable
- `metadata_summary`: JSON/text, nullable
- `created_at`: datetime

### Relationships
- `sale`
- `actor`
- `inventory_movements`

### Constraints Direction
- action_type must be valid
- metadata_summary can store a compact change explanation

### Index Direction
Useful indexes may include:
- sale_id
- action_type
- created_at

---

## 12. Expense Model

### Table Name
`expenses`

### Field Direction
- `id`: integer PK
- `title`: string, required
- `category`: string, required
- `amount`: decimal/numeric, required
- `date`: datetime/date, required
- `note`: text/string, nullable
- `attachment_path`: string, nullable
- `recurring_enabled`: boolean, required default false
- `recurring_rule`: string/text, nullable
- `deleted_at`: datetime, nullable
- `created_by`: FK -> users.id, required
- `updated_by`: FK -> users.id, nullable
- `created_at`: datetime
- `updated_at`: datetime

### Relationships
- `creator`
- `updater`

### Constraints Direction
- amount must be positive
- deleted_at indicates soft deletion
- recurring reminder should not be mistaken for auto-posted expense logic

### Index Direction
Useful indexes may include:
- category
- date
- deleted_at
- created_by

---

## 13. CashflowEntry Model

### Table Name
`cashflow_entries`

### Field Direction
- `id`: integer PK
- `direction`: enum/string, required
- `movement_type`: enum/string, required
- `amount`: decimal/numeric, required
- `note`: text/string, nullable
- `source_module`: string, nullable
- `source_record_id`: integer, nullable
- `related_gcash_account_id`: FK -> gcash_accounts.id, nullable
- `recorded_by`: FK -> users.id, required
- `created_at`: datetime
- `updated_at`: datetime

### Relationships
- `gcash_account`
- `actor`

### Constraints Direction
- direction must be IN or OUT
- amount must be positive
- source references should be used carefully to preserve report clarity

### Index Direction
Useful indexes may include:
- direction
- movement_type
- created_at
- source_module
- source_record_id
- related_gcash_account_id

---

## 14. GCashAccount Model

### Table Name
`gcash_accounts`

### Field Direction
- `id`: integer PK
- `name`: string, required
- `account_identifier`: string, required
- `current_balance`: decimal/numeric, required
- `status`: enum/string, required
- `created_at`: datetime
- `updated_at`: datetime
- `created_by`: FK -> users.id, nullable
- `updated_by`: FK -> users.id, nullable

### Relationships
- `transactions`
- `cashflow_entries`

### Constraints Direction
- account_identifier should be unique if business treats it as unique
- current_balance should remain auditable through related transactions

### Index Direction
Useful indexes may include:
- status
- account_identifier unique if adopted

---

## 15. GCashTransaction Model

### Table Name
`gcash_transactions`

### Field Direction
- `id`: integer PK
- `gcash_account_id`: FK -> gcash_accounts.id, required
- `transaction_type`: enum/string, required
- `amount`: decimal/numeric, required
- `fee_amount`: decimal/numeric, nullable
- `fee_mode`: enum/string, nullable
- `reference_number`: string, required
- `note`: text/string, nullable
- `related_sale_id`: FK -> sales.id, nullable
- `related_cashflow_entry_id`: FK -> cashflow_entries.id, nullable
- `created_by`: FK -> users.id, required
- `created_at`: datetime
- `updated_at`: datetime

### Relationships
- `account`
- `sale`
- `cashflow_entry`
- `actor`

### Constraints Direction
- amount must be positive
- transaction_type must be valid
- reference_number should be stored and may be indexed
- fee_mode required only if fee is present or business rules require it

### Index Direction
Useful indexes may include:
- gcash_account_id
- transaction_type
- reference_number
- related_sale_id
- created_at

---

## 16. AuditLog Model

### Table Name
`audit_logs`

### Field Direction
- `id`: integer PK
- `actor_user_id`: FK -> users.id, required
- `module_name`: string, required
- `action_name`: string, required
- `target_record_type`: string, required
- `target_record_id`: integer, required
- `metadata`: JSON/text, nullable
- `created_at`: datetime

### Relationships
- `actor`

### Constraints Direction
- metadata should remain compact and useful
- audit log complements domain-specific histories, not replaces them

### Index Direction
Useful indexes may include:
- actor_user_id
- module_name
- action_name
- created_at
- target_record_type
- target_record_id

---

## 17. OfflineSyncRecord Model

### Table Name
`offline_sync_records`

### Field Direction
- `id`: integer PK
- `local_reference`: string, required
- `record_type`: string, required
- `payload_snapshot`: JSON/text, required
- `sync_state`: enum/string, required
- `error_message`: text/string, nullable
- `retry_count`: integer, required default 0
- `created_at`: datetime
- `updated_at`: datetime
- `synced_at`: datetime, nullable

### Relationships
- optional future relationship to final created records if adopted later

### Constraints Direction
- local_reference should be indexable and ideally unique for replay safety
- sync_state should remain explicit

### Index Direction
Useful indexes may include:
- local_reference unique if feasible
- record_type
- sync_state
- created_at

---

## 18. Relationship Loading Direction

### Recommended Practical Direction
- use lazy loading carefully
- prefer explicit joins/selectin loading in service/query layers for reporting-heavy routes
- avoid over-eager loading everywhere by default

### Typical Needs
- sale detail should load items and creator efficiently
- product detail may load category and recent stock context
- GCash account detail may load transactions through paginated queries
- reports should use dedicated query patterns, not naive deep relationship loading

---

## 19. Soft Delete / Archive Behavior

### Product
- use `status` and optional `archived_at`
- do not hard delete if historical references exist

### Expense
- use `deleted_at`
- preserve historical financial meaning

### User
- use `status`
- do not hard delete for operational identity safety

### GCashAccount
- use `status`
- preserve old transaction references

---

## 20. Index and Constraint Priorities

### Strong Candidates for Unique Constraints
- sale.reference_number
- offline_sync_record.local_reference
- category.name if business wants strict category uniqueness
- gcash_account.account_identifier if treated as unique

### Strong Candidates for Search/Filter Indexes
- product.name
- product.brand
- product.status
- inventory_movement.product_id
- sale.created_at
- sale.payment_method
- expense.date
- cashflow_entry.created_at
- gcash_transaction.reference_number
- audit_log.created_at

---

## 21. Model-Level Risks and Notes

### Risk: Double Counting Through Cashflow and GCash Links
Model relationships must stay explicit so reporting logic knows which records are source records and which are derived flow records.

### Risk: Archiving Breaking History
Do not hard delete reference-heavy entities like products or GCash accounts.

### Risk: Sale Status Ambiguity
Use sale action history to preserve meaning instead of overloading one sale row with every business event.

### Risk: Inventory Desynchronization
Keep movement records central to stock reasoning even if current stock is stored on Product.

---

## 22. Implementation Direction

This model spec should be followed by:
- actual SQLAlchemy class definitions
- Alembic migration planning
- schema validation classes
- service/repository implementation

Suggested next coding order:
1. users
2. categories
3. products
4. inventory_movements
5. sales and sale_items
6. sale_action_histories
7. expenses
8. cashflow_entries
9. gcash_accounts
10. gcash_transactions
11. audit_logs
12. offline_sync_records

---

## 23. Success Criteria

This model specification is successful if it:
- is concrete enough to implement SQLAlchemy classes
- preserves the approved business behavior
- supports reporting and auditability
- supports archive/soft delete behavior correctly
- supports offline sync tracking
- supports OCR-driven product and GCash workflows indirectly through the proper core entities

