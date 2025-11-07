"""
Item Company Handler - Manages item company (suppliers/manufacturers) CRUD operations using SQLite
"""

import sqlite3
from database.config import DB_PATH


class ItemCompanyHandler:
    def __init__(self):
        self.conn = None
        self.cursor = None

    def connect(self):
        """Establish database connection"""
        try:
            import os
            abs_path = os.path.abspath(DB_PATH)
            print(f"\n{'='*70}")
            print(f"[ITEM_COMPANY_HANDLER] Connecting to SQLite database...")
            print(f"[ITEM_COMPANY_HANDLER] Database path: {abs_path}")
            print(f"[ITEM_COMPANY_HANDLER] File exists: {os.path.exists(abs_path)}")
            if os.path.exists(abs_path):
                print(f"[ITEM_COMPANY_HANDLER] File size: {os.path.getsize(abs_path)} bytes")
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
        """Create item_companies table if it doesn't exist"""
        try:
            create_table_query = """
            CREATE TABLE IF NOT EXISTS item_companies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                company_code TEXT NOT NULL UNIQUE,
                company_name TEXT NOT NULL,
                status TEXT DEFAULT 'Active' CHECK(status IN ('Active', 'Inactive')),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
            self.cursor.execute(create_table_query)
            self.conn.commit()
            print("Item Companies table created/verified successfully")
        except sqlite3.Error as e:
            print(f"Error creating item_companies table: {e}")

    def disconnect(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
            print("SQLite connection closed")

    def validate_company_code(self, code):
        """
        Validate company code:
        - Max 4 characters
        - Alphanumeric only
        """
        if not code or len(code) > 4:
            return False, "Company Code must be 1-4 characters"

        if not code.isalnum():
            return False, "Company Code must be alphanumeric"

        return True, "Valid"

    def get_all_item_companies(self):
        """Get all item companies with their details"""
        try:
            query = """
            SELECT id, company_code, company_name, status, created_at
            FROM item_companies
            ORDER BY company_name ASC
            """
            print(f"\n[GET_ALL_ITEM_COMPANIES] Executing query...")
            self.cursor.execute(query)
            rows = self.cursor.fetchall()

            print(f"[GET_ALL_ITEM_COMPANIES] Raw rows fetched: {len(rows)}")

            # Convert sqlite3.Row objects to dictionaries
            companies = [dict(row) for row in rows]

            print(f"[GET_ALL_ITEM_COMPANIES] Returning {len(companies)} item companies\n")
            return companies
        except sqlite3.Error as e:
            print(f"[GET_ALL_ITEM_COMPANIES] Error fetching item companies: {e}")
            import traceback
            traceback.print_exc()
            return []

    def get_active_item_companies(self):
        """Get only active item companies for dropdowns/foreign key selection"""
        try:
            query = """
            SELECT id, company_code, company_name, status, created_at
            FROM item_companies
            WHERE status = 'Active'
            ORDER BY company_name ASC
            """
            print(f"\n[GET_ACTIVE_ITEM_COMPANIES] Executing query...")
            self.cursor.execute(query)
            rows = self.cursor.fetchall()

            # Convert sqlite3.Row objects to dictionaries
            companies = [dict(row) for row in rows]

            print(f"[GET_ACTIVE_ITEM_COMPANIES] Returning {len(companies)} active item companies\n")
            return companies
        except sqlite3.Error as e:
            print(f"[GET_ACTIVE_ITEM_COMPANIES] Error fetching active item companies: {e}")
            import traceback
            traceback.print_exc()
            return []

    def get_item_company_by_id(self, company_id):
        """Get a single item company by ID"""
        try:
            query = """
            SELECT id, company_code, company_name, status
            FROM item_companies
            WHERE id = ?
            """
            self.cursor.execute(query, (company_id,))
            row = self.cursor.fetchone()
            return dict(row) if row else None
        except sqlite3.Error as e:
            print(f"Error fetching item company: {e}")
            return None

    def get_item_company_by_code(self, company_code):
        """Get a single item company by code"""
        try:
            query = "SELECT id FROM item_companies WHERE company_code = ?"
            self.cursor.execute(query, (company_code,))
            row = self.cursor.fetchone()
            return dict(row) if row else None
        except sqlite3.Error as e:
            print(f"Error checking company code: {e}")
            return None

    def create_item_company(self, company_data):
        """
        Create a new item company
        Returns (success: bool, message: str, company_id: int or None)
        """
        try:
            # Validate company code
            is_valid, message = self.validate_company_code(
                company_data.get('company_code', '')
            )
            if not is_valid:
                return False, message, None

            # Check if code already exists
            if self.get_item_company_by_code(company_data['company_code']):
                return False, "Company Code already exists", None

            query = """
            INSERT INTO item_companies (
                company_code, company_name, status
            ) VALUES (
                ?, ?, ?
            )
            """

            values = (
                company_data['company_code'].upper(),  # Store in uppercase
                company_data['company_name'],
                company_data.get('status', 'Active')
            )

            self.cursor.execute(query, values)
            self.conn.commit()

            company_id = self.cursor.lastrowid
            print(f"Item Company '{company_data['company_name']}' created with code: {company_data['company_code']}")
            return True, f"Item Company created successfully", company_id

        except sqlite3.Error as e:
            print(f"Error creating item company: {e}")
            self.conn.rollback()
            return False, f"Database error: {str(e)}", None

    def update_item_company(self, company_id, company_data):
        """
        Update an existing item company
        Returns (success: bool, message: str)
        Note: Company Code cannot be changed after creation
        """
        try:
            # Check if company exists
            existing = self.get_item_company_by_id(company_id)
            if not existing:
                return False, "Item Company not found"

            query = """
            UPDATE item_companies SET
                company_name = ?,
                status = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
            """

            values = (
                company_data['company_name'],
                company_data.get('status', 'Active'),
                company_id
            )

            self.cursor.execute(query, values)
            self.conn.commit()

            print(f"Item Company ID {company_id} updated successfully")
            return True, "Item Company updated successfully"

        except sqlite3.Error as e:
            print(f"Error updating item company: {e}")
            self.conn.rollback()
            return False, f"Database error: {str(e)}"

    def delete_item_company(self, company_id):
        """
        Delete an item company
        Returns (success: bool, message: str)
        """
        try:
            query = "DELETE FROM item_companies WHERE id = ?"
            self.cursor.execute(query, (company_id,))
            self.conn.commit()

            if self.cursor.rowcount > 0:
                print(f"Item Company ID {company_id} deleted successfully")
                return True, "Item Company deleted successfully"
            else:
                return False, "Item Company not found"

        except sqlite3.Error as e:
            print(f"Error deleting item company: {e}")
            self.conn.rollback()
            return False, f"Database error: {str(e)}"
