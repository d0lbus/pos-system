# Backend Module-by-Module Technical Breakdown

## 1. Document Purpose

This document breaks the backend down into concrete module responsibilities for the FastAPI application.

It defines, per backend module:
- what routes it owns
- what schemas it should contain
- what services it should contain
- what repositories it may use
- what entities it touches
- what cross-module interactions it has

This is the bridge between the business specs and the actual backend codebase structure.

---

## 2. Backend Layering Standard

Each module should follow this structure where practical:
- route layer
- schema layer
- service layer
- repository layer if repeated query logic exists
- model usage layer through SQLAlchemy entities

### Standard Request Flow
`Router -> Schema Validation -> Service -> Repository / ORM -> Database`

### Standard Responsibilities
- routers: endpoint definitions, dependency injection, response shaping
- schemas: request/response validation
- services: business logic
- repositories: repeated query and persistence logic

---

## 3. Auth Module

### Purpose
Handle PIN login, logout, authenticated user lookup, and auth dependencies.

### Files Direction
- `api/routes/auth.py`
- `schemas/auth.py`
- `services/auth_service.py`
- `core/security.py`
- `api/deps/auth.py` or equivalent dependency file

### Main Responsibilities
- validate PIN login input
- authenticate user
- reject inactive users
- provide current-user dependency helpers
- support logout/session clearing behavior

### Main Entities Touched
- User

### Cross-Module Interaction
- all protected modules depend on auth context
- offline-capable session behavior influences frontend/backend coordination

---

## 4. Users Module

### Purpose
Handle Admin-managed user records and role/status changes.

### Files Direction
- `api/routes/users.py`
- `schemas/user.py`
- `services/user_service.py`
- `repositories/user_repository.py`

### Main Responsibilities
- create user
- update user
- activate/deactivate user
- reset/change PIN
- list and fetch users

### Main Entities Touched
- User
- AuditLog

### Cross-Module Interaction
- user role and status affect all other modules
- actor identity is used in all audited business actions

---

## 5. Categories Module

### Purpose
Provide product category CRUD used by Products and Reports.

### Files Direction
- `api/routes/categories.py`
- `schemas/category.py`
- `services/category_service.py`
- `repositories/category_repository.py`

### Main Responsibilities
- list categories
- create category
- update category
- validate category use in products

### Main Entities Touched
- Category
- AuditLog

### Cross-Module Interaction
- Products depends on valid category IDs
- Reports uses category grouping/filtering

---

## 6. Products Module

### Purpose
Manage product records and product images.

### Files Direction
- `api/routes/products.py`
- `schemas/product.py`
- `services/product_service.py`
- `repositories/product_repository.py`
- `utils/files.py` for image storage helpers where needed

### Main Responsibilities
- create product
- update product
- archive/deactivate product
- fetch product list and details
- support product image handling
- support search data used by POS/manual lookup and OCR ranking

### Main Entities Touched
- Product
- Category
- AuditLog

### Cross-Module Interaction
- Inventory uses product IDs and stock
- Sales uses product lookup and pricing
- OCR matching depends on clean product data
- Reports depends on product/category references

---

## 7. Inventory Module

### Purpose
Handle stock movement and inventory history.

### Files Direction
- `api/routes/inventory.py`
- `schemas/inventory.py`
- `services/inventory_service.py`
- `repositories/inventory_repository.py`

### Main Responsibilities
- create stock-in/out/adjustment/damaged/lost movements
- fetch inventory list and product movement history
- compute and validate stock changes
- expose low-stock queries

### Main Entities Touched
- InventoryMovement
- Product
- AuditLog

### Cross-Module Interaction
- Sales triggers sale deduction and refund restore behavior
- Reports uses low-stock and movement history
- Products stores current stock value referenced operationally

---

## 8. Sales Module

### Purpose
Handle sale creation, sale detail retrieval, edit/void/refund actions, and sales action history.

### Files Direction
- `api/routes/sales.py`
- `schemas/sale.py`
- `services/sales_service.py`
- `repositories/sales_repository.py`

### Main Responsibilities
- create sale
- create sale items
- generate reference number
- validate stock before finalization
- create sale action history
- handle edit/void/refund actions
- coordinate with inventory and financial modules

### Main Entities Touched
- Sale
- SaleItem
- SaleActionHistory
- Product
- InventoryMovement
- CashflowEntry
- GCashTransaction
- AuditLog

### Cross-Module Interaction
- Inventory for stock changes
- GCash for GCash-paid sales
- Cashflow for financial movement
- Offline Sync for sync-created sales
- Reports for reporting queries

---

## 9. Expenses Module

### Purpose
Handle expense records, recurring reminders, and expense attachments.

### Files Direction
- `api/routes/expenses.py`
- `schemas/expense.py`
- `services/expense_service.py`
- `repositories/expense_repository.py`

### Main Responsibilities
- create expense
- update expense
- soft delete expense
- list and detail expenses
- manage recurring reminder metadata
- handle attachment storage references
- auto-create linked money-out entries

### Main Entities Touched
- Expense
- CashflowEntry
- AuditLog

### Cross-Module Interaction
- Cashflow for money-out creation
- Reports for expense reporting

