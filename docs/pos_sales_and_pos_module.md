# Sales / POS Module Specification

## 1. Module Purpose

The Sales / POS module is the core operational area of the system. It is responsible for handling day-to-day selling activities inside the minimart, allowing the cashier or admin to quickly identify products, build a cart, process a transaction, record payment details, update stock, and preserve an auditable history of important actions.

This module must be optimized for **fast cashier usage**, must work well on **tablet-first responsive layouts**, and must remain functional during **offline selling scenarios**.

---

## 2. Module Goals

- Support fast in-store selling
- Allow product lookup through OCR-assisted recognition and manual search
- Handle multi-item transactions
- Support cash and GCash payments
- Record finalized sales accurately
- Deduct stock only after sale completion
- Support post-sale actions such as edit, void, and refund
- Keep a full history of sales-related actions
- Work with offline caching and later synchronization

---

## 3. User Access

### Admin
Admin can:
- access the POS screen
- create sales
- edit sales
- void sales
- refund sales
- review sales history
- access categorized sales action tabs
- view detailed sales records

### Cashier
Cashier can:
- access sales-related screens only
- create sales
- use OCR-assisted product lookup
- manually search products
- process cash or GCash transactions
- perform allowed sales-related actions based on configured permissions

---

## 4. Scope of This Module

### In Scope
- sales transaction creation
- cart handling
- quantity editing before finalization
- OCR-assisted product lookup
- manual product search fallback
- cash payment recording
- GCash payment recording
- auto-generated sale reference numbers
- completed sale history
- sale edit tracking
- void actions
- refund actions
- optional stock restoration during refund
- separate action categories/tabs for sales actions
- offline sale recording and sync preparation

### Out of Scope
- receipt printing
- discounts
- tax/VAT computation
- barcode scanning
- serial number scanning
- customer loyalty features

---

## 5. Sales Flow Overview

### Normal Sale Flow
1. User opens the Sales / POS screen.
2. User identifies a product through OCR or manual search.
3. User adds the product to the cart.
4. User adjusts quantity if needed.
5. User repeats the process for additional items.
6. User selects the payment method.
7. User reviews totals.
8. User completes the transaction.
9. System generates a sale reference number.
10. System records the sale.
11. System deducts stock.
12. System creates corresponding financial records.
13. System logs the action in sales history and audit records.

### Post-Sale Action Flow
For an existing sale, an authorized user may:
- edit the sale
- void the sale
- refund the sale

Every post-sale action must:
- be categorized properly
- preserve the original sale reference
- record who performed the action
- record when it happened
- record what changed
- remain visible in history

---

## 6. Main Features

### 6.1 POS Screen
The POS screen must be optimized for speed and clarity.

Expected characteristics:
- touch-friendly layout
- large tap/click targets
- minimal steps to add products
- clear cart summary
- quick payment selection
- visible running totals
- responsive design for tablet and desktop

### 6.2 Product Lookup
This module will not use barcode scanning.

Supported lookup methods:
- OCR using live camera
- OCR using uploaded image
- manual product search

Lookup behavior:
- OCR attempts to extract product text
- system matches OCR result to product records
- system shows up to 5 likely matches
- user selects the correct product
- if OCR confidence is low, manual confirmation is required
- manual search must always be available as fallback

### 6.3 Cart Management
The cart must support:
- adding multiple products
- increasing or decreasing quantity before completion
- removing items before completion
- showing line totals and overall total
- reviewing cart contents before checkout

### 6.4 Payment Handling
Supported payment methods in version 1:
- Cash
- GCash

Payment rules:
- one sale must store the selected payment method
- GCash payment is recorded only, not processed through a payment gateway
- GCash payments should integrate with the selected GCash account balance rules where applicable

### 6.5 Sale Finalization
When the sale is completed, the system must:
- generate a unique reference number
- save the sale master record
- save all sale items
- deduct stock for each product
- create corresponding money movement entries
- create related GCash records if payment method is GCash
- write audit and action history records

### 6.6 Sales History
The module must provide a history area where users can view completed sales and action records.

