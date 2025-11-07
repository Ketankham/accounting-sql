"""
View Demo Data - Display seeded business partners and accounts
"""

import sqlite3
import sys
sys.path.insert(0, '.')
from database.config import DB_PATH


def view_business_partners():
    """Display all business partners"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("""
        SELECT bp_code, bp_name, mobile, opening_balance, balance_type,
               account_type_id, status
        FROM business_partners
        ORDER BY bp_code
    """)

    partners = cursor.fetchall()

    print("\n" + "="*90)
    print("BUSINESS PARTNERS ({} records)".format(len(partners)))
    print("="*90)
    print(f"{'Code':<10} {'Name':<30} {'Mobile':<15} {'Balance':<15} {'Type':<8} {'Status':<8}")
    print("-"*90)

    for p in partners:
        balance_str = f"Rs.{p['opening_balance']:,.2f} {p['balance_type'][:2]}"
        type_label = "Customer" if p['account_type_id'] == 3 else "Supplier"
        print(f"{p['bp_code']:<10} {p['bp_name']:<30} {p['mobile']:<15} {balance_str:<15} {type_label:<8} {p['status']:<8}")

    conn.close()


def view_account_master():
    """Display all accounts"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("""
        SELECT account_code, account_name, book_code_id, account_type_id,
               opening_balance, balance_type, status
        FROM account_master
        ORDER BY account_code
    """)

    accounts = cursor.fetchall()

    print("\n" + "="*110)
    print("CHART OF ACCOUNTS ({} records)".format(len(accounts)))
    print("="*110)
    print(f"{'Code':<10} {'Account Name':<35} {'Book':<8} {'Type':<8} {'Balance':<18} {'Status':<8}")
    print("-"*110)

    for a in accounts:
        balance_str = f"Rs.{a['opening_balance']:,.2f} {a['balance_type'][:2]}"
        print(f"{a['account_code']:<10} {a['account_name']:<35} {a['book_code_id']:<8} {a['account_type_id']:<8} {balance_str:<18} {a['status']:<8}")

    conn.close()


def view_summary():
    """Display summary statistics"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Business partners summary
    cursor.execute("SELECT account_type_id, COUNT(*), SUM(opening_balance) FROM business_partners GROUP BY account_type_id")
    bp_summary = cursor.fetchall()

    # Accounts summary
    cursor.execute("SELECT account_type_id, COUNT(*), SUM(opening_balance) FROM account_master GROUP BY account_type_id")
    acc_summary = cursor.fetchall()

    print("\n" + "="*70)
    print("SUMMARY STATISTICS")
    print("="*70)

    print("\nBusiness Partners:")
    for type_id, count, total in bp_summary:
        type_label = "Customers (Debtors)" if type_id == 3 else "Suppliers (Creditors)"
        print(f"  {type_label}: {count} records, Total: Rs.{total:,.2f}")

    print("\nChart of Accounts:")
    account_type_names = {
        1: "Assets",
        2: "Liability",
        3: "Debtors",
        4: "Creditors",
        5: "Sale",
        6: "Purchase",
        7: "Expenses",
        8: "Revenue"
    }
    for type_id, count, total in acc_summary:
        type_label = account_type_names.get(type_id, f"Type {type_id}")
        print(f"  {type_label}: {count} records, Total: Rs.{total:,.2f}")

    conn.close()


def main():
    """Display all demo data"""
    print("\n" + "="*70)
    print("  VIEWING DEMO DATA")
    print("="*70)

    view_business_partners()
    view_account_master()
    view_summary()

    print("\n" + "="*70)
    print("  Demo data displayed successfully!")
    print("  You can now use this data in the application.")
    print("="*70)
    print()


if __name__ == "__main__":
    main()
