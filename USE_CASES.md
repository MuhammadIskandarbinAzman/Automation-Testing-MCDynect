# USE_CASES

## Scope
This file documents currently automated use cases and their test mappings in this project.

## Current Test Inventory

| Use Case ID | Use Case Name | Actor | Status | Test File | Test Function |
|---|---|---|---|---|---|
| MCD-LCSE-02 | Access User Profile Settings | Licensee | AUTOMATED | `tests/licensee/test_licensee_update_profile.py` | `test_MCD_LCSE_02_update_profile_success` |
| MCD-LCSE-03 (Basic) | Logout of MCdynect (User Menu) | Licensee | AUTOMATED | `tests/licensee/test_licensee_logout_basic_path.py` | `test_MCD_LCSE_03_logout_basic_path_from_user_menu` |
| MCD-LCSE-03 (Alt) | Logout of MCdynect (Sidebar Shortcut) | Licensee | AUTOMATED | `tests/licensee/test_licensee_logout_alternative_path.py` | `test_MCD_LCSE_03_logout_alternative_path_from_sidebar` |
| MCD-LCSE-04 | Access Redeem Tab Shortcut | Licensee | AUTOMATED | `tests/licensee/test_licensee_redeem_shortcut.py` | `test_MCD_LCSE_04_access_redeemable_item_tab_shortcut` |
| MCD-LCSE-05 | Access Trade In Tab Page Shortcut | Licensee | AUTOMATED | `tests/licensee/test_licensee_trade_in_shortcut.py` | `test_MCD_LCSE_05_access_trade_in_tab_page_shortcut` |
| MCD-LCSE-06 | Switch Outlet Account | Licensee | AUTOMATED | `tests/licensee/test_licensee_switch_outlet_account.py` | `test_MCD_LCSE_06_switch_outlet_account` |
| MCD-LCSE-07 (Basic) | Modify Outlet Opening Day | Licensee | AUTOMATED | `tests/licensee/test_licensee_opening_day.py` | `test_MCD_LCSE_07_modify_outlet_opening_day` |
| MCD-LCSE-07 (E1) | Cancel Edit Opening Hours | Licensee | AUTOMATED | `tests/licensee/test_licensee_opening_day.py` | `test_MCD_LCSE_07_cancel_edit_opening_hours` |
| MCD-LCSE-08 | View All Announcement Listings and Details | Licensee | AUTOMATED | `tests/licensee/test_licensee_announcements.py` | `test_MCD_LCSE_08_view_all_announcement_listings_and_details` |
| MCD-LCSE-09 | View all Staff Directory | Licensee | AUTOMATED | `tests/licensee/test_licensee_staff_directory.py` | `test_MCD_LCSE_09_view_all_staff_directory` |
| MCD-LCSE-10 | Modify Staff Information | Licensee | AUTOMATED | `tests/licensee/test_licensee_modify_staff.py` | `test_MCD_LCSE_10_modify_staff_information` |
| MCD-LCSE-11 | Add Staff | Licensee | AUTOMATED | `tests/licensee/test_licensee_add_staff.py` | `test_MCD_LCSE_11_add_staff` |
| MCD-LCSE-12 | View All Licensee Activities Form Application | Licensee | AUTOMATED | `tests/licensee/test_licensee_activities_application.py` | `test_MCD_LCSE_12_view_licensee_activities_form_application` |
| MCD-LCSE-13 | Create Licensee Activities Form Application | Licensee | AUTOMATED | `tests/licensee/test_licensee_activities_application.py` | `test_MCD_LCSE_13_create_licensee_activities_form_application` |
| MCD-LCSE-14 | View Sales Dashboard | Licensee | AUTOMATED | `tests/licensee/test_licensee_sales_dashboard.py` | `test_MCD_LCSE_14_view_sales_dashboard` |
| MCD-LCSE-15 | Add Sales | Licensee | AUTOMATED | `tests/licensee/test_licensee_add_sales.py` | `test_MCD_LCSE_15_add_sales_open_form` |
| MCD-LCSE-16 | View Daily Sales Details | Licensee | AUTOMATED (DATA-DEPENDENT) | `tests/licensee/test_licensee_view_daily_sales_details.py` | `test_MCD_LCSE_16_view_daily_sales_details` |
| MCD-LCSE-17 | Edit Daily Sales Details | Licensee | AUTOMATED (DATA-DEPENDENT) | `tests/licensee/test_licensee_edit_daily_sales_details.py` | `test_MCD_LCSE_17_edit_daily_sales_details_open_form` |
| N/A | Licensee Login Success | Licensee | AUTOMATED | `tests/licensee/test_login_licensee.py` | `test_licensee_can_log_in` |
| N/A | Licensee Login Failure (Invalid Credentials) | Licensee | AUTOMATED | `tests/licensee/test_login_licensee.py` | `test_licensee_cannot_log_in_with_invalid_credentials` |
| N/A | Role Login Success | Area Manager | AUTOMATED | `tests/test_login_area_manager.py` | `test_area_manager_can_log_in` |
| N/A | Role Login Success | Inventory | AUTOMATED | `tests/test_login_inventory.py` | `test_inventory_can_log_in` |
| N/A | Role Login Success | Procurement | AUTOMATED | `tests/test_login_procurement.py` | `test_procurement_can_log_in` |
| N/A | Role Login Success | Production | AUTOMATED | `tests/test_login_production.py` | `test_production_can_log_in` |
| N/A | Role Login Success | Licensing | AUTOMATED | `tests/test_login_licensing.py` | `test_licensing_can_log_in` |
| N/A | Role Login Success | Compliance | AUTOMATED | `tests/test_login_compliance.py` | `test_compliance_can_log_in` |
| N/A | Role Login Success | Finance | AUTOMATED | `tests/test_login_finance.py` | `test_finance_can_log_in` |

