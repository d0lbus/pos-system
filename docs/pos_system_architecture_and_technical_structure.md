# System Architecture and Technical Structure

## 1. Document Purpose

This document defines the technical architecture and structural direction of the POS system. It translates the project overview and module specifications into a practical implementation blueprint using the selected stack:

- **Frontend:** React + Vite
- **Backend:** FastAPI
- **ORM:** SQLAlchemy
- **Database:** MySQL
- **OCR Engine:** PaddleOCR inside the same backend

This document focuses on:
- high-level system architecture
- frontend structure
- backend structure
- module layering
- API direction
- database direction
- file and folder organization
- offline architecture direction
- integration points between technical layers

It is intended to serve as the main technical reference before actual coding begins.

---

## 2. Architecture Summary

The POS system will use a **separated frontend and backend architecture**.

### Frontend Responsibilities
The React + Vite frontend will handle:
- UI rendering
- route handling
- user interaction
- local cache and offline-capable behavior
- camera/image input
- API communication
- local sync status display

### Backend Responsibilities
The FastAPI backend will handle:
- authentication and authorization
- business logic
- OCR processing through PaddleOCR
- product matching logic
- sales processing
- inventory updates
- expense and financial record handling
- GCash account and transaction handling
- reporting endpoints
- data persistence through MySQL and SQLAlchemy

### Database Responsibilities
MySQL will act as the system’s main persistent storage for:
- users
- products
- categories
- stock history
- sales
- expenses
- money movement
- GCash accounts and transactions
- audit records
- sync-aware records where needed

### OCR Placement
PaddleOCR will run **inside the FastAPI backend**, not as a separate OCR service.

This keeps:
- OCR processing
- product matching
- GCash extraction
- business logic coordination

inside a single Python server.

---

## 3. High-Level Architecture

```text
[ React + Vite Frontend ]
        |
        | HTTP / JSON / Multipart Uploads
        v
[ FastAPI Backend ]
   ├── Auth and Access
   ├── Products
   ├── Inventory
   ├── Sales / POS
   ├── Expenses
   ├── Money In / Money Out
   ├── GCash Accounts and Transactions
   ├── OCR and Product Matching
   ├── Dashboard and Reports
   ├── Offline Sync Endpoints
   └── Audit and Logging
        |
        v
[ SQLAlchemy ORM ]
        |
        v
[ MySQL Database ]
```

### Supporting Runtime Concerns
- local cache on frontend for offline-capable selling
- local sync queue on frontend
- backend file/image handling for uploads
- OCR processing pipeline inside backend

---

## 4. Technical Design Principles

### 4.1 Modular Architecture
Each major feature area should be treated as a separate module with its own:
- routes/endpoints
- schemas
- services
- repository/data access logic where needed
- model interactions

### 4.2 Clear Separation of Concerns
- frontend handles presentation and local offline behavior
- backend handles business rules and OCR
- database handles persistence
- modules should not mix unrelated logic carelessly

### 4.3 Backend as Business Source of Truth
Even though offline selling exists, the backend remains the primary source of truth once records are synchronized.

### 4.4 Offline-First for Sales Flow Only
Version 1 should primarily design true offline support around the sales flow and its related essential data, rather than trying to make every admin module fully offline-capable.

### 4.5 Auditability
Stock changes, sale actions, GCash entries, money movement, and important admin actions must be attributable and traceable.

---

## 5. Frontend Architecture Direction

## 5.1 Frontend Responsibilities
The frontend should:
- authenticate the user
- display role-aware navigation
- provide operational screens for Admin and Cashier
- allow OCR image capture/upload
- interact with the FastAPI API
- cache essential data for offline selling
- track sync state of local offline-created sales
- provide responsive tablet-first UI

## 5.2 Frontend State Areas
The frontend will likely need state for:
- authenticated user/session
- product list/cache
- sales cart state
- offline sync queue state
- dashboard/report filters
- GCash transaction entry state
- OCR result state

## 5.3 Frontend Routing Areas
The frontend should have route groups or pages for:
- login
- dashboard
- products
- inventory
- sales / POS
- expenses
- money flow
- GCash
- reports
- user management
- sync review if later exposed in UI

---

## 6. Suggested Frontend Project Structure

