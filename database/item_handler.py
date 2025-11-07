"""
Item Master Handler - Manages item CRUD operations using SQLite
"""

import sqlite3
from database.config import DB_PATH


class ItemHandler:
    def __init__(self):
        self.conn = None
        self.cursor = None

    def connect(self):
        """Establish database connection"""
        try:
            import os
            abs_path = os.path.abspath(DB_PATH)
            print(f"\n{'='*70}")
            print(f"[ITEM_HANDLER] Connecting to SQLite database...")
            print(f"[ITEM_HANDLER] Database path: {abs_path}")
            print(f"[ITEM_HANDLER] File exists: {os.path.exists(abs_path)}")
            if os.path.exists(abs_path):
                print(f"[ITEM_HANDLER] File size: {os.path.getsize(abs_path)} bytes")
            print(f"{'='*70}\n")

            self.conn = sqlite3.connect(DB_PATH)
            self.conn.row_factory = sqlite3.Row
            self.cursor = self.conn.cursor()
            print(f"Successfully connected to SQLite database")

            # Create table if it doesn't exist
            self._create_table()

            return True
        except sqlite3.Error as e:
            print(f"Error connecting to SQLite: {e}")
            return False

    def _create_table(self):
        """Create items table if it doesn't exist"""
        try:
            create_table_query = """
            CREATE TABLE IF NOT EXISTS items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                item_code TEXT NOT NULL UNIQUE,
                external_code TEXT,
                item_name TEXT NOT NULL,
                item_group_code TEXT,
                item_type_code TEXT,
                uom_code TEXT,
                company_name TEXT,
                purchase_rate REAL DEFAULT 0.0,
                mrp REAL DEFAULT 0.0,
                gst_percentage REAL DEFAULT 0.0,
                hsn_code TEXT,
                sale_rate_wh1 REAL DEFAULT 0.0,
                sale_rate_wh2 REAL DEFAULT 0.0,
                discount_wh1 REAL DEFAULT 0.0,
                discount_wh2 REAL DEFAULT 0.0,
                sales_account_code TEXT,
                purchase_account_code TEXT,
                status TEXT DEFAULT 'Active' CHECK(status IN ('Active', 'Inactive')),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
            self.cursor.execute(create_table_query)
            self.conn.commit()
            print("Items table created/verified successfully")
        except sqlite3.Error as e:
            print(f"Error creating items table: {e}")

    def disconnect(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
            print("SQLite connection closed")

    def validate_item_code(self, code):
        """
        Validate item code:
        - Max 20 characters
        - Alphanumeric only
        """
        if not code or len(code) > 20:
            return False, "Item Code must be 1-20 characters"

        if not code.replace('-', '').replace('_', '').isalnum():
            return False, "Item Code must be alphanumeric (hyphens and underscores allowed)"

        return True, "Valid"

    def get_next_item_code(self):
        """Generate next item code in format ITEM001, ITEM002, etc."""
        try:
            query = "SELECT item_code FROM items ORDER BY id DESC LIMIT 1"
            self.cursor.execute(query)
            row = self.cursor.fetchone()

            if row:
                last_code = row[0]
                # Extract number from last code (assuming format like ITEM001)
                if last_code.startswith('ITEM'):
                    try:
                        num = int(last_code[4:]) + 1
                        return f"ITEM{num:03d}"
                    except:
                        return "ITEM001"
            return "ITEM001"
        except sqlite3.Error as e:
            print(f"Error generating item code: {e}")
            return "ITEM001"

    def get_all_items(self):
        """Get all items with their details"""
        try:
            query = """
            SELECT id, item_code, external_code, item_name, item_group_code,
                   item_type_code, uom_code, company_name, purchase_rate, mrp,
                   gst_percentage, hsn_code, sale_rate_wh1, sale_rate_wh2,
                   discount_wh1, discount_wh2, sales_account_code,
                   purchase_account_code, status, created_at
            FROM items
            ORDER BY item_code ASC
            """
            print(f"\n[GET_ALL_ITEMS] Executing query...")
            self.cursor.execute(query)
            rows = self.cursor.fetchall()

            print(f"[GET_ALL_ITEMS] Raw rows fetched: {len(rows)}")

            # Convert sqlite3.Row objects to dictionaries
            items = [dict(row) for row in rows]

            print(f"[GET_ALL_ITEMS] Returning {len(items)} items\n")
            return items
        except sqlite3.Error as e:
            print(f"[GET_ALL_ITEMS] Error fetching items: {e}")
            import traceback
            traceback.print_exc()
            return []

    def get_active_items(self):
        """Get only active items"""
        try:
            query = """
            SELECT id, item_code, external_code, item_name, item_group_code,
                   item_type_code, uom_code, company_name, purchase_rate, mrp,
                   gst_percentage, hsn_code, sale_rate_wh1, sale_rate_wh2,
                   discount_wh1, discount_wh2, sales_account_code,
                   purchase_account_code, status, created_at
            FROM items
            WHERE status = 'Active'
            ORDER BY item_code ASC
            """
            print(f"\n[GET_ACTIVE_ITEMS] Executing query...")
            self.cursor.execute(query)
            rows = self.cursor.fetchall()

            # Convert sqlite3.Row objects to dictionaries
            items = [dict(row) for row in rows]

            print(f"[GET_ACTIVE_ITEMS] Returning {len(items)} active items\n")
            return items
        except sqlite3.Error as e:
            print(f"[GET_ACTIVE_ITEMS] Error fetching active items: {e}")
            import traceback
            traceback.print_exc()
            return []

    def get_item_by_id(self, item_id):
        """Get a single item by ID"""
        try:
            query = """
            SELECT id, item_code, external_code, item_name, item_group_code,
                   item_type_code, uom_code, company_name, purchase_rate, mrp,
                   gst_percentage, hsn_code, sale_rate_wh1, sale_rate_wh2,
                   discount_wh1, discount_wh2, sales_account_code,
                   purchase_account_code, status
            FROM items
            WHERE id = ?
            """
            self.cursor.execute(query, (item_id,))
            row = self.cursor.fetchone()
            return dict(row) if row else None
        except sqlite3.Error as e:
            print(f"Error fetching item: {e}")
            return None

    def get_item_by_code(self, item_code):
        """Get a single item by code"""
        try:
            query = "SELECT id FROM items WHERE item_code = ?"
            self.cursor.execute(query, (item_code,))
            row = self.cursor.fetchone()
            return dict(row) if row else None
        except sqlite3.Error as e:
            print(f"Error checking item code: {e}")
            return None

    def create_item(self, item_data):
        """
        Create a new item
        Returns (success: bool, message: str, item_id: int or None)
        """
        try:
            # Validate item code
            is_valid, message = self.validate_item_code(
                item_data.get('item_code', '')
            )
            if not is_valid:
                return False, message, None

            # Check if code already exists
            if self.get_item_by_code(item_data['item_code']):
                return False, "Item Code already exists", None

            query = """
            INSERT INTO items (
                item_code, external_code, item_name, item_group_code, item_type_code,
                uom_code, company_name, purchase_rate, mrp, gst_percentage, hsn_code,
                sale_rate_wh1, sale_rate_wh2, discount_wh1, discount_wh2,
                sales_account_code, purchase_account_code, status
            ) VALUES (
                ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
            )
            """

            values = (
                item_data['item_code'].upper(),
                item_data.get('external_code', ''),
                item_data['item_name'],
                item_data.get('item_group_code', ''),
                item_data.get('item_type_code', ''),
                item_data.get('uom_code', ''),
                item_data.get('company_name', ''),
                item_data.get('purchase_rate', 0.0),
                item_data.get('mrp', 0.0),
                item_data.get('gst_percentage', 0.0),
                item_data.get('hsn_code', ''),
                item_data.get('sale_rate_wh1', 0.0),
                item_data.get('sale_rate_wh2', 0.0),
                item_data.get('discount_wh1', 0.0),
                item_data.get('discount_wh2', 0.0),
                item_data.get('sales_account_code', ''),
                item_data.get('purchase_account_code', ''),
                item_data.get('status', 'Active')
            )

            self.cursor.execute(query, values)
            self.conn.commit()

            item_id = self.cursor.lastrowid
            print(f"Item '{item_data['item_name']}' created with code: {item_data['item_code']}")
            return True, "Item created successfully", item_id

        except sqlite3.Error as e:
            print(f"Error creating item: {e}")
            self.conn.rollback()
            return False, f"Database error: {str(e)}", None

    def update_item(self, item_id, item_data):
        """
        Update an existing item
        Returns (success: bool, message: str)
        """
        try:
            # Check if item exists
            existing = self.get_item_by_id(item_id)
            if not existing:
                return False, "Item not found"

            query = """
            UPDATE items SET
                item_code = ?,
                external_code = ?,
                item_name = ?,
                item_group_code = ?,
                item_type_code = ?,
                uom_code = ?,
                company_name = ?,
                purchase_rate = ?,
                mrp = ?,
                gst_percentage = ?,
                hsn_code = ?,
                sale_rate_wh1 = ?,
                sale_rate_wh2 = ?,
                discount_wh1 = ?,
                discount_wh2 = ?,
                sales_account_code = ?,
                purchase_account_code = ?,
                status = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
            """

            values = (
                item_data['item_code'].upper(),
                item_data.get('external_code', ''),
                item_data['item_name'],
                item_data.get('item_group_code', ''),
                item_data.get('item_type_code', ''),
                item_data.get('uom_code', ''),
                item_data.get('company_name', ''),
                item_data.get('purchase_rate', 0.0),
                item_data.get('mrp', 0.0),
                item_data.get('gst_percentage', 0.0),
                item_data.get('hsn_code', ''),
                item_data.get('sale_rate_wh1', 0.0),
                item_data.get('sale_rate_wh2', 0.0),
                item_data.get('discount_wh1', 0.0),
                item_data.get('discount_wh2', 0.0),
                item_data.get('sales_account_code', ''),
                item_data.get('purchase_account_code', ''),
                item_data.get('status', 'Active'),
                item_id
            )

            self.cursor.execute(query, values)
            self.conn.commit()

            print(f"Item ID {item_id} updated successfully")
            return True, "Item updated successfully"

        except sqlite3.Error as e:
            print(f"Error updating item: {e}")
            self.conn.rollback()
            return False, f"Database error: {str(e)}"

    def delete_item(self, item_id):
        """
        Delete an item
        Returns (success: bool, message: str)
        """
        try:
            query = "DELETE FROM items WHERE id = ?"
            self.cursor.execute(query, (item_id,))
            self.conn.commit()

            if self.cursor.rowcount > 0:
                print(f"Item ID {item_id} deleted successfully")
                return True, "Item deleted successfully"
            else:
                return False, "Item not found"

        except sqlite3.Error as e:
            print(f"Error deleting item: {e}")
            self.conn.rollback()
            return False, f"Database error: {str(e)}"
