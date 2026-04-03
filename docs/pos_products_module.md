# Products Module Specification

## 1. Module Purpose

The Products module is the main source of product information used across the entire POS system. It is responsible for storing and managing the minimart’s sellable items, including their identity, pricing, categorization, stock-related starting data, visual reference, and operational status.

This module must support accurate product setup because it directly affects:
- OCR-based product matching
- sales processing
- inventory movement
- reporting
- cash flow accuracy

Since the system does **not** use barcodes or serial numbers in version 1, product records must be structured clearly enough for OCR-assisted matching and manual search to work reliably.

---

## 2. Module Goals

- provide a clean and reliable product master list
- support product creation, editing, viewing, and archiving
- ensure each product variant is treated as a separate product record
- support product images for recognition and reference
- support category-based organization
- provide searchable data for OCR matching and manual lookup
- keep archived products visible in historical records
- integrate cleanly with inventory, sales, and reporting

---

## 3. Scope of This Module

### In Scope
- create product
- edit product
- view product details
- list products
- archive or deactivate product
- manage product categories
- upload optional product image
- store required price and cost
- store current stock quantity
- support searchable fields for OCR and manual lookup
- support product creation assistance from OCR

### Out of Scope
- barcode fields
- serial number fields
- supplier linkage in version 1
- purchase order linkage
- multi-store product separation
- discount rules per product
- tax rules per product

---

## 4. Product Identity Rules

### Core Identity Rule
One product record represents one sellable item variant.

### Variant Rule
A different variant is considered a different product.

Examples:
- Coke 500ml and Coke 1.5L are different products
- Shampoo Sachet Regular and Shampoo Sachet Conditioner are different products
- Different flavors, sizes, or major packaging variants should be stored as separate products

### Uniqueness Direction
Product names do not need to be globally unique if the product remains distinguishable by its own full record, but the overall product setup must still avoid confusing duplication.

The final data design should encourage clear naming so that OCR matching and manual search remain practical.

---

## 5. Product Fields

### Confirmed Product Fields
The product record must support:
- name
- brand
- category
- price
- cost
- stock
- image
- status

### Field Rules
- **name**: required
- **brand**: required or strongly expected for matching quality
- **category**: required
- **price**: required
- **cost**: required
- **stock**: required whole-number quantity
- **image**: optional
- **status**: required for active/inactive/archive behavior

### Recommended Additional Internal Fields
For practical implementation, the system may also include:
- id
- created_at
- updated_at
- created_by
- updated_by
- archived_at if soft archiving is used
- searchable_text or derived matching fields if needed internally

---

## 6. Main Features

### 6.1 Product List
The module must provide a product list view for browsing and management.

Expected capabilities:
- view all active products
- search products
- filter by category
- filter by status
- sort products
- access edit and detail actions
- access archive/deactivate action

### 6.2 Product Detail View
The module should provide a detailed view of an individual product.

Suggested content:
- name
- brand
- category
- selling price
- cost
- stock
- image
- status
- timestamps
- product history links if connected to other modules

### 6.3 Product Creation
Admin must be able to create new products.

Creation requirements:
- manual field entry
- optional image upload
- category selection
- whole-number stock entry
- required cost and selling price
- OCR-assisted field suggestion support

### 6.4 Product Editing
Admin must be able to edit product information.

Editable areas may include:
- name
- brand
- category
- price
- cost
- stock if business rules allow it here or via inventory-specific flows
- image
- status

Important note:
If stock changes should remain strictly auditable, the final implementation may route stock updates through the Inventory module rather than allowing unrestricted direct edits inside the Products module.

### 6.5 Product Archiving
The system should use archive/inactive behavior instead of hard delete.

Archive rules:
- archived products should no longer appear as normal active products for selling
- archived products must still remain visible in historical sales and inventory records
- archive actions should be traceable

---

## 7. Business Rules

### Product Creation Rules
- product name is required
- category is required
- price is required
- cost is required
- stock is required
- image is optional
- stock uses whole numbers only

### Product Variant Rules
- each variant is its own product
- no barcode/serial-based product identity is used
- product clarity is important for OCR and manual search

### Status Rules
Possible product statuses may include:
- ACTIVE
- INACTIVE
- ARCHIVED

Version 1 should at least support active versus archived/inactive behavior.

### Deletion Rules
- hard delete should be avoided
- archive/inactive is preferred
- historical references must remain intact

---

## 8. Category Management Requirements

The Products module depends on category support.

### Category Capabilities
- create category
- edit category
- view category list
- assign category to product
- use category in filters and reports

### Category Rules
- category is required for every product
- category naming should remain simple and practical for minimart use
- archived or inactive category behavior can be finalized later if needed

---

## 9. OCR Interaction with Products

This module is tightly connected to the OCR and Product Matching module.

### OCR During Product Creation
OCR may assist product registration by suggesting:
- product name
- brand

### OCR Product Matching Dependence
The quality of OCR product matching depends heavily on having clean product records.

To improve OCR matching quality, product records should:
- use clear naming
- include brand consistently
- avoid vague or incomplete names
- use meaningful category assignment
- include image when possible for user confirmation context

### OCR Confirmation Rule
OCR suggestions should assist the user but must not replace final user confirmation during product creation.

---

## 10. Search and Lookup Requirements

The Products module must support strong manual lookup because OCR is not guaranteed to succeed every time.

### Search Expectations
Users should be able to search products by:
- product name
- brand
- category
- partial text where practical

