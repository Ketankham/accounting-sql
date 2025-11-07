"""
Account Group Handler - Manages account group CRUD operations using SQLite
"""

import sqlite3
from database.config import DB_PATH


class AccountGroupHandler:
    # Account Group Type codes mapping
    AG_TYPE_CODES = {
        'Trading A/C': 'TA',
        'P&L Account': 'PL',
        'Balance Sheet': 'BS'
    }

    def __init__(self):
        self.conn = None
        self.cursor = None

    def connect(self):
        """Establish database connection"""
        try:
            import os
            abs_path = os.path.abspath(DB_PATH)
            print(f"\n{'='*70}")
            print(f"[ACCOUNT_GROUP_HANDLER] Connecting to SQLite database...")
            print(f"[ACCOUNT_GROUP_HANDLER] Database path: {abs_path}")
            print(f"[ACCOUNT_GROUP_HANDLER] File exists: {os.path.exists(abs_path)}")
            if os.path.exists(abs_path):
                print(f"[ACCOUNT_GROUP_HANDLER] File size: {os.path.getsize(abs_path)} bytes")
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
        """Create account_groups table if it doesn't exist"""
        try:
            create_table_query = """
            CREATE TABLE IF NOT EXISTS account_groups (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                account_group_type TEXT NOT NULL CHECK(account_group_type IN ('Trading A/C', 'P&L Account', 'Balance Sheet')),
                status TEXT DEFAULT 'Active' CHECK(status IN ('Active', 'Inactive')),
                ag_code TEXT NOT NULL UNIQUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
            self.cursor.execute(create_table_query)
            self.conn.commit()
            print("Account Groups table created/verified successfully")
        except sqlite3.Error as e:
            print(f"Error creating account_groups table: {e}")

    def disconnect(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
            print("SQLite connection closed")

    def generate_ag_code(self, name, account_group_type):
        """
        Generate AG code based on:
        - First letter from name
        - Next 2 characters from account group type code
        - Next 3 digits as serial number (001, 002, etc.)

        Example: Name="Sales", Type="Trading A/C" => STA001
        """
        # Get first letter from name (uppercase)
        first_letter = name[0].upper() if name else 'X'

        # Get account group type code
        ag_type_code = self.AG_TYPE_CODES.get(account_group_type, 'XX')

        # Get next serial number for this prefix
        prefix = f"{first_letter}{ag_type_code}"

        try:
            query = """
            SELECT ag_code FROM account_groups
            WHERE ag_code LIKE ?
            ORDER BY ag_code DESC
            LIMIT 1
            """
            self.cursor.execute(query, (f"{prefix}%",))
            result = self.cursor.fetchone()

            if result:
                # Extract last 3 digits and increment
                last_code = result['ag_code']
                last_serial = int(last_code[-3:])
                next_serial = last_serial + 1
            else:
                # First entry for this prefix
                next_serial = 1

            # Format serial number as 3 digits (001, 002, etc.)
            serial_str = str(next_serial).zfill(3)

            # Return complete AG code (6 characters: 1 letter + 2 type code + 3 serial digits)
            ag_code = f"{prefix}{serial_str}"
            return ag_code

        except sqlite3.Error as e:
            print(f"Error generating AG code: {e}")
            return f"{prefix}001"

    def get_all_account_groups(self):
        """Get all account groups with their details"""
        try:
            query = """
            SELECT id, name, account_group_type, status, ag_code, created_at
            FROM account_groups
            ORDER BY name ASC
            """
            print(f"\n[GET_ALL_ACCOUNT_GROUPS] Executing query...")
            self.cursor.execute(query)
            rows = self.cursor.fetchall()

            print(f"[GET_ALL_ACCOUNT_GROUPS] Raw rows fetched: {len(rows)}")

            # Convert sqlite3.Row objects to dictionaries
            account_groups = [dict(row) for row in rows]

            print(f"[GET_ALL_ACCOUNT_GROUPS] Returning {len(account_groups)} account groups\n")
            return account_groups
        except sqlite3.Error as e:
            print(f"[GET_ALL_ACCOUNT_GROUPS] Error fetching account groups: {e}")
            import traceback
            traceback.print_exc()
            return []

    def get_active_account_groups(self):
        """Get only active account groups for dropdowns/foreign key selection"""
        try:
            query = """
            SELECT id, name, account_group_type, status, ag_code, created_at
            FROM account_groups
            WHERE status = 'Active'
            ORDER BY name ASC
            """
            print(f"\n[GET_ACTIVE_ACCOUNT_GROUPS] Executing query...")
            self.cursor.execute(query)
            rows = self.cursor.fetchall()

            # Convert sqlite3.Row objects to dictionaries
            account_groups = [dict(row) for row in rows]

            print(f"[GET_ACTIVE_ACCOUNT_GROUPS] Returning {len(account_groups)} active account groups\n")
            return account_groups
        except sqlite3.Error as e:
            print(f"[GET_ACTIVE_ACCOUNT_GROUPS] Error fetching active account groups: {e}")
            import traceback
            traceback.print_exc()
            return []

    def get_account_group_by_id(self, account_group_id):
        """Get a single account group by ID"""
        try:
            query = """
            SELECT id, name, account_group_type, status, ag_code
            FROM account_groups
            WHERE id = ?
            """
            self.cursor.execute(query, (account_group_id,))
            row = self.cursor.fetchone()
            return dict(row) if row else None
        except sqlite3.Error as e:
            print(f"Error fetching account group: {e}")
            return None

    def get_account_group_by_code(self, ag_code):
        """Get a single account group by AG code"""
        try:
            query = "SELECT id FROM account_groups WHERE ag_code = ?"
            self.cursor.execute(query, (ag_code,))
            row = self.cursor.fetchone()
            return dict(row) if row else None
        except sqlite3.Error as e:
            print(f"Error checking AG code: {e}")
            return None

    def create_account_group(self, account_group_data):
        """
        Create a new account group
        Returns (success: bool, message: str, account_group_id: int or None)
        """
        try:
            # Get user-entered AG code (2 characters, alphanumeric)
            ag_code = account_group_data.get('ag_code', '').strip().upper()

            # Validate AG code format
            if not ag_code:
                return False, "AG Code is required", None

            if len(ag_code) != 2:
                return False, "AG Code must be exactly 2 characters", None

            if not ag_code.isalnum():
                return False, "AG Code must be alphanumeric only", None

            # Check if AG code already exists
            if self.get_account_group_by_code(ag_code):
                return False, f"AG Code '{ag_code}' already exists. Please choose a different code.", None

            query = """
            INSERT INTO account_groups (
                name, account_group_type, status, ag_code
            ) VALUES (
                ?, ?, ?, ?
            )
            """

            values = (
                account_group_data['name'],
                account_group_data['account_group_type'],
                account_group_data.get('status', 'Active'),
                ag_code
            )

            self.cursor.execute(query, values)
            self.conn.commit()

            account_group_id = self.cursor.lastrowid
            print(f"Account Group '{account_group_data['name']}' created with AG code: {ag_code}")
            return True, f"Account Group created successfully (AG Code: {ag_code})", account_group_id

        except sqlite3.Error as e:
            print(f"Error creating account group: {e}")
            self.conn.rollback()
            return False, f"Database error: {str(e)}", None

    def update_account_group(self, account_group_id, account_group_data):
        """
        Update an existing account group
        Returns (success: bool, message: str)
        Note: AG code is not updated as it's auto-generated
        """
        try:
            # Check if account group exists
            existing = self.get_account_group_by_id(account_group_id)
            if not existing:
                return False, "Account Group not found"

            query = """
            UPDATE account_groups SET
                name = ?,
                account_group_type = ?,
                status = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
            """

            values = (
                account_group_data['name'],
                account_group_data['account_group_type'],
                account_group_data.get('status', 'Active'),
                account_group_id
            )

            self.cursor.execute(query, values)
            self.conn.commit()

            print(f"Account Group ID {account_group_id} updated successfully")
            return True, "Account Group updated successfully"

        except sqlite3.Error as e:
            print(f"Error updating account group: {e}")
            self.conn.rollback()
            return False, f"Database error: {str(e)}"

    def delete_account_group(self, account_group_id):
        """
        Delete an account group
        Returns (success: bool, message: str)
        """
        try:
            query = "DELETE FROM account_groups WHERE id = ?"
            self.cursor.execute(query, (account_group_id,))
            self.conn.commit()

            if self.cursor.rowcount > 0:
                print(f"Account Group ID {account_group_id} deleted successfully")
                return True, "Account Group deleted successfully"
            else:
                return False, "Account Group not found"

        except sqlite3.Error as e:
            print(f"Error deleting account group: {e}")
            self.conn.rollback()
            return False, f"Database error: {str(e)}"

    def get_account_group_types(self):
        """Get list of account group types"""
        return ['Trading A/C', 'P&L Account', 'Balance Sheet']

    def get_by_type(self, account_group_type):
        """Get all account groups filtered by type"""
        try:
            query = """
            SELECT id, name, account_group_type, status, ag_code, created_at
            FROM account_groups
            WHERE account_group_type = ?
            ORDER BY name ASC
            """
            self.cursor.execute(query, (account_group_type,))
            rows = self.cursor.fetchall()
            return [dict(row) for row in rows]
        except sqlite3.Error as e:
            print(f"Error fetching account groups by type: {e}")
            return []
