# Offline Mode and Sync Module Specification

## 1. Module Purpose

The Offline Mode and Sync module is responsible for allowing the POS system to continue functioning during internet interruptions and then safely synchronize local changes back to the cloud-connected backend when connectivity returns.

This module is essential because version 1 requires **true offline selling**, not just cached viewing. The minimart must still be able to:
- access product data
- continue selling
- update the local operational state
- preserve unsynced transactions
- recover safely after reconnecting

This module must be designed carefully because it affects sales, inventory, product data usage, financial consistency, and user trust.

---

## 2. Module Goals

- support true offline selling in version 1
- cache essential operational data locally
- queue unsynced changes safely
- sync automatically once connectivity returns
- prevent silent data loss
- expose sync state clearly to the user
- preserve traceability of offline-created records
- keep the cashier workflow usable even during unstable internet

---

## 3. Scope of This Module

### In Scope
- detect online and offline state
- cache product and pricing data locally
- allow sales creation while offline
- queue unsynced sales and related actions
- mark records as pending sync, synced, or failed
- automatically attempt synchronization after reconnect
- preserve local transaction history until sync succeeds
- support offline-safe operational UI states
- provide basic conflict-handling direction
- integrate with inventory effects and financial records through sync

### Out of Scope
- fully generalized offline support for every module in version 1
- complex multi-device offline merge logic
- real-time collaborative conflict resolution
- peer-to-peer local sync between multiple store devices
- full offline OCR model execution on-device unless later implemented explicitly

---

## 4. Core Concepts

### Offline-Capable Selling
The Sales / POS module must continue to function during internet loss using cached essential data and locally stored unsynced transactions.

### Local Cache
Certain system data should be stored locally on the device so that key flows still work offline.

### Sync Queue
Unsynced records should be stored in a queue-like structure until the backend confirms successful synchronization.

### Sync State Visibility
Users should always be able to understand whether a record is:
- synced
- pending sync
- failed sync

### Safe Recovery
Refreshing, reconnecting, or reopening the app should not silently erase unsynced operational records.

---

## 5. Offline-Critical Use Cases

### 5.1 Offline Sale Creation
A cashier loses internet connection but still needs to sell products. The system should allow the cashier to create a sale using cached product and price data, store the sale locally, and mark it as pending sync.

### 5.2 Reconnect and Sync
When internet connectivity returns, the system should automatically attempt to synchronize pending records to the backend.

### 5.3 Offline UI Awareness
The cashier should know that the system is offline and that newly created sales are pending synchronization.

### 5.4 Failed Sync Recovery
If a record fails to sync, the system should preserve it, show the failure state clearly, and support retry behavior.

---

## 6. Version 1 Offline Scope Direction

Version 1 should prioritize offline support for the most business-critical operational flows.

### Required Version 1 Offline Support
- cached product and pricing data
- offline sale creation
- local pending sale storage
- later sync to backend
- sync state visibility

### Limited or Cautious Offline Areas
The final implementation may keep some actions online-first or more restricted if reliability would otherwise become too risky, especially for:
- complex admin maintenance flows
- broad financial adjustments
- OCR processing if backend access is unavailable

The detailed boundary can be refined later, but the minimum requirement is true offline selling.

---

## 7. Data That Should Be Cached Locally

The frontend should locally cache the minimum data needed for offline selling.

### Priority Cached Data
- active products
- product pricing
- product images if practical for lookup context
- current known stock values
- category references if needed for UI
- local user session/auth context if allowed by security design

### Notes
- the cache must support quick product lookup during offline selling
- cached data should be refreshed when online
- old cached data should be updated carefully after successful sync or refresh

---

## 8. Offline Sales Flow

### Flow
1. User logs in and has usable cached data available.
2. Internet becomes unavailable.
3. User opens the Sales / POS screen.
4. User selects products using cached product data.
5. User creates and finalizes the sale.
6. System stores the sale locally as pending sync.
7. System marks related local operational state as unsynced.
8. User continues working.
9. Once internet returns, the system attempts to sync the pending sale.
10. If sync succeeds, the record becomes synced.
11. If sync fails, the record remains pending or failed with visible status.

---

## 9. Offline Record States

The system should use explicit local sync states for affected records.

### Suggested States
- PENDING_SYNC
- SYNCED
- FAILED_SYNC
- SYNCING if useful for UX

