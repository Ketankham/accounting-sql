"""
Test script for Account Group functionality
"""

from database.account_group_handler import AccountGroupHandler


def test_account_group_handler():
    """Test the Account Group Handler"""
    print("="*70)
    print("Testing Account Group Handler")
    print("="*70)

    handler = AccountGroupHandler()

    # Connect to database
    if not handler.connect():
        print("Failed to connect to database")
        return

    print("\n1. Testing AG Code Generation:")
    print("-" * 70)

    # Test AG code generation for different scenarios
    test_cases = [
        ("Sales", "Trading A/C"),
        ("Purchase", "Trading A/C"),
        ("Salary", "P&L Account"),
        ("Assets", "Balance Sheet"),
        ("Stock", "Trading A/C")
    ]

    for name, ag_type in test_cases:
        ag_code = handler.generate_ag_code(name, ag_type)
        print(f"Name: {name:20} | Type: {ag_type:20} | AG Code: {ag_code}")

    print("\n2. Testing Create Account Group:")
    print("-" * 70)

    # Create a test account group
    test_data = {
        'name': 'Sales',
        'account_group_type': 'Trading A/C',
        'status': 'Active'
    }

    success, message, ag_id = handler.create_account_group(test_data)
    print(f"Create Status: {success}")
    print(f"Message: {message}")
    print(f"Account Group ID: {ag_id}")

    print("\n3. Testing Get All Account Groups:")
    print("-" * 70)

    # Get all account groups
    account_groups = handler.get_all_account_groups()
    print(f"Total Account Groups: {len(account_groups)}")

    for ag in account_groups:
        print(f"ID: {ag['id']:3} | Name: {ag['name']:20} | Type: {ag['account_group_type']:20} | AG Code: {ag['ag_code']:8} | Status: {ag['status']}")

    print("\n4. Testing Get by Type:")
    print("-" * 70)

    trading_groups = handler.get_by_type('Trading A/C')
    print(f"Trading A/C Groups: {len(trading_groups)}")
    for ag in trading_groups:
        print(f"  - {ag['name']} ({ag['ag_code']})")

    # Cleanup
    handler.disconnect()
    print("\n" + "="*70)
    print("Test Completed Successfully!")
    print("="*70)


if __name__ == "__main__":
    test_account_group_handler()