```text
frontend/
├── public/
├── src/
│   ├── api/
│   │   ├── client.ts
│   │   ├── auth.api.ts
│   │   ├── products.api.ts
│   │   ├── inventory.api.ts
│   │   ├── sales.api.ts
│   │   ├── expenses.api.ts
│   │   ├── cashflow.api.ts
│   │   ├── gcash.api.ts
│   │   ├── ocr.api.ts
│   │   ├── reports.api.ts
│   │   └── sync.api.ts
│   │
│   ├── assets/
│   │   ├── images/
│   │   └── icons/
│   │
│   ├── components/
│   │   ├── common/
│   │   ├── layout/
│   │   ├── forms/
│   │   ├── tables/
│   │   ├── modals/
│   │   ├── feedback/
│   │   └── ocr/
│   │
│   ├── features/
│   │   ├── auth/
│   │   ├── dashboard/
│   │   ├── products/
│   │   ├── inventory/
│   │   ├── sales/
│   │   ├── expenses/
│   │   ├── cashflow/
│   │   ├── gcash/
│   │   ├── reports/
│   │   ├── sync/
│   │   └── users/
│   │
│   ├── hooks/
│   │   ├── useAuth.ts
│   │   ├── useOfflineStatus.ts
│   │   ├── useSyncQueue.ts
│   │   ├── useOCR.ts
│   │   └── useDebounce.ts
│   │
│   ├── layouts/
│   │   ├── AppLayout.tsx
│   │   ├── AuthLayout.tsx
│   │   └── POSLayout.tsx
│   │
│   ├── pages/
│   │   ├── LoginPage.tsx
│   │   ├── DashboardPage.tsx
│   │   ├── ProductsPage.tsx
│   │   ├── ProductFormPage.tsx
│   │   ├── InventoryPage.tsx
│   │   ├── SalesPage.tsx
│   │   ├── ExpensesPage.tsx
│   │   ├── CashflowPage.tsx
│   │   ├── GCashAccountsPage.tsx
│   │   ├── GCashTransactionsPage.tsx
│   │   ├── ReportsPage.tsx
│   │   ├── UsersPage.tsx
│   │   └── NotFoundPage.tsx
│   │
│   ├── routes/
│   │   ├── AppRouter.tsx
│   │   ├── ProtectedRoute.tsx
│   │   └── RoleRoute.tsx
│   │
│   ├── store/
│   │   ├── auth.store.ts
│   │   ├── sales.store.ts
│   │   ├── sync.store.ts
│   │   └── app.store.ts
│   │
│   ├── types/
│   │   ├── auth.types.ts
│   │   ├── product.types.ts
│   │   ├── inventory.types.ts
│   │   ├── sales.types.ts
│   │   ├── expense.types.ts
│   │   ├── cashflow.types.ts
│   │   ├── gcash.types.ts
│   │   ├── ocr.types.ts
│   │   └── report.types.ts
│   │
│   ├── utils/
│   │   ├── formatCurrency.ts
│   │   ├── formatDate.ts
│   │   ├── syncHelpers.ts
│   │   ├── localDb.ts
│   │   └── constants.ts
│   │
│   ├── App.tsx
│   ├── main.tsx
│   └── index.css
│
├── package.json
├── tsconfig.json
└── vite.config.ts
```

---

## 7. Frontend Structural Notes

### Features Directory
The `features/` folder should group logic and UI by business module instead of mixing everything into generic folders only.

### API Layer
The `api/` folder should wrap backend calls cleanly so pages and components do not directly contain repetitive fetch logic.

### Store Layer
A lightweight state layer should be used for:
- authenticated user state
- sales cart state
- offline sync state
- global app/session state

### Local Data Layer
The frontend should include a local storage/indexed storage strategy for:
- cached products
- cached pricing
- local offline sales queue
- sync state metadata

This can be abstracted inside something like `localDb.ts`.

---

## 8. Backend Architecture Direction

## 8.1 Backend Responsibilities
The FastAPI backend should act as the business logic layer for the entire system.

It should handle:
- auth checks
- OCR processing
- data validation
- domain rules
- database persistence
- module-level service logic
- reporting queries

## 8.2 Backend Layering Principle
A practical backend module should separate:
- API/router layer
- schema/validation layer
- service/business layer
- repository/data access layer where useful
- model/entity layer

### Suggested Flow
`Request -> API Router -> Schema Validation -> Service Logic -> Repository / SQLAlchemy -> Database`

---

## 9. Suggested Backend Project Structure

