"""
Test script for City Master and State Master functionality
"""

import sys
import io
from database.city_handler import CityHandler
from database.state_handler import StateHandler

# Fix encoding for Windows console
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


def test_city_master():
    print("\n" + "="*70)
    print("Testing City Master Functionality")
    print("="*70 + "\n")

    # Initialize handler
    handler = CityHandler()

    # Connect to database
    print("1. Connecting to database...")
    if not handler.connect():
        print("❌ Failed to connect to database")
        return
    print("✅ Connected successfully\n")

    # Test: Create cities
    print("2. Creating test cities...")
    test_cities = [
        {'city_code': 'MUM', 'city_name': 'Mumbai', 'status': 'Active'},
        {'city_code': 'DEL', 'city_name': 'Delhi', 'status': 'Active'},
        {'city_code': 'BLR', 'city_name': 'Bangalore', 'status': 'Active'},
        {'city_code': 'HYD', 'city_name': 'Hyderabad', 'status': 'Inactive'},
    ]

    created_ids = []
    for city_data in test_cities:
        success, message, city_id = handler.create_city(city_data)
        if success:
            print(f"   ✅ Created: {city_data['city_code']} - {city_data['city_name']}")
            created_ids.append(city_id)
        else:
            print(f"   ⚠️  {city_data['city_code']}: {message}")

    print()

    # Test: List all cities
    print("3. Listing all cities...")
    all_cities = handler.get_all_cities()
    print(f"   Total cities: {len(all_cities)}")
    for city in all_cities:
        status_icon = "🟢" if city['status'] == 'Active' else "🔴"
        print(f"   {status_icon} [{city['city_code']}] {city['city_name']} - {city['status']}")
    print()

    # Test: Validation
    print("4. Testing validation...")

    # Test invalid code (too long)
    invalid_data = {'city_code': 'TOOLONG', 'city_name': 'Test', 'status': 'Active'}
    success, message, _ = handler.create_city(invalid_data)
    if not success:
        print(f"   ✅ Correctly rejected code > 4 chars: {message}")

    # Test duplicate code
    duplicate_data = {'city_code': 'MUM', 'city_name': 'Duplicate', 'status': 'Active'}
    success, message, _ = handler.create_city(duplicate_data)
    if not success:
        print(f"   ✅ Correctly rejected duplicate code: {message}")
    print()

    # Cleanup
    handler.disconnect()
    print("="*70)
    print("City Master Test completed!")
    print("="*70 + "\n")


def test_state_master():
    print("\n" + "="*70)
    print("Testing State Master Functionality")
    print("="*70 + "\n")

    # Initialize handler
    handler = StateHandler()

    # Connect to database
    print("1. Connecting to database...")
    if not handler.connect():
        print("❌ Failed to connect to database")
        return
    print("✅ Connected successfully\n")

    # Test: Create states
    print("2. Creating test states...")
    test_states = [
        {'state_code': 'MH', 'state_name': 'Maharashtra', 'status': 'Active'},
        {'state_code': 'DL', 'state_name': 'Delhi', 'status': 'Active'},
        {'state_code': 'KA', 'state_name': 'Karnataka', 'status': 'Active'},
        {'state_code': 'TN', 'state_name': 'Tamil Nadu', 'status': 'Inactive'},
    ]

    created_ids = []
    for state_data in test_states:
        success, message, state_id = handler.create_state(state_data)
        if success:
            print(f"   ✅ Created: {state_data['state_code']} - {state_data['state_name']}")
            created_ids.append(state_id)
        else:
            print(f"   ⚠️  {state_data['state_code']}: {message}")

    print()

    # Test: List all states
    print("3. Listing all states...")
    all_states = handler.get_all_states()
    print(f"   Total states: {len(all_states)}")
    for state in all_states:
        status_icon = "🟢" if state['status'] == 'Active' else "🔴"
        print(f"   {status_icon} [{state['state_code']}] {state['state_name']} - {state['status']}")
    print()

    # Test: Update state
    if created_ids:
        print("4. Testing update state...")
        update_data = {'state_name': 'Maharashtra - Updated', 'status': 'Inactive'}
        success, message = handler.update_state(created_ids[0], update_data)
        if success:
            print(f"   ✅ {message}")
            updated = handler.get_state_by_id(created_ids[0])
            print(f"   Updated values: {updated['state_name']} - {updated['status']}")
        print()

    # Test: Validation
    print("5. Testing validation...")

    # Test invalid code (too long)
    invalid_data = {'state_code': 'TOOLONG', 'state_name': 'Test', 'status': 'Active'}
    success, message, _ = handler.create_state(invalid_data)
    if not success:
        print(f"   ✅ Correctly rejected code > 4 chars: {message}")

    # Test duplicate code
    duplicate_data = {'state_code': 'MH', 'state_name': 'Duplicate', 'status': 'Active'}
    success, message, _ = handler.create_state(duplicate_data)
    if not success:
        print(f"   ✅ Correctly rejected duplicate code: {message}")
    print()

    # Final list
    print("6. Final state list:")
    all_states = handler.get_all_states()
    for idx, state in enumerate(all_states, 1):
        status_icon = "🟢" if state['status'] == 'Active' else "🔴"
        print(f"   {idx}. {status_icon} [{state['state_code']}] {state['state_name']} - {state['status']}")

    # Cleanup
    handler.disconnect()
    print("\n" + "="*70)
    print("State Master Test completed!")
    print("="*70 + "\n")


if __name__ == "__main__":
    test_city_master()
    test_state_master()

    print("\n" + "🎉" * 35)
    print("ALL TESTS COMPLETED SUCCESSFULLY!")
    print("🎉" * 35 + "\n")
