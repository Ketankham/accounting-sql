"""
Test script for Item Group Master functionality
"""

import sys
import io
from database.item_group_handler import ItemGroupHandler

# Fix encoding for Windows console
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


def test_item_group_operations():
    print("\n" + "="*70)
    print("Testing Item Group Master Functionality")
    print("="*70 + "\n")

    # Initialize handler
    handler = ItemGroupHandler()

    # Connect to database
    print("1. Connecting to database...")
    if not handler.connect():
        print("❌ Failed to connect to database")
        return
    print("✅ Connected successfully\n")

    # Test 1: Create item groups
    print("2. Creating test item groups...")
    test_groups = [
        {
            'item_group_code': 'FG01',
            'item_group_name': 'Finished Goods',
            'status': 'Active'
        },
        {
            'item_group_code': 'RM01',
            'item_group_name': 'Raw Materials',
            'status': 'Active'
        },
        {
            'item_group_code': 'WIP1',
            'item_group_name': 'Work in Progress',
            'status': 'Active'
        },
        {
            'item_group_code': 'PKG',
            'item_group_name': 'Packaging Materials',
            'status': 'Inactive'
        }
    ]

    created_ids = []
    for group_data in test_groups:
        success, message, item_id = handler.create_item_group(group_data)
        if success:
            print(f"   ✅ Created: {group_data['item_group_code']} - {group_data['item_group_name']}")
            created_ids.append(item_id)
        else:
            print(f"   ❌ Failed to create {group_data['item_group_code']}: {message}")

    print()

    # Test 2: List all item groups
    print("3. Listing all item groups...")
    all_groups = handler.get_all_item_groups()
    print(f"   Total item groups: {len(all_groups)}")
    for group in all_groups:
        status_icon = "🟢" if group['status'] == 'Active' else "🔴"
        print(f"   {status_icon} [{group['item_group_code']}] {group['item_group_name']} - {group['status']}")
    print()

    # Test 3: Get single item group
    if created_ids:
        print("4. Testing get single item group...")
        first_group = handler.get_item_group_by_id(created_ids[0])
        if first_group:
            print(f"   ✅ Retrieved: {first_group['item_group_code']} - {first_group['item_group_name']}")
        else:
            print(f"   ❌ Failed to retrieve item group")
        print()

    # Test 4: Update item group
    if created_ids:
        print("5. Testing update item group...")
        update_data = {
            'item_group_name': 'Finished Goods - Updated',
            'status': 'Inactive'
        }
        success, message = handler.update_item_group(created_ids[0], update_data)
        if success:
            print(f"   ✅ {message}")
            updated = handler.get_item_group_by_id(created_ids[0])
            print(f"   Updated values: {updated['item_group_name']} - {updated['status']}")
        else:
            print(f"   ❌ Failed to update: {message}")
        print()

    # Test 5: Test validation
    print("6. Testing validation...")

    # Test invalid code (too long)
    invalid_data = {
        'item_group_code': 'TOOLONG',
        'item_group_name': 'Test',
        'status': 'Active'
    }
    success, message, _ = handler.create_item_group(invalid_data)
    if not success:
        print(f"   ✅ Correctly rejected code > 4 chars: {message}")
    else:
        print(f"   ❌ Should have rejected long code")

    # Test duplicate code
    duplicate_data = {
        'item_group_code': 'RM01',
        'item_group_name': 'Duplicate Test',
        'status': 'Active'
    }
    success, message, _ = handler.create_item_group(duplicate_data)
    if not success:
        print(f"   ✅ Correctly rejected duplicate code: {message}")
    else:
        print(f"   ❌ Should have rejected duplicate code")
    print()

    # Test 6: List final state
    print("7. Final item group list:")
    all_groups = handler.get_all_item_groups()
    for idx, group in enumerate(all_groups, 1):
        status_icon = "🟢" if group['status'] == 'Active' else "🔴"
        print(f"   {idx}. {status_icon} [{group['item_group_code']}] {group['item_group_name']} - {group['status']}")

    # Cleanup
    handler.disconnect()
    print("\n" + "="*70)
    print("Test completed successfully!")
    print("="*70 + "\n")


if __name__ == "__main__":
    test_item_group_operations()
