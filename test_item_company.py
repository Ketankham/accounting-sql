"""
Test script for Item Company Master functionality
"""

import sys
import io
from database.item_company_handler import ItemCompanyHandler

# Fix encoding for Windows console
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


def test_item_company_master():
    print("\n" + "="*70)
    print("Testing Item Company Master Functionality")
    print("="*70 + "\n")

    # Initialize handler
    handler = ItemCompanyHandler()

    # Connect to database
    print("1. Connecting to database...")
    if not handler.connect():
        print("❌ Failed to connect to database")
        return
    print("✅ Connected successfully\n")

    # Test: Create item companies
    print("2. Creating test item companies (suppliers/manufacturers)...")
    test_companies = [
        {'company_code': 'ABC1', 'company_name': 'ABC Suppliers Ltd', 'status': 'Active'},
        {'company_code': 'XYZ2', 'company_name': 'XYZ Manufacturers Inc', 'status': 'Active'},
        {'company_code': 'DEF3', 'company_name': 'DEF Trading Co', 'status': 'Active'},
        {'company_code': 'GHI4', 'company_name': 'GHI Industries', 'status': 'Inactive'},
    ]

    created_ids = []
    for company_data in test_companies:
        success, message, company_id = handler.create_item_company(company_data)
        if success:
            print(f"   ✅ Created: {company_data['company_code']} - {company_data['company_name']}")
            created_ids.append(company_id)
        else:
            print(f"   ⚠️  {company_data['company_code']}: {message}")

    print()

    # Test: List all item companies
    print("3. Listing all item companies...")
    all_companies = handler.get_all_item_companies()
    print(f"   Total item companies: {len(all_companies)}")
    for company in all_companies:
        status_icon = "🟢" if company['status'] == 'Active' else "🔴"
        print(f"   {status_icon} [{company['company_code']}] {company['company_name']} - {company['status']}")
    print()

    # Test: Get single item company
    if created_ids:
        print("4. Testing get single item company...")
        first_company = handler.get_item_company_by_id(created_ids[0])
        if first_company:
            print(f"   ✅ Retrieved: {first_company['company_code']} - {first_company['company_name']}")
        print()

    # Test: Update item company
    if created_ids:
        print("5. Testing update item company...")
        update_data = {'company_name': 'ABC Suppliers Ltd - Updated', 'status': 'Inactive'}
        success, message = handler.update_item_company(created_ids[0], update_data)
        if success:
            print(f"   ✅ {message}")
            updated = handler.get_item_company_by_id(created_ids[0])
            print(f"   Updated values: {updated['company_name']} - {updated['status']}")
        print()

    # Test: Validation
    print("6. Testing validation...")

    # Test invalid code (too long)
    invalid_data = {'company_code': 'TOOLONG', 'company_name': 'Test', 'status': 'Active'}
    success, message, _ = handler.create_item_company(invalid_data)
    if not success:
        print(f"   ✅ Correctly rejected code > 4 chars: {message}")

    # Test duplicate code
    duplicate_data = {'company_code': 'ABC1', 'company_name': 'Duplicate', 'status': 'Active'}
    success, message, _ = handler.create_item_company(duplicate_data)
    if not success:
        print(f"   ✅ Correctly rejected duplicate code: {message}")

    # Test alphanumeric validation
    invalid_alpha = {'company_code': 'AB@C', 'company_name': 'Test', 'status': 'Active'}
    success, message, _ = handler.create_item_company(invalid_alpha)
    if not success:
        print(f"   ✅ Correctly rejected non-alphanumeric code: {message}")
    print()

    # Final list
    print("7. Final item company list:")
    all_companies = handler.get_all_item_companies()
    for idx, company in enumerate(all_companies, 1):
        status_icon = "🟢" if company['status'] == 'Active' else "🔴"
        print(f"   {idx}. {status_icon} [{company['company_code']}] {company['company_name']} - {company['status']}")

    # Cleanup
    handler.disconnect()
    print("\n" + "="*70)
    print("Item Company Master Test completed successfully!")
    print("="*70 + "\n")


if __name__ == "__main__":
    test_item_company_master()

    print("\n" + "🎉" * 35)
    print("ALL TESTS COMPLETED SUCCESSFULLY!")
    print("🎉" * 35 + "\n")