## Notes By Use Case

### MCD-LCSE-02
- Covers profile update flow via settings/profile page.
- Test restores modified value at end.

### MCD-LCSE-03
- Split into two independent tests: user-menu path and sidebar shortcut path.

### MCD-LCSE-04
- Validates `Redeem` dashboard shortcut redirects to `order/index?tab=redeemable`.

### MCD-LCSE-05
- Validates `Trade In` dashboard shortcut redirects to `licensee/trade-in`.

### MCD-LCSE-06
- Handles optional `Maybe Later` popup.
- Uses dedicated credentials in the test for stable outlet-switch coverage.

### MCD-LCSE-07
- Basic path test toggles Open/Closed status and reverts to original state.
- Exception path test validates Cancel behavior for edit opening-hours modal.

### MCD-LCSE-08
- Validates navigation to announcement listing page.
- Validates opening an announcement detail in a new browser tab.

### MCD-LCSE-09
- Validates navigation from dashboard staff card to full staff directory page.

### MCD-LCSE-10
- Uses dedicated credentials in the test.
- Modifies staff name and reverts it in same test for data stability.
- Fills start date when required by form validation.

### MCD-LCSE-14
- Validates navigation to Sales page from sidebar.
- Verifies Daily Sales and Extra Sets tabs are accessible.
- Verifies key listing headers in Daily Sales tab.

### MCD-LCSE-15
- Validates navigation from Sales page to Add sale page.
- Verifies all key sales input fields are visible.
- Kept non-destructive (does not submit sales record).

### MCD-LCSE-16
- Attempts to open details from a keyed-in daily sales row (not `Not filled`).
- Data-dependent: test skips when no navigable keyed-in sales record exists in current environment.

### MCD-LCSE-17
- Attempts to open Sales Details and then click `Edit`.
- Verifies Edit Sales form fields and `Update Sale` button are visible.
- Data-dependent: skips when listing cannot navigate to details or selected record has no edit action.

## Template For New Use Cases

### Use Case ID
`MCD-XXXX-00`

### Use Case Name
`<Name>`

### Actor
`<Role>`

### Pre-Condition
- `<Condition 1>`

### Basic Path
1. `<Step 1>`
2. `<Step 2>`

### Expected Result
- `<Expected behavior>`

### Automation Mapping
- Status: `PLANNED`
- Test file: `<tests/...py>`
- Test function: `<test_function_name>`
- Notes: `<selectors/data constraints>`
