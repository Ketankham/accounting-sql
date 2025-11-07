# Active Status Filtering - Implementation Guide

## Overview

All dropdown menus and foreign key selections throughout the application now filter to show **ONLY Active records**. This ensures users cannot select inactive/disabled entries when creating or editing data.

---

## What Changed

### All Handlers Now Have `get_active_*` Methods

Every handler that manages entities with a `status` field now has TWO methods:

1. **`get_all_*`** - Returns ALL records (Active + Inactive) - Used for management screens
2. **`get_active_*`** - Returns ONLY Active records - Used for dropdowns/foreign key selection

---

## Updated Handlers

### 1. Account Group Handler
**File:** `database/account_group_handler.py`

```python
# Get ALL account groups (for management screen)
account_groups = handler.get_all_account_groups()
# Returns: Active + Inactive groups

# Get ONLY ACTIVE account groups (for dropdowns)
active_groups = handler.get_active_account_groups()
# Returns: Only Active groups
```

### 2. City Handler
**File:** `database/city_handler.py`

```python
# All cities
cities = handler.get_all_cities()

# Only active cities (for forms)
active_cities = handler.get_active_cities()
```

### 3. State Handler
**File:** `database/state_handler.py`

```python
# All states
states = handler.get_all_states()

# Only active states (for forms)
active_states = handler.get_active_states()
```

### 4. Item Group Handler
**File:** `database/item_group_handler.py`

```python
# All item groups
item_groups = handler.get_all_item_groups()

# Only active item groups (for forms)
active_groups = handler.get_active_item_groups()
```

### 5. Item Company Handler
**File:** `database/item_company_handler.py`

```python
# All item companies
companies = handler.get_all_item_companies()

# Only active item companies (for forms)
active_companies = handler.get_active_item_companies()
```

### 6. UoM Handler
**File:** `database/uom_handler.py`

```python
# All units of measure
uoms = handler.get_all_uoms()

# Only active UoMs (for forms)
active_uoms = handler.get_active_uoms()
```

### 7. Business Partner Handler
**File:** `database/business_partner_handler.py`

```python
# All business partners
partners = handler.get_all_business_partners()

# Only active business partners (for forms)
active_partners = handler.get_active_business_partners()
```

### 8. Account Master Handler
**File:** `database/account_master_handler.py`

```python
# All accounts
accounts = handler.get_all_accounts()

# Only active accounts (for forms)
active_accounts = handler.get_active_accounts()
```

---

## How To Use In Forms

### Example 1: Populating a Dropdown

**BEFORE (Wrong - shows inactive records):**
```python
from database.account_group_handler import AccountGroupHandler

# Populate dropdown
ag_handler = AccountGroupHandler()
ag_handler.connect()

# ❌ BAD - Shows ALL groups including inactive ones
account_groups = ag_handler.get_all_account_groups()

dropdown_values = [f"{ag['ag_code']} - {ag['name']}" for ag in account_groups]
combo_box['values'] = dropdown_values

ag_handler.disconnect()
```

**AFTER (Correct - shows only active records):**
```python
from database.account_group_handler import AccountGroupHandler

# Populate dropdown
ag_handler = AccountGroupHandler()
ag_handler.connect()

# ✅ GOOD - Shows ONLY active groups
account_groups = ag_handler.get_active_account_groups()

dropdown_values = [f"{ag['ag_code']} - {ag['name']}" for ag in account_groups]
combo_box['values'] = dropdown_values

ag_handler.disconnect()
```

### Example 2: Business Partner Form

**File:** `business_partner_form.py`

```python
def populate_dropdowns(self):
    """Populate all dropdowns with ACTIVE records only"""

    # Cities dropdown - only active cities
    city_handler = CityHandler()
    city_handler.connect()
    active_cities = city_handler.get_active_cities()  # ✅ Only active
    self.city_combo['values'] = [c['city_name'] for c in active_cities]
    city_handler.disconnect()

    # States dropdown - only active states
    state_handler = StateHandler()
    state_handler.connect()
    active_states = state_handler.get_active_states()  # ✅ Only active
    self.state_combo['values'] = [s['state_name'] for c in active_states]
    state_handler.disconnect()

    # Account groups - only active groups
    ag_handler = AccountGroupHandler()
    ag_handler.connect()
    active_groups = ag_handler.get_active_account_groups()  # ✅ Only active
    self.account_group_combo['values'] = [g['name'] for g in active_groups]
    ag_handler.disconnect()
```

### Example 3: Transaction Entry Form

**File:** `journal_entry_form.py`

```python
def load_accounts_dropdown(self):
    """Load active accounts for journal entry"""

    am_handler = AccountMasterHandler()
    am_handler.connect()

    # ✅ Get ONLY active accounts
    active_accounts = am_handler.get_active_accounts()

    # Create dropdown values
    account_options = [
        f"{acc['account_code']} - {acc['account_name']}"
        for acc in active_accounts
    ]

    self.debit_account_combo['values'] = account_options
    self.credit_account_combo['values'] = account_options

    am_handler.disconnect()
```

---

## Management Screens vs Entry Forms

### Management Screens
**Purpose:** View, edit, and manage ALL records (including inactive ones)

**Use:** `get_all_*()` methods

**Example:** Account Group Management screen shows all groups (Active + Inactive) so admins can reactivate or delete them.

