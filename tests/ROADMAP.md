🧭 PROJECT ROADMAP — API DEVELOPMENT PLAN

This document summarizes the APIs, model changes and how each change works. It's intended for developer onboarding and automated test guidance.

API 1 — Organization Linking (Done)
- Super Admin creates link between organizations.
- Both organizations must accept. When both accepted → request_status = True. Inventory sharing enabled.

API 2 — Allowed Resellers
- Purpose: Define which reseller organizations are allowed to sell Tickets, Umrah Packages, and Hotels.
- Model: AllowedReseller with fields: inventory_owner_company (FK), reseller_company (FK), discount_group (FK), allowed_types (JSON list e.g. ["TICKETS","UMRAH","HOTELS"]).
- Endpoints: standard CRUD. Only inventory owners can create/update.

API 3 — Tickets
- Load tickets only from Allowed organizations + own organization.
- Exclude inactive, passed dates, available_seats=0, reselling_allowed=False.
- Fields added: owner_organization_id, inventory_owner_organization_id, reselling_allowed.
- Seat counters auto-updated from BookingTicketDetails.save()/delete().

API 4 — Umrah Packages
- Similar visibility rules as tickets.
- Fields: inventory_owner_organization_id, reselling_allowed, commission fields.
- Serializer computes adult/child/infant prices and excluded_tickets list.

API 5 — Hotels
- Removed: google_drive_link.
- Added: HotelPhoto (multiple), video, inventory_owner_organization_id, reselling_allowed.
- Rates can only be changed by the inventory owner.

API 6 — Discount Groups
- Model supports:
  - discounts object for ticket/package discounts (group_ticket_discount_amount, umrah_package_discount_amount)
  - hotel_night_discounts: list of objects grouped by the set of discounted hotels, with per-room-type keys and discounted_hotels array
- POST accepts a convenience payload; GET returns the aggregated shape.

API 7 — Bookings
- Booking model now includes booking_type, is_full_package, payments (JSON list), journal_items (JSON list), expiry_time.
- BookingPersonDetail includes ticket_included.
- BookingTicketDetails overrides save/delete to update Ticket counters atomically.

API 8 — Agencies
- Agency gains credit_limit, credit_limit_days, agency_type, agency_id (6-char auto), assign_to (User)

API 9 — Payments
- Payment model/object extended with agent_bank, organization_bank, kuickpay_trn.

API 10 — Auto Seat Management
- Seat counters updated in BookingTicketDetails.save()/delete(); confirmed state and status transitions handled.
- A cron job (not included here) should run daily to expire bookings and revert seats for expired bookings.

Testing
- A unit test for DiscountGroup serializer was added to `booking/tests.py` to assert the GET shape matches the requested format.

How to run the new test locally
1) Activate your venv and ensure DB is configured in `configuration/settings.py`.
2) Run:

```powershell
python manage.py test booking
```

This will create temporary test DB rows and verify the DiscountGroup serializer output.
