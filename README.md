# 🔐 Tkinter Business Management System

A complete business management application built with Python Tkinter, MySQL, and SQLite featuring user authentication and company/financial year management.

## 📋 Prerequisites

Before running this application, make sure you have:

1. **Python 3.x** installed
2. **MySQL Server** installed and running (for user authentication)
3. **Required Python packages:**

### Install Required Packages

```bash
# Windows
pip install mysql-connector-python tkcalendar

# Linux/Mac
pip3 install mysql-connector-python tkcalendar
```

## 🚀 Quick Start Guide

### Step 1: Configure Database Connection

Open `database/config.py` and update with your MySQL credentials:

```python
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',          # ← Change to your MySQL username
    'password': '',          # ← Change to your MySQL password
    'database': 'login_system_db',
    'port': 3306
}
```

> **Note:** Financial Years use SQLite and require no configuration!

### Step 2: Setup MySQL Database

Run the database setup script **FIRST** (only need to run once):

```bash
# Windows
cd path\to\tkinter_mysql_project
python database/setup_login_db.py

# Linux/Mac
cd path/to/tkinter_mysql_project
python3 database/setup_login_db.py
```

This will:
- Create the database `login_system_db`
- Create `users` and `companies` tables
- Insert 6 sample users and 5 sample companies

### Step 3: (Optional) Add Sample Financial Years

```bash
python database/insert_test_data.py
```

This will add 3 sample financial years to the SQLite database.

### Step 4: Run the Application

```bash
# Windows
python login_screen.py

# Linux/Mac
python3 login_screen.py
```

## 🔑 Sample Login Credentials

Use these credentials to test the login:

| Username    | Password    | Company            |
|-------------|-------------|-------------------|
| admin       | password123 | Tech Solutions Inc |
| john_doe    | password123 | Tech Solutions Inc |
| jane_smith  | password123 | Marketing Masters  |
| bob_wilson  | password123 | Finance Pro Ltd    |
| alice_brown | password123 | Healthcare Plus    |
| demo_user   | password123 | (No company)       |

## 📁 Project Structure

```
tkinter_mysql_project/
│
├── login_screen.py                 ← START HERE (Main login window)
├── register_screen.py              ← Registration form
├── dashboard.py                    ← Main dashboard after login
│
├── company_management.py           ← Company list view
├── company_form.py                 ← Create/Edit company form
│
├── financial_year_management.py    ← Financial Year list view
├── financial_year_form.py          ← Create/Edit financial year form
│
├── ui_config.py                    ← Unified UI styling
│
├── database/
│   ├── __init__.py                ← Makes it a Python package
│   ├── config.py                  ← Database credentials (EDIT THIS)
│   ├── auth_handler.py            ← Login/registration logic (MySQL)
│   ├── company_handler.py         ← Company CRUD operations (MySQL)
│   ├── financial_year_handler.py  ← Financial Year CRUD operations (SQLite)
│   ├── setup_login_db.py          ← MySQL database setup (RUN THIS FIRST)
│   ├── insert_test_data.py        ← Insert sample financial years (Optional)
│   └── create_financial_years_table.py  ← SQLite table creation
│
├── utils/
│   └── __init__.py
│
├── financial_data.db               ← SQLite database (auto-created)
│
└── README.md                       ← This file
```

## ✨ Features

### 🔐 Authentication System
- Username and password authentication
- Optional company selection
- Password show/hide toggle
- Secure password hashing (SHA-256)
- User registration with email validation
- Duplicate username/email check

### 🏢 Company Management (MySQL)
- View all companies in a table
- Create new companies
- Edit existing companies
- Complete company information including:
  - Company Code & Name
  - Bill-to and Ship-to addresses
  - GST Number, PAN Number
  - Contact details (phone, email, website)
  - Logo upload
  - Active/Inactive status

### 📅 Financial Year Management (SQLite)
- View all financial years in a table
- Create new financial years
- Edit existing financial years
- Financial year features:
  - FY Code (e.g., FY2425)
  - Display Name
  - Start and End dates with date picker
  - Active/Inactive status
  - Date overlap validation
  - Automatic duplicate code prevention

### 🎨 Modern UI/UX
- Clean, professional interface
- Consistent color scheme
- Hover effects on buttons
- Responsive table layouts
- Scrollable content areas
- Form validation with helpful error messages

### 🔒 Security
- Passwords hashed with SHA-256
- SQL injection prevention
- Input validation
- Separate databases for different concerns

## 📊 Database Schema

### MySQL Database (login_system_db)