### Why This Matters
These states make it possible to:
- prevent silent loss of data
- show the cashier what is safe and what still needs backend confirmation
- help Admin troubleshoot operational issues

---

## 10. Sync Queue Behavior

### Purpose
Pending offline records should be stored in a durable local queue or queue-like structure.

### Queue Requirements
- records must survive page refresh or app reopen where practical
- pending records must not disappear before sync confirmation
- retry should be possible
- sync ordering should remain safe and understandable

### Practical Direction
The system should treat offline-created sales as locally committed but backend-pending until the server accepts them.

---

## 11. Automatic Synchronization

### Trigger
When connectivity returns, the system should automatically attempt synchronization.

### Sync Expectations
- process pending records in a safe order
- update local state after confirmed success
- preserve failed items for later retry
- avoid duplicate submissions where possible

### UX Expectation
The user should see that synchronization is happening and whether it succeeded or failed.

---

## 12. Conflict and Reconciliation Direction

The exact conflict strategy was not finalized by the user, but the system still needs a safe design direction.

### Important Reality
Offline selling means local decisions may be made using cached data that could become outdated by the time sync occurs.

### Version 1 Design Direction
For version 1, the system should focus on:
- preserving unsynced records
- preventing silent loss
- surfacing failed sync clearly
- keeping reconciliation logic understandable

### Practical Reconciliation Principle
If the backend rejects or flags a pending record during sync, the system should:
- preserve the local record
- mark it clearly as failed or needing attention
- avoid silently discarding it

The full advanced conflict-resolution workflow can be expanded later.

---

## 13. Inventory Considerations During Offline Selling

Offline selling affects stock behavior directly.

### Required Behavior
- cached stock should be available for selling
- local stock presentation should reflect offline-created sales on the device
- once synced, backend inventory should be updated accordingly

### Important Limitation
Because version 1 is currently for one staff only, the conflict risk is lower than in a multi-user store environment, but stock reconciliation still needs caution.

### Practical Direction
The local UI should treat offline sales as operationally real, while still showing that the backend sync is pending.

---

## 14. Financial Considerations During Offline Selling

Sales created offline still affect operational financial understanding.

### Practical Direction
- offline sales should be stored locally with full sale details
- related money movement and GCash-linked interpretation should be synchronized when backend sync completes
- the UI should not pretend that unsynced backend records are already fully confirmed in cloud state

### Important Note
The frontend may still show local operational totals, but sync status should remain visible where relevant.

---

## 15. OCR Considerations in Offline Mode

OCR in this project is handled inside the FastAPI backend using PaddleOCR.

### Implication
If the backend is not reachable because the device is offline from the server, OCR may not be available unless a later version adds special offline OCR support.

### Version 1 Direction
The system should degrade gracefully when OCR is unavailable offline by:
- notifying the user clearly
- preserving manual product search fallback
- avoiding blocked selling flow

### Practical Rule
Offline selling must still work even if OCR does not.

---

## 16. User Experience Requirements

### Required Offline UI Signals
The app should clearly show:
- when the app is offline
- when a sale is pending sync
- when sync is in progress
- when sync succeeds
- when sync fails

### User Messaging Principles
- clear and simple
- no hidden states
- no silent failures
- no false assumption that backend save already happened

### Operational Priority
The cashier must be able to keep selling with minimal confusion.

---

## 17. Main Features

### 17.1 Connectivity State Detection
The frontend should detect whether it is online or offline.

### 17.2 Local Operational Cache
The app should cache essential operational data needed for selling.

### 17.3 Pending Transaction Storage
Offline-created sales should be saved locally until synced.

### 17.4 Sync Status Tracking
Each pending record should have a visible sync state.

### 17.5 Automatic Retry/Sync
The app should automatically attempt synchronization after reconnect.

### 17.6 Failed Sync Preservation
Failed records should remain visible and retryable rather than disappearing.

---

## 18. User Access and Permissions

Offline support primarily affects operational users.

### Cashier
Cashier must be able to continue sales flow while offline.

### Admin
Admin should be able to review sync-related states and possibly retry or inspect failures in future admin workflows.

The exact admin review tools can be refined later.

---

## 19. UI Requirements

### POS Screen Offline Needs
Suggested UI behavior:
- offline badge/banner
- sync pending indicator
- product lookup from cached data
- clear error state when OCR is unavailable offline

