CUSTOMERS APP - README
======================

This document summarizes the Customer Auto-Collection + Lead Management work added to the project.
It describes code changes, data flow, endpoints, JSON formats, migration notes, tests, and next steps.

1) Goal
-------
- Aggregate customer contact data from Bookings, Passport Leads and Area/Branch customers.
- Deduplicate by phone, email, and passport_number (priority order: phone → email → passport).
- Provide endpoints for merged list (auto-collection), manual add, and soft-delete.
- Keep customers in-sync via Booking and Lead flows.

2) Files added / edited (high level)
----------------------------------
- New app: `customers/` (models, serializers, views, utils, signals, urls, tests)
  - `customers/models.py` — Customer (added `passport_number`), Lead, FollowUpHistory, LoanCommitment
  - `customers/utils.py` — upsert_customer_from_data(...) central helper
  - `customers/views.py` — CustomerViewSet (auto_collection action, manual-add, soft-delete), LeadViewSet, followups, loan commitments
  - `customers/serializers.py` — Customer/Lead/FollowUp/Loan serializers
  - `customers/signals.py` — optional receivers (Booking/Lead) to call upsert
  - `customers/tests/` — unit tests for upsert, dedupe, soft-delete and an end-to-end Booking→Lead→Customer test
  - `customers/migrations/` — migrations including adding `passport_number` field

- Integrated teammate `leads` app (existing in repo) — small fixes to migrations and calls to upsert helper in `leads.services`.

3) Data flow (high-level)
-------------------------
1. Booking saved (or created):
   - `leads.services.LeadService.auto_create_from_booking(booking)` examines booking.person_details.
   - It finds/creates a `Lead`, links booking -> lead, marks conversion_status.
   - After linking/creating Lead, it calls `customers.utils.upsert_customer_from_data(...)` to create/update a Customer.

2. Lead created/updated directly (API):
   - Lead creation flow (views/services) also calls `upsert_customer_from_data(...)` so leads push to customers.

3. Manual customer add (API):
   - POST /customers/manual-add/ -> creates Customer record (sets is_active True).

4) Deduplication / Upsert logic (contract)
-----------------------------------------
- Function: customers.utils.upsert_customer_from_data(
    full_name, phone, email, passport_number, branch, organization, source, last_activity
  ) -> returns (customer_instance, created_flag)

- Matching priority used to find existing customer: phone -> email -> passport_number.
- If found: update fields (full_name, branch, organization, last_activity) when changed and return created_flag=False.
- If not found: create a new Customer with provided fields and return created_flag=True.

Edge cases considered:
- Empty or malformed phone/email are ignored for matching.
- Soft-deleted customers (is_active=False) are not returned by public endpoints. Upsert currently will operate on all customers regardless of is_active (adjustable if you want). 

5) API endpoints and JSON formats (examples)
-------------------------------------------
All endpoints require authentication (IsAuthenticated) — use JWT at /api/token/.

- POST /api/token/
  Request: { "username": "user", "password": "pass" }
  Response: { "refresh": "...", "access": "..." }

- GET /customers/
  Response (paginated):
  {
    "count": 2,
    "next": null,
    "previous": null,
    "results": [
      {
        "id": 1,
        "full_name": "Ali Khan",
        "phone": "+92300...",
        "email": "ali@example.com",
        "passport_number": "P12345",
        "city": "Lahore",
        "source": "Lead",
        "branch": 1,
        "organization": 1,
        "is_active": true,
        "service_type": null,
        "last_activity": "2025-10-30T08:12:00Z",
        "created_at": "2025-10-01T10:00:00Z",
        "updated_at": "2025-10-30T08:12:00Z"
      }
    ]
  }

- GET /customers/auto-collection/
  Response:
  {
    "total_customers": 1,
    "customers": [ <same customer objects as above> ]
  }

