import mysql.connector
from mysql.connector import Error
from database.config import DB_CONFIG


class EntityHandler:
    """Template handler for any database entity"""
    
    def __init__(self):
        self.connection = None
        self.cursor = None

    def connect(self):
        """Establish database connection"""
        try:
            self.connection = mysql.connector.connect(**DB_CONFIG)
            if self.connection.is_connected():
                self.cursor = self.connection.cursor(dictionary=True)
                print("Database connected successfully")
                return True
        except Error as e:
            print(f"Connection error: {e}")
            return False

    def disconnect(self):
        """Close database connection"""
        if self.connection and self.connection.is_connected():
            if self.cursor:
                self.cursor.close()
            self.connection.close()

    def get_all(self, table_name):
        """Get all records"""
        try:
            query = f"SELECT * FROM {table_name} ORDER BY created_at DESC"
            self.cursor.execute(query)
            return self.cursor.fetchall() if self.cursor.rowcount > 0 else []
        except Error as e:
            print(f"Error fetching data: {e}")
            return []

    def get_by_id(self, table_name, entity_id):
        """Get single record by ID"""
        try:
            query = f"SELECT * FROM {table_name} WHERE id = %s"
            self.cursor.execute(query, (entity_id,))
            return self.cursor.fetchone()
        except Error as e:
            print(f"Error fetching record: {e}")
            return None

    def create(self, table_name, data):
        """Create new record"""
        try:
            columns = ', '.join(data.keys())
            placeholders = ', '.join(['%s'] * len(data))
            query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
            
            self.cursor.execute(query, tuple(data.values()))
            self.connection.commit()
            
            return True, "Record created successfully", self.cursor.lastrowid
        except Error as e:
            self.connection.rollback()
            return False, f"Error: {str(e)}", None

    def update(self, table_name, entity_id, data):
        """Update existing record"""
        try:
            set_clause = ', '.join([f"{k} = %s" for k in data.keys()])
            query = f"UPDATE {table_name} SET {set_clause} WHERE id = %s"
            
            values = list(data.values()) + [entity_id]
            self.cursor.execute(query, tuple(values))
            self.connection.commit()
            
            return True, "Record updated successfully"
        except Error as e:
            self.connection.rollback()
            return False, f"Error: {str(e)}"

    def delete(self, table_name, entity_id):
        """Delete record"""
        try:
            query = f"DELETE FROM {table_name} WHERE id = %s"
            self.cursor.execute(query, (entity_id,))
            self.connection.commit()
            
            if self.cursor.rowcount > 0:
                return True, "Record deleted successfully"
            else:
                return False, "Record not found"
        except Error as e:
            self.connection.rollback()
            return False, f"Error: {str(e)}"