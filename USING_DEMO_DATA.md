# Using Demo Data - Quick Reference Guide

## Overview

Your accounting system now has demo data populated and ready for testing. This guide shows you how to use and verify the data.

---

## Viewing Demo Data

### Method 1: Using the View Script
```bash
python tkinter_mysql_project/view_demo_data.py
```

This displays:
- All 10 business partners (5 customers, 5 suppliers)
- All 35 chart of accounts
- Summary statistics

### Method 2: Through the Application
1. Launch the application: `python tkinter_mysql_project/main.py`
2. Login with: **admin** / **password123**
3. Navigate to:
   - **Business Partner Management** - See all customers and suppliers
   - **Account Master** - View chart of accounts
   - **Reports** - Generate trial balance, P&L, balance sheet

---

## What's Included

### Business Partners (10 records)

#### Customers (Debtors)
| Code | Name | Opening Balance |
|------|------|----------------|
| CUST001 | ABC Traders Pvt Ltd | Rs.50,000 Dr |
| CUST002 | XYZ Enterprises | Rs.75,000 Dr |
| CUST003 | Global Solutions Ltd | Rs.0 |
| CUST004 | Retail Mart India | Rs.25,000 Dr |
| CUST005 | Tech Hub Pvt Ltd | Rs.1,00,000 Dr |

**Total Outstanding:** Rs.2,50,000

#### Suppliers (Creditors)
| Code | Name | Opening Balance |
|------|------|----------------|
| SUPP001 | Prime Suppliers Co | Rs.80,000 Cr |
| SUPP002 | Quality Goods Traders | Rs.1,20,000 Cr |
| SUPP003 | Wholesale Depot | Rs.0 |
| SUPP004 | Mega Distribution House | Rs.50,000 Cr |
| SUPP005 | United Trading Co | Rs.30,000 Cr |

**Total Outstanding:** Rs.2,80,000

### Chart of Accounts (35 accounts)

#### By Category:
- **Assets:** 10 accounts (Rs.33,10,000)
  - Cash: Rs.60,000
  - Bank: Rs.7,00,000
  - Fixed Assets: Rs.12,00,000
  - Inventory: Rs.13,50,000

- **Liabilities:** 4 accounts (Rs.40,00,000)
  - Capital: Rs.25,00,000
  - Loans: Rs.15,00,000

- **Control Accounts:**
  - Sundry Debtors: Rs.3,50,000 Dr
  - Sundry Creditors: Rs.2,80,000 Cr

- **Income/Expense Accounts:** 19 accounts (Rs.0 - ready for transactions)

---

## Testing Scenarios

### Scenario 1: Record a Sale
1. Go to **Sales Entry**
2. Select customer: **CUST001 - ABC Traders Pvt Ltd**
3. Select account: **ACC5001 - Sales - Products**
4. Amount: Rs.10,000
5. This will update customer balance to Rs.60,000 Dr

### Scenario 2: Record a Purchase
1. Go to **Purchase Entry**
2. Select supplier: **SUPP001 - Prime Suppliers Co**
3. Select account: **ACC6001 - Purchase - Raw Materials**
4. Amount: Rs.15,000
5. This will update supplier balance to Rs.95,000 Cr

### Scenario 3: Record Expenses
1. Go to **Journal Entry**
2. Debit: **ACC7002 - Rent Expense** (Rs.25,000)
3. Credit: **ACC1002 - HDFC Bank Current Account** (Rs.25,000)
4. This records monthly rent payment

### Scenario 4: Receive Payment from Customer
1. Go to **Receipt Entry**
2. Select customer: **CUST002 - XYZ Enterprises**
3. Amount: Rs.50,000
4. Bank account: **ACC1003 - ICICI Bank Savings Account**
5. This reduces customer balance to Rs.25,000 Dr

