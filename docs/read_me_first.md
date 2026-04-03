# Read Me First

## 1. Purpose of This Document

This is the master orientation document for any AI, developer, or technical contributor working on this POS system.

Its purpose is to explain:
- how to read the full spec set
- which specs are the source of truth for different decisions
- how to resolve conflicts between specs
- what the system is, what it is not, and how implementation decisions should be made
- what instructions an AI should follow when generating code, architecture, or technical decisions for this project

This document should be read **before** reading or using any other project document.

---

## 2. What This System Is

This project is a **single-store minimart Point of Sale system** with the following core characteristics:

- **Frontend:** React + Vite
- **Backend:** FastAPI
- **ORM:** SQLAlchemy
- **Database:** MySQL
- **OCR Engine:** PaddleOCR inside the same backend
- **Primary device target:** tablet-first, but responsive for desktop
- **Roles:** Admin and Cashier
- **Authentication:** 6-digit numeric PIN login
- **Offline support:** true offline selling with caching and sync
- **Receipt printing:** out of scope for version 1
- **Barcode/serial scanning:** out of scope for version 1
- **Product identification approach:** OCR + product matching + manual fallback
- **GCash:** manually recorded, balance-tracked, supports multiple accounts, no direct payment gateway

---

## 3. Core Product Philosophy

The system should be built around these principles:

### 3.1 Operational Simplicity
The system is for a real minimart environment. It must prioritize speed, clarity, and minimal friction over overly complex enterprise-style architecture.

### 3.2 Auditability
Important actions must remain traceable, especially those involving:
- sales
- refunds
- voids
- stock changes
- financial movement
- GCash transactions
- user/admin actions

### 3.3 Offline Resilience
The sales flow must continue during internet interruptions. Offline behavior is not optional; it is a core version 1 requirement.

### 3.4 OCR as Assisted Intelligence
OCR is used as an assistance feature, not as an uncontrolled auto-decision system. The user must still confirm important OCR-based suggestions.

### 3.5 Clear Separation of Business Meanings
The system must keep separate meanings clear, especially between:
- cash vs GCash
- sale totals vs cashflow totals
- completed vs refunded/voided sales
- active vs archived records
- synced vs pending-sync records

---

## 4. Reading Order for the Full Spec Set

Any AI or developer should read the specs in this order.

### Step 1: Master Scope and Business Context
Read first:
1. **Read Me First**
2. **POS Project Overview**

These establish the product identity, scope, stack, priorities, and out-of-scope boundaries.

### Step 2: Core Business Modules
Read next:
3. **POS Sales and POS Module**
4. **POS OCR and Product Matching Module**
5. **POS Products Module**
6. **POS Inventory Module**
7. **POS GCash Accounts and Transactions Module**
8. **POS Money In and Money Out Module**
9. **POS Expenses Module**
10. **POS Offline Mode and Sync Module**
11. **POS Dashboard and Reports Module**
12. **POS Auth and Access Module**

These define what the system must do from a business and UX perspective.

### Step 3: Technical Translation Specs
Read next:
13. **POS System Architecture and Technical Structure**
14. **POS Data Model and ERD Overview**
15. **POS API Structure and Endpoint Specification**
16. **POS SQLAlchemy Model Specification**
17. **POS Frontend Route and Screen Structure**
18. **POS Backend Module by Module Technical Breakdown**
19. **POS Local Offline Data Strategy**
20. **POS Audit Logs and History Structure**
21. **POS Reporting Query Specification**

These turn the business requirements into implementation direction.

---

## 5. Source-of-Truth Hierarchy

When multiple docs touch the same topic, follow this priority order.

### Highest Priority
1. **Read Me First**
2. **POS Project Overview**

These define the system identity and overall constraints.

### Business Behavior Priority
3. The specific **module spec** for the feature being worked on

Example:
- for sale logic, the Sales / POS module spec is the business source of truth
- for GCash logic, the GCash module spec is the business source of truth

### Technical Translation Priority
4. Technical structure docs, such as:
- System Architecture and Technical Structure
- Data Model and ERD Overview
- API Structure and Endpoint Specification
- SQLAlchemy Model Specification
- Frontend Route and Screen Structure
- Backend Module by Module Technical Breakdown
- Local Offline Data Strategy
- Audit Logs and History Structure
- Reporting Query Specification

These should implement the business rules, not contradict them.

---

## 6. Conflict Resolution Rules

If two specs seem to conflict, resolve them like this.

### Rule 1
Business behavior always takes priority over a more generic technical shortcut.

### Rule 2
Module-specific docs override broad/general docs for the same feature.

