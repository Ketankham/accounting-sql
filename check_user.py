"""
Check user in database and verify password hash
"""

import sqlite3
import hashlib
from database.config import DB_PATH

def hash_password(password):
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def check_user():
    """Check if admin user exists and verify password"""
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        username = "admin"
        password = "password123"
        hashed_password = hash_password(password)

        print(f"Looking for user: {username}")
        print(f"Expected password hash: {hashed_password}")

        # Check user in database
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()

        if user:
            print(f"\n[OK] User found in database:")
            print(f"   ID: {user['id']}")
            print(f"   Username: {user['username']}")
            print(f"   Email: {user['email']}")
            print(f"   Full Name: {user['full_name']}")
            print(f"   Company ID: {user['company_id']}")
            print(f"   Stored Hash: {user['password']}")
            print(f"\n   Hash Match: {user['password'] == hashed_password}")
        else:
            print(f"\n[X] User '{username}' NOT found in database")

        conn.close()

    except sqlite3.Error as e:
        print(f"[ERROR] Database error: {e}")

if __name__ == "__main__":
    check_user()
