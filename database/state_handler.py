"""
State Handler - Manages state CRUD operations using SQLite
"""

import sqlite3
from database.config import DB_PATH


class StateHandler:
    def __init__(self):
        self.conn = None
        self.cursor = None

    def connect(self):
        """Establish database connection"""
        try:
            import os
            abs_path = os.path.abspath(DB_PATH)
            print(f"\n{'='*70}")
            print(f"[STATE_HANDLER] Connecting to SQLite database...")
            print(f"[STATE_HANDLER] Database path: {abs_path}")
            print(f"[STATE_HANDLER] File exists: {os.path.exists(abs_path)}")
            if os.path.exists(abs_path):
                print(f"[STATE_HANDLER] File size: {os.path.getsize(abs_path)} bytes")
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
        """Create states table if it doesn't exist"""
        try:
            create_table_query = """
            CREATE TABLE IF NOT EXISTS states (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                state_code TEXT NOT NULL UNIQUE,
                state_name TEXT NOT NULL,
                status TEXT DEFAULT 'Active' CHECK(status IN ('Active', 'Inactive')),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
            self.cursor.execute(create_table_query)
            self.conn.commit()
            print("States table created/verified successfully")
        except sqlite3.Error as e:
            print(f"Error creating states table: {e}")

    def disconnect(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
            print("SQLite connection closed")

    def validate_state_code(self, code):
        """
        Validate state code:
        - Max 4 characters
        - Alphanumeric only
        """
        if not code or len(code) > 4:
            return False, "State Code must be 1-4 characters"

        if not code.isalnum():
            return False, "State Code must be alphanumeric"

        return True, "Valid"

    def get_all_states(self):
        """Get all states with their details"""
        try:
            query = """
            SELECT id, state_code, state_name, status, created_at
            FROM states
            ORDER BY state_name ASC
            """
            print(f"\n[GET_ALL_STATES] Executing query...")
            self.cursor.execute(query)
            rows = self.cursor.fetchall()

            print(f"[GET_ALL_STATES] Raw rows fetched: {len(rows)}")

            # Convert sqlite3.Row objects to dictionaries
            states = [dict(row) for row in rows]

            print(f"[GET_ALL_STATES] Returning {len(states)} states\n")
            return states
        except sqlite3.Error as e:
            print(f"[GET_ALL_STATES] Error fetching states: {e}")
            import traceback
            traceback.print_exc()
            return []

    def get_active_states(self):
        """Get only active states for dropdowns/foreign key selection"""
        try:
            query = """
            SELECT id, state_code, state_name, status, created_at
            FROM states
            WHERE status = 'Active'
            ORDER BY state_name ASC
            """
            print(f"\n[GET_ACTIVE_STATES] Executing query...")
            self.cursor.execute(query)
            rows = self.cursor.fetchall()

            # Convert sqlite3.Row objects to dictionaries
            states = [dict(row) for row in rows]

            print(f"[GET_ACTIVE_STATES] Returning {len(states)} active states\n")
            return states
        except sqlite3.Error as e:
            print(f"[GET_ACTIVE_STATES] Error fetching active states: {e}")
            import traceback
            traceback.print_exc()
            return []

    def get_state_by_id(self, state_id):
        """Get a single state by ID"""
        try:
            query = """
            SELECT id, state_code, state_name, status
            FROM states
            WHERE id = ?
            """
            self.cursor.execute(query, (state_id,))
            row = self.cursor.fetchone()
            return dict(row) if row else None
        except sqlite3.Error as e:
            print(f"Error fetching state: {e}")
            return None

    def get_state_by_code(self, state_code):
        """Get a single state by code"""
        try:
            query = "SELECT id FROM states WHERE state_code = ?"
            self.cursor.execute(query, (state_code,))
            row = self.cursor.fetchone()
            return dict(row) if row else None
        except sqlite3.Error as e:
            print(f"Error checking state code: {e}")
            return None

    def create_state(self, state_data):
        """
        Create a new state
        Returns (success: bool, message: str, state_id: int or None)
        """
        try:
            # Validate state code
            is_valid, message = self.validate_state_code(
                state_data.get('state_code', '')
            )
            if not is_valid:
                return False, message, None

            # Check if code already exists
            if self.get_state_by_code(state_data['state_code']):
                return False, "State Code already exists", None

            query = """
            INSERT INTO states (
                state_code, state_name, status
            ) VALUES (
                ?, ?, ?
            )
            """

            values = (
                state_data['state_code'].upper(),  # Store in uppercase
                state_data['state_name'],
                state_data.get('status', 'Active')
            )

            self.cursor.execute(query, values)
            self.conn.commit()

            state_id = self.cursor.lastrowid
            print(f"State '{state_data['state_name']}' created with code: {state_data['state_code']}")
            return True, f"State created successfully", state_id

        except sqlite3.Error as e:
            print(f"Error creating state: {e}")
            self.conn.rollback()
            return False, f"Database error: {str(e)}", None

    def update_state(self, state_id, state_data):
        """
        Update an existing state
        Returns (success: bool, message: str)
        Note: State Code cannot be changed after creation
        """
        try:
            # Check if state exists
            existing = self.get_state_by_id(state_id)
            if not existing:
                return False, "State not found"

            query = """
            UPDATE states SET
                state_name = ?,
                status = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
            """

            values = (
                state_data['state_name'],
                state_data.get('status', 'Active'),
                state_id
            )

            self.cursor.execute(query, values)
            self.conn.commit()

            print(f"State ID {state_id} updated successfully")
            return True, "State updated successfully"

        except sqlite3.Error as e:
            print(f"Error updating state: {e}")
            self.conn.rollback()
            return False, f"Database error: {str(e)}"

    def delete_state(self, state_id):
        """
        Delete a state
        Returns (success: bool, message: str)
        """
        try:
            query = "DELETE FROM states WHERE id = ?"
            self.cursor.execute(query, (state_id,))
            self.conn.commit()

            if self.cursor.rowcount > 0:
                print(f"State ID {state_id} deleted successfully")
                return True, "State deleted successfully"
            else:
                return False, "State not found"

        except sqlite3.Error as e:
            print(f"Error deleting state: {e}")
            self.conn.rollback()
            return False, f"Database error: {str(e)}"
