"""
Create financial_years table in SQLite
Run this script to create the financial years table in the database
"""

import sqlite3
from config import DB_PATH


def create_financial_years_table():
    """Create financial_years table"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

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

        cursor.execute(create_table_query)
        conn.commit()

        print("Financial years table created successfully")
        print(f"Database location: {DB_PATH}")

        cursor.close()
        conn.close()

    except sqlite3.Error as e:
        print(f"Error creating financial years table: {e}")


if __name__ == "__main__":
    create_financial_years_table()
