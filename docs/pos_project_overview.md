# Point of Sale System Project Overview

## 1. Project Summary

### Project Name
Point of Sale System for Minimart Operations

### Project Type
Cloud-based, tablet-first Point of Sale and store management system with offline selling support.

### Business Context
This system is intended for a **single-store minimart**. It is designed to support daily store operations by combining product management, inventory control, sales recording, expense tracking, cash movement tracking, GCash account handling, reporting, and OCR-assisted product recognition.

### Core Direction
The system will prioritize:
- fast cashier operations
- simple store management
- responsive tablet and desktop usability
- OCR-assisted product matching instead of barcode/serial scanning
- online cloud access with offline selling capability through caching and sync

---

## 2. Product Vision

The Point of Sale System will serve as the central operating tool of the minimart. It will allow store staff to register and manage products, process sales, maintain stock records, track expenses, monitor incoming and outgoing money, manage one or more GCash accounts, and use OCR to recognize products or transaction details from camera input or uploaded images.

The system is intended to reduce manual recordkeeping, improve transaction accuracy, support faster selling, and provide clearer visibility into store operations and finances.

---

## 3. Primary Objectives

- Build a modern POS system for a single minimart
- Support both **Admin** and **Cashier** roles
- Use **PIN-based authentication** for quick access
- Enable product registration and lookup without using barcodes or serial numbers
- Use **OCR + product matching** for product identification
- Record sales, refunds, voids, and inventory effects with history tracking
- Record expenses and reflect them in outgoing money records
- Track both **cash** and **GCash** movements separately
- Support **multiple GCash accounts**
- Allow true offline selling with later sync
- Provide dashboard summaries and exportable reports

---

## 4. Users and Roles

### Admin
Admin has full access to the system and can:
- manage users
- manage products
- manage inventory
- process sales
- access sales-related screens
- view dashboards and reports
- manage expenses
- manage cash flow records
- manage GCash accounts and transactions
- view logs and record histories
- perform voids, refunds, edits, and stock-related actions

### Cashier
Cashier is limited to cashier-related screens and can:
- log in using PIN
- access the sales interface
- process sales
- view products needed for selling
- perform allowed sales actions
- use OCR-based product recognition
- handle cash and GCash transaction recording as allowed by business rules

### Authentication Rules
- PIN-based login only
- numeric PIN only
- fixed length: **6 digits**
- no failed-login lockout in version 1

---

## 5. Business Scope

### In Scope
- single-store minimart usage
- responsive tablet and desktop experience
- user login via PIN
- admin and cashier roles
- product management
- category management
- inventory management
- low-stock alerts
- sales processing
- refund, void, and edit tracking
- expense management
- money-in and money-out tracking
- GCash account management
- GCash cash-in and cash-out tracking
- OCR-assisted product matching
- OCR-assisted GCash transaction detail capture
- dashboard summaries
- reports with filters and exports
- offline selling support
- sync after reconnecting to the internet
- image uploads where needed

### Out of Scope for Version 1
- receipt printing
- supplier management
- purchase orders
- discounts
- tax computation
- barcode scanning
- serial number handling
- multi-store support

---

## 6. Functional Module Overview

### 6.1 Authentication and Access Control
The system will support PIN-based authentication for Admin and Cashier accounts.

Key functions:
- login/logout
- user creation and management by Admin
- role-based access control
- activity logging

### 6.2 Product Management
The system will allow Admin to manage store products used in sales and inventory.

Product fields:
- name
- brand
- category
- price
- cost
- stock
- image
- status

Product rules:
- one product maps to one distinct variant
- different variants are treated as different products
- product image is optional
- category is required
- price and cost are required
- products use active/inactive or archived status instead of hard delete

### 6.3 Category Management
The system will maintain product categories for organization, filtering, and reporting.

### 6.4 Inventory Management
The inventory module will track stock movement and availability.

Supported movement types:
- stock in
- stock out
- adjustment
- damaged
- lost

Inventory rules:
- stock uses whole numbers only
- stock decreases only after sale completion
- manual stock-out is allowed
- damaged and lost are separate movement types
- low-stock threshold is set per product
- archived products remain visible in old sales and inventory records
- full inventory history is retained per product

### 6.5 Sales / POS Module
The sales module will support the normal minimart cashier flow.

Capabilities:
- create sales with multiple items
- edit item quantities before finalization
- use OCR-assisted product lookup
- use manual product search fallback
- choose payment method
- auto-generate sale reference numbers
- record completed sales
- allow edit, void, and refund actions
- keep full action history

