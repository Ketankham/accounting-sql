"""
Financial Year Handler - Manages financial year CRUD operations using SQLite
"""

import sqlite3
from database.config import DB_PATH


class FinancialYearHandler:
    def __init__(self):
        self.conn = None
        self.cursor = None

    def connect(self):
        """Establish database connection"""
        try:
            import os
            abs_path = os.path.abspath(DB_PATH)
            print(f"\n{'='*70}")
            print(f"[FY_HANDLER] Connecting to SQLite database...")
            print(f"[FY_HANDLER] Database path: {abs_path}")
            print(f"[FY_HANDLER] File exists: {os.path.exists(abs_path)}")
            if os.path.exists(abs_path):
                print(f"[FY_HANDLER] File size: {os.path.getsize(abs_path)} bytes")
            print(f"{'='*70}\n")

            self.conn = sqlite3.connect(DB_PATH)
            self.conn.row_factory = sqlite3.Row
            self.cursor = self.conn.cursor()
            print(f"✓ Successfully connected to SQLite database")

            # Create table if it doesn't exist
            self._create_table()

            # Debug: Check table contents immediately after connection
            self._debug_print_all()

            return True
        except sqlite3.Error as e:
            print(f"✗ Error connecting to SQLite: {e}")
            return False

    def _create_table(self):
        """Create financial_years table if it doesn't exist"""
        try:
            create_table_query = """
            CREATE TABLE IF NOT EXISTS financial_years (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fy_code TEXT NOT NULL UNIQUE,
                display_name TEXT NOT NULL,
                start_date DATE NOT NULL,
                end_date DATE NOT NULL,
                status TEXT DEFAULT 'Active' CHECK(status IN ('Active', 'Inactive')),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
            self.cursor.execute(create_table_query)
            self.conn.commit()
            print("Financial years table created/verified successfully")
        except sqlite3.Error as e:
            print(f"Error creating table: {e}")

    def disconnect(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
            print("SQLite connection closed")

    def _debug_print_all(self):
        """Debug method to print all financial years in database"""
        try:
            print("\n[DEBUG] Checking financial_years table contents...")
            self.cursor.execute("SELECT COUNT(*) as count FROM financial_years")
            count = self.cursor.fetchone()[0]
            print(f"[DEBUG] Total records in table: {count}")

            if count > 0:
                self.cursor.execute("SELECT * FROM financial_years ORDER BY id")
                rows = self.cursor.fetchall()
                print(f"[DEBUG] Retrieved {len(rows)} rows:")
                for idx, row in enumerate(rows, 1):
                    row_dict = dict(row)
                    print(f"  {idx}. ID={row_dict['id']}, Code={row_dict['fy_code']}, "
                          f"Name={row_dict['display_name']}, Status={row_dict['status']}")
            else:
                print("[DEBUG] ⚠ Table is EMPTY!")
            print()
        except sqlite3.Error as e:
            print(f"[DEBUG] Error checking table: {e}\n")

    def get_all_financial_years(self):
        """Get all financial years with their details"""
        try:
            query = """
            SELECT id, fy_code, display_name, start_date, end_date, status, created_at
            FROM financial_years
            ORDER BY start_date DESC
            """
            print(f"\n[GET_ALL_FY] Executing query...")
            self.cursor.execute(query)
            rows = self.cursor.fetchall()

            print(f"[GET_ALL_FY] Raw rows fetched: {len(rows)}")
            if rows:
                print(f"[GET_ALL_FY] First row type: {type(rows[0])}")
                print(f"[GET_ALL_FY] First row: {rows[0]}")

            # Convert sqlite3.Row objects to dictionaries
            financial_years = [dict(row) for row in rows]

            print(f"[GET_ALL_FY] Converted to {len(financial_years)} dictionaries")
            if financial_years:
                print(f"[GET_ALL_FY] First dict type: {type(financial_years[0])}")
                print(f"[GET_ALL_FY] First dict keys: {list(financial_years[0].keys())}")
                print(f"[GET_ALL_FY] Sample row data:")
                for key, value in financial_years[0].items():
                    print(f"    {key}: {value} (type: {type(value).__name__})")

            print(f"[GET_ALL_FY] Returning {len(financial_years)} financial years\n")
            return financial_years
        except sqlite3.Error as e:
            print(f"[GET_ALL_FY] ✗ Error fetching financial years: {e}")
            import traceback
            traceback.print_exc()
            return []

    def get_financial_year_by_id(self, fy_id):
        """Get a single financial year by ID"""
        try:
            query = """
            SELECT id, fy_code, display_name, start_date, end_date, status
            FROM financial_years
            WHERE id = ?
            """
            self.cursor.execute(query, (fy_id,))
            row = self.cursor.fetchone()
            return dict(row) if row else None
        except sqlite3.Error as e:
            print(f"Error fetching financial year: {e}")
            return None

    def get_financial_year_by_code(self, fy_code):
        """Get a single financial year by code"""
        try:
            query = "SELECT id FROM financial_years WHERE fy_code = ?"
            self.cursor.execute(query, (fy_code,))
            row = self.cursor.fetchone()
            return dict(row) if row else None
        except sqlite3.Error as e:
            print(f"Error checking financial year code: {e}")
            return None

    def check_date_overlap(self, start_date, end_date, exclude_id=None):
        """Check if date range overlaps with existing financial years"""
        try:
            if exclude_id:
                query = """
                SELECT id, fy_code, display_name
                FROM financial_years
                WHERE id != ? AND (
                    (start_date <= ? AND end_date >= ?) OR
                    (start_date <= ? AND end_date >= ?) OR
                    (start_date >= ? AND end_date <= ?)
                )
                """
                self.cursor.execute(query, (exclude_id, start_date, start_date,
                                           end_date, end_date, start_date, end_date))
            else:
                query = """
                SELECT id, fy_code, display_name
                FROM financial_years
                WHERE (
                    (start_date <= ? AND end_date >= ?) OR
                    (start_date <= ? AND end_date >= ?) OR
                    (start_date >= ? AND end_date <= ?)
                )
                """
                self.cursor.execute(query, (start_date, start_date,
                                           end_date, end_date, start_date, end_date))

            row = self.cursor.fetchone()
            return dict(row) if row else None
        except sqlite3.Error as e:
            print(f"Error checking date overlap: {e}")
            return None

    def create_financial_year(self, fy_data):
        """
        Create a new financial year
        Returns (success: bool, message: str, fy_id: int or None)
        """
        try:
            # Check if FY code already exists
            if self.get_financial_year_by_code(fy_data['fy_code']):
                return False, "Financial Year code already exists", None

            # Check for date overlap
            overlap = self.check_date_overlap(fy_data['start_date'], fy_data['end_date'])
            if overlap:
                return False, f"Date range overlaps with existing FY: {overlap['fy_code']}", None

            # Validate dates
            if fy_data['start_date'] >= fy_data['end_date']:
                return False, "End date must be after start date", None

            query = """
            INSERT INTO financial_years (
                fy_code, display_name, start_date, end_date, status
            ) VALUES (
                ?, ?, ?, ?, ?
            )
            """

            values = (
                fy_data['fy_code'],
                fy_data['display_name'],
                fy_data['start_date'],
                fy_data['end_date'],
                fy_data.get('status', 'Active')
            )

            self.cursor.execute(query, values)
            self.conn.commit()

            fy_id = self.cursor.lastrowid
            print(f"Financial Year '{fy_data['display_name']}' created successfully")
            return True, "Financial Year created successfully", fy_id

        except sqlite3.Error as e:
            print(f"Error creating financial year: {e}")
            self.conn.rollback()
            return False, f"Database error: {str(e)}", None

    def update_financial_year(self, fy_id, fy_data):
        """
        Update an existing financial year
        Returns (success: bool, message: str)
        """
        try:
            # Check if financial year exists
            existing = self.get_financial_year_by_id(fy_id)
            if not existing:
                return False, "Financial Year not found"

            # Check if FY code is being changed and if new code already exists
            if existing['fy_code'] != fy_data['fy_code']:
                if self.get_financial_year_by_code(fy_data['fy_code']):
                    return False, "Financial Year code already exists"

            # Check for date overlap (excluding current FY)
            overlap = self.check_date_overlap(
                fy_data['start_date'],
                fy_data['end_date'],
                exclude_id=fy_id
            )
            if overlap:
                return False, f"Date range overlaps with existing FY: {overlap['fy_code']}"

            # Validate dates
            if fy_data['start_date'] >= fy_data['end_date']:
                return False, "End date must be after start date"

            query = """
            UPDATE financial_years SET
                fy_code = ?,
                display_name = ?,
                start_date = ?,
                end_date = ?,
                status = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
            """

            values = (
                fy_data['fy_code'],
                fy_data['display_name'],
                fy_data['start_date'],
                fy_data['end_date'],
                fy_data.get('status', 'Active'),
                fy_id
            )

            self.cursor.execute(query, values)
            self.conn.commit()

            print(f"Financial Year ID {fy_id} updated successfully")
            return True, "Financial Year updated successfully"

        except sqlite3.Error as e:
            print(f"Error updating financial year: {e}")
            self.conn.rollback()
            return False, f"Database error: {str(e)}"

    def delete_financial_year(self, fy_id):
        """
        Delete a financial year
        Returns (success: bool, message: str)
        """
        try:
            query = "DELETE FROM financial_years WHERE id = ?"
            self.cursor.execute(query, (fy_id,))
            self.conn.commit()

            if self.cursor.rowcount > 0:
                print(f"Financial Year ID {fy_id} deleted successfully")
                return True, "Financial Year deleted successfully"
            else:
                return False, "Financial Year not found"

        except sqlite3.Error as e:
            print(f"Error deleting financial year: {e}")
            self.conn.rollback()
            return False, f"Database error: {str(e)}"
