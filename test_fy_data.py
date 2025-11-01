"""Test script to check financial year data"""
from database.financial_year_handler import FinancialYearHandler

handler = FinancialYearHandler()
if handler.connect():
    print("Database connected successfully")

    fys = handler.get_all_financial_years()
    print(f"\nFound {len(fys)} financial years:")
    print("-" * 80)

    if fys:
        for idx, fy in enumerate(fys, 1):
            print(f"\n{idx}. Financial Year:")
            print(f"   ID: {fy.get('id')}")
            print(f"   FY Code: {fy.get('fy_code')}")
            print(f"   Display Name: {fy.get('display_name')}")
            print(f"   Start Date: {fy.get('start_date')}")
            print(f"   End Date: {fy.get('end_date')}")
            print(f"   Status: {fy.get('status')}")
            print(f"   Created At: {fy.get('created_at')}")
    else:
        print("\nNo financial years found in database!")
        print("\nChecking if table exists...")

        try:
            handler.cursor.execute("SHOW TABLES LIKE 'financial_years'")
            result = handler.cursor.fetchone()
            if result:
                print("Table 'financial_years' exists")

                # Check table structure
                handler.cursor.execute("DESCRIBE financial_years")
                columns = handler.cursor.fetchall()
                print("\nTable structure:")
                for col in columns:
                    print(f"  {col}")

                # Count rows
                handler.cursor.execute("SELECT COUNT(*) as count FROM financial_years")
                count = handler.cursor.fetchone()
                print(f"\nTotal rows in table: {count['count']}")
            else:
                print("Table 'financial_years' does NOT exist!")
        except Exception as e:
            print(f"Error checking table: {e}")

    handler.disconnect()
else:
    print("Failed to connect to database")