#### Companies Table
```sql
CREATE TABLE companies (
    id INT AUTO_INCREMENT PRIMARY KEY,
    company_code VARCHAR(10) UNIQUE,
    company_name VARCHAR(100) NOT NULL,
    bill_to_address TEXT,
    ship_to_address TEXT,
    state VARCHAR(50),
    city VARCHAR(50),
    gst_number VARCHAR(15),
    pan_number VARCHAR(10),
    landline_number VARCHAR(15),
    mobile_number VARCHAR(15),
    email_address VARCHAR(100),
    website VARCHAR(100),
    logo_path VARCHAR(255),
    status ENUM('Active', 'Inactive') DEFAULT 'Active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

#### Users Table
```sql
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    full_name VARCHAR(100) NOT NULL,
    company_id INT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP NULL,
    FOREIGN KEY (company_id) REFERENCES companies(id)
)
```

### SQLite Database (financial_data.db)

#### Financial Years Table
```sql
CREATE TABLE financial_years (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fy_code TEXT NOT NULL UNIQUE,
    display_name TEXT NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    status TEXT DEFAULT 'Active' CHECK(status IN ('Active', 'Inactive')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

## 🛠️ Troubleshooting

### "ModuleNotFoundError: No module named 'database'"

**Solution:** Make sure you're running the script from the project root directory:

```bash
# Wrong (will cause error)
python path/to/login_screen.py

# Correct
cd path/to/tkinter_mysql_project
python login_screen.py
```

### "ModuleNotFoundError: No module named 'tkcalendar'"

**Solution:** Install the tkcalendar package:

```bash
pip install tkcalendar
```

### "Failed to connect to database" (MySQL)

**Solutions:**
1. Make sure MySQL server is running
2. Check your username/password in `database/config.py`
3. Verify MySQL is running on port 3306
4. Run `database/setup_login_db.py` first to create the database

### "Can't connect to MySQL server on 'localhost'"

**Solutions:**
1. Start MySQL service:
   - Windows: Start "MySQL" service from Services
   - Linux: `sudo service mysql start`
   - Mac: `brew services start mysql`

### Financial Years not displaying

**Solutions:**
1. Check the console output for debug information
2. Verify the SQLite database file exists at: `tkinter_mysql_project/financial_data.db`
3. Run `database/insert_test_data.py` to add sample data
4. Check file permissions on the database file

### Module import errors

**Solution:** Make sure `__init__.py` files exist in:
- `database/__init__.py`
- `utils/__init__.py`

These files make Python recognize the folders as packages.

## 🎨 Customization

### Change UI Colors

Edit `ui_config.py`:

```python
COLORS = {
    'primary': '#2563eb',        # Main brand color
    'primary_hover': '#1d4ed8',  # Hover state
    'success': '#10b981',        # Success messages
    'error': '#ef4444',          # Error messages
    # ... etc
}
```

### Change Window Size

In `dashboard.py`:

```python
self.geometry("1200x800")  # width x height
```

### Add More Companies

Edit `database/setup_login_db.py` and add to the INSERT statement:

```python
('Your Company', 'Company description'),
```

Then run the setup script again.

### Modify Validation Rules

In form files, update validation functions:

```python
# Financial Year validation
if len(fy_code) > 6:
    errors.append("FY Code must be maximum 6 characters")
```

## 🔄 Running on Different Operating Systems

### Windows
```bash
cd C:\path\to\tkinter_mysql_project
python login_screen.py
```

### Linux/Mac
```bash
cd /path/to/tkinter_mysql_project
python3 login_screen.py
```

## 📝 Usage Guide

### Creating a Financial Year

1. Login to the application
2. Click "Financial Year" from the dashboard
3. Click "Create New Financial Year"
4. Fill in the form:
   - **FY Code:** Short code (e.g., FY2425) - Max 6 characters
   - **Display Name:** Full name (e.g., Financial Year 2024-2025)
   - **Start Date:** Select from calendar
   - **End Date:** Select from calendar
   - **Status:** Active or Inactive
5. Click "Create Financial Year"

### Managing Companies

1. Login to the application
2. Click "Company Management" from the dashboard
3. Click "Create New Company" to add a company
4. Click "Edit" on any row to modify existing company
5. Fill in company details and save

### Dashboard Features

After login, the dashboard provides:
- User information display
- Quick navigation to Company Management
- Quick navigation to Financial Year Management
- Logout functionality
- Clean, card-based navigation

## 📊 Data Storage

### MySQL (User & Company Data)
- Location: MySQL Server
- Database: `login_system_db`
- Tables: `users`, `companies`
- Backup: Use MySQL dump tools

### SQLite (Financial Year Data)
- Location: `tkinter_mysql_project/financial_data.db`
- Tables: `financial_years`
- Backup: Simply copy the `.db` file

## ⚠️ Important Notes

- **Never commit** `database/config.py` with real passwords to version control
- **Always hash** passwords (this project uses SHA-256)
- **Run setup_login_db.py** only once to initialize the MySQL database
- **SQLite database** is auto-created on first use
- **Update config.py** with your MySQL credentials before running
- **Financial years** use date overlap validation to prevent conflicts

## 🆘 Need Help?

If you encounter issues:

1. Make sure you're in the correct directory
2. Check that all `__init__.py` files exist
3. Verify MySQL is running (for login/company features)
4. Check database credentials in `config.py`
5. Ensure you ran `setup_login_db.py` first
6. Check console output for debug information
7. Verify all required packages are installed

## 📄 License

This is a sample project for educational purposes.

---

## 🚀 Ready to start?

1. **Install packages:** `pip install mysql-connector-python tkcalendar`
2. **Update config:** Edit `database/config.py` with your MySQL password
3. **Setup MySQL:** Run `python database/setup_login_db.py`
4. **Add test data:** Run `python database/insert_test_data.py` (optional)
5. **Run app:** `python login_screen.py`
6. **Login:** Username: `admin`, Password: `password123`

Good luck! 🎉

---

## 🔮 Future Enhancements

Potential features to add:
- User role management (Admin, User, Viewer)
- Company logo display in dashboard
- Financial year reports and analytics
- Export data to Excel/PDF
- Password reset functionality
- "Remember Me" feature
- Multi-language support
- Dark mode toggle
- Audit logs for data changes