```text
backend/
├── app/
│   ├── api/
│   │   ├── deps/
│   │   ├── routes/
│   │   │   ├── auth.py
│   │   │   ├── users.py
│   │   │   ├── products.py
│   │   │   ├── categories.py
│   │   │   ├── inventory.py
│   │   │   ├── sales.py
│   │   │   ├── expenses.py
│   │   │   ├── cashflow.py
│   │   │   ├── gcash.py
│   │   │   ├── ocr.py
│   │   │   ├── reports.py
│   │   │   └── sync.py
│   │   └── router.py
│   │
│   ├── core/
│   │   ├── config.py
│   │   ├── security.py
│   │   ├── constants.py
│   │   └── permissions.py
│   │
│   ├── db/
│   │   ├── base.py
│   │   ├── session.py
│   │   ├── init_db.py
│   │   └── migrations/
│   │
│   ├── models/
│   │   ├── user.py
│   │   ├── product.py
│   │   ├── category.py
│   │   ├── inventory_movement.py
│   │   ├── sale.py
│   │   ├── sale_item.py
│   │   ├── sale_action_history.py
│   │   ├── expense.py
│   │   ├── cashflow_entry.py
│   │   ├── gcash_account.py
│   │   ├── gcash_transaction.py
│   │   ├── audit_log.py
│   │   └── offline_sync_record.py
│   │
│   ├── schemas/
│   │   ├── auth.py
│   │   ├── user.py
│   │   ├── product.py
│   │   ├── category.py
│   │   ├── inventory.py
│   │   ├── sale.py
│   │   ├── expense.py
│   │   ├── cashflow.py
│   │   ├── gcash.py
│   │   ├── ocr.py
│   │   ├── report.py
│   │   └── sync.py
│   │
│   ├── services/
│   │   ├── auth_service.py
│   │   ├── user_service.py
│   │   ├── product_service.py
│   │   ├── category_service.py
│   │   ├── inventory_service.py
│   │   ├── sales_service.py
│   │   ├── expense_service.py
│   │   ├── cashflow_service.py
│   │   ├── gcash_service.py
│   │   ├── ocr_service.py
│   │   ├── product_matching_service.py
│   │   ├── report_service.py
│   │   ├── sync_service.py
│   │   └── audit_service.py
│   │
│   ├── repositories/
│   │   ├── user_repository.py
│   │   ├── product_repository.py
│   │   ├── category_repository.py
│   │   ├── inventory_repository.py
│   │   ├── sales_repository.py
│   │   ├── expense_repository.py
│   │   ├── cashflow_repository.py
│   │   ├── gcash_repository.py
│   │   ├── report_repository.py
│   │   └── sync_repository.py
│   │
│   ├── utils/
│   │   ├── datetime.py
│   │   ├── files.py
│   │   ├── currency.py
│   │   ├── ocr_helpers.py
│   │   ├── matching_helpers.py
│   │   └── response.py
│   │
│   ├── uploads/
│   │   ├── products/
│   │   └── expenses/
│   │
│   └── main.py
│
├── tests/
│   ├── unit/
│   ├── integration/
│   └── e2e/
│
├── alembic/
├── requirements.txt
├── .env
└── alembic.ini
```

---

## 10. Backend Structural Notes

### API Layer
`api/routes/` should only define endpoints and request/response handling.

### Schemas Layer
`schemas/` should define request and response models using Pydantic.

### Services Layer
`services/` should hold business logic such as:
- creating sales
- deducting stock
- recording GCash entries
- running OCR
- matching OCR text to products
- preparing reports

### Repositories Layer
`repositories/` may encapsulate repeated SQLAlchemy query logic and keep services cleaner.

### Models Layer
`models/` should represent SQLAlchemy entities/tables.

### Core Layer
`core/` should hold cross-cutting concerns like:
- environment config
- auth helpers
- permission rules
- reusable constants

---

## 11. Suggested Module-to-Layer Mapping

### Auth and Access
- routes: `auth.py`, `users.py`
- schemas: `auth.py`, `user.py`
- services: `auth_service.py`, `user_service.py`
- models: `user.py`

### Products and Categories
- routes: `products.py`, `categories.py`
- schemas: `product.py`, `category.py`
- services: `product_service.py`, `category_service.py`
- models: `product.py`, `category.py`

### Inventory
- routes: `inventory.py`
- schemas: `inventory.py`
- services: `inventory_service.py`
- models: `inventory_movement.py`

