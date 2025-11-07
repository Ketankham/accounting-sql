"""
Seed script to populate Item Master with demo data
Run this once to add sample items to the database
"""

import sqlite3
import os

def seed_items_data():
    """Add sample items to the items table"""

    # Database path
    db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'financial_data.db')

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Sample items data
        items = [
            # Electronics
            {
                'item_code': 'ITEM001',
                'external_code': 'EXT-LAP-001',
                'item_name': 'Dell Latitude 5520 Laptop',
                'item_group_code': 'ELEC',
                'item_type_code': 'TRAD',
                'uom_code': 'PCS',
                'company_name': 'Dell Technologies',
                'purchase_rate': 45000.00,
                'mrp': 55000.00,
                'gst_percentage': 18.00,
                'hsn_code': '84713010',
                'sale_rate_wh1': 52000.00,
                'sale_rate_wh2': 51500.00,
                'discount_wh1': 5.00,
                'discount_wh2': 6.00,
                'sales_account_code': 'SSA001',
                'purchase_account_code': 'PPU001',
                'status': 'Active'
            },
            {
                'item_code': 'ITEM002',
                'external_code': 'EXT-MON-001',
                'item_name': 'LG 24 inch LED Monitor',
                'item_group_code': 'ELEC',
                'item_type_code': 'TRAD',
                'uom_code': 'PCS',
                'company_name': 'LG Electronics',
                'purchase_rate': 8500.00,
                'mrp': 11500.00,
                'gst_percentage': 18.00,
                'hsn_code': '85285210',
                'sale_rate_wh1': 10500.00,
                'sale_rate_wh2': 10200.00,
                'discount_wh1': 8.00,
                'discount_wh2': 10.00,
                'sales_account_code': 'SSA001',
                'purchase_account_code': 'PPU001',
                'status': 'Active'
            },
            {
                'item_code': 'ITEM003',
                'external_code': 'EXT-KEY-001',
                'item_name': 'Logitech Wireless Keyboard',
                'item_group_code': 'ELEC',
                'item_type_code': 'TRAD',
                'uom_code': 'PCS',
                'company_name': 'Logitech',
                'purchase_rate': 1200.00,
                'mrp': 1800.00,
                'gst_percentage': 18.00,
                'hsn_code': '84716060',
                'sale_rate_wh1': 1650.00,
                'sale_rate_wh2': 1600.00,
                'discount_wh1': 5.00,
                'discount_wh2': 7.00,
                'sales_account_code': 'SSA001',
                'purchase_account_code': 'PPU001',
                'status': 'Active'
            },
            # Stationery
            {
                'item_code': 'ITEM004',
                'external_code': 'EXT-PEN-001',
                'item_name': 'Reynolds Ballpoint Pen Blue',
                'item_group_code': 'STAT',
                'item_type_code': 'TRAD',
                'uom_code': 'PCS',
                'company_name': 'Reynolds',
                'purchase_rate': 5.00,
                'mrp': 10.00,
                'gst_percentage': 12.00,
                'hsn_code': '96081099',
                'sale_rate_wh1': 8.00,
                'sale_rate_wh2': 7.50,
                'discount_wh1': 10.00,
                'discount_wh2': 12.00,
                'sales_account_code': 'SSA001',
                'purchase_account_code': 'PPU001',
                'status': 'Active'
            },
            {
                'item_code': 'ITEM005',
                'external_code': 'EXT-NOTE-001',
                'item_name': 'Classmate Notebook 200 Pages',
                'item_group_code': 'STAT',
                'item_type_code': 'TRAD',
                'uom_code': 'PCS',
                'company_name': 'ITC Limited',
                'purchase_rate': 45.00,
                'mrp': 75.00,
                'gst_percentage': 12.00,
                'hsn_code': '48201030',
                'sale_rate_wh1': 65.00,
                'sale_rate_wh2': 62.00,
                'discount_wh1': 8.00,
                'discount_wh2': 10.00,
                'sales_account_code': 'SSA001',
                'purchase_account_code': 'PPU001',
                'status': 'Active'
            },
            {
                'item_code': 'ITEM006',
                'external_code': 'EXT-STA-001',
                'item_name': 'Kangaro Stapler HD-10',
                'item_group_code': 'STAT',
                'item_type_code': 'TRAD',
                'uom_code': 'PCS',
                'company_name': 'Kangaro',
                'purchase_rate': 85.00,
                'mrp': 150.00,
                'gst_percentage': 18.00,
                'hsn_code': '82140000',
                'sale_rate_wh1': 125.00,
                'sale_rate_wh2': 120.00,
                'discount_wh1': 10.00,
                'discount_wh2': 12.00,
                'sales_account_code': 'SSA001',
                'purchase_account_code': 'PPU001',
                'status': 'Active'
            },
            # Furniture
            {
                'item_code': 'ITEM007',
                'external_code': 'EXT-CHAIR-001',
                'item_name': 'Godrej Executive Office Chair',
                'item_group_code': 'FURN',
                'item_type_code': 'TRAD',
                'uom_code': 'PCS',
                'company_name': 'Godrej',
                'purchase_rate': 8500.00,
                'mrp': 12500.00,
                'gst_percentage': 18.00,
                'hsn_code': '94013010',
                'sale_rate_wh1': 11000.00,
                'sale_rate_wh2': 10800.00,
                'discount_wh1': 8.00,
                'discount_wh2': 10.00,
                'sales_account_code': 'SSA001',
                'purchase_account_code': 'PPU001',
                'status': 'Active'
            },
            {
                'item_code': 'ITEM008',
                'external_code': 'EXT-DESK-001',
                'item_name': 'Nilkamal Office Desk 4ft',
                'item_group_code': 'FURN',
                'item_type_code': 'TRAD',
                'uom_code': 'PCS',
                'company_name': 'Nilkamal',
                'purchase_rate': 5500.00,
                'mrp': 8500.00,
                'gst_percentage': 18.00,
                'hsn_code': '94036090',
                'sale_rate_wh1': 7500.00,
                'sale_rate_wh2': 7200.00,
                'discount_wh1': 10.00,
                'discount_wh2': 12.00,
                'sales_account_code': 'SSA001',
                'purchase_account_code': 'PPU001',
                'status': 'Active'
            },
            # Consumables
            {
                'item_code': 'ITEM009',
                'external_code': 'EXT-PAPER-001',
                'item_name': 'JK Copier Paper A4 500 Sheets',
                'item_group_code': 'CONS',
                'item_type_code': 'TRAD',
                'uom_code': 'PKT',
                'company_name': 'JK Paper',
                'purchase_rate': 225.00,
                'mrp': 350.00,
                'gst_percentage': 12.00,
                'hsn_code': '48025610',
                'sale_rate_wh1': 300.00,
                'sale_rate_wh2': 285.00,
                'discount_wh1': 10.00,
                'discount_wh2': 12.00,
                'sales_account_code': 'SSA001',
                'purchase_account_code': 'PPU001',
                'status': 'Active'
            },
            {
                'item_code': 'ITEM010',
                'external_code': 'EXT-TONER-001',
                'item_name': 'HP 88A Toner Cartridge',
                'item_group_code': 'CONS',
                'item_type_code': 'TRAD',
                'uom_code': 'PCS',
                'company_name': 'HP Inc',
                'purchase_rate': 3800.00,
                'mrp': 5500.00,
                'gst_percentage': 18.00,
                'hsn_code': '84439959',
                'sale_rate_wh1': 4800.00,
                'sale_rate_wh2': 4650.00,
                'discount_wh1': 8.00,
                'discount_wh2': 10.00,
                'sales_account_code': 'SSA001',
                'purchase_account_code': 'PPU001',
                'status': 'Active'
            },
            # Raw Materials
            {
                'item_code': 'ITEM011',
                'external_code': 'EXT-STEEL-001',
                'item_name': 'MS Steel Rod 12mm',
                'item_group_code': 'RAW',
                'item_type_code': 'TRAD',
                'uom_code': 'KG',
                'company_name': 'Tata Steel',
                'purchase_rate': 52.00,
                'mrp': 75.00,
                'gst_percentage': 18.00,
                'hsn_code': '72142000',
                'sale_rate_wh1': 68.00,
                'sale_rate_wh2': 65.00,
                'discount_wh1': 5.00,
                'discount_wh2': 7.00,
                'sales_account_code': 'SSA001',
                'purchase_account_code': 'PPU001',
                'status': 'Active'
            },
            {
                'item_code': 'ITEM012',
                'external_code': 'EXT-CEMENT-001',
                'item_name': 'UltraTech Portland Cement',
                'item_group_code': 'RAW',
                'item_type_code': 'TRAD',
                'uom_code': 'BAG',
                'company_name': 'UltraTech',
                'purchase_rate': 325.00,
                'mrp': 450.00,
                'gst_percentage': 28.00,
                'hsn_code': '25232900',
                'sale_rate_wh1': 400.00,
                'sale_rate_wh2': 390.00,
                'discount_wh1': 8.00,
                'discount_wh2': 10.00,
                'sales_account_code': 'SSA001',
                'purchase_account_code': 'PPU001',
                'status': 'Active'
            },
            # Beverages (Some inactive)
            {
                'item_code': 'ITEM013',
                'external_code': 'EXT-TEA-001',
                'item_name': 'Tata Tea Gold 500g',
                'item_group_code': 'CONS',
                'item_type_code': 'TRAD',
                'uom_code': 'PKT',
                'company_name': 'Tata Consumer',
                'purchase_rate': 185.00,
                'mrp': 250.00,
                'gst_percentage': 5.00,
                'hsn_code': '09023000',
                'sale_rate_wh1': 220.00,
                'sale_rate_wh2': 210.00,
                'discount_wh1': 10.00,
                'discount_wh2': 12.00,
                'sales_account_code': 'SSA001',
                'purchase_account_code': 'PPU001',
                'status': 'Active'
            },
            {
                'item_code': 'ITEM014',
                'external_code': 'EXT-COFFEE-001',
                'item_name': 'Nescafe Classic 100g',
                'item_group_code': 'CONS',
                'item_type_code': 'TRAD',
                'uom_code': 'JAR',
                'company_name': 'Nestle',
                'purchase_rate': 285.00,
                'mrp': 380.00,
                'gst_percentage': 5.00,
                'hsn_code': '09012100',
                'sale_rate_wh1': 350.00,
                'sale_rate_wh2': 340.00,
                'discount_wh1': 5.00,
                'discount_wh2': 8.00,
                'sales_account_code': 'SSA001',
                'purchase_account_code': 'PPU001',
                'status': 'Inactive'  # This one is inactive
            },
            # Services
            {
                'item_code': 'ITEM015',
                'external_code': 'EXT-SERV-001',
                'item_name': 'IT Support Services - Monthly',
                'item_group_code': 'SERV',
                'item_type_code': 'SERV',
                'uom_code': 'MON',
                'company_name': 'TechSupport Co',
                'purchase_rate': 8000.00,
                'mrp': 15000.00,
                'gst_percentage': 18.00,
                'hsn_code': '998314',
                'sale_rate_wh1': 12500.00,
                'sale_rate_wh2': 12000.00,
                'discount_wh1': 10.00,
                'discount_wh2': 15.00,
                'sales_account_code': 'SSA001',
                'purchase_account_code': 'PPU001',
                'status': 'Active'
            }
        ]

        # Insert items
        print("Starting to seed items data...")

        insert_query = """
        INSERT OR IGNORE INTO items (
            item_code, external_code, item_name, item_group_code, item_type_code,
            uom_code, company_name, purchase_rate, mrp, gst_percentage, hsn_code,
            sale_rate_wh1, sale_rate_wh2, discount_wh1, discount_wh2,
            sales_account_code, purchase_account_code, status
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """

        inserted_count = 0
        for item in items:
            cursor.execute(insert_query, (
                item['item_code'],
                item['external_code'],
                item['item_name'],
                item['item_group_code'],
                item['item_type_code'],
                item['uom_code'],
                item['company_name'],
                item['purchase_rate'],
                item['mrp'],
                item['gst_percentage'],
                item['hsn_code'],
                item['sale_rate_wh1'],
                item['sale_rate_wh2'],
                item['discount_wh1'],
                item['discount_wh2'],
                item['sales_account_code'],
                item['purchase_account_code'],
                item['status']
            ))

            if cursor.rowcount > 0:
                inserted_count += 1
                print(f"[OK] Added: {item['item_code']} - {item['item_name']}")

        conn.commit()

        print(f"\n[OK] Successfully inserted {inserted_count} items")
        print(f"  Total items attempted: {len(items)}")
        print(f"  Active items: {sum(1 for i in items if i['status'] == 'Active')}")
        print(f"  Inactive items: {sum(1 for i in items if i['status'] == 'Inactive')}")

        # Display summary by category
        print("\nItems by Category:")
        from collections import defaultdict
        by_group = defaultdict(int)
        for item in items:
            by_group[item['item_group_code']] += 1

        for group, count in sorted(by_group.items()):
            print(f"  {group}: {count} items")

        conn.close()
        return True

    except sqlite3.Error as e:
        print(f"[ERROR] Database error: {e}")
        return False
    except Exception as e:
        print(f"[ERROR] Error: {e}")
        return False


if __name__ == "__main__":
    print("=" * 60)
    print("Item Master - Demo Data Seeding Script")
    print("=" * 60)
    print()

    success = seed_items_data()

    print()
    print("=" * 60)
    if success:
        print("[OK] Seeding completed successfully!")
        print("\nYou can now:")
        print("  1. View items in Item Master screen")
        print("  2. Edit existing items")
        print("  3. Create new items following the same pattern")
    else:
        print("[ERROR] Seeding failed - check error messages above")
    print("=" * 60)
