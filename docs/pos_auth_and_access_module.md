# Auth and Access Module Specification

## 1. Module Purpose

The Auth and Access module is responsible for controlling who can enter the POS system, how they authenticate, what they are allowed to do, and how access behaves during normal online use and offline-capable operation.

This module is especially important because the POS is designed for:
- fast minimart operations
- PIN-based login instead of traditional username/password-only flow
- two main roles: Admin and Cashier
- tablet-first use inside a store environment
- offline selling support after authentication

The module must balance speed, simplicity, operational practicality, and system safety.

---

## 2. Module Goals

- support fast PIN-based login
- support Admin and Cashier roles
- give Admin full access
- restrict Cashier to cashier-related screens and actions
- allow Admin to create and manage users
- preserve activity traceability
- support practical session behavior for offline-capable selling
- keep authorization logic understandable and maintainable

---

## 3. Scope of This Module

### In Scope
- PIN-based login
- logout
- session/auth state handling
- Admin and Cashier role support
- role-based screen and action access
- Admin-managed user creation and updates
- user activation/deactivation
- activity logging for important user actions
- offline-capable session continuity direction
- permission checks across modules

### Out of Scope
- biometric login
- OTP or SMS verification
- email-based login flow as the main method
- advanced multi-factor authentication in version 1
- complex role hierarchy beyond Admin and Cashier
- multi-store user isolation logic

---

## 4. Core Concepts

### PIN-Based Authentication
Users log in using a numeric PIN rather than a traditional complex credential flow.

### Role-Based Access
Each authenticated user belongs to a role that controls what screens and actions they can access.

### Session State
Once logged in, the system maintains a session or authenticated state that allows continued use of permitted features.

### Offline-Capable Continuity
Because the POS supports offline selling, the auth design must support practical continued operation for an already authenticated user during connectivity loss.

### Activity Traceability
Important user actions must remain attributable to the user who performed them.

---

## 5. Confirmed Authentication Rules

### Login Method
- PIN-based login
- numeric PIN only
- fixed length: **6 digits**

### Version 1 Login Constraints
- no failed-login lockout requirement in version 1
- fast operational login is prioritized

### Practical Meaning
The login experience should be simple and fast enough for store use while still preserving user identity and role context.

---

## 6. Roles

The system currently supports two roles.

### 6.1 Admin
Admin has full access to the system.

Admin should be able to:
- manage users
- access products
- access inventory
- access sales / POS
- access expenses
- access money in / money out
- access GCash accounts and transactions
- access dashboard and reports
- access logs/history where applicable
- perform sensitive post-sale actions such as edit, void, refund, and related stock decisions

### 6.2 Cashier
Cashier is limited to cashier-related screens and operational sales behavior.

Cashier should be able to:
- log in using PIN
- access the sales / POS area
- use OCR-assisted product lookup in sales
- use manual product lookup in sales
- process allowed sales
- record payment method in sales
- use allowed GCash sales-related flows where business rules allow
- interact with offline selling flows

Cashier should not have full Admin management access.

---

## 7. Access Control Direction

### Admin Access Principle
Admin has full system-wide access.

### Cashier Access Principle
Cashier should only see and use screens relevant to cashier work.

### Access Enforcement Areas
Authorization should be enforced at:
- frontend route/screen level
- frontend action visibility level
- backend endpoint level
- backend business logic level where sensitive actions are involved

### Important Rule
Frontend hiding alone is not enough. Backend authorization must also enforce role restrictions.

---

## 8. User Management

Admin must be able to manage user accounts.

### Required User Management Capabilities
- create user
- edit user
- activate/deactivate user
- assign role
- manage PIN or reset PIN if implemented in the final version 1 flow
- view user list

### User Record Direction
A user record should represent one store operator who can log in and perform actions according to role.

### Suggested User Fields
- full name or display name
- role
- PIN credential representation
- active/inactive status
- created_at
- updated_at

Additional fields can be finalized later based on the final backend data model.

---

## 9. Login Flow

### Online Login Flow
1. User opens the login screen.
2. User enters a 6-digit numeric PIN.
3. System validates the credential.
4. System loads the authenticated user context.
5. System routes the user to the allowed area based on role.