Sales rules:
- no discounts in version 1
- no tax computation in version 1
- sales-related actions are categorized and shown in separate tabs or views
- sale edit history is retained
- void and refund are separate actions
- refund may optionally restore stock automatically
- if stock is not restored, that may represent damage or another business case
- cashier is allowed to perform sales-related actions based on configured permissions

### 6.6 Expense Management
The system will allow Admin to record and manage store expenses.

Expense behavior:
- uses typical expense fields
- supports categories
- supports edit and delete
- supports recurring expense reminders
- supports attachment/image upload
- affects money-out automatically
- soft delete preferred over permanent deletion

### 6.7 Money In / Money Out Management
The system will track financial movement outside of basic sales reporting.

Capabilities:
- track incoming and outgoing money
- support typical cash flow categories
- auto-create cash flow records from sales and expenses
- track register cash separately
- support opening and closing cash records daily
- support transfers between register and GCash accounts
- notes are optional

### 6.8 GCash Account and Transaction Management
The system will support one or more GCash accounts and maintain separate GCash transaction history.

Capabilities:
- create and manage multiple GCash accounts
- store account name, number, and running balance
- record GCash payment transactions
- record GCash cash-in and cash-out
- store reference number and transaction details
- treat GCash as both a payment method and a separate tracked balance
- support manual fee handling per transaction
- use OCR to extract details from screenshots or photos when recording GCash transactions

GCash fee handling rules:
- fee may be deducted
- fee may be included
- fee may go to the register
- transaction entry should allow manual choice based on actual case

### 6.9 OCR and Product Matching
The system will use OCR as the primary recognition method instead of barcode scanning.

OCR uses:
- product recognition during selling
- product assistance during product registration
- GCash detail recognition from screenshots or photos

OCR behavior:
- works through live camera and uploaded image
- shows up to **5 suggested matches**
- requires manual confirmation when confidence is low
- supports manual search fallback
- may assist in extracting product name and brand during creation
- OCR results themselves are not required to be stored in version 1

### 6.10 Dashboard and Reports
The system will provide summaries and reports for operations and finance.

Dashboard direction:
- show typical store summary cards
- show separate totals for cash and GCash
- show inventory alerts and operational highlights

Reports direction:
- all typical minimart reports
- filter by date, cashier, category, payment type, and other relevant dimensions
- export support enabled
- printable reports supported even without receipt printing

---

## 7. Product Identification Strategy

The system will **not** use barcodes or serial numbers in version 1.

Instead, product identification will rely on:
- OCR from live camera
- OCR from uploaded images
- manual product search fallback

Matching flow:
1. User captures a product image or uploads one.
2. OCR extracts visible text.
3. System compares extracted text against product records.
4. System returns up to 5 likely matches.
5. User confirms the correct product.
6. Confirmed product is used in the sale or registration flow.

This makes OCR a practical replacement for barcode dependency while keeping manual confirmation as a safeguard.

---

## 8. Sales and Inventory Interaction Rules

- Completed sales reduce stock automatically
- Refunds may restore stock automatically depending on chosen action
- If stock is not restored during refund, that can represent damaged or otherwise unusable returned goods
- All sales-related actions must be recorded
- Edits, voids, refunds, and sale adjustments should be auditable
- Inventory movement should remain traceable at all times

---

## 9. Offline-First Behavior

The system should support true offline selling in version 1.

Offline expectations:
- product and pricing data can be cached locally
- sales can still be recorded while offline
- once connection returns, sync should happen automatically
- offline mode is part of version 1, not a later enhancement

Conflict handling:
- exact conflict rules are not finalized yet
- the final design should include a safe and understandable sync strategy

This requirement makes offline resilience an important architectural concern for both frontend caching and backend reconciliation.

---

## 10. Technical Architecture

### Frontend Stack
- React
- Vite
- tablet-first responsive UI
- desktop responsive support

### Backend Stack
- FastAPI
- Python
- SQLAlchemy ORM
- MySQL
- PaddleOCR integrated into the same backend

### Deployment Direction
- cloud-based deployment
- FastAPI, OCR processing, and MySQL can run on the same server
- Docker is not required in version 1
- local file storage can be used first, with future cloud storage support

### Architectural Principle
The system should use a **single Python backend** to simplify OCR integration and keep business logic, product matching, transaction handling, and data access within one server-side application.

---

## 11. High-Level Component Breakdown

### Frontend Components
- login interface
- main layout
- dashboard
- product pages
- inventory pages
- sales POS screen
- expense pages
- cash flow pages
- GCash pages
- OCR capture/input interface
- reports pages
- offline sync indicators

