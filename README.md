# 🔐 Tkinter Login System with MySQL

A complete, ready-to-use login system built with Python Tkinter and MySQL.

## 📋 Prerequisites

Before running this application, make sure you have:

1. **Python 3.x** installed
2. **MySQL Server** installed and running
3. **mysql-connector-python** package

### Install Required Package

```bash
# Windows
pip install mysql-connector-python

# Linux/Mac
pip3 install mysql-connector-python
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

### Step 2: Setup Database

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

### Step 3: Run the Login Application

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
├── login_screen.py           ← START HERE (Main login window)
├── register_screen.py        ← Registration form
│
├── database/
│   ├── __init__.py          ← Makes it a Python package
│   ├── config.py            ← Database credentials (EDIT THIS)
│   ├── auth_handler.py      ← Login/registration logic
│   └── setup_login_db.py    ← Database setup (RUN THIS FIRST)
│
├── utils/
│   └── __init__.py
│
└── README.md                ← This file
```

## ✨ Features

✅ **Login System**
- Username and password authentication
- Optional company selection
- Password show/hide toggle
- Secure password hashing (SHA-256)

✅ **Registration System**
- New user registration
- Email validation
- Password confirmation
- Duplicate username/email check

✅ **Security**
- Passwords hashed with SHA-256
- SQL injection prevention
- Input validation

✅ **Database**
- Users table with authentication data
- Companies table for organization management
- Foreign key relationships

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

### "Failed to connect to database"

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

### Module import errors

**Solution:** Make sure `__init__.py` files exist in:
- `database/__init__.py`
- `utils/__init__.py`

These files make Python recognize the folders as packages.

## 🎨 Customization

### Change Window Appearance

In `login_screen.py`:

```python
# Change window size (line 16)
self.geometry("450x500")  # width x height

# Change title (line 15)
self.title("Your App Name - Login")

# Change colors
foreground="blue"   # Text color
background="white"  # Background color
```

### Add More Companies

Edit `database/setup_login_db.py` and add to the INSERT statement:

```python
('Your Company', 'Company description'),
```

Then run the setup script again.

### Modify Password Requirements

In `register_screen.py`, line 155:

```python
if len(password) < 8:  # Change minimum length
    messagebox.showwarning("Validation Error", 
                          "Password must be at least 8 characters")
```

## 📊 Database Schema

### Companies Table
```sql
CREATE TABLE companies (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

### Users Table
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

## 📝 Next Steps

After successful login, you can:
1. Integrate with your main application
2. Add session management
3. Implement "Remember Me" functionality
4. Add password reset feature
5. Create admin dashboard

## ⚠️ Important Notes

- **Never commit** `database/config.py` with real passwords to version control
- **Always hash** passwords (this project uses SHA-256)
- **Run setup_login_db.py** only once to initialize the database
- **Update config.py** with your MySQL credentials before running

## 🆘 Need Help?

If you encounter issues:

1. Make sure you're in the correct directory
2. Check that all `__init__.py` files exist
3. Verify MySQL is running
4. Check database credentials in `config.py`
5. Ensure you ran `setup_login_db.py` first

## 📄 License

This is a sample project for educational purposes.

---

**Ready to start?**

1. Update `database/config.py` with your MySQL password
2. Run `python database/setup_login_db.py`
3. Run `python login_screen.py`
4. Login with username: `admin`, password: `password123`

Good luck! 🎉
