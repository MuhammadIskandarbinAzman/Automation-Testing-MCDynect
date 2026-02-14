# TEST_MATRIX

## Latest Execution Summary
- Run date: `2026-02-12`
- Command: `MCDYNECT_HEADLESS=true pytest -q`
- Result: `21 passed`
- Duration: `219.15s`

## Coverage Matrix

| Test ID | Use Case ID | Scenario | Actor | Test File | Test Function | Type | Priority | Status |
|---|---|---|---|---|---|---|---|---|
| T-LCSE-02-01 | MCD-LCSE-02 | Update profile success | Licensee | `tests/test_licensee_update_profile.py` | `test_MCD_LCSE_02_update_profile_success` | Functional | High | PASS |
| T-LCSE-03-01 | MCD-LCSE-03 | Logout via user menu (basic path) | Licensee | `tests/test_licensee_logout_basic_path.py` | `test_MCD_LCSE_03_logout_basic_path_from_user_menu` | Functional | High | PASS |
| T-LCSE-03-02 | MCD-LCSE-03 | Logout via sidebar shortcut (alternative path) | Licensee | `tests/test_licensee_logout_alternative_path.py` | `test_MCD_LCSE_03_logout_alternative_path_from_sidebar` | Functional | High | PASS |
| T-LCSE-04-01 | MCD-LCSE-04 | Open Redeem tab via shortcut | Licensee | `tests/test_licensee_redeem_shortcut.py` | `test_MCD_LCSE_04_access_redeemable_item_tab_shortcut` | Functional | Medium | PASS |
| T-LCSE-05-01 | MCD-LCSE-05 | Open Trade In page via shortcut | Licensee | `tests/test_licensee_trade_in_shortcut.py` | `test_MCD_LCSE_05_access_trade_in_tab_page_shortcut` | Functional | Medium | PASS |
| T-LCSE-06-01 | MCD-LCSE-06 | Switch outlet account | Licensee | `tests/test_licensee_switch_outlet_account.py` | `test_MCD_LCSE_06_switch_outlet_account` | Functional | High | PASS |
| T-LCSE-07-01 | MCD-LCSE-07 | Modify outlet opening day status + save hours modal | Licensee | `tests/test_licensee_opening_day.py` | `test_MCD_LCSE_07_modify_outlet_opening_day` | Functional | High | PASS |
| T-LCSE-07-E1 | MCD-LCSE-07 | Cancel edit opening hours modal (exception path) | Licensee | `tests/test_licensee_opening_day.py` | `test_MCD_LCSE_07_cancel_edit_opening_hours` | Functional | Medium | PASS |
| T-LCSE-08-01 | MCD-LCSE-08 | View all announcements and open detail in new tab | Licensee | `tests/test_licensee_announcements.py` | `test_MCD_LCSE_08_view_all_announcement_listings_and_details` | Functional | Medium | PASS |
| T-LCSE-09-01 | MCD-LCSE-09 | Navigate to full staff directory via dashboard | Licensee | `tests/test_licensee_staff_directory.py` | `test_MCD_LCSE_09_view_all_staff_directory` | Functional | Medium | PASS |
| T-LCSE-10-01 | MCD-LCSE-10 | Modify staff information and revert | Licensee | `tests/test_licensee_modify_staff.py` | `test_MCD_LCSE_10_modify_staff_information` | Functional | High | PASS |
| T-LCSE-PWD-01 | N/A | Password update should fail with incorrect current password flow | Licensee | `tests/test_licensee_update_password.py` | `test_MCD_LCSE_password_update_and_revert` | Negative | Medium | PASS |
| T-LOGIN-LCSE-01 | N/A | Login success | Licensee | `tests/test_login_licensee.py` | `test_licensee_can_log_in` | Smoke | High | PASS |
| T-LOGIN-LCSE-02 | N/A | Login failure with invalid credentials | Licensee | `tests/test_login_licensee.py` | `test_licensee_cannot_log_in_with_invalid_credentials` | Negative | High | PASS |
| T-LOGIN-AM-01 | N/A | Login success | Area Manager | `tests/test_login_area_manager.py` | `test_area_manager_can_log_in` | Smoke | Medium | PASS |
| T-LOGIN-INV-01 | N/A | Login success | Inventory | `tests/test_login_inventory.py` | `test_inventory_can_log_in` | Smoke | Medium | PASS |
| T-LOGIN-PROC-01 | N/A | Login success | Procurement | `tests/test_login_procurement.py` | `test_procurement_can_log_in` | Smoke | Medium | PASS |
| T-LOGIN-PROD-01 | N/A | Login success | Production | `tests/test_login_production.py` | `test_production_can_log_in` | Smoke | Medium | PASS |
| T-LOGIN-LIC-01 | N/A | Login success | Licensing | `tests/test_login_licensing.py` | `test_licensing_can_log_in` | Smoke | Medium | PASS |
| T-LOGIN-COMP-01 | N/A | Login success | Compliance | `tests/test_login_compliance.py` | `test_compliance_can_log_in` | Smoke | Medium | PASS |
| T-LOGIN-FIN-01 | N/A | Login success | Finance | `tests/test_login_finance.py` | `test_finance_can_log_in` | Smoke | Medium | PASS |

## Suggested Status Values
- `PASS`
- `FAIL`
- `BLOCKED`
- `NOT RUN`

## Update Procedure
1. Run full suite: `MCDYNECT_HEADLESS=true pytest -q`
2. Update `Latest Execution Summary`.
3. Update `Status` values only for tests executed.
4. Add new rows whenever a new automated test is added.
