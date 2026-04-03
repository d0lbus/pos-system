# OCR and Product Matching Module Specification

## 1. Module Purpose

The OCR and Product Matching module is responsible for converting captured product or transaction images into usable text and then mapping that text to meaningful system records. In this project, OCR is a core feature because the system will **not** rely on barcode or serial number scanning in version 1.

This module supports two main business functions:
- identifying products during selling and product registration
- extracting GCash transaction details from screenshots or photos during transaction recording

The module must work with **live camera capture** and **uploaded images**, and it must always support manual confirmation and manual fallback flows.

---

## 2. Module Goals

- Use OCR as the main assisted recognition method in the system
- Extract readable text from product packaging and GCash screenshots/photos
- Match OCR results against product records in the database
- Suggest likely matches instead of forcing blind automation
- Keep the workflow practical for cashier use
- Support product creation assistance during registration
- Support GCash detail capture during transaction recording
- Remain usable even when OCR is imperfect

---

## 3. Core Use Cases

### 3.1 Selling / POS Product Lookup
The user captures or uploads a product image. The system extracts visible text and matches it against products in the database, returning up to 5 likely matches. The user selects the correct product, and the system adds it to the sale flow.

### 3.2 Product Registration Assistance
The user captures or uploads an image of a product during product creation. OCR attempts to extract text such as product name and brand to help prefill fields or suggest values. The final saved product still depends on user confirmation.

### 3.3 GCash Transaction Recording Assistance
The user uploads or captures a GCash screenshot or transaction image. OCR attempts to extract transaction-related details such as reference number, amount, account clues, and other readable content that can help the user record the GCash transaction faster.

---

## 4. Scope of This Module

### In Scope
- OCR from live camera input
- OCR from uploaded images
- OCR text extraction for products
- OCR text extraction for GCash screenshots/photos
- product matching against stored product records
- showing up to 5 likely product suggestions
- manual confirmation before final selection
- manual fallback search
- OCR assistance in product creation
- OCR assistance in GCash transaction recording
- confidence-aware behavior
- integration with FastAPI backend using PaddleOCR

### Out of Scope
- barcode scanning
- serial number scanning
- full image-classification AI trained on product appearance alone
- automatic no-confirmation product insertion based on weak OCR
- long-term OCR result storage as a required version 1 feature

---

## 5. OCR Workflow Overview

### General OCR Flow
1. User chooses an OCR-supported action.
2. User provides an image through live camera or upload.
3. Frontend sends the image to the backend.
4. Backend runs PaddleOCR.
5. Backend extracts text and confidence-related information.
6. Backend performs interpretation and matching depending on use case.
7. Backend returns results to the frontend.
8. User confirms, corrects, or falls back to manual input.

---

## 6. Product OCR Flow

### 6.1 Product Lookup During Sales
1. User opens OCR from the Sales / POS screen.
2. User captures product image or uploads one.
3. Backend runs OCR and extracts visible packaging text.
4. System normalizes the extracted text.
5. System compares normalized OCR text with product records.
6. System returns up to 5 likely matches.
7. User selects the correct product.
8. Selected product is returned to the sales flow.

### 6.2 Product Assistance During Registration
1. User opens product creation.
2. User uploads or captures the product image.
3. OCR extracts likely product text.
4. System attempts to identify useful fields such as name and brand.
5. Suggested values are shown in the form.
6. User reviews, edits, and confirms before saving the product.

---

## 7. GCash OCR Flow

### GCash Screenshot/Photo Processing
1. User opens GCash transaction entry.
2. User uploads or captures a GCash screenshot/photo.
3. Backend runs OCR.
4. System attempts to identify relevant text such as:
   - reference number
   - amount
   - account clues
   - timestamps if visible
   - fee-related text if visible
5. Extracted values are returned as suggestions.
6. User reviews and confirms before saving the transaction.

Important note:
- OCR is an assistance feature only
- the final transaction record must still depend on user confirmation

---

## 8. Supported Input Methods

### Live Camera
The module must support capturing an image from the device camera directly within the browser-based frontend.

### Uploaded Image
The module must support uploaded images from local files, including:
- product photos
- screenshots
- transaction photos

### Input Rules
- both input methods are required in version 1
- image quality affects OCR performance
- the UI should guide the user when the image is unclear or when OCR fails

