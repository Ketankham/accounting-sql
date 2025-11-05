"""
Authentication Handler - Manages user login and company data (SQLite)
"""

import sqlite3
import hashlib
from database.config import DB_PATH


class AuthHandler:
    def __init__(self):
        self.conn = None
        self.cursor = None

    def connect(self):
        """Establish database connection"""
        try:
            self.conn = sqlite3.connect(DB_PATH)
            self.conn.row_factory = sqlite3.Row
            self.cursor = self.conn.cursor()
            print("Successfully connected to SQLite database")

            # Create companies table first (referenced by users)
            self._create_companies_table()

            # Create users table if it doesn't exist
            self._create_users_table()

            return True
        except sqlite3.Error as e:
            print(f"Error connecting to SQLite: {e}")
            return False

    def _create_companies_table(self):
        """Create companies table if it doesn't exist (needed for foreign key)"""
        try:
            create_table_query = """
            CREATE TABLE IF NOT EXISTS companies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                company_code TEXT NOT NULL UNIQUE,
                company_name TEXT NOT NULL,
                bill_to_address TEXT NOT NULL,
                ship_to_address TEXT NOT NULL,
                state TEXT NOT NULL,
                city TEXT NOT NULL,
                gst_number TEXT NOT NULL,
                pan_number TEXT NOT NULL,
                landline_number TEXT,
                mobile_number TEXT,
                email_address TEXT,
                website TEXT,
                logo_path TEXT NOT NULL,
                status TEXT DEFAULT 'Active' CHECK(status IN ('Active', 'Inactive')),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
            self.cursor.execute(create_table_query)
            self.conn.commit()
            print("Companies table created/verified successfully")
        except sqlite3.Error as e:
            print(f"Error creating companies table: {e}")

    def _create_users_table(self):
        """Create users table if it doesn't exist"""
        try:
            create_table_query = """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                full_name TEXT NOT NULL,
                company_id INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (company_id) REFERENCES companies (id)
            )
            """
            self.cursor.execute(create_table_query)
            self.conn.commit()
            print("Users table created/verified successfully")
        except sqlite3.Error as e:
            print(f"Error creating users table: {e}")

    def disconnect(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
            print("SQLite connection closed")

    def hash_password(self, password):
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()

    def authenticate_user(self, username, password, company_name=None):
        """
        Authenticate user with username, password, and optional company
        Returns user data if successful, None otherwise
        """
        try:
            hashed_password = self.hash_password(password)

            if company_name:
                # Login with company selection
                query = """
                SELECT u.id, u.username, u.email, u.full_name,
                       c.id as company_id, c.company_name as company_name
                FROM users u
                LEFT JOIN companies c ON u.company_id = c.id
                WHERE u.username = ? AND u.password = ? AND c.company_name = ?
                """
                self.cursor.execute(query, (username, hashed_password, company_name))
            else:
                # Login without company selection
                query = """
                SELECT u.id, u.username, u.email, u.full_name,
                       c.id as company_id, c.company_name as company_name
                FROM users u
                LEFT JOIN companies c ON u.company_id = c.id
                WHERE u.username = ? AND u.password = ?
                """
                self.cursor.execute(query, (username, hashed_password))

            row = self.cursor.fetchone()

            if row:
                user = dict(row)
                print(f"User {username} authenticated successfully")
                return user
            else:
                print(f"Authentication failed for user {username}")
                return None

        except sqlite3.Error as e:
            print(f"Error during authentication: {e}")
            return None

    def get_all_companies(self):
        """Get all companies from database"""
        try:
            query = """
            SELECT id, company_name as name, company_code as description
            FROM companies
            ORDER BY company_name
            """
            self.cursor.execute(query)
            rows = self.cursor.fetchall()
            return [dict(row) for row in rows]
        except sqlite3.Error as e:
            print(f"Error fetching companies: {e}")
            return []

    def register_user(self, username, password, email, full_name, company_id=None):
        """
        Register a new user
        Returns True if successful, False otherwise
        """
        try:
            hashed_password = self.hash_password(password)

            query = """
            INSERT INTO users (username, password, email, full_name, company_id)
            VALUES (?, ?, ?, ?, ?)
            """
            self.cursor.execute(query, (username, hashed_password, email, full_name, company_id))
            self.conn.commit()

            print(f"User {username} registered successfully")
            return True

        except sqlite3.Error as e:
            print(f"Error registering user: {e}")
            self.conn.rollback()
            return False

    def username_exists(self, username):
        """Check if username already exists"""
        try:
            query = "SELECT COUNT(*) as count FROM users WHERE username = ?"
            self.cursor.execute(query, (username,))
            result = self.cursor.fetchone()
            return result['count'] > 0
        except sqlite3.Error as e:
            print(f"Error checking username: {e}")
            return False

    def email_exists(self, email):
        """Check if email already exists"""
        try:
            query = "SELECT COUNT(*) as count FROM users WHERE email = ?"
            self.cursor.execute(query, (email,))
            result = self.cursor.fetchone()
            return result['count'] > 0
        except sqlite3.Error as e:
            print(f"Error checking email: {e}")
            return False
