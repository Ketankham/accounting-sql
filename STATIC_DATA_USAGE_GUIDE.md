# Static Data Usage Guide

Quick reference for using Book Codes and Account Types in your accounting system.

## 📚 Overview

Two static reference tables are now available:
1. **Book Codes** - 6 accounting books (Cash, Bank, Ledger, Sale, Purchase, Credit Note)
2. **Account Types** - 8 account classifications (Assets, Liability, Debtors, Creditors, Sale, Purchase, Expenses, Revenue)

## 🚀 Quick Start

### Import the Handler

```python
from database.static_data_handler import StaticDataHandler

# Initialize
static_handler = StaticDataHandler()
static_handler.connect()

# Use the data
book_codes = static_handler.get_all_book_codes()
account_types = static_handler.get_all_account_types()

# Clean up
static_handler.disconnect()
```

## 📖 Book Codes Reference

| Number | Code | Name | Description |
|--------|------|------|-------------|
| 1 | CASH | Cash Book | Cash transactions and petty cash |
| 2 | BANK | Bank Book | Bank transactions and reconciliation |
| 3 | LEDGER | Ledger Book | General ledger entries |
| 4 | SALE | Sales Book | Sales transactions and invoices |
| 5 | PURCHASE | Purchase Book | Purchase transactions and bills |
| 6 | CREDITNOTE | Credit Note | Credit note entries |

### Usage Examples

```python
# Get all book codes
book_codes = static_handler.get_all_book_codes()
# Returns: [{'id': 1, 'code': 'CASH', 'name': 'Cash Book', ...}, ...]

# Get specific book code by code
cash_book = static_handler.get_book_code_by_code('CASH')
# Returns: {'id': 1, 'code': 'CASH', 'book_number': 1, 'name': 'Cash Book', ...}

# Get specific book code by number
bank_book = static_handler.get_book_code_by_number(2)
# Returns: {'id': 2, 'code': 'BANK', 'book_number': 2, 'name': 'Bank Book', ...}

# For dropdown/combobox (returns formatted list)
dropdown_data = static_handler.get_book_codes_for_dropdown()
# Returns: [(1, '1. Cash Book'), (2, '2. Bank Book'), ...]
```

## 💼 Account Types Reference

| Code | Name | Category | Nature | Description |
|------|------|----------|--------|-------------|
| A | Assets | balance_sheet | debit | Asset accounts (cash, inventory, etc.) |
| L | Liability | balance_sheet | credit | Liability accounts (loans, payables) |
| D | Debtors | balance_sheet | debit | Accounts receivable / Sundry debtors |
| C | Creditors | balance_sheet | credit | Accounts payable / Sundry creditors |
| S | Sale | profit_loss | credit | Sales and revenue accounts |
| P | Purchase | profit_loss | debit | Purchase and cost of goods sold |
| E | Expenses | profit_loss | debit | Operating expenses and costs |
| R | Revenue | profit_loss | credit | Other income and revenue |

### Usage Examples

```python
# Get all account types
account_types = static_handler.get_all_account_types()
# Returns: [{'id': 1, 'code': 'A', 'name': 'Assets', ...}, ...]

# Get specific account type by code
assets = static_handler.get_account_type_by_code('A')
# Returns: {'id': 1, 'code': 'A', 'name': 'Assets', 'category': 'balance_sheet', ...}

# Get account types by category
balance_sheet_types = static_handler.get_account_types_by_category('balance_sheet')
# Returns: [Assets, Liability, Debtors, Creditors]

profit_loss_types = static_handler.get_account_types_by_category('profit_loss')
# Returns: [Sale, Purchase, Expenses, Revenue]

# Get account types by nature
debit_types = static_handler.get_account_types_by_nature('debit')
# Returns: [Assets, Debtors, Purchase, Expenses]

credit_types = static_handler.get_account_types_by_nature('credit')
# Returns: [Liability, Creditors, Sale, Revenue]

# For dropdown/combobox
dropdown_data = static_handler.get_account_types_for_dropdown()
# Returns: [(1, 'A - Assets'), (2, 'L - Liability'), ...]
```

## 🔗 Using with Other Tables

### Example 1: Accounts Table

```python
# Create accounts table with foreign key to account_types
CREATE TABLE accounts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    account_code TEXT NOT NULL UNIQUE,
    account_name TEXT NOT NULL,
    account_type_id INTEGER NOT NULL,  -- Foreign key!
    book_code_id INTEGER,
    opening_balance REAL DEFAULT 0,
    current_balance REAL DEFAULT 0,
    FOREIGN KEY (account_type_id) REFERENCES account_types(id),
    FOREIGN KEY (book_code_id) REFERENCES book_codes(id)
);

# Python usage
def create_account(account_code, account_name, account_type_code):
    # Get account type ID from code
    account_type = static_handler.get_account_type_by_code(account_type_code)

    if account_type:
        account_handler.create_account({
            'account_code': account_code,
            'account_name': account_name,
            'account_type_id': account_type['id']  # Use ID!
        })
```

### Example 2: Transactions Table

```python
# Create transactions table with foreign key to book_codes
CREATE TABLE transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    transaction_number TEXT NOT NULL UNIQUE,
    book_code_id INTEGER NOT NULL,  -- Foreign key!
    transaction_date DATE NOT NULL,
    amount REAL NOT NULL,
    FOREIGN KEY (book_code_id) REFERENCES book_codes(id)
);

# Python usage
def create_transaction(trans_no, book_code, date, amount):
    # Get book code ID
    book = static_handler.get_book_code_by_code(book_code)

    if book:
        transaction_handler.create_transaction({
            'transaction_number': trans_no,
            'book_code_id': book['id'],  # Use ID!
            'transaction_date': date,
            'amount': amount
        })
```

