"""
Seed Demo Data - Final Version (Matches actual database schema)
"""

import sqlite3
import sys
sys.path.insert(0, '.')
from database.config import DB_PATH


def seed_business_partners():
    """Seed demo business partners"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Check if data already exists
        cursor.execute("SELECT COUNT(*) FROM business_partners")
        count = cursor.fetchone()[0]

        if count > 0:
            print(f"[INFO] Business partners already seeded ({count} records)")
            conn.close()
            return True

        # Get first state ID
        cursor.execute("SELECT id FROM states LIMIT 1")
        state_row = cursor.fetchone()
        state_id = state_row[0] if state_row else 1

        # Get first city ID
        cursor.execute("SELECT id FROM cities LIMIT 1")
        city_row = cursor.fetchone()
        city_id = city_row[0] if city_row else 1

        # Account types: 3=Debtors (for customers), 4=Creditors (for suppliers)
        # Book codes: 3=Ledger
        # Account groups: 8=Accounts Receivable, 1=Sales (we'll use 1 for now)

        partners = [
            # Customers (Debtors)
            ('CUST001', 'ABC Traders Pvt Ltd', '123 MG Road, Andheri East, Mumbai - 400069',
             '123 MG Road, Andheri East, Mumbai - 400069', city_id, state_id, '+91-9876543210',
             1, 3, 3, 50000.00, 'Debit', 'Active'),

            ('CUST002', 'XYZ Enterprises', '456 Park Street, Bandra West, Mumbai - 400050',
             '456 Park Street, Bandra West, Mumbai - 400050', city_id, state_id, '+91-9876543211',
             1, 3, 3, 75000.00, 'Debit', 'Active'),

            ('CUST003', 'Global Solutions Ltd', '789 Link Road, Malad West, Mumbai - 400064',
             '789 Link Road, Malad West, Mumbai - 400064', city_id, state_id, '+91-9876543212',
             1, 3, 3, 0.00, 'Debit', 'Active'),

            ('CUST004', 'Retail Mart India', '321 SV Road, Goregaon East, Mumbai - 400063',
             '321 SV Road, Goregaon East, Mumbai - 400063', city_id, state_id, '+91-9876543213',
             1, 3, 3, 25000.00, 'Debit', 'Active'),

            ('CUST005', 'Tech Hub Pvt Ltd', '555 Western Express Highway, Andheri, Mumbai - 400053',
             '555 Western Express Highway, Andheri, Mumbai - 400053', city_id, state_id, '+91-9876543214',
             1, 3, 3, 100000.00, 'Debit', 'Active'),

            # Suppliers (Creditors)
            ('SUPP001', 'Prime Suppliers Co', '888 Industrial Estate, Vikhroli, Mumbai - 400083',
             '888 Industrial Estate, Vikhroli, Mumbai - 400083', city_id, state_id, '+91-9876543215',
             6, 3, 4, 80000.00, 'Credit', 'Active'),

            ('SUPP002', 'Quality Goods Traders', '999 Trade Center, Kurla, Mumbai - 400070',
             '999 Trade Center, Kurla, Mumbai - 400070', city_id, state_id, '+91-9876543216',
             6, 3, 4, 120000.00, 'Credit', 'Active'),

            ('SUPP003', 'Wholesale Depot', '777 Market Yard, Vashi, Navi Mumbai - 400703',
             '777 Market Yard, Vashi, Navi Mumbai - 400703', city_id, state_id, '+91-9876543217',
             6, 3, 4, 0.00, 'Credit', 'Active'),

            ('SUPP004', 'Mega Distribution House', '444 Commerce Complex, Dadar, Mumbai - 400014',
             '444 Commerce Complex, Dadar, Mumbai - 400014', city_id, state_id, '+91-9876543218',
             6, 3, 4, 50000.00, 'Credit', 'Active'),

            ('SUPP005', 'United Trading Co', '666 Business Plaza, Powai, Mumbai - 400076',
             '666 Business Plaza, Powai, Mumbai - 400076', city_id, state_id, '+91-9876543219',
             6, 3, 4, 30000.00, 'Credit', 'Active'),
        ]

        cursor.executemany("""
            INSERT INTO business_partners (
                bp_code, bp_name, bill_to_address, ship_to_address,
                city_id, state_id, mobile, account_group_id, book_code_id, account_type_id,
                opening_balance, balance_type, status
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, partners)

        conn.commit()
        print(f"[OK] Seeded {len(partners)} business partners")
        print("     - 5 Customers (Debtors)")
        print("     - 5 Suppliers (Creditors)")
        conn.close()
        return True

    except sqlite3.Error as e:
        print(f"[ERROR] Error seeding business partners: {e}")
        import traceback
        traceback.print_exc()
        return False


