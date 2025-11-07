# Account Group Code - User Entry Implementation

## Summary

Changed the Account Group (AG) Code from auto-generated to **user-entered** with strict validation.

---

## Changes Made

### 1. Form Changes - [account_group_form.py](account_group_form.py)

#### New Field Type: `create_ag_code_field()`
- **2-character limit** - Maximum 2 characters allowed
- **Alphanumeric only** - Letters A-Z and numbers 0-9
- **Auto-uppercase** - Automatically converts to uppercase
- **Real-time validation** - Prevents invalid characters as you type
- **Required field** - Must be filled before saving

#### Field Behavior:
- **Create Mode:** User enters AG Code (editable, required)
- **Edit Mode:** AG Code shown as read-only (cannot be changed after creation)

#### Validation:
```python
# Frontend validation (as you type):
- Max 2 characters
- Only alphanumeric (A-Z, 0-9)
- Auto-uppercase

# Form submission validation:
- Must be exactly 2 characters
- Must be alphanumeric
- Cannot be empty
```

#### Helper Text Added:
```
"2 characters max, alphanumeric only (e.g., SA, PU, AS)"
```

### 2. Handler Changes - [account_group_handler.py](database/account_group_handler.py:196-244)

#### Updated `create_account_group()` method:

**Before:**
- Auto-generated AG code from name + type
- Complex generation logic

**After:**
- Uses user-entered AG code from form
- Server-side validation
- Duplicate checking

#### Validation Rules:
```python
1. AG Code is required (not null/empty)
2. Must be exactly 2 characters
3. Must be alphanumeric only
4. Must be unique (no duplicates)
5. Auto-converted to uppercase
```

#### Error Messages:
- "AG Code is required"
- "AG Code must be exactly 2 characters"
- "AG Code must be alphanumeric only"
- "AG Code 'XX' already exists. Please choose a different code."

---

## User Experience

### Creating a New Account Group

**Step 1:** Fill in Name
```
Name: Sales
```

**Step 2:** Select Account Group Type
```
Account Group Type: P&L Account
```

**Step 3:** Enter AG Code (NEW)
```
AG Code: SA
```
- Type only 2 characters
- Only letters/numbers allowed
- Automatically converts to uppercase
- Shows helper text below field

**Step 4:** Select Status
```
Status: Active
```

**Step 5:** Click "Create Account Group"
- Validates AG Code format
- Checks for duplicates
- Creates record if valid

### Editing Existing Account Group

When editing an existing record:
- AG Code field is **read-only** (grayed out)
- Cannot change AG Code after creation
- Can only update Name, Account Group Type, Status

---

## Examples

### Valid AG Codes:
- `SA` - Sales
- `PU` - Purchase
- `AS` - Assets
- `LI` - Liabilities
- `SG` - Sales Group
- `01` - Numeric
- `A1` - Alphanumeric mix

### Invalid AG Codes:
- `S` - Too short (1 character)
- `SAL` - Too long (3 characters)
- `S-A` - Contains special character (-)
- `S A` - Contains space
- `s@` - Contains special character (@)

---

## Technical Implementation Details

### Form Field Creation (Create Mode):
```python
# In account_group_form.py
self.create_ag_code_field(form_container, "AG Code", "ag_code",
                         required=True, row=current_row)
```

### Real-time Validation:
```python
def validate_ag_code(action, value_if_allowed):
    if action == '1':  # Insert
        # Only allow alphanumeric characters
        if not value_if_allowed.isalnum():
            return False
        # Limit to 2 characters
        return len(value_if_allowed) <= 2
    return True
```

### Auto-uppercase:
```python
def to_uppercase(*_args):
    var.set(var.get().upper())
var.trace_add('write', to_uppercase)
```

### Form Validation (on save):
```python
if field_info['type'] == 'ag_code' and value:
    if len(value) < 2:
        errors.append("AG Code must be exactly 2 characters")
    elif not value.isalnum():
        errors.append("AG Code must be alphanumeric only")
```