```python
# In account_group_management.py
def load_records(self):
    handler = AccountGroupHandler()
    handler.connect()

    # ✅ Management screen - show ALL records
    all_groups = handler.get_all_account_groups()

    self.populate_table(all_groups)
    handler.disconnect()
```

### Entry/Transaction Forms
**Purpose:** Create new transactions or records with valid active references

**Use:** `get_active_*()` methods

**Example:** Business Partner form only shows active cities when user selects city.

```python
# In business_partner_form.py
def populate_city_dropdown(self):
    handler = CityHandler()
    handler.connect()

    # ✅ Entry form - show ONLY active records
    active_cities = handler.get_active_cities()

    self.city_combo['values'] = [c['city_name'] for c in active_cities]
    handler.disconnect()
```

---

## Implementation Checklist

When creating a new form with dropdowns:

- [ ] Identify all dropdowns that reference other entities
- [ ] Use `get_active_*()` methods for dropdown population
- [ ] NEVER use `get_all_*()` in entry/transaction forms
- [ ] Test by making a record Inactive and verifying it doesn't appear in dropdown
- [ ] Document which fields use active filtering in form comments

---

## SQL Queries

All `get_active_*` methods use this WHERE clause:

```sql
WHERE status = 'Active'
```

### Simple Example (City):
```sql
SELECT id, city_code, city_name, status, created_at
FROM cities
WHERE status = 'Active'
ORDER BY city_name ASC
```

### Complex Example (Business Partner with joins):
```sql
SELECT
    bp.id,
    bp.bp_code,
    bp.bp_name,
    bp.city_id,
    c.name as city_name,
    bp.status
FROM business_partners bp
LEFT JOIN cities c ON bp.city_id = c.id
WHERE bp.status = 'Active'  -- Filters business partners
ORDER BY bp.bp_name ASC
```

**Note:** The WHERE clause filters the main table (business_partners), NOT the joined tables (cities). If you want to also filter joined tables, add additional conditions:

```sql
WHERE bp.status = 'Active'
  AND (c.id IS NULL OR c.status = 'Active')  -- Also filter cities
```

---

## Benefits

1. **Data Integrity** - Users cannot create records referencing inactive entries
2. **Clean UX** - Dropdowns only show relevant, active options
3. **Consistency** - Same pattern across all modules
4. **Audit Trail** - Inactive records remain in database for historical reference
5. **Easy Reactivation** - Admins can reactivate records from management screens

---

## Testing

### Test Scenario 1: Dropdown Filtering
1. Open City Master management screen
2. Create a new city "Test City" with status=Active
3. Open Business Partner form
4. Verify "Test City" appears in city dropdown
5. Go back to City Master
6. Change "Test City" status to Inactive
7. Go back to Business Partner form
8. Refresh/reopen form
9. ✅ Verify "Test City" does NOT appear in dropdown anymore

### Test Scenario 2: Existing Records
1. Create a Business Partner with City = "Mumbai" (Active)
2. Mark "Mumbai" as Inactive in City Master
3. Edit the existing Business Partner
4. ✅ The form should still show "Mumbai" for existing record
5. ✅ But "Mumbai" should NOT appear in dropdown for new partners

---

## Troubleshooting

### Problem: Inactive records still appearing in dropdown

**Cause:** Form is using `get_all_*()` instead of `get_active_*()`

**Fix:**
```python
# Change this:
records = handler.get_all_records()

# To this:
records = handler.get_active_records()
```

### Problem: Can't find records in dropdown

**Cause:** Records are marked Inactive

**Solution:**
1. Go to management screen
2. Check status column
3. Change status to Active
4. Record will now appear in dropdowns

### Problem: Form crashes when loading dropdown

**Cause:** Handler method doesn't exist

**Fix:** Ensure all handlers have `get_active_*` methods. Check:
- account_group_handler.py
- city_handler.py
- state_handler.py
- item_group_handler.py
- item_company_handler.py
- uom_handler.py
- business_partner_handler.py
- account_master_handler.py

---

## Future Enhancements

### 1. Global Active Filter Toggle
Add a checkbox in management screens: "Show Inactive Records"

```python
def load_records(self, show_inactive=False):
    handler = AccountGroupHandler()
    handler.connect()

    if show_inactive:
        records = handler.get_all_account_groups()
    else:
        records = handler.get_active_account_groups()

    self.populate_table(records)
    handler.disconnect()
```

### 2. Cascade Filtering
When selecting Account Group, filter Account Types to those used by active Account Groups.

### 3. Warning on Deactivation
Before marking a record Inactive, check if it's used in any Active parent records:

```python
def before_deactivate(self, city_id):
    # Check if any active business partners use this city
    active_bp_count = count_active_business_partners_with_city(city_id)

    if active_bp_count > 0:
        show_warning(f"{active_bp_count} active Business Partners use this city.
                      Deactivating will hide it from new entries.")
```

---

## Summary

✅ **ALL handlers updated** with `get_active_*` methods
✅ **Consistent pattern** across the application
✅ **Next step:** Update all forms to use active filtering

**Key Rule:**
- Management screens: `get_all_*()`
- Entry/Transaction forms: `get_active_*()`

---

**Last Updated:** 2025-11-06
**Updated By:** Claude Code Assistant
