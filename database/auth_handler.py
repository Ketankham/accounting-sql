"""
Authentication Handler - Manages user login and company data
"""

import mysql.connector
from mysql.connector import Error
import hashlib
from database.config import DB_CONFIG


class AuthHandler:
    def __init__(self):
        self.connection = None
        self.cursor = None
    
    def connect(self):
        """Establish database connection"""
        try:
            self.connection = mysql.connector.connect(**DB_CONFIG)
            if self.connection.is_connected():
                self.cursor = self.connection.cursor(dictionary=True)
                print("Successfully connected to MySQL database")
                return True
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
            return False
    
    def disconnect(self):
        """Close database connection"""
        if self.connection and self.connection.is_connected():
            if self.cursor:
                self.cursor.close()
            self.connection.close()
            print("MySQL connection closed")
    
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
                       c.id as company_id, c.name as company_name
                FROM users u
                LEFT JOIN companies c ON u.company_id = c.id
                WHERE u.username = %s AND u.password = %s AND c.name = %s
                """
                self.cursor.execute(query, (username, hashed_password, company_name))
            else:
                # Login without company selection
                query = """
                SELECT u.id, u.username, u.email, u.full_name, 
                       c.id as company_id, c.name as company_name
                FROM users u
                LEFT JOIN companies c ON u.company_id = c.id
                WHERE u.username = %s AND u.password = %s
                """
                self.cursor.execute(query, (username, hashed_password))
            
            user = self.cursor.fetchone()
            
            if user:
                print(f"User {username} authenticated successfully")
                return user
            else:
                print(f"Authentication failed for user {username}")
                return None
                
        except Error as e:
            print(f"Error during authentication: {e}")
            return None
    
    def get_all_companies(self):
        """Get all companies from database"""
        try:
            query = """
            SELECT id,
                   COALESCE(company_name, name) as name,
                   description
            FROM companies
            ORDER BY COALESCE(company_name, name)
            """
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except Error as e:
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
            VALUES (%s, %s, %s, %s, %s)
            """
            self.cursor.execute(query, (username, hashed_password, email, full_name, company_id))
            self.connection.commit()
            
            print(f"User {username} registered successfully")
            return True
            
        except Error as e:
            print(f"Error registering user: {e}")
            self.connection.rollback()
            return False
    
    def username_exists(self, username):
        """Check if username already exists"""
        try:
            query = "SELECT COUNT(*) as count FROM users WHERE username = %s"
            self.cursor.execute(query, (username,))
            result = self.cursor.fetchone()
            return result['count'] > 0
        except Error as e:
            print(f"Error checking username: {e}")
            return False
    
    def email_exists(self, email):
        """Check if email already exists"""
        try:
            query = "SELECT COUNT(*) as count FROM users WHERE email = %s"
            self.cursor.execute(query, (email,))
            result = self.cursor.fetchone()
            return result['count'] > 0
        except Error as e:
            print(f"Error checking email: {e}")
            return False
