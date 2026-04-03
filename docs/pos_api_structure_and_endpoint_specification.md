# API Structure and Endpoint Specification

## 1. Document Purpose

This document defines the REST API structure for the POS system. It maps the approved modules into backend endpoint groups and clarifies the direction of requests, responses, permissions, and integration behavior.

This is not yet the final code-level router file, but it is concrete enough to guide FastAPI route design.

---

## 2. API Design Principles

- use REST-style resource grouping
- keep endpoints grouped by business module
- validate input with Pydantic schemas
- enforce backend authorization on protected endpoints
- keep response structures consistent
- separate operational actions from reporting endpoints
- keep OCR endpoints isolated from ordinary CRUD endpoints
- keep sync endpoints isolated from ordinary online CRUD flows

---

## 3. Base API Prefix

Suggested base prefix:

```text
/api/v1
```

Suggested module groups:
- `/auth`
- `/users`
- `/products`
- `/categories`
- `/inventory`
- `/sales`
- `/expenses`
- `/cashflow`
- `/gcash`
- `/ocr`
- `/dashboard`
- `/reports`
- `/sync`
- `/audit`

---

## 4. Response Direction

### Success Response Direction
Responses should be predictable and consistent.

Suggested response style:
- success flag or standard HTTP success code
- message where useful
- data payload
- metadata for pagination/filter summaries where useful

### Error Response Direction
Errors should return:
- appropriate HTTP status code
- machine-readable error type/code if implemented
- human-readable message
- field validation details where relevant

---

## 5. Auth Endpoints

Base group:
```text
/api/v1/auth
```

### Endpoints
- `POST /login`
  - PIN-based login
  - input: PIN
  - output: authenticated user context + session/token data
  - access: public

- `POST /logout`
  - logout current user
  - access: authenticated

- `GET /me`
  - get current authenticated user
  - access: authenticated

### Notes
- login uses 6-digit numeric PIN
- auth structure may be session-based or token-based depending on final implementation

---

## 6. User Management Endpoints

Base group:
```text
/api/v1/users
```

### Endpoints
- `GET /`
  - list users
  - access: Admin

- `POST /`
  - create user
  - access: Admin

- `GET /{user_id}`
  - get user details
  - access: Admin

- `PATCH /{user_id}`
  - update user details
  - access: Admin

- `PATCH /{user_id}/status`
  - activate/deactivate user
  - access: Admin

- `PATCH /{user_id}/pin`
  - reset/change user PIN
  - access: Admin

### Notes
- user roles: Admin, Cashier
- inactive users should not be able to log in

---

## 7. Category Endpoints

Base group:
```text
/api/v1/categories
```

### Endpoints
- `GET /`
  - list categories
  - access: authenticated

- `POST /`
  - create category
  - access: Admin

- `GET /{category_id}`
  - get category detail
  - access: Admin

- `PATCH /{category_id}`
  - update category
  - access: Admin

---

## 8. Product Endpoints

Base group:
```text
/api/v1/products
```

### Endpoints
- `GET /`
  - list products
  - filters: search, category, status, low-stock
  - access: authenticated

- `POST /`
  - create product
  - access: Admin

- `GET /{product_id}`
  - get product detail
  - access: authenticated

- `PATCH /{product_id}`
  - update product
  - access: Admin

- `PATCH /{product_id}/archive`
  - archive/deactivate product
  - access: Admin

- `POST /{product_id}/image`
  - upload/update product image
  - access: Admin

### Notes
- product lookup for selling also uses this module indirectly through OCR/manual search
- no barcode/serial endpoints needed in version 1

---

## 9. Inventory Endpoints

Base group:
```text
/api/v1/inventory
```

### Endpoints
- `GET /`
  - get inventory list
  - filters: search, category, low-stock, status
  - access: Admin

- `GET /low-stock`
  - get low-stock products
  - access: Admin

- `GET /products/{product_id}/movements`
  - get movement history for a product
  - access: Admin

- `POST /stock-in`
  - create stock-in movement
  - access: Admin

