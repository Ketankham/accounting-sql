"""
Company Handler - Manages company CRUD operations
"""

import mysql.connector
from mysql.connector import Error
from database.config import DB_CONFIG


class CompanyHandler:
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

    def get_all_companies(self):
        """Get all companies with their details"""
        try:
            query = """
            SELECT id, company_code, company_name, bill_to_address, ship_to_address,
                   state, city, gst_number, pan_number, landline_number,
                   mobile_number, email_address, website, logo_path, status,
                   created_at
            FROM companies
            ORDER BY created_at DESC
            """
            self.cursor.execute(query)
            companies = self.cursor.fetchall()
            return companies if companies else []
        except Error as e:
            print(f"Error fetching companies: {e}")
            return []

    def get_company_by_id(self, company_id):
        """Get a single company by ID"""
        try:
            query = """
            SELECT id, company_code, company_name, bill_to_address, ship_to_address,
                   state, city, gst_number, pan_number, landline_number,
                   mobile_number, email_address, website, logo_path, status
            FROM companies
            WHERE id = %s
            """
            self.cursor.execute(query, (company_id,))
            return self.cursor.fetchone()
        except Error as e:
            print(f"Error fetching company: {e}")
            return None

    def get_company_by_code(self, company_code):
        """Get a single company by company code"""
        try:
            query = "SELECT id FROM companies WHERE company_code = %s"
            self.cursor.execute(query, (company_code,))
            return self.cursor.fetchone()
        except Error as e:
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
                state, city, gst_number, pan_number, landline_number,
                mobile_number, email_address, website, logo_path, status
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
            )
            """

            values = (
                company_data['company_code'],
                company_data['company_name'],
                company_data.get('bill_to_address', ''),
                company_data.get('ship_to_address', ''),
                company_data.get('state', ''),
                company_data.get('city', ''),
                company_data.get('gst_number', ''),
                company_data.get('pan_number', ''),
                company_data.get('landline_number', ''),
                company_data.get('mobile_number', ''),
                company_data.get('email_address', ''),
                company_data.get('website', ''),
                company_data.get('logo_path', ''),
                company_data.get('status', 'Active')
            )

            self.cursor.execute(query, values)
            self.connection.commit()

            company_id = self.cursor.lastrowid
            print(f"Company '{company_data['company_name']}' created successfully")
            return True, "Company created successfully", company_id

        except Error as e:
            print(f"Error creating company: {e}")
            self.connection.rollback()
            return False, f"Database error: {str(e)}", None

    def update_company(self, company_id, company_data):
        """
        Update an existing company
        Returns (success: bool, message: str)
        """
        try:
            # Check if company code is being changed and if new code already exists
            existing = self.get_company_by_id(company_id)
            if not existing:
                return False, "Company not found"

            if existing['company_code'] != company_data['company_code']:
                if self.get_company_by_code(company_data['company_code']):
                    return False, "Company code already exists"

            query = """
            UPDATE companies SET
                company_code = %s,
                company_name = %s,
                bill_to_address = %s,
                ship_to_address = %s,
                state = %s,
                city = %s,
                gst_number = %s,
                pan_number = %s,
                landline_number = %s,
                mobile_number = %s,
                email_address = %s,
                website = %s,
                logo_path = %s,
                status = %s
            WHERE id = %s
            """

            values = (
                company_data['company_code'],
                company_data['company_name'],
                company_data.get('bill_to_address', ''),
                company_data.get('ship_to_address', ''),
                company_data.get('state', ''),
                company_data.get('city', ''),
                company_data.get('gst_number', ''),
                company_data.get('pan_number', ''),
                company_data.get('landline_number', ''),
                company_data.get('mobile_number', ''),
                company_data.get('email_address', ''),
                company_data.get('website', ''),
                company_data.get('logo_path', ''),
                company_data.get('status', 'Active'),
                company_id
            )

            self.cursor.execute(query, values)
            self.connection.commit()

            print(f"Company ID {company_id} updated successfully")
            return True, "Company updated successfully"

        except Error as e:
            print(f"Error updating company: {e}")
            self.connection.rollback()
            return False, f"Database error: {str(e)}"

    def delete_company(self, company_id):
        """
        Delete a company
        Returns (success: bool, message: str)
        """
        try:
            query = "DELETE FROM companies WHERE id = %s"
            self.cursor.execute(query, (company_id,))
            self.connection.commit()

            if self.cursor.rowcount > 0:
                print(f"Company ID {company_id} deleted successfully")
                return True, "Company deleted successfully"
            else:
                return False, "Company not found"

        except Error as e:
            print(f"Error deleting company: {e}")
            self.connection.rollback()
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