Example:
- if the Project Overview is broad but the Inventory module is more specific about stock movement, follow the Inventory module.

### Rule 3
Technical docs must adapt to business rules, not weaken them for convenience.

### Rule 4
If something is not fully finalized, do not invent a rigid rule and present it as confirmed. Mark it as an implementation decision point.

### Rule 5
When uncertain, preserve:
- historical integrity
- auditability
- offline safety
- financial clarity
- role-based access boundaries

---

## 7. Non-Negotiable Project Rules

These are fixed unless the user explicitly changes them later.

### System Scope
- one store only
- minimart context
- tablet-first responsive design
- desktop support required

### Roles and Auth
- Admin and Cashier only
- PIN-based login only
- 6-digit numeric PIN
- Admin manages users

### Product Rules
- one product record = one product variant
- different variant = different product
- no barcode/serial support in version 1
- OCR + manual fallback used instead

### Inventory Rules
- whole numbers only
- stock movement must be traceable
- low-stock thresholds supported
- archived products remain visible in historical records

### Sales Rules
- multi-item sales supported
- no discount in version 1
- no tax/VAT in version 1
- edit, void, refund supported
- refund may restore stock or not, depending on user choice
- all sensitive sales actions must be logged/history-aware

### GCash Rules
- no gateway integration
- manually recorded only
- multiple GCash accounts supported
- account balances tracked
- separate GCash history required
- reference number required
- fee handling is a manual choice per transaction
- OCR can assist GCash entry from screenshot/photo

### Money Flow Rules
- track money in and money out
- track register cash separately
- separate GCash balances from cash-on-hand
- opening and closing cash supported

### OCR Rules
- OCR works through backend using PaddleOCR
- OCR supports product matching and GCash extraction
- OCR must show suggestions first
- do not auto-finalize critical records from OCR without confirmation
- manual fallback must always exist

### Offline Rules
- true offline selling is required in version 1
- cached products/pricing required
- offline-created sales must sync later
- sync state must be visible
- never silently lose unsynced records
- OCR may be unavailable offline if backend is unreachable, and manual fallback must remain usable

### Out of Scope for Version 1
- receipt printing
- barcode scanning
- serial number handling
- supplier management
- purchase orders
- discounts
- tax/VAT logic
- multi-store support

---

## 8. How an AI Should Work on This Project

Any AI assisting with this system must follow these working rules.

### 8.1 Do Not Change the Stack
Do not switch the stack unless explicitly told.

Approved stack:
- React + Vite
- FastAPI
- SQLAlchemy
- MySQL
- PaddleOCR in same backend

### 8.2 Do Not Reintroduce Removed Features
Do not add or assume:
- barcode scanning
- serial number logic
- receipt printing
- discounts
- tax/VAT
- supplier/purchase order logic
- multi-store logic

unless the user explicitly asks for them later.

### 8.3 Respect the Current System Boundaries
If generating code, architecture, or advice, stay inside the approved version 1 rules.

### 8.4 Keep Financial Meanings Clear
Never casually mix or merge:
- GCash balances with register cash
- sales totals with cashflow totals
- refunds/voids with normal completed sales totals

### 8.5 Preserve History
Avoid destructive logic that would erase:
- sale history
- stock movement history
- financial history
- actor attribution

### 8.6 Build for Real Use, Not Just Clean Theory
Prefer practical minimart-friendly behavior over unnecessary abstraction.

### 8.7 Treat Offline as a Core Constraint
Do not design the Sales / POS system as if internet is always available.

### 8.8 Keep OCR in the Backend
Do not split OCR into a separate service unless the user later asks for that architecture.

---

## 9. How an AI Should Read Each Type of Spec

### If working on backend code
Read in this order:
1. relevant module spec
2. System Architecture and Technical Structure
3. Data Model and ERD Overview
4. API Structure and Endpoint Specification
5. SQLAlchemy Model Specification
6. Backend Module by Module Technical Breakdown
7. Audit Logs and History Structure
8. Local Offline Data Strategy if the module touches sync/offline logic

### If working on frontend code
Read in this order:
1. relevant module spec
2. Frontend Route and Screen Structure
3. API Structure and Endpoint Specification
4. Local Offline Data Strategy
5. System Architecture and Technical Structure

### If working on reports or dashboard
Read in this order:
1. Dashboard and Reports Module
2. Reporting Query Specification
3. Data Model and ERD Overview
4. relevant source module specs

