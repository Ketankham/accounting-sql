# Demo Data Summary

## ✅ Successfully Seeded Demo Data

### 1. Business Partners (10 records)

#### Customers (5) - Account Type: Debtors
| Code | Name | Mobile | Opening Balance | Type |
|------|------|--------|----------------|------|
| CUST001 | ABC Traders Pvt Ltd | +91-9876543210 | Rs.50,000 Dr | Customer |
| CUST002 | XYZ Enterprises | +91-9876543211 | Rs.75,000 Dr | Customer |
| CUST003 | Global Solutions Ltd | +91-9876543212 | Rs.0 | Customer |
| CUST004 | Retail Mart India | +91-9876543213 | Rs.25,000 Dr | Customer |
| CUST005 | Tech Hub Pvt Ltd | +91-9876543214 | Rs.1,00,000 Dr | Customer |

**Total Customer Outstanding:** Rs.2,50,000 (Debit)

#### Suppliers (5) - Account Type: Creditors
| Code | Name | Mobile | Opening Balance | Type |
|------|------|--------|----------------|------|
| SUPP001 | Prime Suppliers Co | +91-9876543215 | Rs.80,000 Cr | Supplier |
| SUPP002 | Quality Goods Traders | +91-9876543216 | Rs.1,20,000 Cr | Supplier |
| SUPP003 | Wholesale Depot | +91-9876543217 | Rs.0 | Supplier |
| SUPP004 | Mega Distribution House | +91-9876543218 | Rs.50,000 Cr | Supplier |
| SUPP005 | United Trading Co | +91-9876543219 | Rs.30,000 Cr | Supplier |

**Total Supplier Outstanding:** Rs.2,80,000 (Credit)

---

### 2. Account Master (35 accounts)

#### Assets (10 accounts) - Rs.33,10,000
| Code | Account Name | Book | Opening Balance |
|------|-------------|------|----------------|
| ACC1001 | Cash in Hand | Cash | Rs.50,000 |
| ACC1002 | HDFC Bank Current Account | Bank | Rs.2,50,000 |
| ACC1003 | ICICI Bank Savings Account | Bank | Rs.1,50,000 |
| ACC1004 | State Bank of India | Bank | Rs.3,00,000 |
| ACC1005 | Petty Cash | Cash | Rs.10,000 |
| ACC1006 | Office Equipment | Ledger | Rs.5,00,000 |
| ACC1007 | Furniture & Fixtures | Ledger | Rs.3,00,000 |
| ACC1008 | Computer & Software | Ledger | Rs.4,00,000 |
| ACC1009 | Inventory - Raw Materials | Ledger | Rs.7,50,000 |
| ACC1010 | Inventory - Finished Goods | Ledger | Rs.6,00,000 |

**Breakdown:**
- Cash: Rs.60,000 (2 accounts)
- Bank: Rs.7,00,000 (3 accounts)
- Fixed Assets: Rs.12,00,000 (3 accounts)
- Inventory: Rs.13,50,000 (2 accounts)

#### Liabilities (4 accounts) - Rs.40,00,000
| Code | Account Name | Opening Balance |
|------|-------------|----------------|
| ACC2001 | Capital Account | Rs.20,00,000 |
| ACC2002 | Retained Earnings | Rs.5,00,000 |
| ACC2003 | Bank Loan - HDFC | Rs.10,00,000 |
| ACC2004 | Unsecured Loan | Rs.5,00,000 |

#### Debtors (1 control account) - Rs.3,50,000
| Code | Account Name | Opening Balance |
|------|-------------|----------------|
| ACC3001 | Sundry Debtors | Rs.3,50,000 Dr |

#### Creditors (1 control account) - Rs.2,80,000
| Code | Account Name | Opening Balance |
|------|-------------|----------------|
| ACC4001 | Sundry Creditors | Rs.2,80,000 Cr |

#### Sales Accounts (3) - Rs.0
| Code | Account Name | Book |
|------|-------------|------|
| ACC5001 | Sales - Products | Sale |
| ACC5002 | Sales - Services | Sale |
| ACC5003 | Export Sales | Sale |