---

## 9. OCR Result Behavior

### Product Matching Result Rules
- show suggestions first
- do not force automatic selection when OCR confidence is low
- return up to **5 likely product matches**
- always support manual search fallback

### GCash Extraction Result Rules
- OCR should prefill likely fields where possible
- user must still verify extracted data before saving
- fee handling remains a manual business decision per entry

### Failure Handling
If OCR fails or returns unusable text, the system must:
- notify the user clearly
- avoid silent wrong matches
- provide fallback manual workflow immediately

---

## 10. Product Matching Strategy

The matching layer is responsible for taking OCR text and finding the most relevant product records.

### Matching Inputs
The matching process may use fields such as:
- product name
- brand
- category
- other searchable text derived from product records

### Suggested Matching Process
1. collect OCR text blocks
2. combine useful text into a normalized text set
3. clean punctuation and casing
4. split words/tokens
5. compare OCR-derived terms against product records
6. score candidate products
7. return top matches in ranked order

### Matching Output
For each suggestion, the system should return enough information for user confirmation, such as:
- product name
- brand
- category
- price
- image if available
- confidence or match quality indicator if designed into the UI

### Matching Safeguards
- never assume OCR is always correct
- always support human confirmation
- allow manual search when no good result exists

---

## 11. OCR-Assisted Field Extraction

### Product Registration Assistance
OCR may help suggest:
- product name
- brand

It should not blindly finalize all product fields because:
- OCR may be incomplete
- pricing and stock still require manual entry
- packaging text may not map cleanly to category decisions

### GCash Entry Assistance
OCR may help suggest:
- reference number
- amount
- visible account identifier clues
- fee-related text if readable
- transaction date/time if visible

The system should still require user verification before submission.

---

## 12. Confidence and Confirmation Rules

### Confidence-Aware Design
The module should behave differently based on OCR quality.

#### High Confidence Scenario
- show ranked suggestions
- still allow user confirmation before proceeding

#### Low Confidence Scenario
- clearly indicate uncertain result
- do not auto-select a product or transaction field blindly
- emphasize manual confirmation or manual entry

### Mandatory Confirmation Cases
Manual confirmation is required when:
- OCR confidence is low
- product suggestions are ambiguous
- GCash details appear incomplete
- extracted fields do not strongly match stored records

---

## 13. UI Requirements

### Product OCR UI Needs
- button to launch camera OCR
- button to upload image
- preview of selected/captured image
- loading state while OCR is running
- list of up to 5 likely product matches
- manual search fallback input
- clear empty/no-result state

### Product Creation OCR UI Needs
- image capture/upload area
- extracted text preview or suggestions
- suggested product name/brand values
- editable form fields before saving

### GCash OCR UI Needs
- upload/capture area for screenshot/photo
- extracted field preview
- editable transaction fields
- confirmation before save

### UX Priorities
- quick and clear workflow
- minimal confusion when OCR fails
- strong fallback experience
- responsive behavior on tablet and desktop

---

## 14. Backend Technical Direction

### OCR Engine
- PaddleOCR integrated into the same FastAPI backend

### Backend Responsibilities
- receive image input
- preprocess image if needed
- run OCR pipeline
- extract text blocks
- normalize OCR results
- perform product matching
- prepare GCash field suggestions
- return structured response to the frontend

### Architectural Principle
The OCR module must remain a service inside the same backend so that:
- business logic remains centralized
- OCR and matching are easy to coordinate
- there is no need for a separate OCR server in version 1

---

## 15. API Direction

### Possible Endpoint Groups
- ocr/products/match
- ocr/products/extract
- ocr/gcash/extract

### Example Use Directions
- OCR product lookup from image during selling
- OCR product field assistance during registration
- OCR GCash detail extraction from screenshot/photo

Exact endpoint naming can be finalized in a dedicated API canvas later.

---

## 16. Data and Storage Considerations

### Required Inputs
- uploaded image file or captured image blob

### Temporary Processing
OCR image input may be:
- processed in memory
- stored temporarily during processing
- deleted after processing if persistent storage is not required

### Version 1 Storage Rule
Storing OCR results themselves is **not required** in version 1.