### If working on OCR
Read in this order:
1. OCR and Product Matching Module
2. Sales / POS Module
3. Products Module
4. GCash Accounts and Transactions Module
5. System Architecture and Technical Structure
6. API Structure and Endpoint Specification

---

## 10. What an AI Must Avoid

Do not:
- assume missing requirements are approved
- invent extra business rules and present them as confirmed
- simplify away audit/history behavior
- build product identity around barcodes/serials
- assume OCR can auto-commit records safely
- ignore offline behavior in the sales flow
- treat Cashier like Admin
- hard delete records that should be archived or soft deleted
- produce report logic that double-counts sales, GCash, and cashflow

---

## 11. Implementation Mindset

If the AI is asked to help build the system, it should work in this mindset:

### Priority 1
Get the **core minimart flow** working.

That means:
- login
- products
- inventory
- sales
- OCR-assisted lookup
- offline sale queue
- sync back to backend

### Priority 2
Add operational finance support.

That means:
- expenses
- money in/out
- GCash accounts and transactions

### Priority 3
Add oversight and system support.

That means:
- dashboard
- reports
- audit visibility
- user management refinement

---

## 12. Implementation Readiness Status

At this point, the spec set is strong enough to support:
- project planning
- file/folder scaffolding
- backend module implementation
- frontend page/route implementation
- database modeling
- API building
- offline strategy implementation
- report logic implementation

This means the project is now in a **build-ready planning state**.

---

## 13. AI Instructions for This System

Below is a ready-to-use instruction block for any AI that will help build or extend this POS system.

## Ready-to-Use AI Prompt / Instructions

You are assisting in the development of a single-store minimart Point of Sale system. Before making decisions, treat the project documentation as the source of truth and follow it in the proper hierarchy. Read the documents in this order: Read Me First, POS Project Overview, the relevant module specification for the feature being worked on, then the supporting technical specs such as System Architecture and Technical Structure, Data Model and ERD Overview, API Structure and Endpoint Specification, SQLAlchemy Model Specification, Frontend Route and Screen Structure, Backend Module by Module Technical Breakdown, Local Offline Data Strategy, Audit Logs and History Structure, and Reporting Query Specification.

The approved stack is fixed unless explicitly changed by the user: React + Vite for the frontend, FastAPI for the backend, SQLAlchemy ORM, MySQL database, and PaddleOCR integrated inside the same backend. Do not switch frameworks, ORMs, databases, or OCR architecture unless the user explicitly asks.

The system is for one minimart only, tablet-first but responsive for desktop. Roles are Admin and Cashier only. Authentication is 6-digit numeric PIN-based login. Admin has full access. Cashier is restricted to cashier-related screens and actions. Do not introduce extra roles or permission models unless the user asks.

Version 1 does not include receipt printing, barcode scanning, serial number handling, discounts, tax/VAT, supplier management, purchase orders, or multi-store support. Do not reintroduce these features unless explicitly requested.

Product identification in version 1 is based on OCR + product matching + manual fallback, not barcodes. OCR is an assistant feature only. It may suggest product matches or GCash transaction details, but it must not blindly auto-finalize critical records without user confirmation. OCR runs in the FastAPI backend through PaddleOCR. If the app is offline and cannot reach the backend, OCR may be unavailable, and manual fallback must remain usable.

Offline selling is a core requirement. Design the system so that the sales flow can continue offline using cached product/pricing data, store unsynced sales locally, show clear sync states, and synchronize them when connectivity returns. Never silently drop unsynced records.

Preserve auditability and historical integrity. Do not hard delete entities that need historical references, such as products, users, expenses, or GCash accounts, unless explicitly designed otherwise. Sales actions like edit, void, and refund must preserve history. Inventory changes must be movement-based and traceable. Financial actions must preserve actor attribution and timestamps.

Keep cash and GCash meanings separate. Do not casually merge GCash balance tracking with register cash. Do not produce reporting logic that double-counts sales, cashflow, and GCash records. Refunded and voided sales must not be reported as normal completed sales totals unless a report explicitly defines that behavior.

When generating code, architecture, schema, endpoints, or UI behavior, stay aligned with the approved specs. If something is not explicitly finalized, do not invent a rigid rule and present it as confirmed. Instead, mark it as an implementation decision point and choose the safest path that preserves auditability, offline resilience, financial clarity, and role-based access boundaries.

When in doubt, optimize for real minimart operations: fast selling, clear UI, traceable actions, safe offline behavior, practical OCR assistance, and maintainable modular code.

---

## 14. Final Instruction

Anyone or any AI working on this project should treat this document as the entry point. If a new spec is created later, it should still align with the rules and hierarchy defined here.