### Logout Flow
1. User chooses logout.
2. System clears authenticated session state.
3. User is returned to the login screen.

### Invalid PIN Behavior
- invalid login should show a clear error
- no lockout is required in version 1
- the system should not expose sensitive user details during failed login feedback

---

## 10. Session Behavior

### Purpose
The system must maintain authenticated user state during normal use.

### Practical Requirements
- preserve logged-in state appropriately during active use
- support role-aware routing and permissions
- support logout clearing
- maintain user identity for audit logging

### Security Direction
The exact implementation may use token-based or session-based auth depending on final technical design, but the business behavior must remain the same:
- user signs in with PIN
- user becomes authenticated
- system knows who the user is and what they can do

---

## 11. Offline Authentication and Session Direction

The system supports offline selling, so authentication behavior must remain practical when internet is interrupted.

### Confirmed Need
An already authenticated operational user should still be able to continue practical store work during internet loss, especially for offline selling.

### Version 1 Direction
The auth design should support:
- practical continuation for an already authenticated user when connectivity drops
- role-aware access during offline selling
- no silent loss of operational access in the middle of store use when the session is still valid locally

### Important Limitation
The exact rules for fresh offline login while fully disconnected were not explicitly finalized by the user.

### Safe Design Direction
Version 1 should prioritize:
- continuation of an existing authenticated session during offline state
- not depending on online revalidation for every sale action once the session is already active

The exact offline login boundary can be finalized later in the technical implementation document.

---

## 12. Permission Direction by Module

This section gives a business-level direction for access boundaries.

### Sales / POS
- Admin: full access
- Cashier: allowed

### Products
- Admin: full access
- Cashier: no product management access

### Inventory
- Admin: full access
- Cashier: generally restricted from direct inventory adjustment

### Expenses
- Admin: full access
- Cashier: restricted

### Money In / Money Out
- Admin: full access
- Cashier: direct manual entry generally restricted

### GCash Accounts and Transactions
- Admin: full access
- Cashier: limited to allowed operational flows tied to sales or approved business cases

### Dashboard and Reports
- Admin: full access
- Cashier: limited or restricted based on finalized operational design

### User Management
- Admin: full access
- Cashier: no access

### Offline Sync Visibility
- Admin: may access broader sync visibility and operational review
- Cashier: should at least see necessary sync state in the sales workflow

---

## 13. Activity Logging Requirements

The user requested activity logs for important actions.

### Important Logged Actions Should Include
- login attempts or successful login events if later chosen
- logout events if later chosen
- user creation
- user updates
- role changes
- user activation/deactivation
- sales-related sensitive actions by actor
- inventory adjustments by actor
- expense changes by actor
- GCash transaction entries by actor
- money movement entries by actor

### Main Purpose
The system should be able to answer:
- who performed the action
- what action was performed
- when it happened
- which record or module it affected

---

## 14. Main Features

### 14.1 Login Screen
The login screen should support fast PIN entry and role-aware entry into the system.

### 14.2 Authenticated User Context
The frontend should know the current user’s:
- identity
- role
- allowed access areas

### 14.3 Route and Screen Protection
Protected routes/screens must only be available to authenticated users with the correct role.

### 14.4 User Management Screen
Admin should have access to a user management area to create and manage accounts.

### 14.5 Activity Attribution
The module should expose current-user identity to other modules so actions can be attributed properly.

---

## 15. UI Requirements

### Login Screen
Suggested UI elements:
- PIN input
- numeric keypad-friendly interaction
- login button
- error feedback area
- simple branding/context for store use

### UX Priorities for Login
- fast
- simple
- touch-friendly on tablet
- minimal confusion

### User Management Screen
Suggested UI elements:
- user list
- role column
- status column
- create user button
- edit action
- activate/deactivate action
- reset/change PIN action if included in version 1 implementation

### Auth-Aware Navigation Behavior
The UI should:
- show only relevant navigation items based on role
- block access to unauthorized pages
- clearly preserve operational simplicity for Cashier

---

## 16. Validation Rules

### PIN Validation
- must be numeric
- must be exactly 6 digits
- invalid format should be rejected cleanly

