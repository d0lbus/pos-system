# Expenses Module Specification

## 1. Module Purpose

The Expenses module is responsible for recording, organizing, and maintaining the minimart’s non-sales business costs. It allows the system to track outgoing operational spending in a structured way and ensures that expense records remain connected to broader financial tracking through the Money In / Money Out module.

This module is important because expenses affect:
- business cash outflow
- operational summaries
- profitability visibility
- financial reports
- auditability of store spending

The module must support typical expense recording, editable records, soft deletion behavior, recurring expense reminders, and optional attachment/image uploads.

---

## 2. Module Goals

- record business expenses clearly
- organize expenses by category
- support typical minimart expense use cases
- allow Admin to edit and manage expense records
- support recurring expense reminders
- support optional image or attachment uploads
- automatically create corresponding money-out records
- preserve traceable expense history for operational review

---

## 3. Scope of This Module

### In Scope
- create expense
- edit expense
- view expense details
- list expenses
- categorize expenses
- soft delete expense
- upload optional attachment/image
- support recurring expense reminders
- auto-create related money-out entries
- filter and report expenses
- preserve audit history for important changes

### Out of Scope
- supplier invoice management
- accounts payable workflows
- tax accounting behavior
- purchase order linkage
- multi-store expense separation
- approval workflows in version 1

---

## 4. Core Concepts

### Expense Record
An expense record represents one business spending event or one reminder instance for spending that the store needs to track.

### Expense Category
Every expense should belong to a category to improve organization, filtering, and reporting.

### Recurring Reminder
Some expenses happen repeatedly. In version 1, recurring support should act as a reminder mechanism rather than an automatic financial entry generator.

### Money-Out Linkage
When an expense is created, it should automatically create a corresponding money-out record in the Money In / Money Out module.

---

## 5. Main Features

### 5.1 Expense List
The module should provide a list view for browsing and managing expense records.

Expected capabilities:
- view expense records
- search or filter expenses
- filter by category
- filter by date range
- access detail, edit, and delete actions
- view attachment indicator if present

### 5.2 Expense Detail View
The detail view should show the full expense context.

Suggested content:
- title or label
- category
- amount
- date
- note/description
- attachment/image if present
- recurring reminder information if applicable
- created/updated timestamps
- linked money-out reference if shown later

### 5.3 Expense Creation
Admin should be able to create an expense manually.

Creation requirements:
- typical expense fields
- category selection
- amount entry
- date entry
- optional note/description
- optional image or attachment upload
- optional recurring reminder setup

### 5.4 Expense Editing
Admin should be able to edit expense details.

Editable areas may include:
- title/label
- category
- amount
- date
- note/description
- attachment/image
- recurring reminder settings

### 5.5 Expense Deletion
Expense deletion in version 1 should use soft delete behavior.

Delete rules:
- deleted expenses should not behave like permanently erased records
- history should remain understandable
- related financial meaning must stay interpretable

### 5.6 Recurring Expense Reminder
The module should support recurring expense reminders.

Important rule:
- recurring expenses serve as reminders only in version 1
- they should not automatically create real expense entries unless the user confirms the actual expense

---

## 6. Typical Expense Fields

The exact schema can be finalized later, but the module should support typical expense information such as:
- title or label
- category
- amount
- date
- note/description
- attachment/image
- recurring reminder details if applicable
- status if needed later

### Confirmed Rules
- amount is required
- date is required
- categories are supported
- note/description can remain optional unless finalized otherwise
- attachments/images are supported

---

## 7. Suggested Expense Categories

The user did not lock a final category list, so the system should support typical minimart expense categories.

Examples may include:
- utilities
- rent
- transportation
- supplies
- maintenance
- wages or labor if used later
- miscellaneous

The final category list can remain configurable or be finalized later.

---

## 8. Expense Flow Overview

### Normal Expense Flow
1. Admin opens expense creation.
2. Admin enters expense details.
3. Admin selects category.
4. Admin enters amount and date.
5. Admin optionally adds note/description.
6. Admin optionally uploads attachment/image.
7. Admin optionally enables recurring reminder settings.
8. System saves the expense.
9. System creates a corresponding money-out record.
10. System writes audit/history information.

### Edit Expense Flow
1. Admin opens an existing expense.
2. Admin updates allowed fields.
3. System saves the changes.
4. System updates linked financial interpretation as required by finalized implementation rules.
5. System keeps edit history traceable.

### Soft Delete Flow
1. Admin deletes an expense.
2. System soft deletes the record.
3. System preserves historical context.
4. The related money-out behavior remains understandable according to finalized implementation rules.

---

## 9. Business Rules

### Expense Rules
- expenses must support categories
- amount and date are required
- attachments/images are allowed
- notes are allowed
- recurring support is reminder-only in version 1
- soft delete is preferred over hard delete

### Financial Rules
- creating an expense should create a money-out record automatically
- expense-linked money movement should remain traceable to the original expense
- financial history should remain understandable even if the expense is later edited or soft deleted

### Audit Rules
- important expense changes must remain traceable
- timestamps and user context should be preserved

---

## 10. Recurring Expense Reminder Behavior

### Purpose
Recurring reminders help the business remember regularly expected expenses without automatically creating false financial records.