### Scenario 5: Make Payment to Supplier
1. Go to **Payment Entry**
2. Select supplier: **SUPP002 - Quality Goods Traders**
3. Amount: Rs.1,00,000
4. Bank account: **ACC1004 - State Bank of India**
5. This reduces supplier balance to Rs.20,000 Cr

---

## Reports to Test

### Trial Balance
- Shows all accounts with their balances
- Debit total should equal Credit total
- Current totals (before transactions):
  - Debits: Rs.39,60,000
  - Credits: Rs.42,80,000

### Balance Sheet
- Assets side: Rs.39,60,000
- Liabilities side: Rs.42,80,000
- Shows financial position

### Profit & Loss Statement
- Currently all income/expense accounts at Rs.0
- After recording transactions, shows profit/loss

### Customer Outstanding Report
- Shows all customers with their balances
- Total debtors: Rs.2,50,000

### Supplier Outstanding Report
- Shows all suppliers with their balances
- Total creditors: Rs.2,80,000

---

## Re-seeding Demo Data

If you want to reset and re-seed the demo data:

### Option 1: Clear and Re-seed
```bash
python -c "import sqlite3; from database.config import DB_PATH; conn = sqlite3.connect(DB_PATH); conn.execute('DELETE FROM business_partners'); conn.execute('DELETE FROM account_master'); conn.commit(); print('Demo data cleared')"

python tkinter_mysql_project/database/seed_demo_data_final.py
```

### Option 2: Delete Database and Re-create
```bash
# Delete the database file
rm tkinter_mysql_project/financial_data.db  # Linux/Mac
del tkinter_mysql_project\financial_data.db  # Windows

# Launch app - tables will be auto-created
python tkinter_mysql_project/main.py

# Run seed script
python tkinter_mysql_project/database/seed_demo_data_final.py
```

---

## Database Schema Reference

### Business Partners Table
```sql
business_partners (
    id, bp_code, bp_name,
    bill_to_address, ship_to_address,
    city_id, state_id, mobile,
    account_group_id, book_code_id, account_type_id,
    opening_balance, balance_type, status
)
```

### Account Master Table
```sql
account_master (
    id, account_code, account_name,
    account_group_id, book_code_id, account_type_id,
    opening_balance, balance_type, status
)
```

### Reference Tables (Master Data - SQLite)
- `book_codes` - Cash(1), Bank(2), Ledger(3), Sale(4), Purchase(5), CreditNote(6)
- `account_types` - Assets(1), Liability(2), Debtors(3), Creditors(4), Sale(5), Purchase(6), Expenses(7), Revenue(8)
- `account_groups` - Sales(1), Purchase(6), Stock(3), Salary(4), Assets(7), AR(8)

---

## Troubleshooting

### Issue: Can't see demo data in application
**Solution:** Make sure you're logged in and navigating to the correct modules. Demo data is in:
- Business Partner Management
- Account Master

### Issue: Demo data seed script says "already seeded"
**Solution:** Data already exists. To re-seed, clear the data first (see Re-seeding section above).

### Issue: Transactions fail with "invalid account"
**Solution:** Make sure you're selecting valid accounts from the dropdowns populated by demo data.

### Issue: Reports show different totals
**Solution:** Check if any transactions have been recorded after seeding. Reports show current balances including all transactions.

---

## Next Steps

1. **Test CRUD Operations:**
   - Create new business partners
   - Add new accounts
   - Edit existing records
   - Delete test records

2. **Record Transactions:**
   - Use the 5 testing scenarios above
   - Try different transaction types
   - Verify balances update correctly

3. **Generate Reports:**
   - Trial balance
   - Balance sheet
   - Profit & Loss
   - Customer/Supplier outstanding

4. **Build Your Own Data:**
   - Add your actual customers
   - Add your actual suppliers
   - Set up your chart of accounts
   - Record real transactions

---

**Demo Data Created:** 2025-11-05
**Script:** [seed_demo_data_final.py](database/seed_demo_data_final.py)
**Summary:** [DEMO_DATA_SUMMARY.md](DEMO_DATA_SUMMARY.md)
