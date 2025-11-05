"""
Database configuration settings
Update these values with your MySQL credentials
"""
import os

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',          # Change to your MySQL username
    'password': 'Ketanmk@26',          # Change to your MySQL password
    'database': 'login_system_db',
    'port': 3306
}

# SQLite database path for financial years
# Using absolute path to ensure we always connect to the same database
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.abspath(
    os.path.join(BASE_DIR, "..", "tkinter_mysql_project", "financial_data.db")
)
# Print the absolute path for debugging
print(f"[CONFIG] SQLite DB Path configured as: {os.path.abspath(DB_PATH)}")
