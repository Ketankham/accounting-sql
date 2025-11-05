"""
Create a test admin user in the database
"""

import sqlite3
import hashlib
from database.config import DB_PATH

def hash_password(password):
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def create_test_user():
    """Create test admin user"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Create admin user
        username = "admin"
        password = "password123"
        email = "admin@example.com"
        full_name = "Admin User"
        hashed_password = hash_password(password)

        # Check if user already exists
        cursor.execute("SELECT COUNT(*) FROM users WHERE username = ?", (username,))
        count = cursor.fetchone()[0]

        if count > 0:
            print(f"[X] User '{username}' already exists!")
        else:
            cursor.execute("""
                INSERT INTO users (username, password, email, full_name, company_id)
                VALUES (?, ?, ?, ?, NULL)
            """, (username, hashed_password, email, full_name))
            conn.commit()
            print(f"[OK] Test user created successfully!")
            print(f"   Username: {username}")
            print(f"   Password: {password}")
            print(f"   Email: {email}")

        conn.close()

    except sqlite3.Error as e:
        print(f"[ERROR] Error creating test user: {e}")

if __name__ == "__main__":
    print("Creating test admin user...")
    create_test_user()
