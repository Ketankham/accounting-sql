"""
Database Migration Script
Migrates the companies table to the new schema with all required fields
Run this if you already have an existing database
"""

import mysql.connector
from mysql.connector import Error


def migrate_companies_table():
    """Migrate companies table to new schema"""
    print("\n" + "="*70)
    print("  COMPANIES TABLE MIGRATION")
    print("="*70 + "\n")

    try:
        # Connect to database
        connection = mysql.connector.connect(
            host='localhost',
            user='root',          # CHANGE THIS to your MySQL username
            password='Ketanmk@26',     # CHANGE THIS to your MySQL password
            database='login_system_db'
        )

        cursor = connection.cursor()

        print("✓ Connected to database\n")

        # Check if new columns already exist
        cursor.execute("""
            SELECT COLUMN_NAME
            FROM INFORMATION_SCHEMA.COLUMNS
            WHERE TABLE_SCHEMA = 'login_system_db'
            AND TABLE_NAME = 'companies'
        """)

        existing_columns = [row[0] for row in cursor.fetchall()]
        print(f"Found {len(existing_columns)} existing columns in companies table")

        # Define new columns to add
        new_columns = {
            'company_code': "VARCHAR(50) NOT NULL DEFAULT ''",
            'company_name': "VARCHAR(200) NOT NULL DEFAULT ''",
            'bill_to_address': "TEXT",
            'ship_to_address': "TEXT",
            'state': "VARCHAR(100)",
            'city': "VARCHAR(100)",
            'gst_number': "VARCHAR(50)",
            'pan_number': "VARCHAR(50)",
            'landline_number': "VARCHAR(20)",
            'mobile_number': "VARCHAR(20)",
            'email_address': "VARCHAR(100)",
            'website': "VARCHAR(200)",
            'logo_path': "VARCHAR(500)",
            'status': "VARCHAR(20) DEFAULT 'Active'"
        }

        # Add missing columns
        columns_added = 0
        for column_name, column_definition in new_columns.items():
            if column_name not in existing_columns:
                try:
                    query = f"ALTER TABLE companies ADD COLUMN {column_name} {column_definition}"
                    cursor.execute(query)
                    print(f"  ✓ Added column: {column_name}")
                    columns_added += 1
                except Error as e:
                    print(f"  ✗ Error adding {column_name}: {e}")

        if columns_added > 0:
            connection.commit()
            print(f"\n✓ Successfully added {columns_added} new column(s)")
        else:
            print("\n✓ All columns already exist - no migration needed")

        # Migrate data from 'name' to 'company_name' if needed
        if 'name' in existing_columns and 'company_name' in new_columns:
            cursor.execute("""
                UPDATE companies
                SET company_name = name
                WHERE company_name = '' OR company_name IS NULL
            """)
            rows_updated = cursor.rowcount
            if rows_updated > 0:
                connection.commit()
                print(f"✓ Migrated {rows_updated} company name(s) from 'name' to 'company_name'")

        # Update company_code for existing companies if empty
        cursor.execute("""
            SELECT id, COALESCE(company_name, name) as cname
            FROM companies
            WHERE company_code = '' OR company_code IS NULL
        """)
        companies_without_code = cursor.fetchall()

        if companies_without_code:
            print(f"\n✓ Generating company codes for {len(companies_without_code)} compan(ies)...")
            for company_id, company_name in companies_without_code:
                # Generate a company code from name
                if company_name:
                    # Take first 4 letters of company name and add ID
                    code_prefix = ''.join(filter(str.isalnum, company_name[:4])).upper()
                    company_code = f"{code_prefix}-{str(company_id).zfill(3)}"
                else:
                    company_code = f"COMP-{str(company_id).zfill(3)}"

                cursor.execute("""
                    UPDATE companies
                    SET company_code = %s
                    WHERE id = %s
                """, (company_code, company_id))
                print(f"  ✓ Generated code: {company_code}")

            connection.commit()

        # Add unique constraint to company_code if not exists
        try:
            cursor.execute("""
                ALTER TABLE companies
                ADD UNIQUE INDEX idx_company_code (company_code)
            """)
            connection.commit()
            print("\n✓ Added unique constraint to company_code")
        except Error as e:
            if "Duplicate key name" in str(e):
                print("\n✓ Unique constraint already exists on company_code")
            else:
                print(f"\n⚠ Warning adding unique constraint: {e}")

        # Show current companies
        cursor.execute("""
            SELECT id, company_code, COALESCE(company_name, name) as cname, status
            FROM companies
        """)
        companies = cursor.fetchall()

        print("\n" + "="*70)
        print("  CURRENT COMPANIES IN DATABASE")
        print("="*70)
        if companies:
            print(f"\n{'ID':<5} {'Code':<15} {'Name':<30} {'Status':<10}")
            print("-"*70)
            for company in companies:
                comp_id, code, name, status = company
                status = status if status else 'Active'
                print(f"{comp_id:<5} {code:<15} {name:<30} {status:<10}")
        else:
            print("\nNo companies found in database")

        print("\n" + "="*70)
        print("  MIGRATION COMPLETED SUCCESSFULLY")
        print("="*70)
        print("\nYour companies table is now ready to use!")
        print("\nYou can now run the application:")
        print("  python login_screen.py")
        print("\nNavigate to: Utilities → Companies")
        print("="*70 + "\n")

        cursor.close()
        connection.close()

        return True

    except Error as e:
        print(f"\n✗ Migration failed: {e}")
        print("\n⚠️  ALTERNATIVE SOLUTION:")
        print("  If you don't have important data, you can recreate the database:")
        print("  1. Run: python database/drop_database.py")
        print("  2. Run: python database/setup_login_db.py")
        print("="*70 + "\n")
        return False


if __name__ == "__main__":
    print("\n⚠️  IMPORTANT: This script will modify your database!")
    print("Make sure you have backed up important data if needed.\n")

    response = input("Continue with migration? (yes/no): ").lower()

    if response in ['yes', 'y']:
        migrate_companies_table()
    else:
        print("\nMigration cancelled.")
