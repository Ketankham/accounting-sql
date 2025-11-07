"""
Business Partner Handler - Manages business partner CRUD operations using SQLite
"""

import sqlite3
from database.config import DB_PATH


class BusinessPartnerHandler:
    def __init__(self):
        self.conn = None
        self.cursor = None

    def connect(self):
        """Establish database connection"""
        try:
            import os
            abs_path = os.path.abspath(DB_PATH)
            print(f"\n{'='*70}")
            print(f"[BUSINESS_PARTNER_HANDLER] Connecting to SQLite database...")
            print(f"[BUSINESS_PARTNER_HANDLER] Database path: {abs_path}")
            print(f"[BUSINESS_PARTNER_HANDLER] File exists: {os.path.exists(abs_path)}")
            if os.path.exists(abs_path):
                print(f"[BUSINESS_PARTNER_HANDLER] File size: {os.path.getsize(abs_path)} bytes")
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
        """Create business_partners table if it doesn't exist"""
        try:
            create_table_query = """
            CREATE TABLE IF NOT EXISTS business_partners (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                bp_code TEXT NOT NULL UNIQUE,
                bp_name TEXT NOT NULL,
                bill_to_address TEXT,
                ship_to_address TEXT,
                city_id INTEGER,
                state_id INTEGER,
                mobile TEXT,
                account_group_id INTEGER NOT NULL,
                book_code_id INTEGER NOT NULL,
                account_type_id INTEGER NOT NULL,
                opening_balance REAL DEFAULT 0,
                balance_type TEXT DEFAULT 'Debit' CHECK(balance_type IN ('Credit', 'Debit')),
                status TEXT DEFAULT 'Active' CHECK(status IN ('Active', 'Inactive')),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (city_id) REFERENCES cities(id),
                FOREIGN KEY (state_id) REFERENCES states(id),
                FOREIGN KEY (account_group_id) REFERENCES account_groups(id),
                FOREIGN KEY (book_code_id) REFERENCES book_codes(id),
                FOREIGN KEY (account_type_id) REFERENCES account_types(id)
            )
            """
            self.cursor.execute(create_table_query)
            self.conn.commit()
            print("Business Partners table created/verified successfully")
        except sqlite3.Error as e:
            print(f"Error creating business_partners table: {e}")

    def disconnect(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
            print("SQLite connection closed")

    def generate_bp_code(self, bp_name, account_group_id):
        """
        Generate BP code based on:
        - First letter from BP name
        - Next 2 letters from account group code
        - Next 3 digits as serial number (001, 002, etc.)

        Example: BP Name="ABC Company", Account Group Code="CTA" => ACT001
        """
        # Get first letter from BP name (uppercase)
        first_letter = bp_name[0].upper() if bp_name else 'X'

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
            SELECT bp_code FROM business_partners
            WHERE bp_code LIKE ?
            ORDER BY bp_code DESC
            LIMIT 1
            """
            self.cursor.execute(query, (f"{prefix}%",))
            result = self.cursor.fetchone()

            if result:
                # Extract last 3 digits and increment
                last_code = result['bp_code']
                last_serial = int(last_code[-3:])
                next_serial = last_serial + 1
            else:
                # First entry for this prefix
                next_serial = 1

            # Format serial number as 3 digits (001, 002, etc.)
            serial_str = str(next_serial).zfill(3)

            # Return complete BP code (6 characters)
            bp_code = f"{prefix}{serial_str}"
            return bp_code

        except sqlite3.Error as e:
            print(f"Error generating BP code: {e}")
            return f"{first_letter}XX001"

    def get_all_business_partners(self):
        """Get all business partners with their details"""
        try:
            query = """
            SELECT
                bp.id,
                bp.bp_code,
                bp.bp_name,
                bp.bill_to_address,
                bp.ship_to_address,
                bp.city_id,
                c.name as city_name,
                bp.state_id,
                s.name as state_name,
                bp.mobile,
                bp.account_group_id,
                ag.name as account_group_name,
                bp.book_code_id,
                bc.name as book_code_name,
                bp.account_type_id,
                at.name as account_type_name,
                bp.opening_balance,
                bp.balance_type,
                bp.status,
                bp.created_at
            FROM business_partners bp
            LEFT JOIN cities c ON bp.city_id = c.id
            LEFT JOIN states s ON bp.state_id = s.id
            LEFT JOIN account_groups ag ON bp.account_group_id = ag.id
            LEFT JOIN book_codes bc ON bp.book_code_id = bc.id
            LEFT JOIN account_types at ON bp.account_type_id = at.id
            ORDER BY bp.bp_name ASC
            """
            print(f"\n[GET_ALL_BUSINESS_PARTNERS] Executing query...")
            self.cursor.execute(query)
            rows = self.cursor.fetchall()

            print(f"[GET_ALL_BUSINESS_PARTNERS] Raw rows fetched: {len(rows)}")

            # Convert sqlite3.Row objects to dictionaries
            partners = [dict(row) for row in rows]

            print(f"[GET_ALL_BUSINESS_PARTNERS] Returning {len(partners)} business partners\n")
            return partners
        except sqlite3.Error as e:
            print(f"[GET_ALL_BUSINESS_PARTNERS] Error fetching business partners: {e}")
            import traceback
            traceback.print_exc()
            return []

    def get_active_business_partners(self):
        """Get only active business partners for dropdowns/foreign key selection"""
        try:
            query = """
            SELECT
                bp.id,
                bp.bp_code,
                bp.bp_name,
                bp.bill_to_address,
                bp.ship_to_address,
                bp.city_id,
                c.name as city_name,
                bp.state_id,
                s.name as state_name,
                bp.mobile,
                bp.account_group_id,
                ag.name as account_group_name,
                bp.book_code_id,
                bc.name as book_code_name,
                bp.account_type_id,
                at.name as account_type_name,
                bp.opening_balance,
                bp.balance_type,
                bp.status,
                bp.created_at
            FROM business_partners bp
            LEFT JOIN cities c ON bp.city_id = c.id
            LEFT JOIN states s ON bp.state_id = s.id
            LEFT JOIN account_groups ag ON bp.account_group_id = ag.id
            LEFT JOIN book_codes bc ON bp.book_code_id = bc.id
            LEFT JOIN account_types at ON bp.account_type_id = at.id
            WHERE bp.status = 'Active'
            ORDER BY bp.bp_name ASC
            """
            print(f"\n[GET_ACTIVE_BUSINESS_PARTNERS] Executing query...")
            self.cursor.execute(query)
            rows = self.cursor.fetchall()

            # Convert sqlite3.Row objects to dictionaries
            partners = [dict(row) for row in rows]

            print(f"[GET_ACTIVE_BUSINESS_PARTNERS] Returning {len(partners)} active business partners\n")
            return partners
        except sqlite3.Error as e:
            print(f"[GET_ACTIVE_BUSINESS_PARTNERS] Error fetching active business partners: {e}")
            import traceback
            traceback.print_exc()
            return []

    def get_business_partner_by_id(self, bp_id):
        """Get a single business partner by ID"""
        try:
            query = """
            SELECT
                bp.id,
                bp.bp_code,
                bp.bp_name,
                bp.bill_to_address,
                bp.ship_to_address,
                bp.city_id,
                c.name as city_name,
                bp.state_id,
                s.name as state_name,
                bp.mobile,
                bp.account_group_id,
                ag.name as account_group_name,
                bp.book_code_id,
                bc.name as book_code_name,
                bp.account_type_id,
                at.name as account_type_name,
                bp.opening_balance,
                bp.balance_type,
                bp.status
            FROM business_partners bp
            LEFT JOIN cities c ON bp.city_id = c.id
            LEFT JOIN states s ON bp.state_id = s.id
            LEFT JOIN account_groups ag ON bp.account_group_id = ag.id
            LEFT JOIN book_codes bc ON bp.book_code_id = bc.id
            LEFT JOIN account_types at ON bp.account_type_id = at.id
            WHERE bp.id = ?
            """
            self.cursor.execute(query, (bp_id,))
            row = self.cursor.fetchone()
            return dict(row) if row else None
        except sqlite3.Error as e:
            print(f"Error fetching business partner: {e}")
            return None

    def get_business_partner_by_code(self, bp_code):
        """Get a single business partner by BP code"""
        try:
            query = "SELECT id FROM business_partners WHERE bp_code = ?"
            self.cursor.execute(query, (bp_code,))
            row = self.cursor.fetchone()
            return dict(row) if row else None
        except sqlite3.Error as e:
            print(f"Error checking BP code: {e}")
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

    def get_active_cities(self):
        """Get all active cities for dropdown"""
        try:
            query = """
            SELECT id, city_name as name, city_code
            FROM cities
            WHERE status = 'Active'
            ORDER BY city_name ASC
            """
            self.cursor.execute(query)
            rows = self.cursor.fetchall()
            return [dict(row) for row in rows]
        except sqlite3.Error as e:
            print(f"Error fetching active cities: {e}")
            return []

    def get_active_states(self):
        """Get all active states for dropdown"""
        try:
            query = """
            SELECT id, state_name as name, state_code
            FROM states
            WHERE status = 'Active'
            ORDER BY state_name ASC
            """
            self.cursor.execute(query)
            rows = self.cursor.fetchall()
            return [dict(row) for row in rows]
        except sqlite3.Error as e:
            print(f"Error fetching active states: {e}")
            return []

    def create_business_partner(self, bp_data):
        """
        Create a new business partner
        Returns (success: bool, message: str, bp_id: int or None)
        """
        try:
            # Generate BP code
            bp_code = self.generate_bp_code(
                bp_data['bp_name'],
                bp_data['account_group_id']
            )

            # Check if BP code already exists (shouldn't happen with auto-generation)
            if self.get_business_partner_by_code(bp_code):
                return False, "BP code already exists", None

            query = """
            INSERT INTO business_partners (
                bp_code, bp_name, bill_to_address, ship_to_address,
                city_id, state_id, mobile, account_group_id, book_code_id,
                account_type_id, opening_balance, balance_type, status
            ) VALUES (
                ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
            )
            """

            values = (
                bp_code,
                bp_data['bp_name'],
                bp_data.get('bill_to_address', ''),
                bp_data.get('ship_to_address', ''),
                bp_data.get('city_id'),
                bp_data.get('state_id'),
                bp_data.get('mobile', ''),
                bp_data['account_group_id'],
                bp_data['book_code_id'],
                bp_data['account_type_id'],
                bp_data.get('opening_balance', 0),
                bp_data.get('balance_type', 'Debit'),
                bp_data.get('status', 'Active')
            )

            self.cursor.execute(query, values)
            self.conn.commit()

            bp_id = self.cursor.lastrowid
            print(f"Business Partner '{bp_data['bp_name']}' created with BP code: {bp_code}")
            return True, f"Business Partner created successfully (BP Code: {bp_code})", bp_id

        except sqlite3.Error as e:
            print(f"Error creating business partner: {e}")
            self.conn.rollback()
            return False, f"Database error: {str(e)}", None

    def update_business_partner(self, bp_id, bp_data):
        """
        Update an existing business partner
        Returns (success: bool, message: str)
        Note: BP code is not updated as it's auto-generated
        """
        try:
            # Check if business partner exists
            existing = self.get_business_partner_by_id(bp_id)
            if not existing:
                return False, "Business Partner not found"

            query = """
            UPDATE business_partners SET
                bp_name = ?,
                bill_to_address = ?,
                ship_to_address = ?,
                city_id = ?,
                state_id = ?,
                mobile = ?,
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
                bp_data['bp_name'],
                bp_data.get('bill_to_address', ''),
                bp_data.get('ship_to_address', ''),
                bp_data.get('city_id'),
                bp_data.get('state_id'),
                bp_data.get('mobile', ''),
                bp_data['account_group_id'],
                bp_data['book_code_id'],
                bp_data['account_type_id'],
                bp_data.get('opening_balance', 0),
                bp_data.get('balance_type', 'Debit'),
                bp_data.get('status', 'Active'),
                bp_id
            )

            self.cursor.execute(query, values)
            self.conn.commit()

            print(f"Business Partner ID {bp_id} updated successfully")
            return True, "Business Partner updated successfully"

        except sqlite3.Error as e:
            print(f"Error updating business partner: {e}")
            self.conn.rollback()
            return False, f"Database error: {str(e)}"

    def delete_business_partner(self, bp_id):
        """
        Delete a business partner
        Returns (success: bool, message: str)
        """
        try:
            query = "DELETE FROM business_partners WHERE id = ?"
            self.cursor.execute(query, (bp_id,))
            self.conn.commit()

            if self.cursor.rowcount > 0:
                print(f"Business Partner ID {bp_id} deleted successfully")
                return True, "Business Partner deleted successfully"
            else:
                return False, "Business Partner not found"

        except sqlite3.Error as e:
            print(f"Error deleting business partner: {e}")
            self.conn.rollback()
            return False, f"Database error: {str(e)}"