This means:
- OCR logs are optional
- full OCR text history is not required for the first release
- the main goal is usable recognition, not OCR analytics

### Future Storage Option
A future version may add:
- OCR attempt logs
- confirmed product pairing history
- OCR improvement feedback data

---

## 17. Performance and Practical Constraints

### OCR Performance Risks
OCR may struggle when:
- the image is blurry
- text is too small
- the image is poorly lit
- packaging is reflective or crumpled
- the screenshot/photo is cropped badly
- product text is too similar across variants

### Practical Design Response
To keep this usable:
- always provide manual fallback
- return suggestions, not forced answers
- optimize UI for quick retry
- keep OCR as an assistant, not an uncontrolled decision-maker

---

## 18. Security and Validation Considerations

### Input Validation
The backend should validate:
- accepted file types
- file size limits
- empty or invalid uploads

### Processing Safety
The OCR route should avoid:
- accepting unsupported file content
- crashing on unreadable images
- returning misleading results without user-facing status

### User Safety in Workflow
The module should never save business-critical product or GCash records solely from OCR without user confirmation.

---

## 19. Integration with Other Modules

### Sales / POS Module
This module provides product suggestions for the Sales / POS flow.

### Product Module
This module helps prefill product name and brand during product creation.

### GCash Module
This module helps prefill GCash transaction details from screenshots or images.

### Reports Module
Direct reporting use is limited in version 1 because OCR result storage is not required.

### Offline Module
OCR itself may require online or backend availability depending on deployment and caching behavior, but the frontend should still handle no-connection states gracefully.

---

## 20. Business Rules Summary

- OCR is the main assisted recognition method
- barcode/serial scanning is out of scope
- OCR supports both selling and product registration
- OCR also supports GCash transaction detail extraction
- product suggestions must be shown first
- up to 5 product suggestions are allowed
- manual confirmation is required in uncertain cases
- manual fallback is always available
- OCR results are not required to be permanently stored in version 1

---

## 21. Suggested Response Structures

### Product OCR Response Direction
Possible response structure should include:
- extracted text summary
- ranked product suggestions
- optional confidence indicators
- fallback/manual guidance flags

### GCash OCR Response Direction
Possible response structure should include:
- extracted reference number suggestion
- extracted amount suggestion
- extracted account clue suggestion
- extracted fee clue suggestion if found
- extracted date/time suggestion if found
- confidence-related indicators

---

## 22. Non-Functional Requirements for This Module

### Usability
- quick enough for real cashier support
- simple enough for non-technical staff
- clear result presentation

### Reliability
- must fail safely
- must not auto-commit critical records without user confirmation

### Maintainability
- OCR processing and matching logic should be modular
- product matching logic should be separable from OCR extraction logic

### Performance
- response should be fast enough for practical minimart use on common hardware

---

## 23. Risks and Mitigation

### Risk: Wrong Product Match
OCR may extract incomplete or misleading packaging text.

Mitigation:
- ranked suggestions only
- manual confirmation required
- manual search fallback always available

### Risk: Bad GCash Extraction
OCR may misread digits or reference characters.

Mitigation:
- user verifies fields before save
- editable prefills rather than locked output

### Risk: Poor Image Quality
Users may take unclear product photos or screenshots.

Mitigation:
- allow retry
- show image preview
- show clear guidance on failure

---

## 24. Version 1 Success Criteria for This Module

This module is successful in version 1 if it can:
- accept live camera and uploaded image input
- extract useful text using PaddleOCR
- return up to 5 product suggestions for OCR-based product lookup
- support manual confirmation and manual fallback
- help prefill product name and brand during product registration
- help extract GCash details from screenshots/photos
- integrate cleanly with Sales, Product, and GCash modules
- remain understandable and safe even when OCR is imperfect

---

## 25. Suggested Future Enhancements

Possible later enhancements include:
- OCR attempt logging and analytics
- smarter ranking based on prior confirmed matches
- better preprocessing for difficult images
- variant-aware ranking improvements
- image-based recognition beyond text-only OCR
- learning from user confirmations over time

---

## 26. Next Related Module Documents

After this module, the most connected documents to create are:
- Product Module
- GCash Accounts and Transactions Module
- Inventory Module
- Offline Mode and Sync Module
- OCR API and Matching Logic Specification

