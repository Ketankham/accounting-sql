"""
Clear Master Data Utility
Removes all Master Data entries while preserving Utilities data (Companies and Financial Years)
"""

import sqlite3
import sys
from pathlib import Path

# Add parent directory to path to import config
sys.path.append(str(Path(__file__).parent.parent))
from database.config import DB_PATH


def clear_master_data():
    """
    Clear all Master Data tables while preserving:
    - companies (Utilities)
    - financial_years (Utilities)
    - users (Authentication)
    - book_codes (Static reference data)
    - account_types (Static reference data)

    Master Data tables to be cleared:
    - items
    - item_groups
    - item_types
    - item_companies (manufacturers)
    - uom
    - account_master
    - account_groups
    - business_partners
    - cities
    - states
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Disable foreign key constraints temporarily
        cursor.execute("PRAGMA foreign_keys = OFF")

        # List of Master Data tables to clear
        master_data_tables = [
            'items',
            'item_groups',
            'item_types',
            'item_companies',
            'uom',
            'account_master',
            'account_groups',
            'business_partners',
            'cities',
            'states'
        ]

        print("="*70)
        print("CLEARING MASTER DATA")
        print("="*70)
        print("\nPreserving:")
        print("  - Companies (Utilities)")
        print("  - Financial Years (Utilities)")
        print("  - Users (Authentication)")
        print("  - Book Codes (Static Data)")
        print("  - Account Types (Static Data)")
        print("\nClearing Master Data tables:")

        total_deleted = 0

        for table in master_data_tables:
            # Check if table exists
            cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table,))
            if not cursor.fetchone():
                print(f"  [WARNING] Table '{table}' does not exist - skipping")
                continue

            # Count rows before deletion
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            row_count = cursor.fetchone()[0]

            if row_count == 0:
                print(f"  [OK] {table}: Already empty")
                continue

            # Delete all rows
            cursor.execute(f"DELETE FROM {table}")
            print(f"  [OK] {table}: Deleted {row_count} rows")
            total_deleted += row_count

        # Re-enable foreign key constraints
        cursor.execute("PRAGMA foreign_keys = ON")

        # Commit changes
        conn.commit()

        print("\n" + "="*70)
        print(f"TOTAL ROWS DELETED: {total_deleted}")
        print("="*70)
        print("\n[OK] Master Data cleared successfully!")
        print("[OK] Utilities data (Companies, Financial Years) preserved")
        print("[OK] Static data (Book Codes, Account Types) preserved")
        print("[OK] User authentication data preserved")

        conn.close()
        return True, f"Successfully cleared {total_deleted} master data entries"

    except sqlite3.Error as e:
        print(f"\n[ERROR] Failed to clear master data: {e}")
        if conn:
            conn.rollback()
            conn.close()
        return False, str(e)


def confirm_and_clear():
    """Ask for confirmation before clearing data"""
    print("\n" + "="*70)
    print("WARNING: MASTER DATA DELETION")
    print("="*70)
    print("\nThis will DELETE all entries from the following tables:")
    print("  - Items")
    print("  - Item Groups")
    print("  - Item Types")
    print("  - Manufacturers (Item Companies)")
    print("  - Units of Measure")
    print("  - Account Master")
    print("  - Account Groups")
    print("  - Business Partners")
    print("  - Cities")
    print("  - States")
    print("\nThe following will be PRESERVED:")
    print("  - Companies")
    print("  - Financial Years")
    print("  - Users")
    print("  - Book Codes")
    print("  - Account Types")

    response = input("\nAre you sure you want to proceed? (yes/no): ")

    if response.lower() in ['yes', 'y']:
        print("\nProceeding with master data deletion...")
        return clear_master_data()
    else:
        print("\nOperation cancelled.")
        return False, "Operation cancelled by user"


if __name__ == "__main__":
    # Run with confirmation
    confirm_and_clear()
