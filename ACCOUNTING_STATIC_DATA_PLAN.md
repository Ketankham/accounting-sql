# Accounting Static Data Architecture Plan

## Overview

This document outlines the architecture for managing static reference data (Book Codes, Account Types) in the accounting system.

## Reference Data Tables

### 1. Book Codes Table

**Purpose:** Define the different books/journals used in accounting

```sql
CREATE TABLE book_codes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code TEXT NOT NULL UNIQUE,  -- Short code (e.g., "CASH", "BANK")
    book_number INTEGER NOT NULL UNIQUE,  -- Display number (1-6)
    name TEXT NOT NULL,  -- Display name (e.g., "Cash Book")
    description TEXT,  -- Detailed description
    is_active INTEGER DEFAULT 1,  -- 1 = Active, 0 = Inactive
    sort_order INTEGER,  -- For display ordering
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Initial Data:**
```
1 | CASH      | 1 | Cash Book      | Cash transactions
2 | BANK      | 2 | Bank Book      | Bank transactions
3 | LEDGER    | 3 | Ledger Book    | General ledger entries
4 | SALE      | 4 | Sales Book     | Sales transactions
5 | PURCHASE  | 5 | Purchase Book  | Purchase transactions
6 | CREDITNOTE| 6 | Credit Note    | Credit note entries
```

### 2. Account Types Table

**Purpose:** Define account classifications for chart of accounts

```sql
CREATE TABLE account_types (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code TEXT NOT NULL UNIQUE,  -- Single letter code (A, L, D, C, S, P, E, R)
    name TEXT NOT NULL,  -- Full name (Assets, Liability, etc.)
    description TEXT,  -- Detailed description
    category TEXT,  -- Grouping: "balance_sheet" or "profit_loss"
    nature TEXT,  -- "debit" or "credit"
    is_active INTEGER DEFAULT 1,
    sort_order INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Initial Data:**
```
1 | A | Assets     | Asset accounts         | balance_sheet | debit  | 1
2 | L | Liability  | Liability accounts     | balance_sheet | credit | 2
3 | D | Debtors    | Accounts receivable    | balance_sheet | debit  | 3
4 | C | Creditors  | Accounts payable       | balance_sheet | credit | 4
5 | S | Sale       | Sales/Revenue          | profit_loss   | credit | 5
6 | P | Purchase   | Purchase/COGS          | profit_loss   | debit  | 6
7 | E | Expenses   | Operating expenses     | profit_loss   | debit  | 7
8 | R | Revenue    | Other income/revenue   | profit_loss   | credit | 8
```

## Why Database Tables? (vs Enums or Constants)

### ✅ Advantages:

1. **Foreign Key Constraints**
   - Ensures data integrity
   - Prevents invalid references
   - Example: `accounts` table references `account_types.id`

2. **Rich Metadata**
   - Can store descriptions, categories, business rules
   - Can add fields without code changes

3. **Easy Maintenance**
   - Update in one place
   - No application redeployment needed for data changes

4. **Query Flexibility**
   - Easy JOIN operations
   - Better reporting queries

5. **Dropdown Population**
   - Forms automatically populate from database
   - Always up-to-date

6. **Audit Trail**
   - Can track when added/modified
   - Can soft-delete (is_active flag)

### ❌ Alternative Approaches (and why we're not using them):

**1. Python Enums/Constants**
```python
# DON'T DO THIS
class BookCode(Enum):
    CASH = 1
    BANK = 2
```
❌ Hard to change without redeployment
❌ No database validation
❌ Harder to query/report

**2. String Values Only**
```sql
-- DON'T DO THIS
account_type TEXT CHECK(account_type IN ('A', 'L', 'D', ...))
```
❌ No metadata (descriptions, categories)
❌ Harder to maintain
❌ Repetitive constraint definitions

## Usage Examples

### Example 1: Accounts Table

```sql
CREATE TABLE accounts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    account_code TEXT NOT NULL UNIQUE,
    account_name TEXT NOT NULL,
    account_type_id INTEGER NOT NULL,  -- Foreign key to account_types
    book_code_id INTEGER,  -- Optional foreign key to book_codes
    opening_balance REAL DEFAULT 0,
    current_balance REAL DEFAULT 0,
    status TEXT DEFAULT 'Active',
    FOREIGN KEY (account_type_id) REFERENCES account_types(id),
    FOREIGN KEY (book_code_id) REFERENCES book_codes(id)
);
```

### Example 2: Transactions Table

```sql
CREATE TABLE transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    transaction_number TEXT NOT NULL UNIQUE,
    book_code_id INTEGER NOT NULL,  -- Which book is this transaction in?
    transaction_date DATE NOT NULL,
    amount REAL NOT NULL,
    narration TEXT,
    FOREIGN KEY (book_code_id) REFERENCES book_codes(id)
);
```

### Example 3: Queries with JOINs

```sql
-- Get all asset accounts with their type name
SELECT
    a.account_code,
    a.account_name,
    at.name as account_type_name,
    at.category,
    a.current_balance
FROM accounts a
JOIN account_types at ON a.account_type_id = at.id
WHERE at.code = 'A'
ORDER BY a.account_code;

-- Get transactions grouped by book
SELECT
    bc.name as book_name,
    COUNT(*) as transaction_count,
    SUM(t.amount) as total_amount
FROM transactions t
JOIN book_codes bc ON t.book_code_id = bc.id
GROUP BY bc.id, bc.name
ORDER BY bc.book_number;
```

## Python Handler Pattern

### Handler Structure

```python
class StaticDataHandler:
    """Manages static reference data (Book Codes, Account Types)"""

    def __init__(self):
        self.conn = None
        self.cursor = None

    def connect(self):
        """Establish database connection"""
        self.conn = sqlite3.connect(DB_PATH)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()

        # Create tables on first connection
        self._create_book_codes_table()
        self._create_account_types_table()

        # Seed initial data if tables are empty
        self._seed_book_codes()
        self._seed_account_types()

    # Methods for book codes
    def get_all_book_codes(self):
        """Get all active book codes"""

    def get_book_code_by_id(self, book_code_id):
        """Get single book code"""

    def get_book_code_by_code(self, code):
        """Get book code by code string"""

    # Methods for account types
    def get_all_account_types(self):
        """Get all active account types"""

    def get_account_types_by_category(self, category):
        """Get account types filtered by category"""
```

## Benefits for Your Accounting System

### 1. Data Consistency
- All modules reference same data
- No duplicate definitions
- Single source of truth

### 2. Validation
- Database enforces valid references
- Foreign keys prevent orphaned records
- CHECK constraints for business rules

### 3. Reporting & Analytics
- Easy to generate financial reports
- Can filter/group by account type
- Can track transactions by book

### 4. User Experience
- Dropdowns auto-populate from database
- Consistent naming everywhere
- Easy to add new types without code changes

### 5. Scalability
- Can add custom account types per company
- Can add regional variations
- Can track historical changes

## Implementation Steps

### Phase 1: Database Setup
1. ✅ Create `book_codes` table
2. ✅ Create `account_types` table
3. ✅ Seed initial data
4. ✅ Create StaticDataHandler

### Phase 2: Integration
1. Update existing tables to use foreign keys
2. Update forms to use dropdowns from database
3. Update validation logic
4. Migrate any hardcoded values

### Phase 3: Testing
1. Test CRUD operations
2. Test foreign key constraints
3. Test form dropdowns
4. Test reporting queries

## Migration Strategy

If you already have data with hardcoded values:

```python
# Migration script to convert string codes to foreign keys
def migrate_account_type_codes():
    """Convert account_type string codes to foreign key IDs"""

    # Create mapping
    type_map = {
        'A': 1, 'L': 2, 'D': 3, 'C': 4,
        'S': 5, 'P': 6, 'E': 7, 'R': 8
    }

    # Update existing records
    for old_code, new_id in type_map.items():
        cursor.execute(
            "UPDATE accounts SET account_type_id = ? WHERE account_type = ?",
            (new_id, old_code)
        )
```

## Conclusion

**Recommendation:** Use database tables for all static reference data.

This approach provides:
- ✅ Maximum flexibility
- ✅ Best data integrity
- ✅ Easiest maintenance
- ✅ Best user experience
- ✅ Future-proof architecture

The slight overhead of JOINs is negligible compared to the benefits, especially since this is static data that can be cached if needed.

---

**Next Steps:**
1. Review and approve this architecture
2. Implement StaticDataHandler
3. Create seed data scripts
4. Update app_plan.json with new entities
5. Generate CRUD interfaces if needed