### Sales / POS
- routes: `sales.py`
- schemas: `sale.py`
- services: `sales_service.py`
- models: `sale.py`, `sale_item.py`, `sale_action_history.py`

### Expenses
- routes: `expenses.py`
- schemas: `expense.py`
- services: `expense_service.py`
- models: `expense.py`

### Money In / Money Out
- routes: `cashflow.py`
- schemas: `cashflow.py`
- services: `cashflow_service.py`
- models: `cashflow_entry.py`

### GCash
- routes: `gcash.py`
- schemas: `gcash.py`
- services: `gcash_service.py`
- models: `gcash_account.py`, `gcash_transaction.py`

### OCR and Product Matching
- routes: `ocr.py`
- schemas: `ocr.py`
- services: `ocr_service.py`, `product_matching_service.py`

### Dashboard and Reports
- routes: `reports.py`
- schemas: `report.py`
- services: `report_service.py`

### Offline Sync
- routes: `sync.py`
- schemas: `sync.py`
- services: `sync_service.py`
- models: `offline_sync_record.py`

---

## 12. Database Architecture Direction

The database should use a relational design because the system has clear linked business records.

### Major Entity Groups
- auth/user entities
- product and category entities
- inventory entities
- sales entities
- financial entities
- GCash entities
- audit/logging entities
- sync-related entities

### Suggested Core Tables
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

### Design Principles
- prefer explicit foreign keys
- preserve historical relationships
- use soft-delete or archive patterns where needed
- keep stock and financial history auditable

---

## 13. Suggested SQLAlchemy Model Direction

The exact fields can be finalized in the ERD document, but the architecture should be designed around these model areas:

### User
- identity
- role
- secure PIN hash
- status
- timestamps

### Product
- name
- brand
- category
- price
- cost
- stock
- low_stock_threshold
- image path
- status
- timestamps

### Category
- name
- timestamps

### InventoryMovement
- product link
- movement type
- quantity
- previous stock
- new stock
- note
- actor
- timestamps

### Sale
- reference number
- payment method
- total amount
- status
- actor
- sync metadata if needed
- timestamps

### SaleItem
- sale link
- product link
- quantity
- unit price
- line total

### SaleActionHistory
- sale link
- action type
- actor
- metadata summary
- timestamps

### Expense
- title
- category
- amount
- date
- note
- attachment path
- recurring reminder flags
- soft delete support
- timestamps

### CashflowEntry
- direction
- type
- amount
- note
- related source module
- related source record id
- actor
- timestamps

### GCashAccount
- name
- account identifier
- current balance
- status
- timestamps

### GCashTransaction
- account link
- type
- amount
- fee amount
- fee mode
- reference number
- related sale link if applicable
- note
- actor
- timestamps

### AuditLog
- actor
- module
- action
- target record info
- metadata
- timestamps

### OfflineSyncRecord
- local reference
- record type
- payload snapshot
- sync state
- error message
- retry count
- timestamps

---

## 14. API Architecture Direction

The backend should follow a REST-style API structure for version 1.

### API Principles
- use resource/module-based endpoints
- keep request/response schemas explicit
- keep validation close to endpoint boundaries
- return consistent response structures
- return meaningful status codes

### Suggested Base Grouping
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
- `/reports`
- `/sync`

---

## 15. OCR Technical Architecture

PaddleOCR is embedded in the same backend.

### OCR Flow
1. Frontend captures or uploads image.
2. Frontend sends multipart request to backend.
3. Backend validates image.
4. `ocr_service.py` runs PaddleOCR.
5. OCR result is normalized.
6. Product matching or GCash extraction logic runs.
7. Structured response is returned.

### OCR Service Separation
Even though OCR is in the same backend, logic should still be separated into:
- OCR extraction service
- matching/interpretation service

This keeps OCR processing maintainable.

---

## 16. Offline Technical Architecture

The frontend is the main holder of offline behavior for version 1.

### Frontend Offline Responsibilities
- detect connectivity
- cache product/pricing data
- maintain local pending sales queue
- show sync state
- retry sync after reconnect

### Backend Offline Responsibilities
- accept sync submissions safely
- process offline-created sales idempotently where practical
- return success/failure results clearly

### Local Data Direction
The frontend should use a durable browser-side storage strategy for offline data. A local abstraction layer like `localDb.ts` should isolate that logic from the rest of the UI.

---

## 17. File Upload and Image Handling Direction