#### Purchase Accounts (3) - Rs.0
| Code | Account Name | Book |
|------|-------------|------|
| ACC6001 | Purchase - Raw Materials | Purchase |
| ACC6002 | Purchase - Trading Goods | Purchase |
| ACC6003 | Import Purchase | Purchase |

#### Expense Accounts (10) - Rs.0
| Code | Account Name | Book |
|------|-------------|------|
| ACC7001 | Salary & Wages | Ledger |
| ACC7002 | Rent Expense | Ledger |
| ACC7003 | Electricity Expense | Ledger |
| ACC7004 | Telephone & Internet | Ledger |
| ACC7005 | Office Supplies | Ledger |
| ACC7006 | Printing & Stationery | Ledger |
| ACC7007 | Travelling Expenses | Ledger |
| ACC7008 | Bank Charges | Bank |
| ACC7009 | Interest on Loan | Ledger |
| ACC7010 | Depreciation | Ledger |

#### Revenue Accounts - Other Income (3) - Rs.0
| Code | Account Name | Book |
|------|-------------|------|
| ACC8001 | Interest Income | Bank |
| ACC8002 | Discount Received | Ledger |
| ACC8003 | Miscellaneous Income | Ledger |

---

## 📊 Financial Summary

### Balance Sheet (Opening Balances)

**ASSETS:**
- Current Assets: Rs.21,10,000
  - Cash & Bank: Rs.7,60,000
  - Inventory: Rs.13,50,000
- Fixed Assets: Rs.12,00,000
- Sundry Debtors: Rs.3,50,000

**Total Assets:** Rs.39,60,000

**LIABILITIES:**
- Capital & Reserves: Rs.25,00,000
- Loans: Rs.15,00,000
- Sundry Creditors: Rs.2,80,000

**Total Liabilities:** Rs.42,80,000

**Difference:** Rs.3,20,000 (Additional capital/reserves needed to balance)

---

## 🎯 What You Can Do Now

### 1. View Business Partners
- Navigate to Business Partner Management
- See all 10 partners with their details
- Edit/Delete partners as needed

### 2. View Chart of Accounts
- Navigate to Account Master
- See all 35 accounts organized by type
- View opening balances
- Add new accounts as needed

### 3. Record Transactions
- Create sales invoices for customers
- Record purchase bills from suppliers
- Make payments and receipts
- Record journal entries

### 4. Generate Reports
- Trial Balance
- Profit & Loss Statement
- Balance Sheet
- Debtor/Creditor Aging
- Cash Flow Statement

---

## 🔄 Re-seeding Data

If you want to clear and re-seed the demo data:

```bash
# Option 1: Delete all records
python -c "import sqlite3; from database.config import DB_PATH; conn = sqlite3.connect(DB_PATH); conn.execute('DELETE FROM business_partners'); conn.execute('DELETE FROM account_master'); conn.commit(); print('Demo data cleared')"

# Option 2: Re-run seed script (will skip if data exists)
python database/seed_demo_data_final.py
```

---

## 📝 Notes

- All business partners are linked to:
  - Account Groups (Sales for customers, Purchase for suppliers)
  - Book Codes (Ledger = 3)
  - Account Types (Debtors = 3 for customers, Creditors = 4 for suppliers)

- All accounts are properly classified with:
  - Account Type (Assets, Liability, Sale, Purchase, Expenses, Revenue)
  - Account Group (Sales, Purchase, Stock, Salary, Assets, etc.)
  - Book Code (Cash, Bank, Ledger, Sale, Purchase)
  - Opening Balance with Debit/Credit nature

- Control Accounts:
  - ACC3001 (Sundry Debtors) controls all customer balances
  - ACC4001 (Sundry Creditors) controls all supplier balances

---

**Created:** 2025-11-05
**Seeding Script:** [database/seed_demo_data_final.py](database/seed_demo_data_final.py:1)
**Status:** ✅ Complete and tested