### Backend Components
- authentication module
- user management module
- product module
- category module
- inventory module
- sales module
- expense module
- cash flow module
- GCash module
- OCR and matching module
- reports module
- logging/audit module
- sync/offline support module

---

## 12. Suggested Project Structure

```text
pos-system/
├── frontend/
│   ├── public/
│   └── src/
│       ├── api/
│       ├── assets/
│       ├── components/
│       ├── features/
│       ├── hooks/
│       ├── layouts/
│       ├── pages/
│       ├── routes/
│       ├── store/
│       ├── types/
│       ├── utils/
│       ├── App.tsx
│       └── main.tsx
│
└── backend/
    ├── app/
    │   ├── api/
    │   ├── core/
    │   ├── db/
    │   ├── models/
    │   ├── schemas/
    │   ├── services/
    │   ├── repositories/
    │   ├── modules/
    │   ├── utils/
    │   └── main.py
    ├── uploads/
    ├── tests/
    ├── requirements.txt
    └── alembic/
```

---

## 13. Suggested Frontend Feature Areas

- Auth
- Dashboard
- Products
- Categories
- Inventory
- POS / Sales
- Expenses
- Cash Flow
- GCash Accounts
- GCash Transactions
- OCR Capture and Matching
- Reports
- Offline Sync
- Logs and History

---

## 14. Suggested Backend Module Areas

- Auth
- Users
- Roles / Permissions
- Products
- Categories
- Inventory
- Sales
- Refunds / Voids / Sale History
- Expenses
- Cash Flow
- GCash Accounts
- GCash Transactions
- OCR Processing
- Product Matching
- Reports
- Audit Logs
- Offline Sync and Reconciliation

---

## 15. Data Design Direction

### Core Entities
- User
- Role
- Product
- Category
- ProductImage
- InventoryMovement
- Sale
- SaleItem
- SaleActionHistory
- Expense
- ExpenseAttachment
- CashFlowEntry
- GCashAccount
- GCashTransaction
- ReportView / Query Layer
- AuditLog
- OfflineSyncRecord

### Data Principles
- keep historical records even when items are archived
- use soft delete where practical
- store timestamps on major records
- keep financial and stock changes auditable
- separate operational data from derived summaries

---

## 16. Reporting Direction

The reporting layer should support operational and financial visibility.

Likely report groups:
- sales reports
- inventory reports
- expense reports
- cash flow reports
- GCash reports
- action/history reports

Common filters:
- date range
- cashier
- category
- payment type
- transaction type
- product

Output expectations:
- on-screen summary
- export support
- printable reports

---

## 17. Non-Functional Requirements

### Usability
- fast cashier workflow
- touch-friendly tablet interface
- desktop responsive support
- minimal friction during selling

### Reliability
- offline selling support
- later synchronization
- clear handling of sync failures or conflicts

### Maintainability
- modular backend and frontend structure
- clear separation of modules and responsibilities
- scalable enough for future feature additions

### Performance
- responsive OCR-assisted workflows
- efficient product lookup and matching
- smooth POS interaction on common store hardware

### Auditability
- important edits and actions must be traceable
- sales, inventory, cash, and GCash changes must keep history

---

## 18. Risks and Design Considerations

### OCR Reliability
OCR-based product recognition may fail when:
- product text is unclear
- image is blurry
- packaging is damaged
- products are visually similar

Mitigation:
- always provide manual search fallback
- show multiple suggested matches
- require confirmation when needed

### Offline Sync Complexity
Offline selling introduces data sync challenges.

Mitigation:
- define clear sync rules
- preserve local transaction queues
- keep server reconciliation understandable

### GCash Fee Variability
GCash transaction fees may be handled differently per real-world case.

Mitigation:
- allow manual fee mode selection per transaction
- preserve full transaction detail history

---

## 19. Version 1 Success Criteria

Version 1 will be considered successful if it can:
- let Admin and Cashier log in using PIN
- manage products, categories, and stock
- process sales smoothly on tablet and desktop
- use OCR to help identify products and transaction details
- record expenses and money flow accurately
- track separate GCash accounts and balances
- keep action histories for sensitive operations
- generate useful dashboard summaries and reports
- continue recording sales offline and sync them later

---

## 20. Next Documentation Breakdown

After this project overview, separate feature/module documents should be created for:
- Authentication and Users
- Products and Categories
- Inventory
- Sales / POS
- Expenses
- Money In / Money Out
- GCash Accounts and Transactions
- OCR and Product Matching
- Dashboard and Reports
- Offline Mode and Sync
- Audit Logs and Histories
- System Architecture and Project Structure

These documents will expand the overview into implementation-level specifications.