---

## 10. Cashflow Module

### Purpose
Handle the broader money-in and money-out ledger behavior.

### Files Direction
- `api/routes/cashflow.py`
- `schemas/cashflow.py`
- `services/cashflow_service.py`
- `repositories/cashflow_repository.py`

### Main Responsibilities
- create manual money-in/out entries
- record opening/closing cash
- fetch cashflow history and summaries
- preserve source-linked financial movement meaning

### Main Entities Touched
- CashflowEntry
- GCashAccount where related
- AuditLog

### Cross-Module Interaction
- Sales auto-creates financial entries
- Expenses auto-creates money-out entries
- GCash transactions may create linked entries
- Reports uses this heavily

---

## 11. GCash Module

### Purpose
Handle GCash accounts, balances, and transaction history.

### Files Direction
- `api/routes/gcash.py`
- `schemas/gcash.py`
- `services/gcash_service.py`
- `repositories/gcash_repository.py`

### Main Responsibilities
- create/update GCash accounts
- activate/deactivate GCash accounts
- create GCash transactions
- compute balance effects
- preserve fee mode behavior
- fetch GCash account and transaction views

### Main Entities Touched
- GCashAccount
- GCashTransaction
- CashflowEntry where linked
- Sale where sale-related
- AuditLog

### Cross-Module Interaction
- Sales for GCash payment flows
- Cashflow for linked money movement
- OCR for screenshot/photo extraction assistance
- Reports for GCash reporting

---

## 12. OCR Module

### Purpose
Handle OCR extraction from product images and GCash screenshots/photos.

### Files Direction
- `api/routes/ocr.py`
- `schemas/ocr.py`
- `services/ocr_service.py`
- `services/product_matching_service.py`
- `utils/ocr_helpers.py`
- `utils/matching_helpers.py`

### Main Responsibilities
- validate OCR image input
- run PaddleOCR
- normalize OCR output
- rank product matches
- extract GCash detail suggestions

### Main Entities Touched
- Product
- GCashAccount indirectly for matching clues if needed

### Cross-Module Interaction
- Sales for product lookup
- Products for creation assistance
- GCash for screenshot-based entry assistance

---

## 13. Reports Module

### Purpose
Provide dashboard summaries and report query logic.

### Files Direction
- `api/routes/reports.py`
- `api/routes/dashboard.py` or shared reports router sections
- `schemas/report.py`
- `services/report_service.py`
- `repositories/report_repository.py`

### Main Responsibilities
- build dashboard summary data
- generate report result sets
- apply filters safely
- support export-ready data payloads
- avoid double counting across related financial modules

### Main Entities Touched
- Sale
- SaleItem
- Product
- InventoryMovement
- Expense
- CashflowEntry
- GCashAccount
- GCashTransaction
- OfflineSyncRecord where relevant

### Cross-Module Interaction
- consumes almost all major source modules

---

## 14. Sync Module

### Purpose
Handle backend-side acceptance and processing of offline-created sales.

### Files Direction
- `api/routes/sync.py`
- `schemas/sync.py`
- `services/sync_service.py`
- `repositories/sync_repository.py`

### Main Responsibilities
- accept pending offline sales payloads
- validate replay/idempotency safety using local references if implemented
- create official backend records
- track sync outcomes
- preserve failure information where needed

### Main Entities Touched
- OfflineSyncRecord
- Sale
- SaleItem
- SaleActionHistory
- InventoryMovement
- CashflowEntry
- GCashTransaction
- AuditLog

### Cross-Module Interaction
- deeply connected to Sales, Inventory, Cashflow, and GCash

---

## 15. Audit Module

### Purpose
Provide reusable logging of important backend actions.

### Files Direction
- `services/audit_service.py`
- optional `api/routes/audit.py`
- optional `repositories/audit_repository.py`

### Main Responsibilities
- create audit log entries
- standardize metadata format
- support audit log queries if exposed

### Main Entities Touched
- AuditLog

### Cross-Module Interaction
- all major business modules should call audit service for significant actions

---

## 16. Common Dependency Areas

### Permission Helpers
A shared permission utility/dependency should handle:
- require authenticated user
- require Admin
- require allowed sales operator

### DB Session Dependency
A shared DB dependency should provide SQLAlchemy session injection.

### File Handling Helpers
A shared utility should handle:
- file path generation
- file validation support
- upload destination rules

---

## 17. Suggested Router Registration Order

A clean registration order in the main API router may be:
1. auth
2. users
3. categories
4. products
5. inventory
6. sales
7. expenses
8. cashflow
9. gcash
10. ocr
11. dashboard/reports
12. sync
13. audit

---

## 18. Backend Coding Priority Recommendation

Most practical backend implementation order:
1. core config/security/db setup
2. auth and users
3. categories and products
4. inventory
5. sales
6. expenses
7. cashflow
8. GCash
9. OCR
10. sync
11. reports
12. audit refinement

This order supports building the most critical business flow early.

---

## 19. Success Criteria

This technical breakdown is successful if it:
- tells you what files/modules to build
- shows what each backend module owns
- shows which entities each module touches
- shows the cross-module dependencies clearly
- is concrete enough to start backend implementation module by module