- `POST /stock-out`
  - create stock-out movement
  - access: Admin

- `POST /adjustment`
  - create adjustment movement
  - access: Admin

- `POST /damaged`
  - record damaged stock
  - access: Admin

- `POST /lost`
  - record lost stock
  - access: Admin

### Notes
- stock changes should be movement-driven, not arbitrary field overwrites

---

## 10. Sales Endpoints

Base group:
```text
/api/v1/sales
```

### Endpoints
- `GET /`
  - list sales
  - filters: date range, cashier, payment method, status, sync status
  - access: Admin, Cashier with limited scope if desired

- `POST /`
  - create sale
  - access: Admin, Cashier

- `GET /{sale_id}`
  - get sale detail
  - access: Admin, Cashier with allowed scope

- `PATCH /{sale_id}`
  - edit sale
  - access: Admin, Cashier if allowed

- `POST /{sale_id}/void`
  - void sale
  - access: Admin, Cashier if allowed

- `POST /{sale_id}/refund`
  - refund sale
  - access: Admin, Cashier if allowed

- `GET /{sale_id}/actions`
  - get sale action history
  - access: Admin

### Notes
- creation should generate sale, sale items, inventory changes, financial effects, and logs
- refund route should support stock restore choice

---

## 11. Expense Endpoints

Base group:
```text
/api/v1/expenses
```

### Endpoints
- `GET /`
  - list expenses
  - filters: date range, category, deleted state
  - access: Admin

- `POST /`
  - create expense
  - access: Admin

- `GET /{expense_id}`
  - get expense detail
  - access: Admin

- `PATCH /{expense_id}`
  - update expense
  - access: Admin

- `DELETE /{expense_id}`
  - soft delete expense
  - access: Admin

- `GET /reminders`
  - get recurring expense reminders
  - access: Admin

- `POST /{expense_id}/attachment`
  - upload/update expense attachment
  - access: Admin

---

## 12. Cashflow Endpoints

Base group:
```text
/api/v1/cashflow
```

### Endpoints
- `GET /`
  - list money-in and money-out records
  - filters: date range, direction, type, source module
  - access: Admin

- `POST /in`
  - create manual money-in entry
  - access: Admin

- `POST /out`
  - create manual money-out entry
  - access: Admin

- `POST /opening-cash`
  - record opening cash
  - access: Admin

- `POST /closing-cash`
  - record closing cash
  - access: Admin

- `GET /summary`
  - get summary totals
  - access: Admin

### Notes
- sales and expenses auto-create linked entries separately through their own service flows

---

## 13. GCash Endpoints

Base group:
```text
/api/v1/gcash
```

### Account Endpoints
- `GET /accounts`
  - list GCash accounts
  - access: Admin

- `POST /accounts`
  - create GCash account
  - access: Admin

- `GET /accounts/{account_id}`
  - get GCash account detail
  - access: Admin

- `PATCH /accounts/{account_id}`
  - update GCash account
  - access: Admin

- `PATCH /accounts/{account_id}/status`
  - activate/deactivate GCash account
  - access: Admin

### Transaction Endpoints
- `GET /transactions`
  - list GCash transactions
  - filters: date range, account, type, reference number
  - access: Admin

- `POST /transactions`
  - create GCash transaction
  - access: Admin, Cashier if allowed in operational context

- `GET /transactions/{transaction_id}`
  - get transaction detail
  - access: Admin

### Notes
- sale-related GCash entries may be created automatically through Sales service logic

---

## 14. OCR Endpoints

Base group:
```text
/api/v1/ocr
```

### Endpoints
- `POST /products/match`
  - OCR product image and return ranked product suggestions
  - input: image
  - output: extracted text + up to 5 product matches
  - access: Admin, Cashier

- `POST /products/extract`
  - OCR product image for creation assistance
  - input: image
  - output: suggested product name/brand text
  - access: Admin

- `POST /gcash/extract`
  - OCR GCash screenshot/photo
  - input: image
  - output: suggested reference number, amount, account clue, fee clue, date/time clue
  - access: Admin, Cashier if allowed

