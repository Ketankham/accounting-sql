"""
Drop Database Script
Use this to completely remove the database and start fresh
WARNING: This will delete all data!
"""

import mysql.connector
from mysql.connector import Error


def drop_database():
    """Drop the login_system_db database"""
    print("\n" + "="*70)
    print("  ⚠️  DATABASE DROP UTILITY")
    print("="*70 + "\n")

    print("⚠️  WARNING: This will DELETE the entire 'login_system_db' database!")
    print("⚠️  All users, companies, and other data will be LOST!")
    print("\n" + "="*70 + "\n")

    response = input("Are you SURE you want to continue? Type 'DELETE' to confirm: ")

    if response != 'DELETE':
        print("\nDatabase drop cancelled. No changes made.")
        return False

    try:
        # Connect without specifying database
        connection = mysql.connector.connect(
            host='localhost',
            user='root',          # CHANGE THIS to your MySQL username
            password='Ketanmk@26'      # CHANGE THIS to your MySQL password
        )

        cursor = connection.cursor()

        # Drop database
        database_name = 'login_system_db'
        print(f"\nDropping database '{database_name}'...")

        cursor.execute(f"DROP DATABASE IF EXISTS {database_name}")
        print(f"✓ Database '{database_name}' has been dropped")

        cursor.close()
        connection.close()

        print("\n" + "="*70)
        print("  DATABASE DROPPED SUCCESSFULLY")
        print("="*70)
        print("\nNext steps:")
        print("  1. Run: python database/setup_login_db.py")
        print("  2. This will create a fresh database with sample data")
        print("="*70 + "\n")

        return True

    except Error as e:
        print(f"\n✗ Error: {e}")
        return False


if __name__ == "__main__":
    drop_database()
