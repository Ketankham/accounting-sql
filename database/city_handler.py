"""
City Handler - Manages city CRUD operations using SQLite
"""

import sqlite3
from database.config import DB_PATH


class CityHandler:
    def __init__(self):
        self.conn = None
        self.cursor = None

    def connect(self):
        """Establish database connection"""
        try:
            import os
            abs_path = os.path.abspath(DB_PATH)
            print(f"\n{'='*70}")
            print(f"[CITY_HANDLER] Connecting to SQLite database...")
            print(f"[CITY_HANDLER] Database path: {abs_path}")
            print(f"[CITY_HANDLER] File exists: {os.path.exists(abs_path)}")
            if os.path.exists(abs_path):
                print(f"[CITY_HANDLER] File size: {os.path.getsize(abs_path)} bytes")
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
        """Create cities table if it doesn't exist"""
        try:
            create_table_query = """
            CREATE TABLE IF NOT EXISTS cities (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                city_code TEXT NOT NULL UNIQUE,
                city_name TEXT NOT NULL,
                status TEXT DEFAULT 'Active' CHECK(status IN ('Active', 'Inactive')),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
            self.cursor.execute(create_table_query)
            self.conn.commit()
            print("Cities table created/verified successfully")
        except sqlite3.Error as e:
            print(f"Error creating cities table: {e}")

    def disconnect(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
            print("SQLite connection closed")

    def validate_city_code(self, code):
        """
        Validate city code:
        - Max 4 characters
        - Alphanumeric only
        """
        if not code or len(code) > 4:
            return False, "City Code must be 1-4 characters"

        if not code.isalnum():
            return False, "City Code must be alphanumeric"

        return True, "Valid"

    def get_all_cities(self):
        """Get all cities with their details"""
        try:
            query = """
            SELECT id, city_code, city_name, status, created_at
            FROM cities
            ORDER BY city_name ASC
            """
            print(f"\n[GET_ALL_CITIES] Executing query...")
            self.cursor.execute(query)
            rows = self.cursor.fetchall()

            print(f"[GET_ALL_CITIES] Raw rows fetched: {len(rows)}")

            # Convert sqlite3.Row objects to dictionaries
            cities = [dict(row) for row in rows]

            print(f"[GET_ALL_CITIES] Returning {len(cities)} cities\n")
            return cities
        except sqlite3.Error as e:
            print(f"[GET_ALL_CITIES] Error fetching cities: {e}")
            import traceback
            traceback.print_exc()
            return []

    def get_active_cities(self):
        """Get only active cities for dropdowns/foreign key selection"""
        try:
            query = """
            SELECT id, city_code, city_name, status, created_at
            FROM cities
            WHERE status = 'Active'
            ORDER BY city_name ASC
            """
            print(f"\n[GET_ACTIVE_CITIES] Executing query...")
            self.cursor.execute(query)
            rows = self.cursor.fetchall()

            # Convert sqlite3.Row objects to dictionaries
            cities = [dict(row) for row in rows]

            print(f"[GET_ACTIVE_CITIES] Returning {len(cities)} active cities\n")
            return cities
        except sqlite3.Error as e:
            print(f"[GET_ACTIVE_CITIES] Error fetching active cities: {e}")
            import traceback
            traceback.print_exc()
            return []

    def get_city_by_id(self, city_id):
        """Get a single city by ID"""
        try:
            query = """
            SELECT id, city_code, city_name, status
            FROM cities
            WHERE id = ?
            """
            self.cursor.execute(query, (city_id,))
            row = self.cursor.fetchone()
            return dict(row) if row else None
        except sqlite3.Error as e:
            print(f"Error fetching city: {e}")
            return None

    def get_city_by_code(self, city_code):
        """Get a single city by code"""
        try:
            query = "SELECT id FROM cities WHERE city_code = ?"
            self.cursor.execute(query, (city_code,))
            row = self.cursor.fetchone()
            return dict(row) if row else None
        except sqlite3.Error as e:
            print(f"Error checking city code: {e}")
            return None

    def create_city(self, city_data):
        """
        Create a new city
        Returns (success: bool, message: str, city_id: int or None)
        """
        try:
            # Validate city code
            is_valid, message = self.validate_city_code(
                city_data.get('city_code', '')
            )
            if not is_valid:
                return False, message, None

            # Check if code already exists
            if self.get_city_by_code(city_data['city_code']):
                return False, "City Code already exists", None

            query = """
            INSERT INTO cities (
                city_code, city_name, status
            ) VALUES (
                ?, ?, ?
            )
            """

            values = (
                city_data['city_code'].upper(),  # Store in uppercase
                city_data['city_name'],
                city_data.get('status', 'Active')
            )

            self.cursor.execute(query, values)
            self.conn.commit()

            city_id = self.cursor.lastrowid
            print(f"City '{city_data['city_name']}' created with code: {city_data['city_code']}")
            return True, f"City created successfully", city_id

        except sqlite3.Error as e:
            print(f"Error creating city: {e}")
            self.conn.rollback()
            return False, f"Database error: {str(e)}", None

    def update_city(self, city_id, city_data):
        """
        Update an existing city
        Returns (success: bool, message: str)
        Note: City Code cannot be changed after creation
        """
        try:
            # Check if city exists
            existing = self.get_city_by_id(city_id)
            if not existing:
                return False, "City not found"

            query = """
            UPDATE cities SET
                city_name = ?,
                status = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
            """

            values = (
                city_data['city_name'],
                city_data.get('status', 'Active'),
                city_id
            )

            self.cursor.execute(query, values)
            self.conn.commit()

            print(f"City ID {city_id} updated successfully")
            return True, "City updated successfully"

        except sqlite3.Error as e:
            print(f"Error updating city: {e}")
            self.conn.rollback()
            return False, f"Database error: {str(e)}"

    def delete_city(self, city_id):
        """
        Delete a city
        Returns (success: bool, message: str)
        """
        try:
            query = "DELETE FROM cities WHERE id = ?"
            self.cursor.execute(query, (city_id,))
            self.conn.commit()

            if self.cursor.rowcount > 0:
                print(f"City ID {city_id} deleted successfully")
                return True, "City deleted successfully"
            else:
                return False, "City not found"

        except sqlite3.Error as e:
            print(f"Error deleting city: {e}")
            self.conn.rollback()
            return False, f"Database error: {str(e)}"
