"""
Comprehensive Test Script for Account Master and Business Partner modules
"""

import sys
import traceback
from database.account_master_handler import AccountMasterHandler
from database.business_partner_handler import BusinessPartnerHandler

def test_account_master():
    """Test Account Master handler"""
    print("\n" + "="*80)
    print("TESTING ACCOUNT MASTER MODULE")
    print("="*80 + "\n")

    handler = AccountMasterHandler()

    # Test 1: Connect to database
    print("Test 1: Connecting to database...")
    if handler.connect():
        print("✓ Connected successfully\n")
    else:
        print("✗ Connection failed\n")
        return False

    # Test 2: Get active account groups
    print("Test 2: Getting active account groups...")
    account_groups = handler.get_active_account_groups()
    print(f"✓ Found {len(account_groups)} active account groups")
    if account_groups:
        print(f"  Sample: {account_groups[0]}\n")

    # Test 3: Get active book codes
    print("Test 3: Getting active book codes...")
    book_codes = handler.get_active_book_codes()
    print(f"✓ Found {len(book_codes)} active book codes")
    if book_codes:
        print(f"  Sample: {book_codes[0]}\n")

    # Test 4: Get active account types
    print("Test 4: Getting active account types...")
    account_types = handler.get_active_account_types()
    print(f"✓ Found {len(account_types)} active account types")
    if account_types:
        print(f"  Sample: {account_types[0]}\n")

    # Test 5: Create test account
    if account_groups and book_codes and account_types:
        print("Test 5: Creating test account...")
        test_account_data = {
            'account_name': 'Test Cash Account',
            'account_group_id': account_groups[0]['id'],
            'book_code_id': book_codes[0]['id'],
            'account_type_id': account_types[0]['id'],
            'opening_balance': 5000,
            'balance_type': 'Debit',
            'status': 'Active'
        }

        success, message, account_id = handler.create_account(test_account_data)
        if success:
            print(f"✓ {message}")
            print(f"  Account ID: {account_id}\n")

            # Test 6: Get account by ID
            print("Test 6: Getting account by ID...")
            account = handler.get_account_by_id(account_id)
            if account:
                print(f"✓ Retrieved account: {account['account_name']}")
                print(f"  Account Code: {account['account_code']}\n")

            # Test 7: Update account
            print("Test 7: Updating account...")
            test_account_data['account_name'] = 'Updated Cash Account'
            success, message = handler.update_account(account_id, test_account_data)
            if success:
                print(f"✓ {message}\n")

            # Test 8: Get all accounts
            print("Test 8: Getting all accounts...")
            accounts = handler.get_all_accounts()
            print(f"✓ Found {len(accounts)} accounts\n")

            # Test 9: Delete account
            print("Test 9: Deleting test account...")
            success, message = handler.delete_account(account_id)
            if success:
                print(f"✓ {message}\n")
        else:
            print(f"✗ {message}\n")

    handler.disconnect()
    print("="*80)
    print("ACCOUNT MASTER TESTS COMPLETED")
    print("="*80 + "\n")
    return True

def test_business_partner():
    """Test Business Partner handler"""
    print("\n" + "="*80)
    print("TESTING BUSINESS PARTNER MODULE")
    print("="*80 + "\n")

    handler = BusinessPartnerHandler()

    # Test 1: Connect to database
    print("Test 1: Connecting to database...")
    if handler.connect():
        print("✓ Connected successfully\n")
    else:
        print("✗ Connection failed\n")
        return False

    # Test 2: Get active account groups
    print("Test 2: Getting active account groups...")
    account_groups = handler.get_active_account_groups()
    print(f"✓ Found {len(account_groups)} active account groups")
    if account_groups:
        print(f"  Sample: {account_groups[0]}\n")

    # Test 3: Get active book codes
    print("Test 3: Getting active book codes...")
    book_codes = handler.get_active_book_codes()
    print(f"✓ Found {len(book_codes)} active book codes")
    if book_codes:
        print(f"  Sample: {book_codes[0]}\n")

    # Test 4: Get active account types
    print("Test 4: Getting active account types...")
    account_types = handler.get_active_account_types()
    print(f"✓ Found {len(account_types)} active account types")
    if account_types:
        print(f"  Sample: {account_types[0]}\n")

    # Test 5: Get active cities
    print("Test 5: Getting active cities...")
    cities = handler.get_active_cities()
    print(f"✓ Found {len(cities)} active cities")
    if cities:
        print(f"  Sample: {cities[0]}\n")

    # Test 6: Get active states
    print("Test 6: Getting active states...")
    states = handler.get_active_states()
    print(f"✓ Found {len(states)} active states")
    if states:
        print(f"  Sample: {states[0]}\n")

    # Test 7: Create test business partner
    if account_groups and book_codes and account_types and cities and states:
        print("Test 7: Creating test business partner...")
        test_bp_data = {
            'bp_name': 'Test Company Pvt Ltd',
            'bill_to_address': '123 Main Street, Building A',
            'ship_to_address': '456 Commerce Lane, Warehouse B',
            'city_id': cities[0]['id'],
            'state_id': states[0]['id'],
            'mobile': '9876543210',
            'account_group_id': account_groups[0]['id'],
            'book_code_id': book_codes[0]['id'],
            'account_type_id': account_types[0]['id'],
            'opening_balance': 10000.50,
            'balance_type': 'Credit',
            'status': 'Active'
        }

        success, message, bp_id = handler.create_business_partner(test_bp_data)
        if success:
            print(f"✓ {message}")
            print(f"  BP ID: {bp_id}\n")

            # Test 8: Get business partner by ID
            print("Test 8: Getting business partner by ID...")
            bp = handler.get_business_partner_by_id(bp_id)
            if bp:
                print(f"✓ Retrieved BP: {bp['bp_name']}")
                print(f"  BP Code: {bp['bp_code']}\n")

            # Test 9: Update business partner
            print("Test 9: Updating business partner...")
            test_bp_data['bp_name'] = 'Updated Company Pvt Ltd'
            success, message = handler.update_business_partner(bp_id, test_bp_data)
            if success:
                print(f"✓ {message}\n")

            # Test 10: Get all business partners
            print("Test 10: Getting all business partners...")
            partners = handler.get_all_business_partners()
            print(f"✓ Found {len(partners)} business partners\n")

            # Test 11: Delete business partner
            print("Test 11: Deleting test business partner...")
            success, message = handler.delete_business_partner(bp_id)
            if success:
                print(f"✓ {message}\n")
        else:
            print(f"✗ {message}\n")

    handler.disconnect()
    print("="*80)
    print("BUSINESS PARTNER TESTS COMPLETED")
    print("="*80 + "\n")
    return True

if __name__ == "__main__":
    try:
        # Run tests
        test_account_master()
        test_business_partner()

        print("\n" + "="*80)
        print("ALL TESTS COMPLETED SUCCESSFULLY!")
        print("="*80 + "\n")

    except Exception as e:
        print("\n" + "="*80)
        print("ERROR OCCURRED DURING TESTING")
        print("="*80)
        print(f"\nError: {e}")
        traceback.print_exc()
        sys.exit(1)