### Handler Validation:
```python
# In account_group_handler.py - create_account_group()
ag_code = account_group_data.get('ag_code', '').strip().upper()

if not ag_code:
    return False, "AG Code is required", None

if len(ag_code) != 2:
    return False, "AG Code must be exactly 2 characters", None

if not ag_code.isalnum():
    return False, "AG Code must be alphanumeric only", None

if self.get_account_group_by_code(ag_code):
    return False, f"AG Code '{ag_code}' already exists...", None
```

---

## Database

### Table Structure (No changes needed):
```sql
CREATE TABLE account_groups (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    account_group_type TEXT NOT NULL,
    status TEXT DEFAULT 'Active',
    ag_code TEXT NOT NULL UNIQUE,  -- Already has UNIQUE constraint
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

The `UNIQUE` constraint on `ag_code` ensures no duplicates at database level.

---

## Migration Notes

### Existing Records:
- Existing AG codes (auto-generated) remain unchanged
- They may be longer than 2 characters (e.g., "SAL001")
- Can continue to be used
- Only NEW records require 2-character codes

### If You Want to Update Existing Records:
1. Go to Account Group Management screen
2. View existing AG codes
3. Manually edit if needed (AG code is read-only in edit mode by design)
4. To allow editing existing AG codes, remove read-only restriction temporarily

---

## Testing

### Test Case 1: Valid AG Code
1. Create new Account Group
2. Enter Name: "Sales"
3. Select Type: "P&L Account"
4. Enter AG Code: "SA"
5. Status: Active
6. Click Create
7. ✅ Should succeed with message: "Account Group created successfully (AG Code: SA)"

### Test Case 2: Duplicate AG Code
1. Create first Account Group with AG Code: "SA"
2. Try to create second Account Group with AG Code: "SA"
3. ✅ Should fail with error: "AG Code 'SA' already exists. Please choose a different code."

### Test Case 3: Invalid Length (1 char)
1. Create new Account Group
2. Enter AG Code: "S"
3. Click Create
4. ✅ Should fail with error: "AG Code must be exactly 2 characters"

### Test Case 4: Invalid Length (3+ chars)
1. Try to type "SAL" in AG Code field
2. ✅ Field should only accept "SA" (2 chars max)
3. Cannot type more than 2 characters

### Test Case 5: Special Characters
1. Try to type "S-" or "S@" in AG Code field
2. ✅ Special characters should be rejected
3. Only alphanumeric allowed

### Test Case 6: Auto-uppercase
1. Type "sa" in AG Code field
2. ✅ Should automatically convert to "SA"

### Test Case 7: Edit Mode Read-only
1. Create Account Group with AG Code "SA"
2. Edit the same Account Group
3. ✅ AG Code field should be read-only (grayed out)
4. Cannot modify AG Code

---

## Benefits

1. **Standardization** - All AG codes are exactly 2 characters
2. **Consistency** - Uniform format across all records
3. **User Control** - Users choose meaningful codes
4. **Simplicity** - Shorter codes are easier to remember (SA, PU, AS)
5. **Validation** - Multiple layers prevent invalid data

---

## Removed Features

### ~~Auto-generation Logic~~
The `generate_ag_code()` method in handler is no longer used for new records:
```python
# DEPRECATED (for new records)
def generate_ag_code(self, name, account_group_type):
    # This method is kept for backward compatibility
    # but not used for new records
    pass
```

### ~~Info Text~~
Removed auto-generation info message:
```python
# REMOVED
"ℹ AG Code will be auto-generated based on Name and Account Group Type"
```

Replaced with:
```python
"2 characters max, alphanumeric only (e.g., SA, PU, AS)"
```

---

## Files Modified

1. **[account_group_form.py](account_group_form.py)**
   - Added `create_ag_code_field()` method
   - Updated field layout (AG Code before Status)
   - Updated validation logic
   - Updated `get_form_data()` to include ag_code type
   - Updated `load_account_group_data()` for ag_code type

2. **[database/account_group_handler.py](database/account_group_handler.py)**
   - Updated `create_account_group()` to use user-entered code
   - Added server-side validation
   - Added duplicate checking with custom error message

---

**Last Updated:** 2025-11-06
**Change Type:** Feature Enhancement
**Status:** ✅ Complete
