# Local Offline Data Strategy

## 1. Document Purpose

This document defines how the frontend should handle local data for offline-capable operation, especially for true offline selling.

It focuses on:
- what data should be cached locally
- what data should be queued locally
- how sync states should work
- how local records should be structured
- how the UI should interpret local offline data

This is a frontend-heavy technical strategy document, not a backend database schema document.

---

## 2. Offline Strategy Principles

- prioritize true offline selling first
- cache only what is necessary for version 1 critical flows
- preserve unsynced data durably
- never silently lose offline-created sales
- keep local sync states explicit
- make the UI clearly reflect pending or failed sync
- allow manual fallback when backend-only features like OCR are unavailable offline

---

## 3. What Must Work Offline in Version 1

### Required
- product lookup from cached data
- product pricing from cached data
- sale cart creation
- sale finalization locally
- local pending sale storage
- sync state display
- automatic sync attempt after reconnect

### Not Required as Fully Offline-First
- full admin maintenance across all modules
- full backend OCR processing while disconnected from server
- all reports and dashboard data in fully offline mode

---

## 4. Local Storage Layers Direction

A practical frontend implementation should separate local data into categories.

### 4.1 Cached Reference Data
Used for reading and selling while offline.

### 4.2 Local Operational Queue Data
Used for records created offline that must sync later.

### 4.3 Local Session/App State
Used for current user session continuity and sync visibility.

---

## 5. Recommended Local Data Buckets

## 5.1 Cached Products
Should include enough product data for offline selling:
- product id
- name
- brand
- category reference or label
- price
- current known stock
- low-stock threshold if useful
- image reference if practical
- product status
- last updated timestamp

### Purpose
- manual product search offline
- POS product selection offline
- cart pricing offline

## 5.2 Cached Categories
Should include:
- category id
- category name

### Purpose
- optional filter/display use in offline-ready screens

## 5.3 Local Pending Sales Queue
Should store offline-created sales not yet synced.

### Purpose
- preserve unsynced completed sales
- allow retry after reconnect
- show sync state in UI

## 5.4 Local Sync Metadata
Should track:
- sync attempts
- error messages
- retry counts
- local references
- sync state

## 5.5 Local Session State
Should preserve enough auth/app state to continue operation when already logged in and then internet drops.

---

## 6. Recommended Local Storage Technology Direction

The frontend should use a durable browser-side storage strategy rather than relying only on in-memory state.

### Direction
Use a local abstraction layer such as `localDb.ts` or equivalent to isolate:
- cached product storage
- local pending sales storage
- sync metadata storage

### Why
This keeps offline logic centralized and avoids scattering storage access all over the app.

---

## 7. Cached Product Strategy

### Data to Cache
At minimum:
- active sellable products
- pricing
- stock snapshot
- status
- searchable text fields

### Refresh Behavior
When online:
- fetch latest product list
- update local cache
- refresh stale records

### Practical Rule
Only cache products needed for selling, not every possible admin-only dataset in version 1.

---

## 8. Local Pending Sale Record Structure

Each offline-created sale should be stored locally in a way that is safe to replay to the backend.

### Suggested Local Fields
- local_reference
- created_at
- created_by
- payment_method
- selected_gcash_account_id if relevant
- items array
- totals
- sync_state
- retry_count
- error_message nullable
- last_attempted_at nullable

### Each Item Should Include
- product_id
- quantity
- unit_price
- line_total
- cached product snapshot fields if useful for UI display

### Important Rule
The local payload must be complete enough that the backend can recreate the sale later.

---

## 9. Sync State Definitions

The frontend should use explicit sync states.

### Suggested States
- `PENDING_SYNC`
- `SYNCING`
- `SYNCED`
- `FAILED_SYNC`

### State Meaning
- `PENDING_SYNC`: stored locally, not yet submitted successfully
- `SYNCING`: currently being submitted
- `SYNCED`: backend confirmed success
- `FAILED_SYNC`: submission failed and needs retry

### UI Use
These states should be visible in sales history or operational indicators where relevant.

---

## 10. Offline Sale Creation Flow

1. User is authenticated and product cache exists.
2. User loses internet connection.
3. User creates sale using cached product data.
4. Sale is finalized locally.
5. Sale is inserted into local pending queue with `PENDING_SYNC` state.
6. UI confirms local success and shows pending sync state.
7. Local stock representation is updated on the device for operational continuity.

---

## 11. Sync Submission Flow

1. App detects internet connection restored.
2. App scans local queue for pending/failed records eligible for retry.
3. App marks one or more records as `SYNCING`.
4. App submits payload to sync endpoint.
5. If backend confirms success:
   - mark record as `SYNCED`
   - store backend reference if returned
