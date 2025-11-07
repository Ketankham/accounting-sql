"""
UoM (Unit of Measure) Handler - Manages UoM CRUD operations using SQLite
"""

import sqlite3
from database.config import DB_PATH


class UoMHandler:
    def __init__(self):
        self.conn = None
        self.cursor = None

    def connect(self):
        """Establish database connection"""
        try:
            import os
            abs_path = os.path.abspath(DB_PATH)
            print(f"\n{'='*70}")
            print(f"[UOM_HANDLER] Connecting to SQLite database...")
            print(f"[UOM_HANDLER] Database path: {abs_path}")
            print(f"[UOM_HANDLER] File exists: {os.path.exists(abs_path)}")
            if os.path.exists(abs_path):
                print(f"[UOM_HANDLER] File size: {os.path.getsize(abs_path)} bytes")
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
        """Create uom table if it doesn't exist"""
        try:
            create_table_query = """
            CREATE TABLE IF NOT EXISTS uom (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                uom_code TEXT NOT NULL UNIQUE,
                uom_name TEXT NOT NULL,
                status TEXT DEFAULT 'Active' CHECK(status IN ('Active', 'Inactive')),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
            self.cursor.execute(create_table_query)
            self.conn.commit()
            print("UoM table created/verified successfully")
        except sqlite3.Error as e:
            print(f"Error creating UoM table: {e}")

    def disconnect(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
            print("SQLite connection closed")

    def validate_uom_code(self, code):
        """
        Validate UoM code:
        - Max 10 characters (flexible for codes like "SQFT", "KG", etc.)
        - Alphanumeric only
        """
        if not code or len(code) > 10:
            return False, "UoM Code must be 1-10 characters"

        if not code.replace('-', '').replace('_', '').isalnum():
            return False, "UoM Code must be alphanumeric (hyphens and underscores allowed)"

        return True, "Valid"

    def get_all_uoms(self):
        """Get all UoMs with their details"""
        try:
            query = """
            SELECT id, uom_code, uom_name, status, created_at
            FROM uom
            ORDER BY uom_name ASC
            """
            print(f"\n[GET_ALL_UOMS] Executing query...")
            self.cursor.execute(query)
            rows = self.cursor.fetchall()

            print(f"[GET_ALL_UOMS] Raw rows fetched: {len(rows)}")

            # Convert sqlite3.Row objects to dictionaries
            uoms = [dict(row) for row in rows]

            print(f"[GET_ALL_UOMS] Returning {len(uoms)} UoMs\n")
            return uoms
        except sqlite3.Error as e:
            print(f"[GET_ALL_UOMS] Error fetching UoMs: {e}")
            import traceback
            traceback.print_exc()
            return []

    def get_active_uoms(self):
        """Get only active uom for dropdowns/foreign key selection"""
        try:
            query = """
            SELECT id, uom_code, uom_name, status, created_at
            FROM uom
            WHERE status = 'Active'
            ORDER BY uom_name ASC
            """
            print(f"\n[GET_ACTIVE_UOMS] Executing query...")
            self.cursor.execute(query)
            rows = self.cursor.fetchall()

            # Convert sqlite3.Row objects to dictionaries
            uoms = [dict(row) for row in rows]

            print(f"[GET_ACTIVE_UOMS] Returning {len(uoms)} active uom\n")
            return uoms
        except sqlite3.Error as e:
            print(f"[GET_ACTIVE_UOMS] Error fetching active uom: {e}")
            import traceback
            traceback.print_exc()
            return []


    def get_uom_by_id(self, uom_id):
        """Get a single UoM by ID"""
        try:
            query = """
            SELECT id, uom_code, uom_name, status
            FROM uom
            WHERE id = ?
            """
            self.cursor.execute(query, (uom_id,))
            row = self.cursor.fetchone()
            return dict(row) if row else None
        except sqlite3.Error as e:
            print(f"Error fetching UoM: {e}")
            return None

    def get_uom_by_code(self, uom_code):
        """Get a single UoM by code"""
        try:
            query = "SELECT id FROM uom WHERE uom_code = ?"
            self.cursor.execute(query, (uom_code,))
            row = self.cursor.fetchone()
            return dict(row) if row else None
        except sqlite3.Error as e:
            print(f"Error checking UoM code: {e}")
            return None

    def create_uom(self, uom_data):
        """
        Create a new UoM
        Returns (success: bool, message: str, uom_id: int or None)
        """
        try:
            # Validate UoM code
            is_valid, message = self.validate_uom_code(
                uom_data.get('uom_code', '')
            )
            if not is_valid:
                return False, message, None

            # Check if code already exists
            if self.get_uom_by_code(uom_data['uom_code']):
                return False, "UoM Code already exists", None

            query = """
            INSERT INTO uom (
                uom_code, uom_name, status
            ) VALUES (
                ?, ?, ?
            )
            """

            values = (
                uom_data['uom_code'].upper(),  # Store in uppercase
                uom_data['uom_name'],
                uom_data.get('status', 'Active')
            )

            self.cursor.execute(query, values)
            self.conn.commit()

            uom_id = self.cursor.lastrowid
            print(f"UoM '{uom_data['uom_name']}' created with code: {uom_data['uom_code']}")
            return True, f"UoM created successfully", uom_id

        except sqlite3.Error as e:
            print(f"Error creating UoM: {e}")
            self.conn.rollback()
            return False, f"Database error: {str(e)}", None

    def update_uom(self, uom_id, uom_data):
        """
        Update an existing UoM
        Returns (success: bool, message: str)
        Note: UoM Code cannot be changed after creation
        """
        try:
            # Check if UoM exists
            existing = self.get_uom_by_id(uom_id)
            if not existing:
                return False, "UoM not found"

            query = """
            UPDATE uom SET
                uom_name = ?,
                status = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
            """

            values = (
                uom_data['uom_name'],
                uom_data.get('status', 'Active'),
                uom_id
            )

            self.cursor.execute(query, values)
            self.conn.commit()

            print(f"UoM ID {uom_id} updated successfully")
            return True, "UoM updated successfully"

        except sqlite3.Error as e:
            print(f"Error updating UoM: {e}")
            self.conn.rollback()
            return False, f"Database error: {str(e)}"

    def delete_uom(self, uom_id):
        """
        Delete a UoM
        Returns (success: bool, message: str)
        """
        try:
            query = "DELETE FROM uom WHERE id = ?"
            self.cursor.execute(query, (uom_id,))
            self.conn.commit()

            if self.cursor.rowcount > 0:
                print(f"UoM ID {uom_id} deleted successfully")
                return True, "UoM deleted successfully"
            else:
                return False, "UoM not found"

        except sqlite3.Error as e:
            print(f"Error deleting UoM: {e}")
            self.conn.rollback()
            return False, f"Database error: {str(e)}"
