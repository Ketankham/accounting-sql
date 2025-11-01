"""
Migrate financial years data from MySQL to SQLite
This script will copy all financial year records from MySQL to SQLite
"""

import sqlite3
import mysql.connector
from config import DB_PATH, DB_CONFIG


def migrate_financial_years():
    """Migrate financial years from MySQL to SQLite"""

    mysql_conn = None
    sqlite_conn = None

    try:
        # Connect to MySQL
        print("Connecting to MySQL...")
        mysql_conn = mysql.connector.connect(**DB_CONFIG)
        mysql_cursor = mysql_conn.cursor(dictionary=True)
        print("✓ Connected to MySQL")

        # Connect to SQLite
        print("Connecting to SQLite...")
        sqlite_conn = sqlite3.connect(DB_PATH)
        sqlite_cursor = sqlite_conn.cursor()
        print(f"✓ Connected to SQLite at: {DB_PATH}")

        # Create SQLite table if it doesn't exist
        print("\nCreating SQLite table...")
        create_table_query = """
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
        """
        sqlite_cursor.execute(create_table_query)
        sqlite_conn.commit()
        print("✓ SQLite table created/verified")

        # Fetch data from MySQL
        print("\nFetching data from MySQL...")
        mysql_cursor.execute("""
            SELECT id, fy_code, display_name, start_date, end_date, status, created_at
            FROM financial_years
            ORDER BY id
        """)
        mysql_rows = mysql_cursor.fetchall()
        print(f"✓ Found {len(mysql_rows)} records in MySQL")

        if not mysql_rows:
            print("\n⚠ No data to migrate from MySQL")
            return

        # Insert into SQLite
        print("\nMigrating data to SQLite...")
        migrated_count = 0
        skipped_count = 0

        for row in mysql_rows:
            try:
                # Check if record already exists in SQLite
                sqlite_cursor.execute("SELECT id FROM financial_years WHERE fy_code = ?",
                                     (row['fy_code'],))
                exists = sqlite_cursor.fetchone()

                if exists:
                    print(f"  ⊘ Skipping {row['fy_code']} - already exists in SQLite")
                    skipped_count += 1
                    continue

                # Insert into SQLite
                sqlite_cursor.execute("""
                    INSERT INTO financial_years
                    (fy_code, display_name, start_date, end_date, status, created_at)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    row['fy_code'],
                    row['display_name'],
                    row['start_date'],
                    row['end_date'],
                    row['status'],
                    row['created_at']
                ))

                print(f"  ✓ Migrated: {row['fy_code']} - {row['display_name']}")
                migrated_count += 1

            except sqlite3.Error as e:
                print(f"  ✗ Error migrating {row['fy_code']}: {e}")

        sqlite_conn.commit()

        # Summary
        print("\n" + "=" * 60)
        print("MIGRATION COMPLETE")
        print("=" * 60)
        print(f"Total records in MySQL: {len(mysql_rows)}")
        print(f"Successfully migrated: {migrated_count}")
        print(f"Skipped (already exist): {skipped_count}")
        print(f"SQLite database location: {DB_PATH}")

        # Verify SQLite data
        sqlite_cursor.execute("SELECT COUNT(*) FROM financial_years")
        total_sqlite = sqlite_cursor.fetchone()[0]
        print(f"Total records now in SQLite: {total_sqlite}")

    except mysql.connector.Error as e:
        print(f"✗ MySQL Error: {e}")
        print("\nNote: If MySQL table doesn't exist, that's okay!")
        print("You can create new financial years directly in the application.")

    except sqlite3.Error as e:
        print(f"✗ SQLite Error: {e}")

    finally:
        # Clean up connections
        if mysql_conn and mysql_conn.is_connected():
            mysql_cursor.close()
            mysql_conn.close()
            print("\n✓ MySQL connection closed")

        if sqlite_conn:
            sqlite_conn.close()
            print("✓ SQLite connection closed")


if __name__ == "__main__":
    print("=" * 60)
    print("FINANCIAL YEARS MIGRATION: MySQL → SQLite")
    print("=" * 60)
    print()
    migrate_financial_years()
