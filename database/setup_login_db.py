"""
Database Setup for Login System
Creates users and companies tables with sample data
Run this file FIRST before running the login application
"""

import mysql.connector
from mysql.connector import Error
import hashlib


def hash_password(password):
    """Hash password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()


def setup_login_database():
    """Create the database and tables for login system"""
    try:
        # Connect without specifying database
        connection = mysql.connector.connect(
            host='localhost',
            user='root',      # CHANGE THIS to your MySQL username
            password='Ketanmk@26'       # CHANGE THIS to your MySQL password
        )
        
        cursor = connection.cursor()
        
        # Create database
        database_name = 'login_system_db'
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database_name}")
        print(f"✓ Database '{database_name}' created successfully")
        
        # Use the database
        cursor.execute(f"USE {database_name}")
        
        # Create companies table
        create_companies_table = """
        CREATE TABLE IF NOT EXISTS companies (
            id INT AUTO_INCREMENT PRIMARY KEY,
            company_code VARCHAR(50) NOT NULL UNIQUE,
            company_name VARCHAR(200) NOT NULL,
            name VARCHAR(100) NULL,
            description TEXT,
            bill_to_address TEXT,
            ship_to_address TEXT,
            state VARCHAR(100),
            city VARCHAR(100),
            gst_number VARCHAR(50),
            pan_number VARCHAR(50),
            landline_number VARCHAR(20),
            mobile_number VARCHAR(20),
            email_address VARCHAR(100),
            website VARCHAR(200),
            logo_path VARCHAR(500),
            status VARCHAR(20) DEFAULT 'Active',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
        cursor.execute(create_companies_table)
        print("✓ Table 'companies' created successfully")
        
        # Create users table
        create_users_table = """
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50) NOT NULL UNIQUE,
            password VARCHAR(255) NOT NULL,
            email VARCHAR(100) NOT NULL UNIQUE,
            full_name VARCHAR(100) NOT NULL,
            company_id INT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_login TIMESTAMP NULL,
            FOREIGN KEY (company_id) REFERENCES companies(id) ON DELETE SET NULL
        )
        """
        cursor.execute(create_users_table)
        print("✓ Table 'users' created successfully")
        
        # Insert sample companies
        insert_companies = """
        INSERT INTO companies (company_code, company_name, name, description, status,
                             gst_number, pan_number, state, city, mobile_number, email_address) VALUES
        ('ACME-001', 'Acme Corporation', 'Tech Solutions Inc', 'Leading technology solutions provider', 'Active',
         '27AABCT1332L1Z5', 'AABCT1332L', 'Maharashtra', 'Mumbai', '9876543210', 'contact@acme.com'),
        ('GLBX-002', 'Globex Inc.', 'Marketing Masters', 'Digital marketing and advertising agency', 'Active',
         '29AABCG1234M1Z6', 'AABCG1234M', 'Karnataka', 'Bangalore', '9876543211', 'info@globex.com'),
        ('STK-003', 'Stark Industries', 'Finance Pro Ltd', 'Financial services and consulting', 'Inactive',
         '27AABCS5432N1Z7', 'AABCS5432N', 'Maharashtra', 'Pune', '9876543212', 'stark@stark.com'),
        ('WAYNE-004', 'Wayne Enterprises', 'Healthcare Plus', 'Healthcare management solutions', 'Active',
         '07AABCW6789P1Z8', 'AABCW6789P', 'Delhi', 'New Delhi', '9876543213', 'wayne@wayne.com')
        ON DUPLICATE KEY UPDATE company_code=company_code
        """
        cursor.execute(insert_companies)
        print("✓ Sample companies inserted")
        
        # Insert sample users
        # Password for all sample users is 'password123'
        sample_password = hash_password('password123')
        
        insert_users = """
        INSERT INTO users (username, password, email, full_name, company_id) VALUES 
        ('admin', %s, 'admin@example.com', 'Admin User', 1),
        ('john_doe', %s, 'john@techsolutions.com', 'John Doe', 1),
        ('jane_smith', %s, 'jane@marketing.com', 'Jane Smith', 2),
        ('bob_wilson', %s, 'bob@finance.com', 'Bob Wilson', 3),
        ('alice_brown', %s, 'alice@healthcare.com', 'Alice Brown', 4),
        ('demo_user', %s, 'demo@example.com', 'Demo User', NULL)
        ON DUPLICATE KEY UPDATE username=username
        """
        cursor.execute(insert_users, (sample_password, sample_password, sample_password, 
                                      sample_password, sample_password, sample_password))
        
        connection.commit()
        print("✓ Sample users inserted")
        
        print("\n" + "="*70)
        print("DATABASE SETUP COMPLETED SUCCESSFULLY!")
        print("="*70)
        print(f"\nDatabase Name: {database_name}")
        print("\n✅ Sample Users Created (Password: password123 for all):")
        print("-" * 70)
        print(f"{'Username':<15} {'Password':<15} {'Company':<25}")
        print("-" * 70)
        print(f"{'admin':<15} {'password123':<15} {'Tech Solutions Inc':<25}")
        print(f"{'john_doe':<15} {'password123':<15} {'Tech Solutions Inc':<25}")
        print(f"{'jane_smith':<15} {'password123':<15} {'Marketing Masters':<25}")
        print(f"{'bob_wilson':<15} {'password123':<15} {'Finance Pro Ltd':<25}")
        print(f"{'alice_brown':<15} {'password123':<15} {'Healthcare Plus':<25}")
        print(f"{'demo_user':<15} {'password123':<15} {'(No company)':<25}")
        print("-" * 70)
        
        print("\n✅ Companies Available:")
        print("-" * 70)
        companies = [
            "Tech Solutions Inc",
            "Marketing Masters",
            "Finance Pro Ltd",
            "Healthcare Plus",
            "Retail Giants Co"
        ]
        for i, company in enumerate(companies, 1):
            print(f"  {i}. {company}")
        print("-" * 70)
        
        print("\n📝 NEXT STEPS:")
        print("  1. Update database/config.py with your MySQL password")
        print("  2. Run: python login_screen.py")
        print("  3. Login with username: admin, password: password123")
        print("="*70 + "\n")
        
        cursor.close()
        connection.close()
        
    except Error as e:
        print(f"✗ Error: {e}")
        print("\n⚠️ TROUBLESHOOTING:")
        print("  - Make sure MySQL server is running")
        print("  - Check your MySQL username and password in this file")
        print("  - Verify you have permission to create databases")


if __name__ == "__main__":
    print("\n🚀 Starting Database Setup...\n")
    setup_login_database()