### Version 1 Rule
Recurring expense support should:
- remind the user
- not auto-create a real expense entry by itself
- still require user confirmation when recording the actual expense

### Examples
This may be used for:
- rent reminders
- utility reminders
- regular supply purchase reminders

The exact reminder scheduling behavior can be finalized later in implementation.

---

## 11. Attachment and Image Support

### Purpose
Attachments or images help provide proof or supporting context for expenses.

Possible uses:
- receipt photo
- invoice image
- store supply proof
- handwritten note image if needed

### Rules
- attachment/image support is included in version 1
- attachment is optional
- accepted file handling rules should be validated in backend implementation

### Storage Direction
Version 1 may use:
- local storage first
- cloud-capable structure later

Exact file storage details can be finalized in the technical implementation document.

---

## 12. Integration with Money In / Money Out Module

The Expenses module must automatically create corresponding money-out records.

### Relationship Rules
- every real expense should generate a money-out entry
- the money-out entry should remain linkable to the source expense
- financial reports should be able to trace expense-driven outflows clearly
- edits and soft deletes should preserve understandable financial history behavior

This linkage is one of the most important parts of the module.

---

## 13. Integration with Dashboard and Reports

The Expenses module should feed expense summaries and filtered reporting.

### Dashboard Uses
The dashboard may show:
- recent expenses
- total expenses for the day/week/month
- category-based expense breakdowns if later desired

### Reporting Uses
The reporting layer should support:
- expense list report
- expense totals by date range
- expense totals by category
- recurring reminder-related views if implemented visually
- attachment-aware review where useful

### Common Filters
- date range
- category
- amount range if desired later
- user who recorded the expense if useful

---

## 14. User Access and Permissions

### Admin
Admin should be able to:
- create expenses
- edit expenses
- soft delete expenses
- upload attachments
- configure recurring reminders
- view expense history
- view expense-related reports

### Cashier
Cashier should generally not manage expense records directly unless future business rules allow a limited role.

Version 1 direction:
- keep expense management under Admin control

---

## 15. UI Requirements

### Expense List Screen
Suggested UI elements:
- search/filter controls
- category filter
- date filter
- amount display
- attachment indicator
- recurring reminder indicator
- actions for view, edit, delete

### Expense Create/Edit Screen
Suggested form fields:
- title/label
- category selector
- amount
- date
- note/description
- attachment/image upload
- recurring reminder controls

### Expense Detail Screen
Suggested content:
- full expense details
- linked attachment preview/download if supported
- timestamps
- recurring reminder details if applicable
- linked money-out context if shown later

### UX Priorities
- simple data entry
- clear distinction between real expenses and recurring reminders
- responsive layout for tablet and desktop
- easy filtering and review for Admin

---

## 16. Validation Rules

### Field Validation
- category should be selected
- amount must be valid and positive
- date must be valid
- title/label should not be empty if required by final design
- attachments must meet accepted file type and size rules

### Data Quality Rules
- expense categories should remain consistent
- recurring reminders should not be confused with actual posted expenses
- edits should not silently destroy financial traceability

---

## 17. Data Design Direction

### Core Expense Entity
Suggested fields:
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

### Possible Supporting Fields
If the final design needs more structure later, it may also support:
- expense status
- linked money flow record id
- reminder next due date
- reminder last triggered date

---

## 18. API Direction

### Possible Endpoint Groups
- expenses
- expenses/reminders
- expenses/attachments

### Example Endpoint Direction
- create expense
- get expense list
- get expense details
- update expense
- soft delete expense
- get recurring reminders

Exact endpoint naming can be finalized later in the API-specific canvas.

---

## 19. Logging and Audit Requirements

The following must be traceable:
- expense creation
- expense edits
- expense soft deletion
- attachment changes if important
- recurring reminder configuration changes
- user and timestamp for important expense actions

This is necessary because expenses affect:
- money-out records
- financial reports
- operational transparency

---

## 20. Risks and Considerations

### Risk: Confusing Reminder Records with Real Expenses
Recurring reminders could be mistaken for actual posted expenses.

Mitigation:
- clearly separate reminder logic from real expense records
- require confirmation before creating real expense entries

### Risk: Financial History Becoming Unclear After Edits or Deletes
If an expense is changed without preserving linkage, money-out history may become hard to trust.

Mitigation:
- keep source linkage explicit
- prefer soft delete
- preserve audit history

### Risk: Attachment Mismanagement
Large or invalid uploads may affect usability or storage.

Mitigation:
- validate file type and size
- keep attachment optional
- design clear file handling rules

---

## 21. Version 1 Success Criteria for This Module

This module is successful in version 1 if it can:
- let Admin create, edit, view, and soft delete expenses
- support categories and typical expense fields
- support optional attachments/images
- support recurring expense reminders as reminders only
- automatically create linked money-out records
- provide searchable and filterable expense history
- integrate cleanly with Money Flow, Dashboard, and Reports

---

## 22. Suggested Future Enhancements

Possible later enhancements include:
- richer recurring scheduling rules
- attachment previews and OCR for receipts
- approval workflows
- category management enhancements
- stronger financial reconciliation tools
- supplier-linked expense sources

---

## 23. Next Related Module Documents

After this module, the most connected documents to create are:
- Offline Mode and Sync Module
- Dashboard and Reports Module
- Auth and Access Module
- Expenses API and Data Model Module