- POST /customers/auto-collection/  (trigger scan)
  Request body: { "cutoff_days": 30 }
  Response: { "created": 4, "updated": 2 }

- POST /customers/manual-add/
  Request body example:
  {
    "full_name": "Test User",
    "phone": "+92300...",
    "email": "test@example.com",
    "passport_number": "PX111",
    "city": "Karachi",
    "source": "Manual",
    "branch": 2,
    "organization": 1
  }
  Success response: created customer object (201)

- DELETE /customers/{id}/  -> Soft-delete (sets is_active=False), returns 204 No Content

- Leads endpoints: /leads/ (list/create) — Lead model has passport_number and contact_number fields; lead creation also calls upsert helper.

6) Migration notes / DB instructions
----------------------------------
- I fixed migration dependency names in `leads/migrations` to match this repository's `booking` migration names.
- I added and applied migrations for `customers` including adding `passport_number` field.

Safe procedure used for development DB in this repo:
1. Inspect DB tables (ensure booking, organization exist).
2. If tables already exist but Django's migration history doesn't mark initial migrations applied, use `python manage.py migrate <app> 0001 --fake` to mark initial migrations as applied (development only).
3. Then run `python manage.py migrate` to apply subsequent migrations.

Important: If this is a production DB, take a full backup before faking or altering migration history. Prefer running migrations on a copy or follow a DB-approved migration plan.

7) Tests
--------
- Tests added under `customers/tests/`:
  - `test_upsert.py` — upsert create/update by phone/email, auto-collection merging and soft-delete API test.
  - `test_passport_and_integration.py` — passport dedupe test and end-to-end Booking -> Lead -> Customer integration test.

- How tests were run locally by the implementer:
  - `python manage.py test customers --verbosity=2`
  - All customers tests passed (6 tests at time of run).

8) How to exercise the endpoints locally (quick steps)
---------------------------------------------------
1) Start dev server (in your venv):
   python manage.py runserver

2) Create a superuser (for admin):
   python manage.py createsuperuser

3) Use JWT login to get token:
   POST /api/token/ with {"username":"...","password":"..."}

4) Call endpoints using Authorization header: `Authorization: Bearer <access_token>`

PowerShell example (get token then list customers):
  $t = Invoke-RestMethod -Method Post -Uri http://127.0.0.1:8000/api/token/ -Body (@{username='admin'; password='pass'} | ConvertTo-Json) -ContentType 'application/json'
  $acc = $t.access
  Invoke-RestMethod -Method Get -Uri http://127.0.0.1:8000/customers/ -Headers @{ Authorization = "Bearer $acc" }

5) Use admin UI at /admin/ to add sample Bookings / BookingPersonDetail or Customers for quick inspection.

9) AreaCustomer integration options
----------------------------------
If an AreaCustomers app appears, integrate it by one of these low-risk options:

(A) Signals
    - Add a small `post_save` receiver in that app (or in `customers.signals`) that calls `customers.utils.upsert_customer_from_data(...)` when an AreaCustomer record is created/updated.

(B) Public util
    - Other apps can import `from customers.utils import upsert_customer_from_data` and call it directly with the relevant fields.

(C) Webhook
    - Expose a secure webhook endpoint in `customers` that external systems can POST to for bulk/real-time sync.

10) Next steps & recommendations
--------------------------------
- Add a small `docs/CUSTOMERS_README.txt` (this file) to the repository — done.
- Add CI job to run `python manage.py test` for the repo (recommended).
- Consider adding RBAC/permissions to the endpoints if different teams need different access.
- If you expect heavy write/scan load, consider adding an asynchronous job for the auto-collection scan (Celery/RQ) instead of scanning synchronously on API call.

Contact / follow-up
-------------------
If you'd like, I can:
- create a few sample customers so Swagger shows non-empty responses,
- run the full project test suite,
- add a PR-ready description or open a branch with these changes,
- implement an AreaCustomer signal hook sample.

End of README