### Search Use Cases
- POS fallback when OCR fails
- Admin browsing product list
- product selection during edits or reviews
- report filtering support

### Search Quality Consideration
Product naming should be optimized for fast human recognition and OCR-based suggestion ranking.

---

## 11. Product Images

### Purpose of Product Images
Product images help with:
- visual confirmation in product management
- faster confirmation during OCR match suggestions
- clearer distinction between similar products

### Rules
- product image is optional
- image upload should be supported
- image should not be required for product creation
- image usage should remain practical and not block workflow

### Storage Direction
Version 1 may use:
- local file storage first
- cloud storage later if expanded

Exact file handling can be finalized in the technical implementation document.

---

## 12. Integration with Inventory Module

The Products module provides the base product data that the Inventory module uses.

### Product and Inventory Relationship
- every stock movement belongs to a product
- low-stock rules depend on product-level configuration
- archived products remain visible in historical inventory records

### Stock Handling Note
Although the product record stores stock, the preferred design is that actual stock changes remain tied to inventory movements for auditability.

This means the product’s current stock should behave as a derived operational value supported by inventory history, even if it is also stored directly for performance.

---

## 13. Integration with Sales / POS Module

The Sales / POS module uses Products as the source of sellable items.

### Key Relationship Rules
- only active products should normally be sellable
- product price must be available for sales
- product stock must be available for validation during sale flow
- archived products must remain visible in old sales history

### Search and OCR Dependence
Sales depends on:
- manual product search from this module
- OCR suggestions mapped to records from this module

---

## 14. Integration with Reports Module

The Products module provides reference data for reporting.

### Reporting Use Cases
- product sales summaries
- stock-related reports
- low-stock listings
- category-based reports
- archived versus active product views where needed

The reporting layer should remain able to resolve old records even if a product later becomes archived.

---

## 15. UI Requirements

### Product List Screen
Suggested UI elements:
- search bar
- category filter
- status filter
- product table or card list
- product image thumbnail if available
- actions for view, edit, archive
- add product button

### Product Create/Edit Screen
Suggested form fields:
- product name
- brand
- category selector
- selling price
- cost
- stock
- image upload
- status

### OCR Assistance Area
The create/edit form may include:
- image capture/upload trigger
- OCR suggestion preview
- prefilled suggested values for name and brand
- editable confirmation before save

### UX Priorities
- fast entry for Admin
- simple and readable forms
- good tablet and desktop responsiveness
- easy distinction between similar variants

---

## 16. Validation Rules

### Field Validation Direction
- name must not be empty
- category must be selected
- price must be a valid positive number
- cost must be a valid positive number or at least valid according to business rules
- stock must be a whole number
- image must use accepted file formats if uploaded

### Product Data Quality Rules
The module should encourage consistent data entry, especially for:
- brand naming
- size/variant naming in the product name where relevant
- category consistency

This is important not only for data cleanliness but also for OCR matching quality.

---

## 17. Data Design Direction

### Core Product Entity
Suggested fields:
- id
- name
- brand
- category_id
- price
- cost
- stock
- image_path
- status
- created_by
- updated_by
- created_at
- updated_at
- archived_at nullable

### Category Entity
Suggested fields:
- id
- name
- status if needed later
- created_at
- updated_at

### Possible Supporting Data
Depending on final implementation, the system may also support:
- product searchable text index
- product image metadata
- product audit logs

---

## 18. API Direction

### Possible Endpoint Groups
- products
- categories
- products/images

### Example Endpoint Direction
- create product
- get product list
- get product details
- update product
- archive product
- get category list
- create category
- update category

Exact endpoint naming can be finalized in a dedicated API canvas later.

---

## 19. Logging and Audit Requirements

The following actions should be traceable:
- product creation
- product updates
- product archiving
- category creation
- category updates
- important field changes such as price and cost

This is important because product data affects:
- sales totals
- stock accuracy
- OCR matching quality
- historical reporting

---

## 20. Risks and Considerations

### Risk: Confusing Product Duplication
Since variants are separate products, careless naming may create confusing duplicates.

Mitigation:
- use clear naming conventions
- require brand and category
- use images when helpful
- make search results informative

### Risk: OCR Matching Weakness from Poor Product Data
If product names are vague or inconsistent, OCR matching becomes less reliable.

Mitigation:
- keep product names descriptive
- store brand consistently
- maintain category accuracy
- support OCR-assisted but user-confirmed entry

### Risk: Uncontrolled Stock Editing
If stock is edited directly in products without inventory tracking, stock history becomes harder to trust.

Mitigation:
- prefer inventory-based stock adjustments for major stock changes
- preserve movement history in the Inventory module

---

## 21. Version 1 Success Criteria for This Module

This module is successful in version 1 if it can:
- let Admin create, edit, view, and archive products
- store required product fields cleanly
- support required categories
- support optional product image upload
- treat different variants as separate products
- provide reliable product search for manual lookup
- support OCR-assisted product creation inputs
- integrate correctly with Inventory, Sales, and Reports
- preserve historical record integrity when products are archived

---

## 22. Suggested Future Enhancements

Possible later enhancements include:
- supplier linkage
- purchase cost history
- product aliases for stronger OCR matching
- more advanced search ranking
- category management enhancements
- product bundles or grouped items
- product-level analytics views

---

## 23. Next Related Module Documents

After this module, the most connected documents to create are:
- Inventory Module
- Categories Module if separated further
- GCash Accounts and Transactions Module
- Offline Mode and Sync Module
- Products API and Data Model Module

