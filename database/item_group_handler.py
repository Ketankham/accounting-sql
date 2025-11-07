"""
Item Group Handler - Manages item group CRUD operations using SQLite
"""

import sqlite3
from database.config import DB_PATH


class ItemGroupHandler:
    def __init__(self):
        self.conn = None
        self.cursor = None

    def connect(self):
        """Establish database connection"""
        try:
            import os
            abs_path = os.path.abspath(DB_PATH)
            print(f"\n{'='*70}")
            print(f"[ITEM_GROUP_HANDLER] Connecting to SQLite database...")
            print(f"[ITEM_GROUP_HANDLER] Database path: {abs_path}")
            print(f"[ITEM_GROUP_HANDLER] File exists: {os.path.exists(abs_path)}")
            if os.path.exists(abs_path):
                print(f"[ITEM_GROUP_HANDLER] File size: {os.path.getsize(abs_path)} bytes")
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
        """Create item_groups table if it doesn't exist"""
        try:
            create_table_query = """
            CREATE TABLE IF NOT EXISTS item_groups (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                item_group_code TEXT NOT NULL UNIQUE,
                item_group_name TEXT NOT NULL,
                status TEXT DEFAULT 'Active' CHECK(status IN ('Active', 'Inactive')),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
            self.cursor.execute(create_table_query)
            self.conn.commit()
            print("Item Groups table created/verified successfully")
        except sqlite3.Error as e:
            print(f"Error creating item_groups table: {e}")

    def disconnect(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
            print("SQLite connection closed")

    def validate_item_group_code(self, code):
        """
        Validate item group code:
        - Max 4 characters
        - Alphanumeric only
        """
        if not code or len(code) > 4:
            return False, "Item Group Code must be 1-4 characters"

        if not code.isalnum():
            return False, "Item Group Code must be alphanumeric"

        return True, "Valid"

    def get_all_item_groups(self):
        """Get all item groups with their details"""
        try:
            query = """
            SELECT id, item_group_code, item_group_name, status, created_at
            FROM item_groups
            ORDER BY item_group_name ASC
            """
            print(f"\n[GET_ALL_ITEM_GROUPS] Executing query...")
            self.cursor.execute(query)
            rows = self.cursor.fetchall()

            print(f"[GET_ALL_ITEM_GROUPS] Raw rows fetched: {len(rows)}")

            # Convert sqlite3.Row objects to dictionaries
            item_groups = [dict(row) for row in rows]

            print(f"[GET_ALL_ITEM_GROUPS] Returning {len(item_groups)} item groups\n")
            return item_groups
        except sqlite3.Error as e:
            print(f"[GET_ALL_ITEM_GROUPS] Error fetching item groups: {e}")
            import traceback
            traceback.print_exc()
            return []

    def get_active_item_groups(self):
        """Get only active item groups for dropdowns/foreign key selection"""
        try:
            query = """
            SELECT id, item_group_code, item_group_name, status, created_at
            FROM item_groups
            WHERE status = 'Active'
            ORDER BY item_group_name ASC
            """
            print(f"\n[GET_ACTIVE_ITEM_GROUPS] Executing query...")
            self.cursor.execute(query)
            rows = self.cursor.fetchall()

            # Convert sqlite3.Row objects to dictionaries
            item_groups = [dict(row) for row in rows]

            print(f"[GET_ACTIVE_ITEM_GROUPS] Returning {len(item_groups)} active item groups\n")
            return item_groups
        except sqlite3.Error as e:
            print(f"[GET_ACTIVE_ITEM_GROUPS] Error fetching active item groups: {e}")
            import traceback
            traceback.print_exc()
            return []

    def get_item_group_by_id(self, item_group_id):
        """Get a single item group by ID"""
        try:
            query = """
            SELECT id, item_group_code, item_group_name, status
            FROM item_groups
            WHERE id = ?
            """
            self.cursor.execute(query, (item_group_id,))
            row = self.cursor.fetchone()
            return dict(row) if row else None
        except sqlite3.Error as e:
            print(f"Error fetching item group: {e}")
            return None

    def get_item_group_by_code(self, item_group_code):
        """Get a single item group by code"""
        try:
            query = "SELECT id FROM item_groups WHERE item_group_code = ?"
            self.cursor.execute(query, (item_group_code,))
            row = self.cursor.fetchone()
            return dict(row) if row else None
        except sqlite3.Error as e:
            print(f"Error checking item group code: {e}")
            return None

    def create_item_group(self, item_group_data):
        """
        Create a new item group
        Returns (success: bool, message: str, item_group_id: int or None)
        """
        try:
            # Validate item group code
            is_valid, message = self.validate_item_group_code(
                item_group_data.get('item_group_code', '')
            )
            if not is_valid:
                return False, message, None

            # Check if code already exists
            if self.get_item_group_by_code(item_group_data['item_group_code']):
                return False, "Item Group Code already exists", None

            query = """
            INSERT INTO item_groups (
                item_group_code, item_group_name, status
            ) VALUES (
                ?, ?, ?
            )
            """

            values = (
                item_group_data['item_group_code'].upper(),  # Store in uppercase
                item_group_data['item_group_name'],
                item_group_data.get('status', 'Active')
            )

            self.cursor.execute(query, values)
            self.conn.commit()

            item_group_id = self.cursor.lastrowid
            print(f"Item Group '{item_group_data['item_group_name']}' created with code: {item_group_data['item_group_code']}")
            return True, f"Item Group created successfully", item_group_id

        except sqlite3.Error as e:
            print(f"Error creating item group: {e}")
            self.conn.rollback()
            return False, f"Database error: {str(e)}", None

    def update_item_group(self, item_group_id, item_group_data):
        """
        Update an existing item group
        Returns (success: bool, message: str)
        Note: Item Group Code cannot be changed after creation
        """
        try:
            # Check if item group exists
            existing = self.get_item_group_by_id(item_group_id)
            if not existing:
                return False, "Item Group not found"

            query = """
            UPDATE item_groups SET
                item_group_name = ?,
                status = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
            """

            values = (
                item_group_data['item_group_name'],
                item_group_data.get('status', 'Active'),
                item_group_id
            )

            self.cursor.execute(query, values)
            self.conn.commit()

            print(f"Item Group ID {item_group_id} updated successfully")
            return True, "Item Group updated successfully"

        except sqlite3.Error as e:
            print(f"Error updating item group: {e}")
            self.conn.rollback()
            return False, f"Database error: {str(e)}"

    def delete_item_group(self, item_group_id):
        """
        Delete an item group
        Returns (success: bool, message: str)
        """
        try:
            query = "DELETE FROM item_groups WHERE id = ?"
            self.cursor.execute(query, (item_group_id,))
            self.conn.commit()

            if self.cursor.rowcount > 0:
                print(f"Item Group ID {item_group_id} deleted successfully")
                return True, "Item Group deleted successfully"
            else:
                return False, "Item Group not found"

        except sqlite3.Error as e:
            print(f"Error deleting item group: {e}")
            self.conn.rollback()
            return False, f"Database error: {str(e)}"