### Sync Status Views
The system may provide:
- pending sync count
- failed sync count
- recent sync status display
- sale-level sync badge in history views

### UX Priorities
- cashier confidence
- low friction during bad connectivity
- clear sync transparency
- recoverability after reconnect

---

## 20. Validation and Safety Rules

### Offline Entry Safety
- local records must remain complete enough for later sync
- incomplete offline records should not be silently accepted as final if critical data is missing

### Duplicate Safety Direction
The sync mechanism should be designed to reduce duplicate record creation, especially if the same local record is retried after unstable connectivity.

### Record Integrity
Pending offline records must preserve:
- transaction content
- timestamps
- relevant local identifiers
- sync state metadata

---

## 21. Data Design Direction

### Suggested Offline Sync Record Structure
Possible fields:
- id
- local_reference
- record_type
- payload_snapshot
- sync_state
- error_message nullable
- retry_count
- created_at
- updated_at
- synced_at nullable

### Record Types That May Need Support
Version 1 should at least support:
- SALE

Later versions may expand to other types as needed.

### Important Design Idea
The local record should have enough data to replay or submit the transaction safely to the backend after reconnect.

---

## 22. Integration with Sales / POS Module

This is the most important integration.

### Relationship Rules
- offline sales must still be creatable
- offline-created sales must remain visible in sales history with sync state
- backend-confirmed sync should update sale status accordingly
- failed sync should not silently erase the local sale

---

## 23. Integration with Inventory Module

### Relationship Rules
- local operational stock should reflect offline sales on the device
- backend inventory should update when sync succeeds
- future reconciliation logic should remain understandable if discrepancies appear

---

## 24. Integration with Money Flow and GCash Modules

### Relationship Rules
- offline sales that imply financial records should carry enough information for backend creation later
- GCash-linked offline sales should still preserve the intended payment context
- final backend-linked financial records should be created during successful sync

---

## 25. Integration with Auth Module

Offline behavior depends partly on how login/session state is handled.

### Direction
The final auth design should support practical continued use for already authenticated users when connectivity drops, while still respecting security boundaries.

The exact PIN/session/offline login behavior can be refined later in the Auth and Access module.

---

## 26. API Direction

### Possible Endpoint Groups
- sync/sales
- sync/status

### Example Endpoint Direction
- submit pending offline sales
- check sync status
- acknowledge synced records if needed

Exact endpoint naming can be finalized later in the API-specific canvas.

---

## 27. Logging and Audit Requirements

The following should be traceable:
- offline sale creation
- sync attempts
- sync success
- sync failure
- retry attempts
- timestamps for offline creation and final sync

This is important because offline behavior can otherwise make records harder to trust operationally.

---

## 28. Risks and Considerations

### Risk: Silent Data Loss
If unsynced records are not stored durably, a refresh or app close could lose real sales.

Mitigation:
- durable local storage
- explicit sync states
- preserve records until success

### Risk: Duplicate Sync Submission
If unstable connectivity causes repeated sync attempts, duplicate records may occur.

Mitigation:
- use local identifiers
- design idempotent-safe sync behavior where practical
- track sync state carefully

### Risk: User Confusion About Record State
If the UI does not distinguish synced vs pending, users may assume the backend already has the record.

Mitigation:
- visible sync badges
- clear banners/messages
- sale-level sync transparency

### Risk: OCR Unavailable Offline
Because OCR depends on the backend, offline OCR may not work in version 1.

Mitigation:
- clear fallback messaging
- strong manual product search flow

---

## 29. Version 1 Success Criteria for This Module

This module is successful in version 1 if it can:
- allow true offline selling
- cache essential product/pricing data locally
- store offline-created sales safely
- show sync state clearly
- automatically sync when connectivity returns
- preserve failed records for retry
- integrate safely with Sales, Inventory, Money Flow, and GCash behavior
- avoid silent data loss during offline operation

---

## 30. Suggested Future Enhancements

Possible later enhancements include:
- richer sync conflict resolution tools
- admin sync troubleshooting views
- broader offline support for more modules
- local offline OCR support if ever needed
- multi-device reconciliation strategies
- more advanced retry and recovery controls

---

## 31. Next Related Module Documents

After this module, the most connected documents to create are:
- Dashboard and Reports Module
- Auth and Access Module
- System Architecture and Technical Structure Module
- Offline Data Strategy and API Module

