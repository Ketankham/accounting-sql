"""
Insert test financial year data into SQLite database
"""

import sqlite3
import os
import sys

# Fix Unicode encoding for Windows console
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from config import DB_PATH

def insert_test_data():
    """Insert sample financial years for testing"""

    print("="*70)
    print("INSERTING TEST DATA INTO SQLite DATABASE")
    print("="*70)

    abs_path = os.path.abspath(DB_PATH)
    print(f"\nDatabase path: {abs_path}")
    print(f"File exists: {os.path.exists(abs_path)}")

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        print("✓ Connected to database\n")

        # Create table if it doesn't exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS financial_years (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fy_code TEXT NOT NULL UNIQUE,
                display_name TEXT NOT NULL,
                start_date DATE NOT NULL,
                end_date DATE NOT NULL,
                status TEXT DEFAULT 'Active' CHECK(status IN ('Active', 'Inactive')),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        print("✓ Table verified\n")

        # Test data
        test_data = [
            ('FY2324', 'Financial Year 2023-2024', '2023-04-01', '2024-03-31', 'Inactive'),
            ('FY2425', 'Financial Year 2024-2025', '2024-04-01', '2025-03-31', 'Active'),
            ('FY2526', 'Financial Year 2025-2026', '2025-04-01', '2026-03-31', 'Active'),
        ]

        inserted = 0
        skipped = 0

        for fy_code, display_name, start_date, end_date, status in test_data:
            try:
                # Check if already exists
                cursor.execute("SELECT id FROM financial_years WHERE fy_code = ?", (fy_code,))
                if cursor.fetchone():
                    print(f"⊘ Skipped {fy_code} - already exists")
                    skipped += 1
                    continue

                # Insert
                cursor.execute("""
                    INSERT INTO financial_years (fy_code, display_name, start_date, end_date, status)
                    VALUES (?, ?, ?, ?, ?)
                """, (fy_code, display_name, start_date, end_date, status))

                conn.commit()
                print(f"✓ Inserted: {fy_code} - {display_name} ({status})")
                inserted += 1

            except sqlite3.Error as e:
                print(f"✗ Error inserting {fy_code}: {e}")

        # Verify
        print("\n" + "="*70)
        print("VERIFICATION")
        print("="*70)
        cursor.execute("SELECT COUNT(*) FROM financial_years")
        total = cursor.fetchone()[0]
        print(f"\nTotal records in database: {total}")
        print(f"Inserted in this run: {inserted}")
        print(f"Skipped (already existed): {skipped}")

        # Show all records
        print("\nAll Financial Years in Database:")
        print("-"*70)
        cursor.execute("SELECT * FROM financial_years ORDER BY start_date")
        rows = cursor.fetchall()

        for row in rows:
            print(f"ID: {row[0]}, Code: {row[1]}, Name: {row[2]}")
            print(f"  Period: {row[3]} to {row[4]}, Status: {row[5]}")

        cursor.close()
        conn.close()

        print("\n" + "="*70)
        print("✓ TEST DATA INSERTED SUCCESSFULLY")
        print("="*70)
        print(f"\nDatabase location: {abs_path}")
        print("\nYou can now run your application and the financial years should display!")

    except sqlite3.Error as e:
        print(f"\n✗ Error: {e}")

if __name__ == "__main__":
    insert_test_data()
