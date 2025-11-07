"""
Account Master Handler - Manages account master CRUD operations using SQLite
"""

import sqlite3
from database.config import DB_PATH


class AccountMasterHandler:
    def __init__(self):
        self.conn = None
        self.cursor = None

    def connect(self):
        """Establish database connection"""
        try:
            import os
            abs_path = os.path.abspath(DB_PATH)
            print(f"\n{'='*70}")
            print(f"[ACCOUNT_MASTER_HANDLER] Connecting to SQLite database...")
            print(f"[ACCOUNT_MASTER_HANDLER] Database path: {abs_path}")
            print(f"[ACCOUNT_MASTER_HANDLER] File exists: {os.path.exists(abs_path)}")
            if os.path.exists(abs_path):
                print(f"[ACCOUNT_MASTER_HANDLER] File size: {os.path.getsize(abs_path)} bytes")
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
        """Create account_master table if it doesn't exist"""
        try:
            create_table_query = """
            CREATE TABLE IF NOT EXISTS account_master (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                account_name TEXT NOT NULL,
                account_group_id INTEGER NOT NULL,
                book_code_id INTEGER NOT NULL,
                account_type_id INTEGER NOT NULL,
                opening_balance REAL DEFAULT 0,
                balance_type TEXT DEFAULT 'Debit' CHECK(balance_type IN ('Credit', 'Debit')),
                status TEXT DEFAULT 'Active' CHECK(status IN ('Active', 'Inactive')),
                account_code TEXT NOT NULL UNIQUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (account_group_id) REFERENCES account_groups(id),
                FOREIGN KEY (book_code_id) REFERENCES book_codes(id),
                FOREIGN KEY (account_type_id) REFERENCES account_types(id)
            )
            """
            self.cursor.execute(create_table_query)
            self.conn.commit()
            print("Account Master table created/verified successfully")
        except sqlite3.Error as e:
            print(f"Error creating account_master table: {e}")

    def disconnect(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
            print("SQLite connection closed")

    def generate_account_code(self, account_name, account_group_id):
        """
        Generate Account code based on:
        - First letter from account name
        - Next 2 letters from account group code
        - Next 3 digits as serial number (001, 002, etc.)

        Example: Account Name="Sales Account", Account Group Code="STA" => SST001
        """
        # Get first letter from account name (uppercase)
        first_letter = account_name[0].upper() if account_name else 'X'

        # Get account group code (AG code from account_groups table)
        try:
            query = "SELECT ag_code FROM account_groups WHERE id = ?"
            self.cursor.execute(query, (account_group_id,))
            result = self.cursor.fetchone()

            if result:
                ag_code = result['ag_code']
                # Take first 2 letters from AG code (which is 6 chars: e.g., STA001)
                ag_prefix = ag_code[:2] if len(ag_code) >= 2 else 'XX'
            else:
                ag_prefix = 'XX'

            # Get next serial number for this prefix
            prefix = f"{first_letter}{ag_prefix}"

            query = """
            SELECT account_code FROM account_master
            WHERE account_code LIKE ?
            ORDER BY account_code DESC
            LIMIT 1
            """
            self.cursor.execute(query, (f"{prefix}%",))
            result = self.cursor.fetchone()

            if result:
                # Extract last 3 digits and increment
                last_code = result['account_code']
                last_serial = int(last_code[-3:])
                next_serial = last_serial + 1
            else:
                # First entry for this prefix
                next_serial = 1

            # Format serial number as 3 digits (001, 002, etc.)
            serial_str = str(next_serial).zfill(3)

            # Return complete Account code (6 characters)
            account_code = f"{prefix}{serial_str}"
            return account_code

        except sqlite3.Error as e:
            print(f"Error generating Account code: {e}")
            return f"{first_letter}XX001"

    def get_all_accounts(self):
        """Get all account masters with their details"""
        try:
            query = """
            SELECT
                am.id,
                am.account_name,
                am.account_group_id,
                ag.name as account_group_name,
                am.book_code_id,
                bc.name as book_code_name,
                am.account_type_id,
                at.name as account_type_name,
                am.opening_balance,
                am.balance_type,
                am.status,
                am.account_code,
                am.created_at
            FROM account_master am
            LEFT JOIN account_groups ag ON am.account_group_id = ag.id
            LEFT JOIN book_codes bc ON am.book_code_id = bc.id
            LEFT JOIN account_types at ON am.account_type_id = at.id
            ORDER BY am.account_name ASC
            """
            print(f"\n[GET_ALL_ACCOUNTS] Executing query...")
            self.cursor.execute(query)
            rows = self.cursor.fetchall()

            print(f"[GET_ALL_ACCOUNTS] Raw rows fetched: {len(rows)}")

            # Convert sqlite3.Row objects to dictionaries
            accounts = [dict(row) for row in rows]

            print(f"[GET_ALL_ACCOUNTS] Returning {len(accounts)} accounts\n")
            return accounts
        except sqlite3.Error as e:
            print(f"[GET_ALL_ACCOUNTS] Error fetching accounts: {e}")
            import traceback
            traceback.print_exc()
            return []

    def get_active_accounts(self):
        """Get only active accounts for dropdowns/foreign key selection"""
        try:
            query = """
            SELECT
                am.id,
                am.account_name,
                am.account_group_id,
                ag.name as account_group_name,
                am.book_code_id,
                bc.name as book_code_name,
                am.account_type_id,
                at.name as account_type_name,
                am.opening_balance,
                am.balance_type,
                am.status,
                am.account_code,
                am.created_at
            FROM account_master am
            LEFT JOIN account_groups ag ON am.account_group_id = ag.id
            LEFT JOIN book_codes bc ON am.book_code_id = bc.id
            LEFT JOIN account_types at ON am.account_type_id = at.id
            WHERE am.status = 'Active'
            ORDER BY am.account_name ASC
            """
            print(f"\n[GET_ACTIVE_ACCOUNTS] Executing query...")
            self.cursor.execute(query)
            rows = self.cursor.fetchall()

            # Convert sqlite3.Row objects to dictionaries
            accounts = [dict(row) for row in rows]

            print(f"[GET_ACTIVE_ACCOUNTS] Returning {len(accounts)} active accounts\n")
            return accounts
        except sqlite3.Error as e:
            print(f"[GET_ACTIVE_ACCOUNTS] Error fetching active accounts: {e}")
            import traceback
            traceback.print_exc()
            return []

    def get_account_by_id(self, account_id):
        """Get a single account by ID"""
        try:
            query = """
            SELECT
                am.id,
                am.account_name,
                am.account_group_id,
                ag.name as account_group_name,
                am.book_code_id,
                bc.name as book_code_name,
                am.account_type_id,
                at.name as account_type_name,
                am.opening_balance,
                am.balance_type,
                am.status,
                am.account_code
            FROM account_master am
            LEFT JOIN account_groups ag ON am.account_group_id = ag.id
            LEFT JOIN book_codes bc ON am.book_code_id = bc.id
            LEFT JOIN account_types at ON am.account_type_id = at.id
            WHERE am.id = ?
            """
            self.cursor.execute(query, (account_id,))
            row = self.cursor.fetchone()
            return dict(row) if row else None
        except sqlite3.Error as e:
            print(f"Error fetching account: {e}")
            return None

    def get_account_by_code(self, account_code):
        """Get a single account by account code"""
        try:
            query = "SELECT id FROM account_master WHERE account_code = ?"
            self.cursor.execute(query, (account_code,))
            row = self.cursor.fetchone()
            return dict(row) if row else None
        except sqlite3.Error as e:
            print(f"Error checking account code: {e}")
            return None

    def get_active_account_groups(self):
        """Get all active account groups for dropdown"""
        try:
            query = """
            SELECT id, name, ag_code
            FROM account_groups
            WHERE status = 'Active'
            ORDER BY name ASC
            """
            self.cursor.execute(query)
            rows = self.cursor.fetchall()
            return [dict(row) for row in rows]
        except sqlite3.Error as e:
            print(f"Error fetching active account groups: {e}")
            return []

    def get_active_book_codes(self):
        """Get all active book codes for dropdown"""
        try:
            query = """
            SELECT id, code, name, book_number
            FROM book_codes
            WHERE is_active = 1
            ORDER BY sort_order ASC
            """
            self.cursor.execute(query)
            rows = self.cursor.fetchall()
            return [dict(row) for row in rows]
        except sqlite3.Error as e:
            print(f"Error fetching active book codes: {e}")
            return []

    def get_active_account_types(self):
        """Get all active account types for dropdown"""
        try:
            query = """
            SELECT id, code, name
            FROM account_types
            WHERE is_active = 1
            ORDER BY sort_order ASC
            """
            self.cursor.execute(query)
            rows = self.cursor.fetchall()
            return [dict(row) for row in rows]
        except sqlite3.Error as e:
            print(f"Error fetching active account types: {e}")
            return []

    def create_account(self, account_data):
        """
        Create a new account master
        Returns (success: bool, message: str, account_id: int or None)
        """
        try:
            # Generate Account code
            account_code = self.generate_account_code(
                account_data['account_name'],
                account_data['account_group_id']
            )

            # Check if Account code already exists (shouldn't happen with auto-generation)
            if self.get_account_by_code(account_code):
                return False, "Account code already exists", None

            query = """
            INSERT INTO account_master (
                account_name, account_group_id, book_code_id, account_type_id,
                opening_balance, balance_type, status, account_code
            ) VALUES (
                ?, ?, ?, ?, ?, ?, ?, ?
            )
            """

            values = (
                account_data['account_name'],
                account_data['account_group_id'],
                account_data['book_code_id'],
                account_data['account_type_id'],
                account_data.get('opening_balance', 0),
                account_data.get('balance_type', 'Debit'),
                account_data.get('status', 'Active'),
                account_code
            )

            self.cursor.execute(query, values)
            self.conn.commit()

            account_id = self.cursor.lastrowid
            print(f"Account '{account_data['account_name']}' created with Account code: {account_code}")
            return True, f"Account created successfully (Account Code: {account_code})", account_id

        except sqlite3.Error as e:
            print(f"Error creating account: {e}")
            self.conn.rollback()
            return False, f"Database error: {str(e)}", None

    def update_account(self, account_id, account_data):
        """
        Update an existing account master
        Returns (success: bool, message: str)
        Note: Account code is not updated as it's auto-generated
        """
        try:
            # Check if account exists
            existing = self.get_account_by_id(account_id)
            if not existing:
                return False, "Account not found"

            query = """
            UPDATE account_master SET
                account_name = ?,
                account_group_id = ?,
                book_code_id = ?,
                account_type_id = ?,
                opening_balance = ?,
                balance_type = ?,
                status = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
            """

            values = (
                account_data['account_name'],
                account_data['account_group_id'],
                account_data['book_code_id'],
                account_data['account_type_id'],
                account_data.get('opening_balance', 0),
                account_data.get('balance_type', 'Debit'),
                account_data.get('status', 'Active'),
                account_id
            )

            self.cursor.execute(query, values)
            self.conn.commit()

            print(f"Account ID {account_id} updated successfully")
            return True, "Account updated successfully"

        except sqlite3.Error as e:
            print(f"Error updating account: {e}")
            self.conn.rollback()
            return False, f"Database error: {str(e)}"

    def delete_account(self, account_id):
        """
        Delete an account master
        Returns (success: bool, message: str)
        """
        try:
            query = "DELETE FROM account_master WHERE id = ?"
            self.cursor.execute(query, (account_id,))
            self.conn.commit()

            if self.cursor.rowcount > 0:
                print(f"Account ID {account_id} deleted successfully")
                return True, "Account deleted successfully"
            else:
                return False, "Account not found"

        except sqlite3.Error as e:
            print(f"Error deleting account: {e}")
            self.conn.rollback()
            return False, f"Database error: {str(e)}"
