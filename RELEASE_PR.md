# Release candidate: Finance module (profit/loss & expense management)

Summary
-------
This PR contains the Finance app enhancements: auditable double-entry posting, FinancialRecord/p&l engine, Expense APIs, manual posting endpoint, COA seeder, walk-in & linked booking aggregation, reporting endpoints, audit logs, permission commands, extra integration tests, and smoke test script.

What changed
- `finance/` new and updated files: models, utils, views, signals, management commands
- Added aggregation + integration tests and smoke test script: `finance/tests_integration_extra.py`, `finance/tests_merge_walkin.py`, `finance/SMOKE_TESTS.ps1`
- Management command to merge walk-in FRs: `finance/management/commands/merge_walkin_financials.py`

Migration notes
- Review `booking/migrations/0067_booking_is_walkin_booking_linked_booking.py` (adds `is_walkin` and `linked_booking`) — run in staging first.
- Follow `finance/MIGRATION_PLAN.md` before applying to production.

Checklist for reviewers
- [ ] Run unit tests: `python manage.py test booking finance -v 2`
- [ ] Run migration plan (dry-run): `python manage.py migrate --plan`
- [ ] Apply migrations in staging and run `.\finance\SMOKE_TESTS.ps1`
- [ ] Verify `assign_finance_permissions` run in staging and `finance_managers` exists
- [ ] Confirm FBR export is intentionally skipped (we implemented an inferred exporter but finalization requires the official FBR spec)

How to deploy
1. Create a staging backup
2. Apply migrations in staging
3. Run smoke-tests (see `finance/SMOKE_TESTS.ps1`)
4. Run full test suite / CI
5. After smoke tests, deploy to production and apply migrations during a maintenance window

Notes
- Git not available in some local dev environments; commit and push from your local machine.
- If persisted merging of walk-in FRs is not desired, the `merge_walkin_financials` command is optional and non-destructive.