### Example 3: Query with JOIN

```python
# Get all accounts with their account type names
query = """
    SELECT
        a.account_code,
        a.account_name,
        at.code as type_code,
        at.name as type_name,
        at.category,
        a.current_balance
    FROM accounts a
    JOIN account_types at ON a.account_type_id = at.id
    WHERE at.category = 'balance_sheet'
    ORDER BY at.sort_order, a.account_code
"""

# Get transactions grouped by book
query = """
    SELECT
        bc.book_number,
        bc.name as book_name,
        COUNT(*) as transaction_count,
        SUM(t.amount) as total_amount
    FROM transactions t
    JOIN book_codes bc ON t.book_code_id = bc.id
    GROUP BY bc.id
    ORDER BY bc.book_number
"""
```

## 🎨 Using in Tkinter Forms

### Example: Dropdown for Account Type

```python
from tkinter import ttk
from database.static_data_handler import StaticDataHandler

class AccountForm(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # Get static data
        static_handler = StaticDataHandler()
        static_handler.connect()

        # Get account types for dropdown
        account_types = static_handler.get_account_types_for_dropdown()

        # Create dropdown
        self.account_type_var = tk.StringVar()
        self.account_type_combo = ttk.Combobox(
            self,
            textvariable=self.account_type_var,
            values=[at[1] for at in account_types],  # Display names
            state="readonly"
        )

        # Store ID mapping for later use
        self.account_type_map = {at[1]: at[0] for at in account_types}

        static_handler.disconnect()

    def get_selected_account_type_id(self):
        """Get the ID of selected account type"""
        selected_name = self.account_type_var.get()
        return self.account_type_map.get(selected_name)
```

### Example: Dropdown for Book Code

```python
class TransactionForm(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # Get static data
        static_handler = StaticDataHandler()
        static_handler.connect()

        # Get book codes for dropdown
        book_codes = static_handler.get_book_codes_for_dropdown()

        # Create dropdown
        self.book_code_var = tk.StringVar()
        self.book_code_combo = ttk.Combobox(
            self,
            textvariable=self.book_code_var,
            values=[bc[1] for bc in book_codes],  # "1. Cash Book", etc.
            state="readonly"
        )

        # Store ID mapping
        self.book_code_map = {bc[1]: bc[0] for bc in book_codes}

        static_handler.disconnect()

    def get_selected_book_code_id(self):
        """Get the ID of selected book code"""
        selected_name = self.book_code_var.get()
        return self.book_code_map.get(selected_name)
```

## 🔍 Querying and Filtering

### Financial Reports

```python
# Get all balance sheet accounts
balance_sheet_types = static_handler.get_account_types_by_category('balance_sheet')
balance_sheet_ids = [at['id'] for at in balance_sheet_types]

query = """
    SELECT * FROM accounts
    WHERE account_type_id IN ({})
""".format(','.join('?' * len(balance_sheet_ids)))

# Get all profit & loss accounts
profit_loss_types = static_handler.get_account_types_by_category('profit_loss')
profit_loss_ids = [at['id'] for at in profit_loss_types]

# Calculate total expenses
expense_type = static_handler.get_account_type_by_code('E')
query = """
    SELECT SUM(current_balance) as total_expenses
    FROM accounts
    WHERE account_type_id = ?
"""
```

### Transaction Analysis

```python
# Get all cash book transactions
cash_book = static_handler.get_book_code_by_code('CASH')
query = """
    SELECT * FROM transactions
    WHERE book_code_id = ?
    ORDER BY transaction_date DESC
"""

# Get sales book total
sales_book = static_handler.get_book_code_by_code('SALE')
query = """
    SELECT SUM(amount) as total_sales
    FROM transactions
    WHERE book_code_id = ?
    AND transaction_date BETWEEN ? AND ?
"""
```

## ⚠️ Important Notes

### 1. Always Use Foreign Keys (IDs), Not Codes

✅ **CORRECT:**
```python
account_data = {
    'account_type_id': 1  # Use ID from account_types table
}
```

❌ **WRONG:**
```python
account_data = {
    'account_type': 'A'  # Don't store code directly!
}
```

### 2. Seed Data is Automatic

Tables are automatically seeded on first connection. No manual seeding required.

### 3. Data Consistency

These tables are the single source of truth. Never hardcode these values in your application code.

### 4. Connection Management

Always connect and disconnect properly:

```python
handler = StaticDataHandler()
try:
    handler.connect()
    # Use the handler
    data = handler.get_all_book_codes()
finally:
    handler.disconnect()
```

## 🧪 Testing

Test the static data:

```bash
# Run the handler directly to see all data
python database/static_data_handler.py
```

Output will show:
```
BOOK CODES
======================================================================
1. CASH         | Cash Book            | Cash transactions and petty cash
2. BANK         | Bank Book            | Bank transactions and reconciliation
...

ACCOUNT TYPES
======================================================================
A | Assets          | balance_sheet   | debit  | Asset accounts...
L | Liability       | balance_sheet   | credit | Liability accounts...
...
```

## 📝 Summary

**Key Takeaways:**
- ✅ Use `static_data_handler` for all book codes and account types
- ✅ Store foreign key IDs in your tables, not string codes
- ✅ Use helper methods for dropdowns: `get_*_for_dropdown()`
- ✅ JOIN tables for queries and reports
- ✅ Data is automatically seeded on first use
- ✅ Single source of truth for all accounting classifications

---

**Created:** 2025-11-05
**Handler:** `database/static_data_handler.py`
**Reference:** `ACCOUNTING_STATIC_DATA_PLAN.md`
