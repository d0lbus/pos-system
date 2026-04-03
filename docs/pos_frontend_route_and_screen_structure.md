# Frontend Route and Screen Structure

## 1. Document Purpose

This document defines the frontend route hierarchy, page structure, and screen-level organization for the POS system.

It translates the approved business modules into concrete React + Vite frontend screens, route groups, and role-aware navigation behavior.

This is not yet a component-by-component UI design file, but it is concrete enough to guide page creation and route setup.

---

## 2. Route Design Principles

- keep routes grouped by business module
- separate public auth routes from protected app routes
- enforce role-aware route access
- keep Cashier flow focused and simple
- keep tablet-first operational screens fast to access
- make Admin navigation broad but organized
- allow sync/offline state to appear in operational screens where needed

---

## 3. Route Groups Overview

### Public Routes
- login

### Protected Core Routes
- dashboard
- products
- inventory
- sales / POS
- expenses
- money flow
- GCash
- reports
- users

### System Behavior Routes/Views
- unauthorized/not allowed view if needed
- not found page

---

## 4. Top-Level Route Direction

Suggested top-level structure:

```text
/
/login
/app
/app/dashboard
/app/products
/app/products/new
/app/products/:productId
/app/products/:productId/edit
/app/inventory
/app/inventory/:productId
/app/sales
/app/sales/:saleId
/app/expenses
/app/expenses/new
/app/expenses/:expenseId
/app/expenses/:expenseId/edit
/app/cashflow
/app/gcash/accounts
/app/gcash/accounts/new
/app/gcash/accounts/:accountId
/app/gcash/transactions
/app/reports
/app/users
/app/users/new
/app/users/:userId
/app/users/:userId/edit
/*
```

The final exact path naming can be simplified during implementation, but this is the route intent.

---

## 5. Public Route Structure

## 5.1 Login Route
Path:
```text
/login
```

### Purpose
- entry point for Admin and Cashier
- PIN-based authentication screen

### Main UI Areas
- PIN input
- numeric-friendly interaction
- login action
- error feedback

### Access Rule
- public only
- authenticated users may be redirected away automatically

---

## 6. Protected App Layout Structure

All protected operational routes should sit under an authenticated app layout.

Path base:
```text
/app
```

### App Layout Responsibilities
- role-aware navigation
- route protection
- session-aware rendering
- offline/sync status visibility where useful
- consistent header/sidebar/topbar behavior

### Possible Layout Variants
- general app layout for Admin
- simplified operational layout for Cashier
- POS-focused layout for sales screen if needed

---

## 7. Dashboard Route

Path:
```text
/app/dashboard
```

### Main Purpose
- show summary cards and operational highlights

### Expected Sections
- today’s sales
- expenses summary
- money in/out summary
- GCash summary
- low-stock alerts
- pending/failed sync visibility
- recent activity

### Access Rule
- Admin only by default
- Cashier access optional only if later desired

---

## 8. Products Routes

Base group:
```text
/app/products
```

### Routes
- `/app/products`
  - product list page
- `/app/products/new`
  - create product page
- `/app/products/:productId`
  - product detail page
- `/app/products/:productId/edit`
  - edit product page

### Product List Screen
Expected sections:
- search bar
- category filter
- status filter
- product list/table
- add product action

### Product Create/Edit Screens
Expected sections:
- product form
- optional image upload
- OCR assist for name/brand suggestion

### Access Rule
- Admin only for create/edit/archive
- read-only access for operational lookup can be controlled by business need, but not full management for Cashier

---

## 9. Inventory Routes

Base group:
```text
/app/inventory
```

### Routes
- `/app/inventory`
  - inventory list screen
- `/app/inventory/:productId`
  - product inventory detail and movement history screen

### Inventory List Screen
Expected sections:
- search/filter area
- current stock view
- low-stock indicators
- action buttons for stock movement operations

### Inventory Detail Screen
Expected sections:
- product summary
- current stock
- movement history
- stock in/out/adjustment/damaged/lost actions

### Access Rule
- Admin only

---

## 10. Sales / POS Routes

Base group:
```text
/app/sales
```

### Routes
- `/app/sales`
  - main POS screen
- `/app/sales/:saleId`
  - sale detail / review screen

### Main POS Screen
Expected sections:
- OCR/manual product lookup
- product suggestions
- cart
- totals
- payment selection
- finalize sale action
- offline/sync status indicators

### Sale Detail Screen
Expected sections:
- sale summary
- item list
- payment info
- action history
- edit/void/refund actions if allowed

### Access Rule
- Admin: yes
- Cashier: yes

---

## 11. Expenses Routes

Base group:
```text
/app/expenses
```

### Routes
- `/app/expenses`
  - expense list screen
- `/app/expenses/new`
  - create expense screen
- `/app/expenses/:expenseId`
  - expense detail screen
- `/app/expenses/:expenseId/edit`
  - edit expense screen