### User Management Validation
- role must be valid
- user status must be valid
- PIN must follow system rules
- inactive users should not be allowed to log in

### Authorization Validation
- backend must validate authenticated identity and role for protected actions
- forbidden actions should return appropriate denial responses

---

## 17. Security Considerations

### Practical Security Focus for Version 1
- do not store PINs in unsafe plain form in the final backend design
- protect auth/session data properly
- enforce backend authorization checks
- keep operational login fast but role boundaries strict

### Version 1 Constraint
The business prioritized a fast store flow and did not require lockout handling yet.

### Important Note
Even with a simple PIN flow, the implementation should still follow safe credential handling practices in the backend.

---

## 18. Data Design Direction

### Core User Entity
Suggested fields:
- id
- full_name or display_name
- role
- pin_hash or secure credential field
- status
- created_at
- updated_at

### Possible Role Values
- ADMIN
- CASHIER

### Optional Supporting Fields
Depending on implementation:
- last_login_at
- deactivated_at
- created_by
- updated_by

The final exact schema can be refined later in the data model and API documents.

---

## 19. API Direction

### Possible Endpoint Groups
- auth
- users
- users/status
- users/pin

### Example Endpoint Direction
- login with PIN
- logout
- get current authenticated user
- get users list
- create user
- update user
- activate/deactivate user
- reset/change PIN

Exact endpoint naming can be finalized later in the API-specific canvas.

---

## 20. Integration with Other Modules

### Sales / POS Module
Auth provides the identity and role context needed to:
- allow or deny sales actions
- attribute transactions to the acting user
- preserve accountability in edit/void/refund history

### Inventory Module
Auth controls who can perform stock-changing actions and preserves the actor identity for inventory movement history.

### Expenses Module
Auth restricts expense management to authorized users and supports activity attribution.

### GCash Module
Auth controls who can manage accounts or record sensitive GCash transactions.

### Money Flow Module
Auth controls access to financial movement entry and review.

### Offline Mode and Sync Module
Auth must support practical continued operation for already authenticated users during connectivity loss.

### Dashboard and Reports Module
Auth determines who can see the dashboard and which reports are available.

---

## 21. Error and Access Denial Behavior

### Invalid Login
- show clear invalid credential feedback
- do not expose unnecessary identity details

### Unauthorized Access
- prevent page access
- hide or disable unavailable actions where appropriate
- enforce denial in backend even if frontend is bypassed

### Inactive User Handling
- inactive users should not be able to authenticate for normal operational use

---

## 22. Risks and Considerations

### Risk: PIN Simplicity Reducing Security
A fast PIN-based system is convenient but simpler than stronger auth methods.

Mitigation:
- keep role access strict
- securely store PIN credentials in backend
- keep user status management under Admin control

### Risk: Over-Permissive Cashier Access
If permissions are not enforced carefully, Cashier may gain unintended access to sensitive modules.

Mitigation:
- define role boundaries clearly
- enforce authorization at backend level
- keep navigation role-aware

### Risk: Offline Session Ambiguity
If offline auth/session rules are unclear, the store may face operational confusion.

Mitigation:
- support already authenticated session continuity
- keep offline boundaries explicit in implementation
- do not silently invalidate in-use operational sessions during connectivity loss

---

## 23. Version 1 Success Criteria for This Module

This module is successful in version 1 if it can:
- let users log in quickly using a 6-digit numeric PIN
- support Admin and Cashier roles
- give Admin full system access
- restrict Cashier to cashier-related screens and actions
- let Admin manage user accounts
- preserve user identity for activity attribution
- support practical continuation of an active session during offline-capable operation
- enforce authorization properly across protected screens and backend actions

---

## 24. Suggested Future Enhancements

Possible later enhancements include:
- stronger login security controls
- lockout or throttling rules
- optional password or second-factor support
- richer permission matrix beyond two roles
- user-specific dashboards
- deeper admin audit views for auth events

---

## 25. Next Related Module Documents

After this module, the most connected documents to create are:
- System Architecture and Technical Structure Module
- Data Model / ERD Overview
- Auth API and Session Strategy Module
- Logs and Audit Module

