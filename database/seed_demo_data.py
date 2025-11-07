"""
Seed Demo Data - Create sample Business Partners and Account Master records
Following the database strategy: SQLite for master data, MySQL for transactional data
"""

import sqlite3
from database.config import DB_PATH


def seed_business_partners():
    """Seed demo business partners (Customers & Suppliers)"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Create business_partners table if not exists
        create_table = """
        CREATE TABLE IF NOT EXISTS business_partners (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            partner_code TEXT NOT NULL UNIQUE,
            partner_name TEXT NOT NULL,
            partner_type TEXT NOT NULL CHECK(partner_type IN ('Customer', 'Supplier', 'Both')),
            contact_person TEXT,
            email TEXT,
            phone TEXT,
            mobile TEXT,
            address TEXT,
            city TEXT,
            state TEXT,
            pincode TEXT,
            gstin TEXT,
            pan TEXT,
            opening_balance REAL DEFAULT 0,
            balance_type TEXT CHECK(balance_type IN ('Debit', 'Credit')),
            credit_limit REAL DEFAULT 0,
            credit_days INTEGER DEFAULT 0,
            status TEXT DEFAULT 'Active' CHECK(status IN ('Active', 'Inactive')),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        cursor.execute(create_table)

        # Check if data already exists
        cursor.execute("SELECT COUNT(*) FROM business_partners")
        count = cursor.fetchone()[0]

        if count > 0:
            print(f"[INFO] Business partners already seeded ({count} records)")
            conn.close()
            return

        # Demo business partners data
        partners = [
            # Customers
            ('CUST001', 'ABC Traders Pvt Ltd', 'Customer', 'Rajesh Kumar', 'rajesh@abctraders.com',
             '022-12345678', '+91-9876543210', '123 MG Road, Andheri', 'Mumbai', 'Maharashtra',
             '400001', '27AAAAA0000A1Z5', 'AAAAA0000A', 50000.00, 'Debit', 100000.00, 30, 'Active'),

            ('CUST002', 'XYZ Enterprises', 'Customer', 'Priya Sharma', 'priya@xyzent.com',
             '022-23456789', '+91-9876543211', '456 Park Street, Bandra', 'Mumbai', 'Maharashtra',
             '400050', '27BBBBB1111B2Z6', 'BBBBB1111B', 75000.00, 'Debit', 150000.00, 45, 'Active'),

            ('CUST003', 'Global Solutions Ltd', 'Customer', 'Amit Patel', 'amit@globalsol.com',
             '022-34567890', '+91-9876543212', '789 Link Road, Malad', 'Mumbai', 'Maharashtra',
             '400064', '27CCCCC2222C3Z7', 'CCCCC2222C', 0.00, 'Credit', 200000.00, 60, 'Active'),

            ('CUST004', 'Retail Mart India', 'Customer', 'Sneha Desai', 'sneha@retailmart.in',
             '022-45678901', '+91-9876543213', '321 SV Road, Goregaon', 'Mumbai', 'Maharashtra',
             '400062', '27DDDDD3333D4Z8', 'DDDDD3333D', 25000.00, 'Debit', 50000.00, 15, 'Active'),

            ('CUST005', 'Tech Hub Pvt Ltd', 'Customer', 'Rahul Singh', 'rahul@techhub.com',
             '022-56789012', '+91-9876543214', '555 Western Express Highway', 'Mumbai', 'Maharashtra',
             '400053', '27EEEEE4444E5Z9', 'EEEEE4444E', 100000.00, 'Debit', 250000.00, 90, 'Active'),

            # Suppliers
            ('SUPP001', 'Prime Suppliers Co', 'Supplier', 'Vikram Mehta', 'vikram@primesup.com',
             '022-67890123', '+91-9876543215', '888 Industrial Estate', 'Mumbai', 'Maharashtra',
             '400042', '27FFFFF5555F6Z0', 'FFFFF5555F', 80000.00, 'Credit', 0.00, 0, 'Active'),

            ('SUPP002', 'Quality Goods Traders', 'Supplier', 'Anjali Gupta', 'anjali@qualitygoods.com',
             '022-78901234', '+91-9876543216', '999 Trade Center', 'Mumbai', 'Maharashtra',
             '400013', '27GGGGG6666G7Z1', 'GGGGG6666G', 120000.00, 'Credit', 0.00, 0, 'Active'),

            ('SUPP003', 'Wholesale Depot', 'Supplier', 'Manoj Kumar', 'manoj@wholesale.com',
             '022-89012345', '+91-9876543217', '777 Market Yard', 'Mumbai', 'Maharashtra',
             '400028', '27HHHHH7777H8Z2', 'HHHHH7777H', 0.00, 'Credit', 0.00, 0, 'Active'),

            # Both Customer & Supplier
            ('BOTH001', 'Mega Distribution House', 'Both', 'Suresh Reddy', 'suresh@megadist.com',
             '022-90123456', '+91-9876543218', '444 Commerce Complex', 'Mumbai', 'Maharashtra',
             '400002', '27IIIII8888I9Z3', 'IIIII8888I', 50000.00, 'Debit', 100000.00, 30, 'Active'),

            ('BOTH002', 'United Trading Co', 'Both', 'Pooja Jain', 'pooja@unitedtrade.com',
             '022-01234567', '+91-9876543219', '666 Business Plaza', 'Mumbai', 'Maharashtra',
             '400022', '27JJJJJ9999J0Z4', 'JJJJJ9999J', 30000.00, 'Credit', 150000.00, 45, 'Active'),
        ]

        cursor.executemany("""
            INSERT INTO business_partners (
                partner_code, partner_name, partner_type, contact_person, email,
                phone, mobile, address, city, state, pincode, gstin, pan,
                opening_balance, balance_type, credit_limit, credit_days, status
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, partners)

        conn.commit()
        print(f"[OK] Seeded {len(partners)} business partners")
        print("     - 5 Customers")
        print("     - 3 Suppliers")
        print("     - 2 Both (Customer & Supplier)")
        conn.close()
        return True

    except sqlite3.Error as e:
        print(f"[ERROR] Error seeding business partners: {e}")
        return False


def seed_account_master():
    """Seed demo chart of accounts"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Create account_master table if not exists
        create_table = """
        CREATE TABLE IF NOT EXISTS account_master (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            account_code TEXT NOT NULL UNIQUE,
            account_name TEXT NOT NULL,
            account_type_id INTEGER NOT NULL,
            account_group TEXT,
            book_code_id INTEGER,
            parent_account_id INTEGER,
            opening_balance REAL DEFAULT 0,
            balance_type TEXT CHECK(balance_type IN ('Debit', 'Credit')),
            is_bank_account INTEGER DEFAULT 0,
            bank_name TEXT,
            account_number TEXT,
            ifsc_code TEXT,
            is_cash_account INTEGER DEFAULT 0,
            is_control_account INTEGER DEFAULT 0,
            status TEXT DEFAULT 'Active' CHECK(status IN ('Active', 'Inactive')),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (account_type_id) REFERENCES account_types(id),
            FOREIGN KEY (book_code_id) REFERENCES book_codes(id),
            FOREIGN KEY (parent_account_id) REFERENCES account_master(id)
        )
        """
        cursor.execute(create_table)

        # Check if data already exists
        cursor.execute("SELECT COUNT(*) FROM account_master")
        count = cursor.fetchone()[0]

        if count > 0:
            print(f"[INFO] Account master already seeded ({count} records)")
            conn.close()
            return

        # Demo accounts data
        # account_type_id: 1=Assets, 2=Liability, 3=Debtors, 4=Creditors, 5=Sale, 6=Purchase, 7=Expenses, 8=Revenue
        # book_code_id: 1=Cash, 2=Bank, 3=Ledger, 4=Sale, 5=Purchase, 6=CreditNote

        accounts = [
            # ASSETS (Type 1)
            ('ACC1001', 'Cash in Hand', 1, 'Current Assets', 1, None, 50000.00, 'Debit', 0, None, None, None, 1, 0, 'Active'),
            ('ACC1002', 'HDFC Bank Current Account', 1, 'Current Assets', 2, None, 250000.00, 'Debit', 1, 'HDFC Bank', '50100123456789', 'HDFC0001234', 0, 0, 'Active'),
            ('ACC1003', 'ICICI Bank Savings Account', 1, 'Current Assets', 2, None, 150000.00, 'Debit', 1, 'ICICI Bank', '000123456789', 'ICIC0001234', 0, 0, 'Active'),
            ('ACC1004', 'State Bank of India', 1, 'Current Assets', 2, None, 300000.00, 'Debit', 1, 'State Bank of India', '12345678901', 'SBIN0001234', 0, 0, 'Active'),
            ('ACC1005', 'Petty Cash', 1, 'Current Assets', 1, None, 10000.00, 'Debit', 0, None, None, None, 1, 0, 'Active'),
            ('ACC1006', 'Office Equipment', 1, 'Fixed Assets', 3, None, 500000.00, 'Debit', 0, None, None, None, 0, 0, 'Active'),
            ('ACC1007', 'Furniture & Fixtures', 1, 'Fixed Assets', 3, None, 300000.00, 'Debit', 0, None, None, None, 0, 0, 'Active'),
            ('ACC1008', 'Computer & Software', 1, 'Fixed Assets', 3, None, 400000.00, 'Debit', 0, None, None, None, 0, 0, 'Active'),
            ('ACC1009', 'Inventory - Raw Materials', 1, 'Current Assets', 3, None, 750000.00, 'Debit', 0, None, None, None, 0, 0, 'Active'),
            ('ACC1010', 'Inventory - Finished Goods', 1, 'Current Assets', 3, None, 600000.00, 'Debit', 0, None, None, None, 0, 0, 'Active'),

            # LIABILITIES (Type 2)
            ('ACC2001', 'Capital Account', 2, 'Equity', 3, None, 2000000.00, 'Credit', 0, None, None, None, 0, 0, 'Active'),
            ('ACC2002', 'Retained Earnings', 2, 'Equity', 3, None, 500000.00, 'Credit', 0, None, None, None, 0, 0, 'Active'),
            ('ACC2003', 'Bank Loan - HDFC', 2, 'Long Term Liabilities', 3, None, 1000000.00, 'Credit', 0, None, None, None, 0, 0, 'Active'),
            ('ACC2004', 'Unsecured Loan', 2, 'Long Term Liabilities', 3, None, 500000.00, 'Credit', 0, None, None, None, 0, 0, 'Active'),

            # DEBTORS (Type 3) - Sundry Debtors Control Account
            ('ACC3001', 'Sundry Debtors', 3, 'Trade Receivables', 4, None, 350000.00, 'Debit', 0, None, None, None, 0, 1, 'Active'),

            # CREDITORS (Type 4) - Sundry Creditors Control Account
            ('ACC4001', 'Sundry Creditors', 4, 'Trade Payables', 5, None, 280000.00, 'Credit', 0, None, None, None, 0, 1, 'Active'),

            # SALES (Type 5)
            ('ACC5001', 'Sales - Products', 5, 'Revenue', 4, None, 0.00, 'Credit', 0, None, None, None, 0, 0, 'Active'),
            ('ACC5002', 'Sales - Services', 5, 'Revenue', 4, None, 0.00, 'Credit', 0, None, None, None, 0, 0, 'Active'),
            ('ACC5003', 'Export Sales', 5, 'Revenue', 4, None, 0.00, 'Credit', 0, None, None, None, 0, 0, 'Active'),

            # PURCHASE (Type 6)
            ('ACC6001', 'Purchase - Raw Materials', 6, 'Cost of Goods Sold', 5, None, 0.00, 'Debit', 0, None, None, None, 0, 0, 'Active'),
            ('ACC6002', 'Purchase - Trading Goods', 6, 'Cost of Goods Sold', 5, None, 0.00, 'Debit', 0, None, None, None, 0, 0, 'Active'),
            ('ACC6003', 'Import Purchase', 6, 'Cost of Goods Sold', 5, None, 0.00, 'Debit', 0, None, None, None, 0, 0, 'Active'),

            # EXPENSES (Type 7)
            ('ACC7001', 'Salary & Wages', 7, 'Operating Expenses', 3, None, 0.00, 'Debit', 0, None, None, None, 0, 0, 'Active'),
            ('ACC7002', 'Rent Expense', 7, 'Operating Expenses', 3, None, 0.00, 'Debit', 0, None, None, None, 0, 0, 'Active'),
            ('ACC7003', 'Electricity Expense', 7, 'Operating Expenses', 3, None, 0.00, 'Debit', 0, None, None, None, 0, 0, 'Active'),
            ('ACC7004', 'Telephone & Internet', 7, 'Operating Expenses', 3, None, 0.00, 'Debit', 0, None, None, None, 0, 0, 'Active'),
            ('ACC7005', 'Office Supplies', 7, 'Operating Expenses', 3, None, 0.00, 'Debit', 0, None, None, None, 0, 0, 'Active'),
            ('ACC7006', 'Printing & Stationery', 7, 'Operating Expenses', 3, None, 0.00, 'Debit', 0, None, None, None, 0, 0, 'Active'),
            ('ACC7007', 'Travelling Expenses', 7, 'Operating Expenses', 3, None, 0.00, 'Debit', 0, None, None, None, 0, 0, 'Active'),
            ('ACC7008', 'Bank Charges', 7, 'Financial Expenses', 2, None, 0.00, 'Debit', 0, None, None, None, 0, 0, 'Active'),
            ('ACC7009', 'Interest on Loan', 7, 'Financial Expenses', 3, None, 0.00, 'Debit', 0, None, None, None, 0, 0, 'Active'),
            ('ACC7010', 'Depreciation', 7, 'Non-Operating Expenses', 3, None, 0.00, 'Debit', 0, None, None, None, 0, 0, 'Active'),

            # REVENUE (Type 8) - Other Income
            ('ACC8001', 'Interest Income', 8, 'Other Income', 2, None, 0.00, 'Credit', 0, None, None, None, 0, 0, 'Active'),
            ('ACC8002', 'Discount Received', 8, 'Other Income', 3, None, 0.00, 'Credit', 0, None, None, None, 0, 0, 'Active'),
            ('ACC8003', 'Miscellaneous Income', 8, 'Other Income', 3, None, 0.00, 'Credit', 0, None, None, None, 0, 0, 'Active'),
        ]

        cursor.executemany("""
            INSERT INTO account_master (
                account_code, account_name, account_type_id, account_group, book_code_id,
                parent_account_id, opening_balance, balance_type, is_bank_account,
                bank_name, account_number, ifsc_code, is_cash_account, is_control_account, status
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, accounts)

        conn.commit()
        print(f"[OK] Seeded {len(accounts)} accounts")
        print("     - 10 Asset accounts (including 3 banks + 2 cash)")
        print("     - 4 Liability accounts")
        print("     - 1 Sundry Debtors control account")
        print("     - 1 Sundry Creditors control account")
        print("     - 3 Sales accounts")
        print("     - 3 Purchase accounts")
        print("     - 10 Expense accounts")
        print("     - 3 Revenue accounts (other income)")
        conn.close()
        return True

    except sqlite3.Error as e:
        print(f"[ERROR] Error seeding account master: {e}")
        return False


def main():
    """Seed all demo data"""
    print("\n" + "="*70)
    print("SEEDING DEMO DATA FOR ACCOUNTING SYSTEM")
    print("="*70)

    print("\n1. Seeding Business Partners...")
    seed_business_partners()

    print("\n2. Seeding Account Master...")
    seed_account_master()

    print("\n" + "="*70)
    print("DEMO DATA SEEDING COMPLETE!")
    print("="*70)
    print("\nYou now have:")
    print("  • 10 Business Partners (5 customers, 3 suppliers, 2 both)")
    print("  • 35 Chart of Accounts entries")
    print("  • Ready for transaction entry!")
    print("\n")


if __name__ == "__main__":
    main()
