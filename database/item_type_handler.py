"""
Item Type Handler - Manages Item Type CRUD operations using SQLite
"""

import sqlite3
from database.config import DB_PATH


class ItemTypeHandler:
    def __init__(self):
        self.conn = None
        self.cursor = None

    def connect(self):
        """Establish database connection"""
        try:
            import os
            abs_path = os.path.abspath(DB_PATH)
            print(f"\n{'='*70}")
            print(f"[ITEM_TYPE_HANDLER] Connecting to SQLite database...")
            print(f"[ITEM_TYPE_HANDLER] Database path: {abs_path}")
            print(f"[ITEM_TYPE_HANDLER] File exists: {os.path.exists(abs_path)}")
            if os.path.exists(abs_path):
                print(f"[ITEM_TYPE_HANDLER] File size: {os.path.getsize(abs_path)} bytes")
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
        """Create item_types table if it doesn't exist"""
        try:
            create_table_query = """
            CREATE TABLE IF NOT EXISTS item_types (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                type_code TEXT NOT NULL UNIQUE,
                type_name TEXT NOT NULL,
                status TEXT DEFAULT 'Active' CHECK(status IN ('Active', 'Inactive')),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
            self.cursor.execute(create_table_query)
            self.conn.commit()
            print("Item Types table created/verified successfully")
        except sqlite3.Error as e:
            print(f"Error creating Item Types table: {e}")

    def disconnect(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
            print("SQLite connection closed")

    def validate_type_code(self, code):
        """
        Validate item type code:
        - Max 10 characters
        - Alphanumeric only
        """
        if not code or len(code) > 10:
            return False, "Type Code must be 1-10 characters"

        if not code.replace('-', '').replace('_', '').isalnum():
            return False, "Type Code must be alphanumeric (hyphens and underscores allowed)"

        return True, "Valid"

    def get_all_item_types(self):
        """Get all item types with their details"""
        try:
            query = """
            SELECT id, type_code, type_name, status, created_at
            FROM item_types
            ORDER BY type_name ASC
            """
            print(f"\n[GET_ALL_ITEM_TYPES] Executing query...")
            self.cursor.execute(query)
            rows = self.cursor.fetchall()

            print(f"[GET_ALL_ITEM_TYPES] Raw rows fetched: {len(rows)}")

            # Convert sqlite3.Row objects to dictionaries
            item_types = [dict(row) for row in rows]

            print(f"[GET_ALL_ITEM_TYPES] Returning {len(item_types)} item types\n")
            return item_types
        except sqlite3.Error as e:
            print(f"[GET_ALL_ITEM_TYPES] Error fetching item types: {e}")
            import traceback
            traceback.print_exc()
            return []

    def get_active_item_types(self):
        """Get only active item types for dropdowns/foreign key selection"""
        try:
            query = """
            SELECT id, type_code, type_name, status, created_at
            FROM item_types
            WHERE status = 'Active'
            ORDER BY type_name ASC
            """
            print(f"\n[GET_ACTIVE_ITEM_TYPES] Executing query...")
            self.cursor.execute(query)
            rows = self.cursor.fetchall()

            # Convert sqlite3.Row objects to dictionaries
            item_types = [dict(row) for row in rows]

            print(f"[GET_ACTIVE_ITEM_TYPES] Returning {len(item_types)} active item types\n")
            return item_types
        except sqlite3.Error as e:
            print(f"[GET_ACTIVE_ITEM_TYPES] Error fetching active item types: {e}")
            import traceback
            traceback.print_exc()
            return []

    def get_item_type_by_id(self, type_id):
        """Get a single item type by ID"""
        try:
            query = """
            SELECT id, type_code, type_name, status
            FROM item_types
            WHERE id = ?
            """
            self.cursor.execute(query, (type_id,))
            row = self.cursor.fetchone()
            return dict(row) if row else None
        except sqlite3.Error as e:
            print(f"Error fetching item type: {e}")
            return None

    def get_item_type_by_code(self, type_code):
        """Get a single item type by code"""
        try:
            query = "SELECT id FROM item_types WHERE type_code = ?"
            self.cursor.execute(query, (type_code,))
            row = self.cursor.fetchone()
            return dict(row) if row else None
        except sqlite3.Error as e:
            print(f"Error checking item type code: {e}")
            return None

    def create_item_type(self, type_data):
        """
        Create a new item type
        Returns (success: bool, message: str, type_id: int or None)
        """
        try:
            # Validate type code
            is_valid, message = self.validate_type_code(
                type_data.get('type_code', '')
            )
            if not is_valid:
                return False, message, None

            # Check if code already exists
            if self.get_item_type_by_code(type_data['type_code']):
                return False, "Type Code already exists", None

            query = """
            INSERT INTO item_types (
                type_code, type_name, status
            ) VALUES (
                ?, ?, ?
            )
            """

            values = (
                type_data['type_code'].upper(),  # Store in uppercase
                type_data['type_name'],
                type_data.get('status', 'Active')
            )

            self.cursor.execute(query, values)
            self.conn.commit()

            type_id = self.cursor.lastrowid
            print(f"Item Type '{type_data['type_name']}' created with code: {type_data['type_code']}")
            return True, f"Item Type created successfully", type_id

        except sqlite3.Error as e:
            print(f"Error creating item type: {e}")
            self.conn.rollback()
            return False, f"Database error: {str(e)}", None

    def update_item_type(self, type_id, type_data):
        """
        Update an existing item type
        Returns (success: bool, message: str)
        Note: Type Code cannot be changed after creation
        """
        try:
            # Check if item type exists
            existing = self.get_item_type_by_id(type_id)
            if not existing:
                return False, "Item Type not found"

            query = """
            UPDATE item_types SET
                type_name = ?,
                status = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
            """

            values = (
                type_data['type_name'],
                type_data.get('status', 'Active'),
                type_id
            )

            self.cursor.execute(query, values)
            self.conn.commit()

            print(f"Item Type ID {type_id} updated successfully")
            return True, "Item Type updated successfully"

        except sqlite3.Error as e:
            print(f"Error updating item type: {e}")
            self.conn.rollback()
            return False, f"Database error: {str(e)}"

    def delete_item_type(self, type_id):
        """
        Delete an item type
        Returns (success: bool, message: str)
        """
        try:
            query = "DELETE FROM item_types WHERE id = ?"
            self.cursor.execute(query, (type_id,))
            self.conn.commit()

            if self.cursor.rowcount > 0:
                print(f"Item Type ID {type_id} deleted successfully")
                return True, "Item Type deleted successfully"
            else:
                return False, "Item Type not found"

        except sqlite3.Error as e:
            print(f"Error deleting item type: {e}")
            self.conn.rollback()
            return False, f"Database error: {str(e)}"