### Expense Screens
Expected sections:
- expense list with filters
- create/edit form
- attachment upload
- recurring reminder controls

### Access Rule
- Admin only

---

## 12. Money Flow Routes

Base group:
```text
/app/cashflow
```

### Routes
- `/app/cashflow`
  - money in/out list and summary screen

### Screen Purpose
- show money movement history
- allow manual money-in and money-out entry
- allow opening/closing cash actions

### Expected Sections
- summary cards
- filters
- movement table/list
- create entry actions
- opening/closing cash area or modal trigger

### Access Rule
- Admin only

---

## 13. GCash Routes

Base group:
```text
/app/gcash
```

### Routes
- `/app/gcash/accounts`
  - GCash accounts list
- `/app/gcash/accounts/new`
  - create account screen
- `/app/gcash/accounts/:accountId`
  - account detail screen
- `/app/gcash/transactions`
  - GCash transactions list and entry screen

### GCash Account List Screen
Expected sections:
- account list
- balance summary
- create/edit actions

### GCash Account Detail Screen
Expected sections:
- account info
- current balance
- recent transactions

### GCash Transactions Screen
Expected sections:
- filters
- transaction list
- create transaction form or modal
- OCR screenshot/photo assist

### Access Rule
- Admin full access
- Cashier only where specific operational GCash entry permissions are later allowed

---

## 14. Reports Routes

Base group:
```text
/app/reports
```

### Routes
- `/app/reports`
  - reports hub page with internal tabs/sections

### Suggested Internal Report Tabs
- sales
- inventory
- expenses
- cashflow
- GCash
- sync/operational state

### Expected Sections
- report type selector
- filter bar
- summary metrics
- results table/list
- export and print actions

### Access Rule
- Admin only by default

---

## 15. User Management Routes

Base group:
```text
/app/users
```

### Routes
- `/app/users`
  - user list screen
- `/app/users/new`
  - create user screen
- `/app/users/:userId`
  - user detail screen
- `/app/users/:userId/edit`
  - edit user screen

### Expected Sections
- user list
- role/status display
- create/edit form
- activate/deactivate actions
- PIN reset/change action area

### Access Rule
- Admin only

---

## 16. Utility Routes

### Unauthorized Route
Optional path:
```text
/app/unauthorized
```

Purpose:
- show access denied view for route-level failures

### Not Found Route
Path:
```text
*
```

Purpose:
- show not found page

---

## 17. Role-Based Navigation Direction

## 17.1 Admin Navigation
Admin navigation can include:
- Dashboard
- Products
- Inventory
- Sales
- Expenses
- Money Flow
- GCash
- Reports
- Users

## 17.2 Cashier Navigation
Cashier navigation should stay minimal and sales-focused.

Suggested Cashier navigation:
- Sales
- possibly limited sale history/details if allowed
- logout

Optional visibility later if needed:
- limited operational GCash screen

Cashier should not see Admin management routes in navigation.

---

## 18. Route Protection Strategy

### ProtectedRoute
Use a base protected route wrapper to ensure:
- authenticated session exists
- session is still valid locally

### RoleRoute
Use role-specific wrappers to ensure:
- only Admin can access Admin-only pages
- Cashier is restricted to allowed pages

### Important Rule
Frontend route protection is only a UX and navigation layer. Backend authorization must still enforce the real restriction.

---

## 19. Screen State Requirements

Several screens must visibly support state changes.

### Common States
- loading
- empty result
- validation error
- save success
- save failure
- offline mode active
- pending sync
- failed sync

### Critical Screens
The Sales screen especially must show:
- offline state
- OCR loading/result state
- sync state for pending sales

---

## 20. Offline UI Considerations

### Sales Screen
Must continue to work offline using cached data.

### Product Lookup
If OCR is unavailable offline, the UI should:
- show a clear message
- allow manual product search fallback immediately

### Sync Visibility
Screens that show sales or operational history should be able to display sync status where relevant.

---

## 21. Route-to-Module Mapping

- Login -> Auth and Access
- Dashboard -> Dashboard and Reports
- Products -> Products
- Inventory -> Inventory
- Sales -> Sales / POS + OCR + Sync awareness
- Expenses -> Expenses
- Cashflow -> Money In / Money Out
- GCash -> GCash Accounts and Transactions
- Reports -> Dashboard and Reports
- Users -> Auth and Access

---

## 22. Suggested Frontend Build Order

A practical frontend build order would be:
1. login route
2. protected layout and route guards
3. sales / POS screen
4. products list and form screens
5. inventory list and detail screens
6. dashboard
7. expenses
8. GCash
9. cashflow
10. reports
11. user management

This order supports the most business-critical operational areas first.

---

## 23. Success Criteria

This route and screen structure is successful if it:
- maps clearly to the approved modules
- supports Admin and Cashier separation
- keeps the Cashier workflow fast
- provides a clear page hierarchy for implementation
- supports offline-aware sales behavior
- is concrete enough to start frontend page creation and route setup