def seed_account_master():
    """Seed demo chart of accounts"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Check if data already exists
        cursor.execute("SELECT COUNT(*) FROM account_master")
        count = cursor.fetchone()[0]

        if count > 0:
            print(f"[INFO] Account master already seeded ({count} records)")
            conn.close()
            return True

        # Account type IDs: 1=Assets, 2=Liability, 5=Sale, 6=Purchase, 7=Expenses, 8=Revenue
        # Book code IDs: 1=Cash, 2=Bank, 3=Ledger, 4=Sale, 5=Purchase
        # Account group IDs: 1=Sales, 3=Stock, 4=Salary, 6=Purchase, 7=Assets

        accounts = [
            # ASSETS (Type 1, Group 7)
            ('Cash in Hand', 7, 1, 1, 50000.00, 'Debit', 'Active', 'ACC1001'),
            ('HDFC Bank Current Account', 7, 2, 1, 250000.00, 'Debit', 'Active', 'ACC1002'),
            ('ICICI Bank Savings Account', 7, 2, 1, 150000.00, 'Debit', 'Active', 'ACC1003'),
            ('State Bank of India', 7, 2, 1, 300000.00, 'Debit', 'Active', 'ACC1004'),
            ('Petty Cash', 7, 1, 1, 10000.00, 'Debit', 'Active', 'ACC1005'),
            ('Office Equipment', 7, 3, 1, 500000.00, 'Debit', 'Active', 'ACC1006'),
            ('Furniture & Fixtures', 7, 3, 1, 300000.00, 'Debit', 'Active', 'ACC1007'),
            ('Computer & Software', 7, 3, 1, 400000.00, 'Debit', 'Active', 'ACC1008'),
            ('Inventory - Raw Materials', 3, 3, 1, 750000.00, 'Debit', 'Active', 'ACC1009'),
            ('Inventory - Finished Goods', 3, 3, 1, 600000.00, 'Debit', 'Active', 'ACC1010'),

            # LIABILITIES (Type 2, Group 7)
            ('Capital Account', 7, 3, 2, 2000000.00, 'Credit', 'Active', 'ACC2001'),
            ('Retained Earnings', 7, 3, 2, 500000.00, 'Credit', 'Active', 'ACC2002'),
            ('Bank Loan - HDFC', 7, 3, 2, 1000000.00, 'Credit', 'Active', 'ACC2003'),
            ('Unsecured Loan', 7, 3, 2, 500000.00, 'Credit', 'Active', 'ACC2004'),

            # DEBTORS (Type 3, Group 8) - Control
            ('Sundry Debtors', 8, 4, 3, 350000.00, 'Debit', 'Active', 'ACC3001'),

            # CREDITORS (Type 4, Group 6) - Control
            ('Sundry Creditors', 6, 5, 4, 280000.00, 'Credit', 'Active', 'ACC4001'),

            # SALES (Type 5, Group 1)
            ('Sales - Products', 1, 4, 5, 0.00, 'Credit', 'Active', 'ACC5001'),
            ('Sales - Services', 1, 4, 5, 0.00, 'Credit', 'Active', 'ACC5002'),
            ('Export Sales', 1, 4, 5, 0.00, 'Credit', 'Active', 'ACC5003'),

            # PURCHASE (Type 6, Group 6)
            ('Purchase - Raw Materials', 6, 5, 6, 0.00, 'Debit', 'Active', 'ACC6001'),
            ('Purchase - Trading Goods', 6, 5, 6, 0.00, 'Debit', 'Active', 'ACC6002'),
            ('Import Purchase', 6, 5, 6, 0.00, 'Debit', 'Active', 'ACC6003'),

            # EXPENSES (Type 7, Group 4)
            ('Salary & Wages', 4, 3, 7, 0.00, 'Debit', 'Active', 'ACC7001'),
            ('Rent Expense', 7, 3, 7, 0.00, 'Debit', 'Active', 'ACC7002'),
            ('Electricity Expense', 7, 3, 7, 0.00, 'Debit', 'Active', 'ACC7003'),
            ('Telephone & Internet', 7, 3, 7, 0.00, 'Debit', 'Active', 'ACC7004'),
            ('Office Supplies', 7, 3, 7, 0.00, 'Debit', 'Active', 'ACC7005'),
            ('Printing & Stationery', 7, 3, 7, 0.00, 'Debit', 'Active', 'ACC7006'),
            ('Travelling Expenses', 7, 3, 7, 0.00, 'Debit', 'Active', 'ACC7007'),
            ('Bank Charges', 7, 2, 7, 0.00, 'Debit', 'Active', 'ACC7008'),
            ('Interest on Loan', 7, 3, 7, 0.00, 'Debit', 'Active', 'ACC7009'),
            ('Depreciation', 7, 3, 7, 0.00, 'Debit', 'Active', 'ACC7010'),

            # REVENUE (Type 8, Group 1) - Other Income
            ('Interest Income', 1, 2, 8, 0.00, 'Credit', 'Active', 'ACC8001'),
            ('Discount Received', 1, 3, 8, 0.00, 'Credit', 'Active', 'ACC8002'),
            ('Miscellaneous Income', 1, 3, 8, 0.00, 'Credit', 'Active', 'ACC8003'),
        ]

        cursor.executemany("""
            INSERT INTO account_master (
                account_name, account_group_id, book_code_id, account_type_id,
                opening_balance, balance_type, status, account_code
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, accounts)

        conn.commit()
        print(f"[OK] Seeded {len(accounts)} accounts")
        print("     - 10 Asset accounts (5 cash/bank + 5 other)")
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
        import traceback
        traceback.print_exc()
        return False


def main():
    """Seed all demo data"""
    print("\n" + "="*70)
    print("  SEEDING DEMO DATA FOR ACCOUNTING SYSTEM")
    print("="*70)

    print("\n1. Seeding Business Partners...")
    bp_success = seed_business_partners()

    print("\n2. Seeding Account Master...")
    am_success = seed_account_master()

    print("\n" + "="*70)
    if bp_success and am_success:
        print("  DEMO DATA SEEDING COMPLETE!")
    else:
        print("  DEMO DATA SEEDING COMPLETED WITH ERRORS")
    print("="*70)
    print("\nYou now have:")
    print("  - 10 Business Partners (5 customers as Debtors, 5 suppliers as Creditors)")
    print("  - 35 Chart of Accounts entries with opening balances")
    print("  - All accounts properly classified by type and group")
    print("  - Ready for transaction entry!")
    print("\n")


if __name__ == "__main__":
    main()