6. If backend rejects or fails:
   - mark as `FAILED_SYNC`
   - preserve error message
   - keep record locally

---

## 12. Duplicate Safety Direction

Because unstable internet may cause repeated attempts, the local queue must support replay safety.

### Practical Direction
Each pending record should have:
- a stable local reference
- retry count tracking
- clear current sync state

### Backend Coordination
The backend sync endpoint should be designed to use local references or equivalent idempotency-aware behavior where practical.

---

## 13. Local Stock Handling Direction

Offline-created sales should affect the device’s local operational stock view.

### Practical Rule
When a sale is finalized offline:
- deduct quantity from the locally displayed stock snapshot
- do not silently pretend the backend has already confirmed it
- keep sync state visible

### Limitation
Because version 1 is for one staff only, local stock conflict risk is lower, but not zero if cached data becomes stale.

---

## 14. Product Search Offline

Because OCR may not be available offline if the backend is unreachable, manual product search must be strong.

### Offline Search Needs
- search by name
- search by brand
- search through cached products quickly

### Practical Rule
Offline selling must not depend on OCR being available.

---

## 15. OCR Offline Handling

### Current Architecture Constraint
OCR runs inside the backend.

### Result
If the frontend cannot reach the backend, OCR is unavailable.

### Required UI Behavior
- show OCR unavailable message clearly
- allow immediate manual search fallback
- do not block the selling flow

---

## 16. Local Session Behavior Direction

The system should support continued use for an already authenticated user when connectivity drops.

### Practical Rule
If the user is already logged in and the session remains locally valid:
- allow continued offline sales work
- preserve role-aware access to allowed screens

### Important Boundary
Fresh fully offline login behavior was not finalized, so version 1 should prioritize continuity of an existing session rather than promising full cold-start offline authentication.

---

## 17. Local Data Refresh Strategy

When online, cached data should be refreshed periodically or when key screens load.

### Refresh Targets
- products
- categories if used in POS filtering
- current stock snapshot
- selected GCash account references if needed for sales flow

### Safety Direction
Cache refresh should not wipe pending unsynced local sales.

---

## 18. Suggested Local Data Modules

A practical frontend implementation may split offline logic into:
- `localDb.ts` for storage access
- `syncHelpers.ts` for queue handling logic
- `useOfflineStatus.ts` for connectivity state
- `useSyncQueue.ts` for sync lifecycle orchestration

### Possible Local Stores
- `productCacheStore`
- `pendingSalesStore`
- `syncMetaStore`
- `sessionStore`

---

## 19. Error Handling Direction

### Required Behaviors
- failed sync should remain visible
- pending records should not disappear on refresh
- invalid local payloads should be surfaced clearly
- reconnect should trigger retry attempts safely

### Error Fields to Preserve
For failed sync records, keep:
- error message
- last attempted time
- retry count
- current state

---

## 20. UI Integration Requirements

### Sales Screen
Must show:
- offline status banner/badge
- pending sync indicator after offline sale
- manual search availability even if OCR fails offline

### History/Operational Views
Should show:
- pending sync badges
- failed sync badges
- synced state where relevant

### Optional Admin View Later
Could show:
- pending sync queue review
- failed sync troubleshooting list

---

## 21. Recommended Local Data Retention Behavior

### Pending Records
Keep until backend confirms sync success.

### Synced Records
May be removed from the pending queue after success, but the UI may still preserve a local lightweight history marker if useful.

### Cached Products
Refresh when online; old cache may be replaced safely if not tied to pending record integrity.

---

## 22. Risks and Considerations

### Risk: Silent Loss of Unsynced Sales
Mitigation:
- durable local storage
- explicit queue state
- no deletion before backend confirmation

### Risk: Duplicate Submission
Mitigation:
- stable local references
- retry-aware queue handling
- backend idempotency-aware sync logic

### Risk: Stale Product/Stock Data
Mitigation:
- refresh cache when online
- show sync/offline state clearly
- treat offline stock as operational snapshot, not unquestionable truth

### Risk: Overcomplicated Offline Support
Mitigation:
- keep version 1 focused on offline selling first
- avoid trying to make every module fully offline-capable immediately

---

## 23. Success Criteria

This offline data strategy is successful if it:
- supports true offline selling
- preserves pending sales durably
- defines concrete local data buckets
- provides explicit sync states
- supports safe retry behavior
- keeps OCR failure from blocking offline sales
- is concrete enough to guide frontend local storage implementation