The system supports image uploads for:
- product images
- expense attachments
- OCR input images
- GCash screenshots/photos

### Backend Handling
The backend should validate:
- file type
- file size
- upload context

### Storage Direction
Version 1 may use:
- local storage on server for persistent uploaded assets
- temporary processing for OCR input files

### Upload Separation
Persistent asset uploads and temporary OCR input processing should be treated differently where practical.

---

## 18. Security Architecture Direction

### Authentication
The system should securely validate PIN-based login and keep session/auth state practical for POS use.

### Authorization
Role-based access should be enforced in:
- route protection on frontend
- backend dependency checks
- sensitive service-level logic where necessary

### Credential Handling
PIN credentials should be stored safely in hashed form in the backend.

### Input Validation
All module endpoints should validate:
- payload shape
- required fields
- enum values
- uploaded files where relevant

---

## 19. Audit and Logging Architecture

The architecture should support consistent audit attribution across modules.

### Main Logged Areas
- sales actions
- stock-affecting actions
- expense changes
- GCash transactions
- user/admin actions
- money movement entries
- sync attempts where useful

### Design Direction
Audit logging may be handled through:
- centralized audit service
- module-level calls into audit service
- standardized metadata structure

---

## 20. Report and Query Architecture

Reports should be assembled through service-level logic that understands business meaning, rather than raw query dumping only.

### Report Generation Direction
- simple summaries may come from aggregated queries
- complex business views may use service-level composition
- export endpoints may reuse report service logic

### Important Rule
Reports must avoid double counting across:
- sales records
- GCash records
- cashflow entries

---

## 21. Testing Strategy Direction

The system should be designed with testability in mind.

### Backend Testing Areas
- service logic
- permission checks
- OCR route validation behavior
- sales/inventory interactions
- sync behavior
- report logic

### Frontend Testing Areas
- route protection
- POS flow behavior
- offline queue behavior
- sync state display
- OCR flow UI behavior

### Suggested Test Layers
- unit tests for helpers and services
- integration tests for module flows
- end-to-end tests for critical business workflows

---

## 22. Environment and Configuration Direction

### Backend Environment Variables
Expected backend config areas:
- database connection string
- secret/auth config
- upload paths
- OCR-related config
- environment mode

### Frontend Environment Variables
Expected frontend config areas:
- API base URL
- app environment mode
- feature flags later if needed

---

## 23. Deployment Direction

### Current Direction
- cloud-based deployment
- backend, database, and OCR can run on the same server
- no Docker requirement for version 1

### Practical Deployment Shape
- React frontend hosted separately or served through a compatible frontend hosting approach
- FastAPI backend hosted in a Python-capable environment
- MySQL database hosted in the same or connected cloud environment

### Version 1 Simplicity Principle
Keep deployment straightforward rather than overly distributed.

---

## 24. Technical Risks and Considerations

### Risk: Tight Coupling Between Modules
If business logic is placed directly in route handlers, the codebase will become harder to maintain.

Mitigation:
- keep services clean
- keep repositories/data access separate where useful
- keep modules bounded clearly

### Risk: OCR Slowing Backend Requests
OCR can be heavier than normal CRUD logic.

Mitigation:
- isolate OCR logic in services
- validate input before processing
- keep OCR endpoints focused and separate from ordinary CRUD flows

### Risk: Offline Sync Complexity
Offline selling introduces replay and reconciliation concerns.

Mitigation:
- isolate sync logic into its own service/module
- keep local sync states explicit
- design sync endpoints intentionally

### Risk: Reporting Double Counting
Financial data comes from multiple related modules.

Mitigation:
- centralize report logic in dedicated service layer
- define report meanings clearly

---

## 25. Version 1 Technical Success Criteria

The technical structure is successful in version 1 if it can:
- support all confirmed business modules cleanly
- keep frontend and backend responsibilities separated
- keep OCR integrated in the backend without needing another service
- support offline-capable sales flow from the frontend
- keep code organized by modules and layers
- support clean API development
- keep database relationships suitable for auditability and reporting
- remain scalable enough for future expansion

---

## 26. Recommended Next Technical Documents

After this architecture document, the strongest next technical documents to create are:
- Data Model / ERD Overview
- API Structure and Endpoint Specification
- Frontend Route and Screen Structure
- Backend Module-by-Module Technical Breakdown
- Local Offline Data Strategy
- Audit Logs and History Structure

