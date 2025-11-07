"""
Static Data Handler - Manages static reference data (Book Codes, Account Types)
"""

import sqlite3
from database.config import DB_PATH


class StaticDataHandler:
    def __init__(self):
        self.conn = None
        self.cursor = None

    def connect(self):
        """Establish database connection"""
        try:
            self.conn = sqlite3.connect(DB_PATH)
            self.conn.row_factory = sqlite3.Row
            self.cursor = self.conn.cursor()
            print("[OK] StaticDataHandler connected to SQLite database")

            # Create tables if they don't exist
            self._create_book_codes_table()
            self._create_account_types_table()

            # Seed initial data if tables are empty
            self._seed_book_codes()
            self._seed_account_types()

            return True
        except sqlite3.Error as e:
            print(f"[ERROR] Error connecting to SQLite: {e}")
            return False

    def disconnect(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
            print("StaticDataHandler connection closed")

    # ========================================================================
    # TABLE CREATION
    # ========================================================================

    def _create_book_codes_table(self):
        """Create book_codes table if it doesn't exist"""
        try:
            create_table_query = """
            CREATE TABLE IF NOT EXISTS book_codes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                code TEXT NOT NULL UNIQUE,
                book_number INTEGER NOT NULL UNIQUE,
                name TEXT NOT NULL,
                description TEXT,
                is_active INTEGER DEFAULT 1,
                sort_order INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
            self.cursor.execute(create_table_query)
            self.conn.commit()
            print("[OK] Book codes table created/verified")
        except sqlite3.Error as e:
            print(f"[ERROR] Error creating book_codes table: {e}")

    def _create_account_types_table(self):
        """Create account_types table if it doesn't exist"""
        try:
            create_table_query = """
            CREATE TABLE IF NOT EXISTS account_types (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                code TEXT NOT NULL UNIQUE,
                name TEXT NOT NULL,
                description TEXT,
                category TEXT,
                nature TEXT,
                is_active INTEGER DEFAULT 1,
                sort_order INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
            self.cursor.execute(create_table_query)
            self.conn.commit()
            print("[OK] Account types table created/verified")
        except sqlite3.Error as e:
            print(f"[ERROR] Error creating account_types table: {e}")

    # ========================================================================
    # SEED DATA
    # ========================================================================

    def _seed_book_codes(self):
        """Seed initial book codes data"""
        try:
            # Check if data already exists
            self.cursor.execute("SELECT COUNT(*) FROM book_codes")
            count = self.cursor.fetchone()[0]

            if count > 0:
                return  # Data already seeded

            book_codes_data = [
                ('CASH', 1, 'Cash', 'Cash transactions and petty cash', 1, 1),
                ('BANK', 2, 'Bank', 'Bank transactions and reconciliation', 1, 2),
                ('LEDGER', 3, 'Ledger', 'General ledger entries', 1, 3),
                ('SALE', 4, 'Sale', 'Sales transactions and invoices', 1, 4),
                ('PURCHASE', 5, 'Purchase', 'Purchase transactions and bills', 1, 5),
            ]

            self.cursor.executemany("""
                INSERT INTO book_codes (code, book_number, name, description, is_active, sort_order)
                VALUES (?, ?, ?, ?, ?, ?)
            """, book_codes_data)

            self.conn.commit()
            print(f"[OK] Seeded {len(book_codes_data)} book codes")

        except sqlite3.Error as e:
            print(f"[ERROR] Error seeding book codes: {e}")

    def _seed_account_types(self):
        """Seed initial account types data"""
        try:
            # Check if data already exists
            self.cursor.execute("SELECT COUNT(*) FROM account_types")
            count = self.cursor.fetchone()[0]

            if count > 0:
                return  # Data already seeded

            account_types_data = [
                ('A', 'Assets', 'Asset accounts (cash, bank, inventory, fixed assets)', 'balance_sheet', 'debit', 1, 1),
                ('L', 'Liability', 'Liability accounts (loans, payables)', 'balance_sheet', 'credit', 1, 2),
                ('D', 'Debtors', 'Accounts receivable / Sundry debtors', 'balance_sheet', 'debit', 1, 3),
                ('C', 'Creditors', 'Accounts payable / Sundry creditors', 'balance_sheet', 'credit', 1, 4),
                ('S', 'Sale', 'Sales and revenue accounts', 'profit_loss', 'credit', 1, 5),
                ('P', 'Purchase', 'Purchase and cost of goods sold', 'profit_loss', 'debit', 1, 6),
                ('E', 'Expenses', 'Operating expenses and costs', 'profit_loss', 'debit', 1, 7),
                ('R', 'Revenue', 'Other income and revenue', 'profit_loss', 'credit', 1, 8),
            ]

            self.cursor.executemany("""
                INSERT INTO account_types (code, name, description, category, nature, is_active, sort_order)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, account_types_data)

            self.conn.commit()
            print(f"[OK] Seeded {len(account_types_data)} account types")

        except sqlite3.Error as e:
            print(f"[ERROR] Error seeding account types: {e}")

    # ========================================================================
    # BOOK CODES - READ OPERATIONS
    # ========================================================================

    def get_all_book_codes(self, active_only=True):
        """Get all book codes"""
        try:
            if active_only:
                query = "SELECT * FROM book_codes WHERE is_active = 1 ORDER BY sort_order, book_number"
            else:
                query = "SELECT * FROM book_codes ORDER BY sort_order, book_number"

            self.cursor.execute(query)
            rows = self.cursor.fetchall()
            return [dict(row) for row in rows]
        except sqlite3.Error as e:
            print(f"[ERROR] Error fetching book codes: {e}")
            return []

    def get_book_code_by_id(self, book_code_id):
        """Get single book code by ID"""
        try:
            query = "SELECT * FROM book_codes WHERE id = ?"
            self.cursor.execute(query, (book_code_id,))
            row = self.cursor.fetchone()
            return dict(row) if row else None
        except sqlite3.Error as e:
            print(f"[ERROR] Error fetching book code: {e}")
            return None

    def get_book_code_by_code(self, code):
        """Get book code by code string (e.g., 'CASH')"""
        try:
            query = "SELECT * FROM book_codes WHERE code = ? AND is_active = 1"
            self.cursor.execute(query, (code,))
            row = self.cursor.fetchone()
            return dict(row) if row else None
        except sqlite3.Error as e:
            print(f"[ERROR] Error fetching book code: {e}")
            return None

    def get_book_code_by_number(self, book_number):
        """Get book code by book number (1-6)"""
        try:
            query = "SELECT * FROM book_codes WHERE book_number = ? AND is_active = 1"
            self.cursor.execute(query, (book_number,))
            row = self.cursor.fetchone()
            return dict(row) if row else None
        except sqlite3.Error as e:
            print(f"[ERROR] Error fetching book code: {e}")
            return None

    # ========================================================================
    # ACCOUNT TYPES - READ OPERATIONS
    # ========================================================================

    def get_all_account_types(self, active_only=True):
        """Get all account types"""
        try:
            if active_only:
                query = "SELECT * FROM account_types WHERE is_active = 1 ORDER BY sort_order"
            else:
                query = "SELECT * FROM account_types ORDER BY sort_order"

            self.cursor.execute(query)
            rows = self.cursor.fetchall()
            return [dict(row) for row in rows]
        except sqlite3.Error as e:
            print(f"[ERROR] Error fetching account types: {e}")
            return []

    def get_account_type_by_id(self, account_type_id):
        """Get single account type by ID"""
        try:
            query = "SELECT * FROM account_types WHERE id = ?"
            self.cursor.execute(query, (account_type_id,))
            row = self.cursor.fetchone()
            return dict(row) if row else None
        except sqlite3.Error as e:
            print(f"[ERROR] Error fetching account type: {e}")
            return None

    def get_account_type_by_code(self, code):
        """Get account type by code (e.g., 'A', 'L')"""
        try:
            query = "SELECT * FROM account_types WHERE code = ? AND is_active = 1"
            self.cursor.execute(query, (code,))
            row = self.cursor.fetchone()
            return dict(row) if row else None
        except sqlite3.Error as e:
            print(f"[ERROR] Error fetching account type: {e}")
            return None

    def get_account_types_by_category(self, category):
        """Get account types filtered by category (balance_sheet or profit_loss)"""
        try:
            query = """
                SELECT * FROM account_types
                WHERE category = ? AND is_active = 1
                ORDER BY sort_order
            """
            self.cursor.execute(query, (category,))
            rows = self.cursor.fetchall()
            return [dict(row) for row in rows]
        except sqlite3.Error as e:
            print(f"[ERROR] Error fetching account types by category: {e}")
            return []

    def get_account_types_by_nature(self, nature):
        """Get account types filtered by nature (debit or credit)"""
        try:
            query = """
                SELECT * FROM account_types
                WHERE nature = ? AND is_active = 1
                ORDER BY sort_order
            """
            self.cursor.execute(query, (nature,))
            rows = self.cursor.fetchall()
            return [dict(row) for row in rows]
        except sqlite3.Error as e:
            print(f"[ERROR] Error fetching account types by nature: {e}")
            return []

    # ========================================================================
    # HELPER METHODS FOR DROPDOWNS
    # ========================================================================

    def get_book_codes_for_dropdown(self):
        """Get book codes formatted for dropdown (returns list of tuples: [(id, display_name)])"""
        book_codes = self.get_all_book_codes()
        return [(bc['id'], f"{bc['book_number']}-{bc['name']}") for bc in book_codes]

    def get_account_types_for_dropdown(self):
        """Get account types formatted for dropdown (returns list of tuples: [(id, display_name)])"""
        account_types = self.get_all_account_types()
        return [(at['id'], f"{at['code']} - {at['name']}") for at in account_types]

    def get_book_code_names_only(self):
        """Get list of book code names for simple dropdowns"""
        book_codes = self.get_all_book_codes()
        return [bc['name'] for bc in book_codes]

    def get_account_type_names_only(self):
        """Get list of account type names for simple dropdowns"""
        account_types = self.get_all_account_types()
        return [at['name'] for at in account_types]


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def print_all_static_data():
    """Utility function to print all static data (for debugging)"""
    handler = StaticDataHandler()
    handler.connect()

    print("\n" + "="*70)
    print("BOOK CODES")
    print("="*70)
    book_codes = handler.get_all_book_codes()
    for bc in book_codes:
        print(f"{bc['book_number']}. {bc['code']:12} | {bc['name']:20} | {bc['description']}")

    print("\n" + "="*70)
    print("ACCOUNT TYPES")
    print("="*70)
    account_types = handler.get_all_account_types()
    for at in account_types:
        print(f"{at['code']} | {at['name']:15} | {at['category']:15} | {at['nature']:6} | {at['description']}")

    handler.disconnect()


if __name__ == "__main__":
    # Test the static data handler
    print("Testing StaticDataHandler...")
    print_all_static_data()