### Notes
- OCR should never auto-finalize critical data without user confirmation

---

## 15. Dashboard Endpoints

Base group:
```text
/api/v1/dashboard
```

### Endpoints
- `GET /summary`
  - get dashboard summary cards
  - access: Admin

- `GET /alerts`
  - get low-stock, pending sync, failed sync, and other alerts
  - access: Admin

- `GET /recent-activity`
  - get recent operational highlights
  - access: Admin

---

## 16. Report Endpoints

Base group:
```text
/api/v1/reports
```

### Sales Reports
- `GET /sales`
- `GET /sales/export`

### Inventory Reports
- `GET /inventory`
- `GET /inventory/export`

### Expense Reports
- `GET /expenses`
- `GET /expenses/export`

### Cashflow Reports
- `GET /cashflow`
- `GET /cashflow/export`

### GCash Reports
- `GET /gcash`
- `GET /gcash/export`

### Sync Reports
- `GET /sync`
- `GET /sync/export`

### Notes
- report endpoints should support relevant filters only
- export format can be finalized later

---

## 17. Sync Endpoints

Base group:
```text
/api/v1/sync
```

### Endpoints
- `POST /sales`
  - submit pending offline sales
  - access: authenticated

- `GET /status`
  - optional sync status check
  - access: authenticated

- `POST /retry`
  - optional retry hook for failed sync records if needed later
  - access: authenticated or Admin depending on design

### Notes
- version 1 mainly needs sync support for offline-created sales
- sync endpoints should be designed to minimize duplicate record creation

---

## 18. Audit Endpoints

Base group:
```text
/api/v1/audit
```

### Endpoints
- `GET /logs`
  - list audit logs
  - filters: module, action, date range, actor
  - access: Admin

- `GET /logs/{log_id}`
  - get audit log detail if needed
  - access: Admin

### Notes
- audit endpoints may remain basic in version 1 if the UI does not expose deep log browsing yet

---

## 19. Suggested Request/Response Grouping

Each module should have:
- create schema
- update schema
- list filter schema where useful
- detail response schema
- summary response schema where useful

Examples:
- `ProductCreate`
- `ProductUpdate`
- `ProductListItem`
- `ProductDetail`
- `SaleCreate`
- `SaleDetail`
- `GCashTransactionCreate`
- `DashboardSummaryResponse`

---

## 20. Authorization Direction by Endpoint Group

### Public
- auth login

### Authenticated General
- auth me
- logout
- product/category reads needed for operational use
- sales create/detail as role allows
- OCR product match for sales
- sync submit for authenticated operational user

### Admin Only
- user management
- product/category management
- inventory management
- expenses
- manual cashflow
- GCash account management
- dashboard
- reports
- audit logs

### Mixed with Business Rules
- sales edit/void/refund
- GCash transaction creation
- OCR GCash extraction

These depend on the final permission boundaries for Cashier.

---

## 21. Endpoint Dependency Flow Examples

### Create Sale
`POST /sales`
- validate sale payload
- create sale record
- create sale items
- deduct inventory
- create financial records
- create GCash transaction if payment method is GCash
- create action history
- create audit log

### Refund Sale
`POST /sales/{sale_id}/refund`
- validate refund request
- create refund action history
- restore stock optionally
- create linked financial reversal/adjustment behavior
- create audit log

### OCR Product Match
`POST /ocr/products/match`
- validate image
- run PaddleOCR
- normalize extracted text
- rank products
- return suggestions

---

## 22. API Success Criteria

The API structure is successful if it:
- cleanly covers all approved modules
- keeps routes grouped by business meaning
- supports role-based protection
- supports OCR flows cleanly
- supports offline sales sync cleanly
- is concrete enough for FastAPI route implementation

---

## 23. Recommended Next Step

After this document, the strongest next technical spec is the **SQLAlchemy Model Specification**, which will turn the ERD direction into model-by-model implementation guidance.

