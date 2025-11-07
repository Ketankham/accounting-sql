"""
Comprehensive test for Account Group with multiple entries and serial incrementation
"""

from database.account_group_handler import AccountGroupHandler


def test_comprehensive():
    """Test with multiple account groups to verify serial incrementation"""
    print("="*70)
    print("Comprehensive Account Group Test")
    print("="*70)

    handler = AccountGroupHandler()

    if not handler.connect():
        print("Failed to connect to database")
        return

    # Test data with multiple entries having same first letter and type
    test_groups = [
        {"name": "Sales", "account_group_type": "Trading A/C", "status": "Active"},
        {"name": "Sales Return", "account_group_type": "Trading A/C", "status": "Active"},
        {"name": "Stock", "account_group_type": "Trading A/C", "status": "Active"},
        {"name": "Salary", "account_group_type": "P&L Account", "status": "Active"},
        {"name": "Salaries Payable", "account_group_type": "P&L Account", "status": "Active"},
        {"name": "Purchase", "account_group_type": "Trading A/C", "status": "Active"},
        {"name": "Assets", "account_group_type": "Balance Sheet", "status": "Active"},
        {"name": "Accounts Receivable", "account_group_type": "Balance Sheet", "status": "Active"},
    ]

    print("\nCreating Account Groups:")
    print("-" * 70)

    for group in test_groups:
        success, message, ag_id = handler.create_account_group(group)
        if success:
            # Get the created group to see the AG code
            created_group = handler.get_account_group_by_id(ag_id)
            print(f"[OK] {created_group['name']:25} | {created_group['account_group_type']:20} | AG Code: {created_group['ag_code']}")
        else:
            print(f"[FAIL] Failed to create {group['name']}: {message}")

    print("\n" + "="*70)
    print("All Account Groups:")
    print("-" * 70)

    all_groups = handler.get_all_account_groups()
    print(f"\nTotal: {len(all_groups)} account groups\n")

    for idx, ag in enumerate(all_groups, 1):
        print(f"{idx:2}. {ag['name']:25} | {ag['account_group_type']:20} | {ag['ag_code']:8} | {ag['status']}")

    print("\n" + "="*70)
    print("Filter by Account Group Type:")
    print("-" * 70)

    for ag_type in ['Trading A/C', 'P&L Account', 'Balance Sheet']:
        groups = handler.get_by_type(ag_type)
        print(f"\n{ag_type} ({len(groups)} groups):")
        for ag in groups:
            print(f"  - {ag['name']:25} | AG Code: {ag['ag_code']}")

    handler.disconnect()
    print("\n" + "="*70)
    print("Comprehensive Test Completed!")
    print("="*70)


if __name__ == "__main__":
    test_comprehensive()