History views should include:
- all completed sales
- edited sales
- voided sales
- refunded sales
- categorized action tabs or equivalent grouped views

### 6.7 Edit Sale
Authorized users may edit a sale after completion.

Edit rules:
- edit actions must be recorded
- changes must be traceable
- original sale linkage must be preserved
- edit history must remain visible
- stock and financial implications must be handled consistently

### 6.8 Void Sale
Authorized users may void a sale.

Void rules:
- void is separate from refund
- void must be logged as its own action type
- stock effects must be handled according to finalized business logic
- financial effects must also be reversed or adjusted consistently

### 6.9 Refund Sale
Authorized users may refund a sale.

Refund rules:
- refund is separate from void
- refund must be logged as its own action type
- user may choose whether stock is automatically restored
- if stock is not restored, that may represent damaged or unusable returned goods
- financial effects must be reversed or adjusted consistently

---

## 7. Business Rules

### Sale Rules
- a sale can contain multiple items
- quantities are editable before completion
- no discounts in version 1
- no tax computation in version 1
- stock must only decrease after sale completion
- every sale must have an auto-generated reference number

### Action Rules
- edit, void, and refund are separate actions
- all actions must be recorded in history
- changes must be auditable
- sales actions should be visible in separate categorized tabs or equivalent filtered views

### Permission Rules
- Admin has full control
- Cashier can access sales-related screens only
- Cashier is allowed sales-related actions according to business configuration

### Product Lookup Rules
- OCR is the primary assisted lookup method
- manual search is always available
- user confirmation is required for OCR suggestions

---

## 8. UI Requirements

### Sales / POS Screen Sections
Suggested screen sections:
- product lookup area
- OCR trigger area
- manual search input
- suggested matches area
- cart table/list
- order summary
- payment selection area
- action buttons
- recent transaction or quick history area if space allows

### UX Priorities
- fast cashier workflow
- minimal confusion during product selection
- clear visual distinction between lookup, cart, and payment areas
- easy use on tablet
- responsive fallback for desktop

### Important UI States
The module should visibly support these states:
- loading OCR results
- OCR match suggestions shown
- no OCR match found
- offline mode active
- syncing pending sale(s)
- sync completed
- sale saved successfully
- sale failed to save

---

## 9. Data Requirements

### Core Entities Used by This Module
- Sale
- SaleItem
- Product
- InventoryMovement
- SaleActionHistory
- CashFlowEntry
- GCashTransaction
- GCashAccount
- AuditLog
- OfflineSyncRecord

### Sale Record Direction
Suggested sale-level fields:
- id
- reference_number
- payment_method
- total_amount
- subtotal_amount if separated internally
- status
- created_by
- created_at
- updated_at
- synced_at if offline support needs it
- original_sale_id if linked to later action flows

### Sale Item Direction
Suggested sale-item fields:
- id
- sale_id
- product_id
- quantity
- unit_price
- line_total
- created_at

### Sale Action History Direction
Suggested action history fields:
- id
- sale_id
- action_type
- performed_by
- action_note optional
- metadata / change summary
- created_at

Possible action types:
- CREATED
- EDITED
- VOIDED
- REFUNDED
- STOCK_RESTORED
- STOCK_NOT_RESTORED

---

## 10. Inventory Interaction

### On Sale Completion
- create stock-out movement per sold product
- deduct stock based on final sale quantities
- keep movement history traceable

### On Refund
- optional stock restore behavior
- if restore is chosen, create stock-in movement or dedicated refund-restock movement
- if restore is not chosen, still record the refund action without returning quantity to available stock

### On Edit
- stock adjustments must reflect differences between original and updated sale item quantities
- change calculations must remain auditable

---

## 11. Financial Interaction

### Cash Sale
A completed cash sale should:
- increase relevant sales totals
- increase register-related money-in records where applicable
- appear in sales history and money flow records

### GCash Sale
A completed GCash sale should:
- increase relevant sales totals
- create corresponding GCash transaction records
- affect the selected GCash account balance according to business rules
- remain visible in both sales and GCash-related history

