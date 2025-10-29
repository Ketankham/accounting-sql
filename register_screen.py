"""
Registration Screen for New Users
"""

import tkinter as tk
from tkinter import ttk, messagebox
from database.auth_handler import AuthHandler
import re


class RegistrationScreen(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.title("Register - New Account")
        self.geometry("450x650")
        self.resizable(False, False)
        
        # Center the window
        self.center_window()
        
        # Database handler
        self.auth_handler = AuthHandler()
        self.auth_handler.connect()
        
        # Create UI
        self.create_widgets()
        
        # Load companies
        self.load_companies()
    
    def center_window(self):
        """Center the window on the screen"""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')
    
    def create_widgets(self):
        """Create registration UI components"""
        # Main container
        main_frame = ttk.Frame(self, padding="30")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(main_frame, text="Create Account", 
                               font=("Arial", 24, "bold"))
        title_label.pack(pady=(0, 10))
        
        subtitle_label = ttk.Label(main_frame, text="Fill in your details to register", 
                                   font=("Arial", 10), foreground="gray")
        subtitle_label.pack(pady=(0, 20))
        
        # Form frame with scrollbar support
        form_frame = ttk.Frame(main_frame)
        form_frame.pack(fill=tk.BOTH, expand=True)
        
        # Full Name
        ttk.Label(form_frame, text="Full Name *", font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=(0, 5))
        self.fullname_entry = ttk.Entry(form_frame, font=("Arial", 11))
        self.fullname_entry.pack(fill=tk.X, ipady=8, pady=(0, 15))
        
        # Username
        ttk.Label(form_frame, text="Username *", font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=(0, 5))
        self.username_entry = ttk.Entry(form_frame, font=("Arial", 11))
        self.username_entry.pack(fill=tk.X, ipady=8, pady=(0, 15))
        
        # Email
        ttk.Label(form_frame, text="Email *", font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=(0, 5))
        self.email_entry = ttk.Entry(form_frame, font=("Arial", 11))
        self.email_entry.pack(fill=tk.X, ipady=8, pady=(0, 15))
        
        # Password
        ttk.Label(form_frame, text="Password *", font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=(0, 5))
        self.password_entry = ttk.Entry(form_frame, font=("Arial", 11), show="●")
        self.password_entry.pack(fill=tk.X, ipady=8, pady=(0, 15))
        
        # Confirm Password
        ttk.Label(form_frame, text="Confirm Password *", font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=(0, 5))
        self.confirm_password_entry = ttk.Entry(form_frame, font=("Arial", 11), show="●")
        self.confirm_password_entry.pack(fill=tk.X, ipady=8, pady=(0, 15))
        
        # Company (Optional)
        ttk.Label(form_frame, text="Company (Optional)", font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=(0, 5))
        self.company_var = tk.StringVar()
        self.company_combo = ttk.Combobox(form_frame, textvariable=self.company_var,
                                         font=("Arial", 11), state="readonly")
        self.company_combo.pack(fill=tk.X, ipady=8, pady=(0, 20))
        
        # Register button
        register_button = ttk.Button(form_frame, text="Register", command=self.handle_registration)
        register_button.pack(fill=tk.X, ipady=10)
        
        # Back to login link
        back_frame = ttk.Frame(form_frame)
        back_frame.pack(pady=(15, 0))
        
        back_label = ttk.Label(back_frame, text="Already have an account? ")
        back_label.pack(side=tk.LEFT)
        
        back_link = ttk.Label(back_frame, text="Login here", foreground="blue", cursor="hand2")
        back_link.pack(side=tk.LEFT)
        back_link.bind("<Button-1>", lambda e: self.destroy())
    
    def load_companies(self):
        """Load companies from database"""
        companies = self.auth_handler.get_all_companies()
        
        if companies:
            company_names = ["-- No Company --"] + [comp['name'] for comp in companies]
            self.company_combo['values'] = company_names
            self.company_combo.current(0)
        else:
            self.company_combo['values'] = ["-- No Company --"]
            self.company_combo.current(0)
    
    def validate_email(self, email):
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def handle_registration(self):
        """Handle registration form submission"""
        # Get form values
        full_name = self.fullname_entry.get().strip()
        username = self.username_entry.get().strip()
        email = self.email_entry.get().strip()
        password = self.password_entry.get().strip()
        confirm_password = self.confirm_password_entry.get().strip()
        company = self.company_var.get()
        
        # Validation
        if not full_name:
            messagebox.showwarning("Validation Error", "Please enter your full name")
            self.fullname_entry.focus()
            return
        
        if not username:
            messagebox.showwarning("Validation Error", "Please enter a username")
            self.username_entry.focus()
            return
        
        if len(username) < 3:
            messagebox.showwarning("Validation Error", "Username must be at least 3 characters long")
            self.username_entry.focus()
            return
        
        if not email:
            messagebox.showwarning("Validation Error", "Please enter your email")
            self.email_entry.focus()
            return
        
        if not self.validate_email(email):
            messagebox.showwarning("Validation Error", "Please enter a valid email address")
            self.email_entry.focus()
            return
        
        if not password:
            messagebox.showwarning("Validation Error", "Please enter a password")
            self.password_entry.focus()
            return
        
        if len(password) < 6:
            messagebox.showwarning("Validation Error", "Password must be at least 6 characters long")
            self.password_entry.focus()
            return
        
        if password != confirm_password:
            messagebox.showerror("Validation Error", "Passwords do not match")
            self.confirm_password_entry.focus()
            return
        
        # Check if username exists
        if self.auth_handler.username_exists(username):
            messagebox.showerror("Registration Error", "Username already exists. Please choose another one.")
            self.username_entry.focus()
            return
        
        # Check if email exists
        if self.auth_handler.email_exists(email):
            messagebox.showerror("Registration Error", "Email already registered. Please use another email.")
            self.email_entry.focus()
            return
        
        # Get company ID if selected
        company_id = None
        if company and company != "-- No Company --":
            companies = self.auth_handler.get_all_companies()
            for comp in companies:
                if comp['name'] == company:
                    company_id = comp['id']
                    break
        
        # Register user
        if self.auth_handler.register_user(username, password, email, full_name, company_id):
            messagebox.showinfo("Success", 
                              f"Registration successful!\n\n"
                              f"You can now login with:\n"
                              f"Username: {username}\n"
                              f"Password: (your password)")
            self.destroy()
        else:
            messagebox.showerror("Registration Error", "Failed to register. Please try again.")
    
    def destroy(self):
        """Clean up before closing"""
        self.auth_handler.disconnect()
        super().destroy()
