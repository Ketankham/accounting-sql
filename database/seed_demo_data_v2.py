"""
Seed Demo Data V2 - Matches existing table structures
"""

import sqlite3
import sys
sys.path.insert(0, '.')
from database.config import DB_PATH


def seed_business_partners():
    """Seed demo business partners matching existing schema"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Check if data already exists
        cursor.execute("SELECT COUNT(*) FROM business_partners")
        count = cursor.fetchone()[0]

        if count > 0:
            print(f"[INFO] Business partners already seeded ({count} records)")
            conn.close()
            return

        # Get state and city IDs (assuming they exist)
        cursor.execute("SELECT id FROM states WHERE name='Maharashtra' LIMIT 1")
        state_row = cursor.fetchone()
        state_id = state_row[0] if state_row else None

        cursor.execute("SELECT id FROM cities LIMIT 1")
        city_row = cursor.fetchone()
        city_id = city_row[0] if city_row else None

        # Get account type IDs (3=Debtors, 4=Creditors)
        debtors_id = 3  # From account_types
        creditors_id = 4

        # Get book codes (1=Cash, 2=Bank, 3=Ledger, 4=Sale, 5=Purchase)
        ledger_book = 3

        # Demo business partners
        partners = [
            # Customers (Debtors)
            ('CUST001', 'ABC Traders Pvt Ltd', '123 MG Road, Andheri', '123 MG Road, Andheri',
             city_id, state_id, '+91-9876543210', None, ledger_book, debtors_id, 50000.00, 'Debit', 'Active'),

            ('CUST002', 'XYZ Enterprises', '456 Park Street, Bandra', '456 Park Street, Bandra',
             city_id, state_id, '+91-9876543211', None, ledger_book, debtors_id, 75000.00, 'Debit', 'Active'),

            ('CUST003', 'Global Solutions Ltd', '789 Link Road, Malad', '789 Link Road, Malad',
             city_id, state_id, '+91-9876543212', None, ledger_book, debtors_id, 0.00, 'Debit', 'Active'),

            ('CUST004', 'Retail Mart India', '321 SV Road, Goregaon', '321 SV Road, Goregaon',
             city_id, state_id, '+91-9876543213', None, ledger_book, debtors_id, 25000.00, 'Debit', 'Active'),

            ('CUST005', 'Tech Hub Pvt Ltd', '555 Western Express Highway', '555 Western Express Highway',
             city_id, state_id, '+91-9876543214', None, ledger_book, debtors_id, 100000.00, 'Debit', 'Active'),

            # Suppliers (Creditors)
            ('SUPP001', 'Prime Suppliers Co', '888 Industrial Estate', '888 Industrial Estate',
             city_id, state_id, '+91-9876543215', None, ledger_book, creditors_id, 80000.00, 'Credit', 'Active'),

            ('SUPP002', 'Quality Goods Traders', '999 Trade Center', '999 Trade Center',
             city_id, state_id, '+91-9876543216', None, ledger_book, creditors_id, 120000.00, 'Credit', 'Active'),

            ('SUPP003', 'Wholesale Depot', '777 Market Yard', '777 Market Yard',
             city_id, state_id, '+91-9876543217', None, ledger_book, creditors_id, 0.00, 'Credit', 'Active'),

            ('SUPP004', 'Mega Distribution House', '444 Commerce Complex', '444 Commerce Complex',
             city_id, state_id, '+91-9876543218', None, ledger_book, creditors_id, 50000.00, 'Credit', 'Active'),

            ('SUPP005', 'United Trading Co', '666 Business Plaza', '666 Business Plaza',
             city_id, state_id, '+91-9876543219', None, ledger_book, creditors_id, 30000.00, 'Credit', 'Active'),
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
    """Seed demo chart of accounts matching existing schema"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Check if data already exists
        cursor.execute("SELECT COUNT(*) FROM account_master")
        count = cursor.fetchone()[0]

        if count > 0:
            print(f"[INFO] Account master already seeded ({count} records)")
            conn.close()
            return

        # Account type IDs: 1=Assets, 2=Liability, 3=Debtors, 4=Creditors, 5=Sale, 6=Purchase, 7=Expenses, 8=Revenue
        # Book code IDs: 1=Cash, 2=Bank, 3=Ledger, 4=Sale, 5=Purchase, 6=CreditNote

        accounts = [
            # ASSETS (Type 1)
            ('Cash in Hand', None, 1, 1, 50000.00, 'Debit', 'Active', 'ACC1001'),
            ('HDFC Bank Current Account', None, 2, 1, 250000.00, 'Debit', 'Active', 'ACC1002'),
            ('ICICI Bank Savings Account', None, 2, 1, 150000.00, 'Debit', 'Active', 'ACC1003'),
            ('State Bank of India', None, 2, 1, 300000.00, 'Debit', 'Active', 'ACC1004'),
            ('Petty Cash', None, 1, 1, 10000.00, 'Debit', 'Active', 'ACC1005'),
            ('Office Equipment', None, 3, 1, 500000.00, 'Debit', 'Active', 'ACC1006'),
            ('Furniture & Fixtures', None, 3, 1, 300000.00, 'Debit', 'Active', 'ACC1007'),
            ('Computer & Software', None, 3, 1, 400000.00, 'Debit', 'Active', 'ACC1008'),
            ('Inventory - Raw Materials', None, 3, 1, 750000.00, 'Debit', 'Active', 'ACC1009'),
            ('Inventory - Finished Goods', None, 3, 1, 600000.00, 'Debit', 'Active', 'ACC1010'),

            # LIABILITIES (Type 2)
            ('Capital Account', None, 3, 2, 2000000.00, 'Credit', 'Active', 'ACC2001'),
            ('Retained Earnings', None, 3, 2, 500000.00, 'Credit', 'Active', 'ACC2002'),
            ('Bank Loan - HDFC', None, 3, 2, 1000000.00, 'Credit', 'Active', 'ACC2003'),
            ('Unsecured Loan', None, 3, 2, 500000.00, 'Credit', 'Active', 'ACC2004'),

            # DEBTORS (Type 3) - Control Account
            ('Sundry Debtors', None, 4, 3, 350000.00, 'Debit', 'Active', 'ACC3001'),

            # CREDITORS (Type 4) - Control Account
            ('Sundry Creditors', None, 5, 4, 280000.00, 'Credit', 'Active', 'ACC4001'),

            # SALES (Type 5)
            ('Sales - Products', None, 4, 5, 0.00, 'Credit', 'Active', 'ACC5001'),
            ('Sales - Services', None, 4, 5, 0.00, 'Credit', 'Active', 'ACC5002'),
            ('Export Sales', None, 4, 5, 0.00, 'Credit', 'Active', 'ACC5003'),

            # PURCHASE (Type 6)
            ('Purchase - Raw Materials', None, 5, 6, 0.00, 'Debit', 'Active', 'ACC6001'),
            ('Purchase - Trading Goods', None, 5, 6, 0.00, 'Debit', 'Active', 'ACC6002'),
            ('Import Purchase', None, 5, 6, 0.00, 'Debit', 'Active', 'ACC6003'),

            # EXPENSES (Type 7)
            ('Salary & Wages', None, 3, 7, 0.00, 'Debit', 'Active', 'ACC7001'),
            ('Rent Expense', None, 3, 7, 0.00, 'Debit', 'Active', 'ACC7002'),
            ('Electricity Expense', None, 3, 7, 0.00, 'Debit', 'Active', 'ACC7003'),
            ('Telephone & Internet', None, 3, 7, 0.00, 'Debit', 'Active', 'ACC7004'),
            ('Office Supplies', None, 3, 7, 0.00, 'Debit', 'Active', 'ACC7005'),
            ('Printing & Stationery', None, 3, 7, 0.00, 'Debit', 'Active', 'ACC7006'),
            ('Travelling Expenses', None, 3, 7, 0.00, 'Debit', 'Active', 'ACC7007'),
            ('Bank Charges', None, 2, 7, 0.00, 'Debit', 'Active', 'ACC7008'),
            ('Interest on Loan', None, 3, 7, 0.00, 'Debit', 'Active', 'ACC7009'),
            ('Depreciation', None, 3, 7, 0.00, 'Debit', 'Active', 'ACC7010'),

            # REVENUE (Type 8) - Other Income
            ('Interest Income', None, 2, 8, 0.00, 'Credit', 'Active', 'ACC8001'),
            ('Discount Received', None, 3, 8, 0.00, 'Credit', 'Active', 'ACC8002'),
            ('Miscellaneous Income', None, 3, 8, 0.00, 'Credit', 'Active', 'ACC8003'),
        ]

        cursor.executemany("""
            INSERT INTO account_master (
                account_name, account_group_id, book_code_id, account_type_id,
                opening_balance, balance_type, status, account_code
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, accounts)

        conn.commit()
        print(f"[OK] Seeded {len(accounts)} accounts")
        print("     - 10 Asset accounts (5 cash/bank + 5 other assets)")
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
    print("  • 10 Business Partners (5 customers, 5 suppliers)")
    print("  • 35 Chart of Accounts entries")
    print("  • Ready for transaction entry!")
    print("\n")


if __name__ == "__main__":
    main()
