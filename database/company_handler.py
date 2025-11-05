"""
Company Handler - Manages company CRUD operations using SQLite
"""

import sqlite3
from database.config import DB_PATH


class CompanyHandler:
    def __init__(self):
        self.conn = None
        self.cursor = None

    def connect(self):
        """Establish database connection"""
        try:
            import os
            abs_path = os.path.abspath(DB_PATH)
            print(f"\n{'='*70}")
            print(f"[COMPANY_HANDLER] Connecting to SQLite database...")
            print(f"[COMPANY_HANDLER] Database path: {abs_path}")
            print(f"[COMPANY_HANDLER] File exists: {os.path.exists(abs_path)}")
            if os.path.exists(abs_path):
                print(f"[COMPANY_HANDLER] File size: {os.path.getsize(abs_path)} bytes")
            print(f"{'='*70}\n")

            self.conn = sqlite3.connect(DB_PATH)
            self.conn.row_factory = sqlite3.Row
            self.cursor = self.conn.cursor()
            print(f"✓ Successfully connected to SQLite database")

            # Create table if it doesn't exist
            self._create_table()

            return True
        except sqlite3.Error as e:
            print(f"✗ Error connecting to SQLite: {e}")
            return False

    def _create_table(self):
        """Create companies table if it doesn't exist"""
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
            print(f"Error creating table: {e}")

    def disconnect(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
            print("SQLite connection closed")

    def get_all_companies(self):
        """Get all companies with their details"""
        try:
            query = """
            SELECT id, company_code, company_name, bill_to_address, ship_to_address,
                   state, city, gst_number, pan_number, landline_number, mobile_number,
                   email_address, website, logo_path, status, created_at
            FROM companies
            ORDER BY company_name ASC
            """
            print(f"\n[GET_ALL_COMPANIES] Executing query...")
            self.cursor.execute(query)
            rows = self.cursor.fetchall()

            print(f"[GET_ALL_COMPANIES] Raw rows fetched: {len(rows)}")

            # Convert sqlite3.Row objects to dictionaries
            companies = [dict(row) for row in rows]

            print(f"[GET_ALL_COMPANIES] Returning {len(companies)} companies\n")
            return companies
        except sqlite3.Error as e:
            print(f"[GET_ALL_COMPANIES] ✗ Error fetching companies: {e}")
            import traceback
            traceback.print_exc()
            return []

    def get_company_by_id(self, company_id):
        """Get a single company by ID"""
        try:
            query = """
            SELECT id, company_code, company_name, bill_to_address, ship_to_address,
                   state, city, gst_number, pan_number, landline_number, mobile_number,
                   email_address, website, logo_path, status
            FROM companies
            WHERE id = ?
            """
            self.cursor.execute(query, (company_id,))
            row = self.cursor.fetchone()
            return dict(row) if row else None
        except sqlite3.Error as e:
            print(f"Error fetching company: {e}")
            return None

    def get_company_by_code(self, company_code):
        """Get a single company by code"""
        try:
            query = "SELECT id FROM companies WHERE company_code = ?"
            self.cursor.execute(query, (company_code,))
            row = self.cursor.fetchone()
            return dict(row) if row else None
        except sqlite3.Error as e:
            print(f"Error checking company code: {e}")
            return None

    def create_company(self, company_data):
        """
        Create a new company
        Returns (success: bool, message: str, company_id: int or None)
        """
        try:
            # Check if company code already exists
            if self.get_company_by_code(company_data['company_code']):
                return False, "Company code already exists", None

            query = """
            INSERT INTO companies (
                company_code, company_name, bill_to_address, ship_to_address,
                state, city, gst_number, pan_number, landline_number, mobile_number,
                email_address, website, logo_path, status
            ) VALUES (
                ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
            )
            """

            values = (
                company_data['company_code'],
                company_data['company_name'],
                company_data['bill_to_address'],
                company_data['ship_to_address'],
                company_data['state'],
                company_data['city'],
                company_data['gst_number'],
                company_data['pan_number'],
                company_data.get('landline_number', None),
                company_data.get('mobile_number', None),
                company_data.get('email_address', None),
                company_data.get('website', None),
                company_data['logo_path'],
                company_data.get('status', 'Active')
            )

            self.cursor.execute(query, values)
            self.conn.commit()

            company_id = self.cursor.lastrowid
            print(f"Company '{company_data['company_name']}' created successfully")
            return True, "Company created successfully", company_id

        except sqlite3.Error as e:
            print(f"Error creating company: {e}")
            self.conn.rollback()
            return False, f"Database error: {str(e)}", None

    def update_company(self, company_id, company_data):
        """
        Update an existing company
        Returns (success: bool, message: str)
        """
        try:
            # Check if company exists
            existing = self.get_company_by_id(company_id)
            if not existing:
                return False, "Company not found"

            # Check if company code is being changed and if new code already exists
            if existing['company_code'] != company_data['company_code']:
                if self.get_company_by_code(company_data['company_code']):
                    return False, "Company code already exists"

            query = """
            UPDATE companies SET
                company_code = ?,
                company_name = ?,
                bill_to_address = ?,
                ship_to_address = ?,
                state = ?,
                city = ?,
                gst_number = ?,
                pan_number = ?,
                landline_number = ?,
                mobile_number = ?,
                email_address = ?,
                website = ?,
                logo_path = ?,
                status = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
            """

            values = (
                company_data['company_code'],
                company_data['company_name'],
                company_data['bill_to_address'],
                company_data['ship_to_address'],
                company_data['state'],
                company_data['city'],
                company_data['gst_number'],
                company_data['pan_number'],
                company_data.get('landline_number', None),
                company_data.get('mobile_number', None),
                company_data.get('email_address', None),
                company_data.get('website', None),
                company_data['logo_path'],
                company_data.get('status', 'Active'),
                company_id
            )

            self.cursor.execute(query, values)
            self.conn.commit()

            print(f"Company ID {company_id} updated successfully")
            return True, "Company updated successfully"

        except sqlite3.Error as e:
            print(f"Error updating company: {e}")
            self.conn.rollback()
            return False, f"Database error: {str(e)}"

    def delete_company(self, company_id):
        """
        Delete a company
        Returns (success: bool, message: str)
        """
        try:
            query = "DELETE FROM companies WHERE id = ?"
            self.cursor.execute(query, (company_id,))
            self.conn.commit()

            if self.cursor.rowcount > 0:
                print(f"Company ID {company_id} deleted successfully")
                return True, "Company deleted successfully"
            else:
                return False, "Company not found"

        except sqlite3.Error as e:
            print(f"Error deleting company: {e}")
            self.conn.rollback()
            return False, f"Database error: {str(e)}"

    def get_states(self):
        """Get list of Indian states"""
        return [
            "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chhattisgarh",
            "Goa", "Gujarat", "Haryana", "Himachal Pradesh", "Jharkhand", "Karnataka",
            "Kerala", "Madhya Pradesh", "Maharashtra", "Manipur", "Meghalaya", "Mizoram",
            "Nagaland", "Odisha", "Punjab", "Rajasthan", "Sikkim", "Tamil Nadu",
            "Telangana", "Tripura", "Uttar Pradesh", "Uttarakhand", "West Bengal",
            "Andaman and Nicobar Islands", "Chandigarh", "Dadra and Nagar Haveli and Daman and Diu",
            "Delhi", "Jammu and Kashmir", "Ladakh", "Lakshadweep", "Puducherry"
        ]

    def get_cities_by_state(self, state):
        """Get list of cities by state (simplified version with major cities)"""
        cities_map = {
            "Maharashtra": ["Mumbai", "Pune", "Nagpur", "Nashik", "Thane", "Aurangabad"],
            "Karnataka": ["Bangalore", "Mysore", "Hubli", "Mangalore", "Belgaum"],
            "Tamil Nadu": ["Chennai", "Coimbatore", "Madurai", "Tiruchirappalli", "Salem"],
            "Gujarat": ["Ahmedabad", "Surat", "Vadodara", "Rajkot", "Bhavnagar"],
            "Delhi": ["New Delhi", "Central Delhi", "South Delhi", "North Delhi", "East Delhi"],
            # Add more states and cities as needed
        }
        return cities_map.get(state, [])