### Refund / Void Financial Effects
Refunds and voids should:
- reverse or adjust the original financial effect
- remain linked to the original sale
- preserve a visible and traceable money movement history

---

## 12. OCR Interaction in Sales

### OCR Role in Sales
OCR helps the user identify products when selling.

### OCR Sales Flow
1. User opens OCR capture from the sales screen.
2. User captures or uploads product image.
3. Backend runs OCR.
4. Backend performs product matching.
5. Up to 5 product suggestions are returned.
6. User selects the correct product.
7. Product is added to the cart.

### OCR Fallback Rules
- if OCR fails, manual search must be available immediately
- if OCR confidence is low, the system must not auto-add a product without confirmation

---

## 13. Offline Selling Requirements

This module must support true offline selling in version 1.

### Offline Capabilities
- cached product data should remain available offline
- selling should continue without internet connection
- offline-created sales must be queued for sync
- once connection returns, sync should happen automatically

### Offline POS Rules
- locally recorded sales must have temporary or sync-safe references
- the system must show whether a sale is already synced or still pending
- users should be informed when offline mode is active
- sales should not be silently lost during reconnect or refresh scenarios

### Sync Considerations
The final sync conflict strategy is not yet finalized, but this module must be designed to support:
- queued offline transactions
- safe replay/sync after reconnect
- visibility into pending and completed sync states

---

## 14. Reports and Views Related to This Module

The Sales / POS module should feed the reporting layer with:
- daily sales totals
- sales by date range
- sales by cashier
- sales by payment method
- refunded sales
- voided sales
- edited sales
- product sales summaries

The history area should support filters such as:
- date range
- cashier
- payment method
- action type
- product
- sync status if relevant

---

## 15. API Direction

### Possible Endpoint Groups
- sales
- sales-history
- sales-actions
- refunds
- voids
- ocr-product-match
- offline-sync

### Example Endpoint Direction
- create sale
- get sale list
- get sale details
- edit sale
- void sale
- refund sale
- get sales action history
- OCR product lookup from image
- sync offline sales

Exact endpoint naming can be finalized in the API/module canvas later.

---

## 16. Logging and Audit Requirements

The following must be logged:
- sale creation
- sale edits
- sale voids
- sale refunds
- stock restoration decisions
- payment method used
- user who performed the action
- timestamps for all important actions

This ensures that the system remains auditable for both operational and financial review.

---

## 17. Risks and Considerations

### OCR Matching Errors
Products may be matched incorrectly if packaging text is unclear or similar.

Mitigation:
- always show suggestions first
- require user confirmation
- preserve manual search fallback

### Offline Sync Risk
Sales recorded offline may create later sync complexity.

Mitigation:
- use transaction queueing
- clearly show sync state
- preserve local records until confirmed synced

### Refund and Stock Logic Complexity
Refunds may or may not restore stock.

Mitigation:
- present explicit restore-stock choice
- log the chosen behavior clearly
- link inventory movement to refund history

---

## 18. Version 1 Success Criteria for This Module

The Sales / POS module is successful in version 1 if it can:
- let Admin and Cashier access the POS appropriately
- let users identify products through OCR or manual search
- let users build and finalize multi-item sales
- support Cash and GCash sale recording
- generate sale reference numbers automatically
- deduct stock only after final sale completion
- support edit, void, and refund actions with history
- support optional stock restoration during refund
- work during offline selling and sync later
- provide traceable history for all sensitive sales actions

---

## 19. Suggested Future Enhancements

Not part of version 1, but possible later enhancements include:
- receipt printing
- discount support
- tax/VAT support
- suspended carts
- split or mixed payments
- return reasons catalog
- customer profiles
- faster predictive/manual search enhancements
- smarter OCR ranking based on prior confirmations

---

## 20. Next Related Module Documents

After this module, the most connected documents to create are:
- OCR and Product Matching Module
- Inventory Module
- GCash Accounts and Transactions Module
- Offline Mode and Sync Module
- Sales API and Data Model Module

