"""
Login Screen - Main Entry Point
Run this file to start the login application
"""

import tkinter as tk
from tkinter import ttk, messagebox
from database.auth_handler import AuthHandler
from ui_config import COLORS, FONTS, SPACING, LAYOUT


class LoginScreen(tk.Tk):
    def __init__(self):
        super().__init__()
        
        # Window configuration
        self.title("Login - Application")
        self.geometry(f"{LAYOUT['login_width']}x{LAYOUT['login_height']}")
        self.resizable(False, False)
        self.configure(bg=COLORS['background'])
        
        # Center the window on screen
        self.center_window()
        
        # Database handler for authentication
        self.auth_handler = AuthHandler()
        
        # Connect to database
        if not self.auth_handler.connect():
            messagebox.showerror("Database Error", 
                               "Failed to connect to database.\n\n"
                               "Please check:\n"
                               "1. MySQL server is running\n"
                               "2. Database credentials in database/config.py\n"
                               "3. Run database/setup_login_db.py first")
            self.destroy()
            return
        
        # Store logged-in user info
        self.logged_in_user = None
        
        # Create UI
        self.create_widgets()
        
        # Load companies for dropdown
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
        """Create the login UI components"""
        # Main container
        main_frame = tk.Frame(self, bg=COLORS['background'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=SPACING['xxl'], pady=SPACING['xl'])

        # Logo/Title area
        title_frame = tk.Frame(main_frame, bg=COLORS['background'])
        title_frame.pack(pady=(0, SPACING['lg']))

        title_label = tk.Label(title_frame, text="Welcome Back!",
                               font=FONTS['display'],
                               bg=COLORS['background'],
                               fg=COLORS['text_primary'])
        title_label.pack()

        subtitle_label = tk.Label(title_frame, text="Please login to continue",
                                   font=FONTS['body'],
                                   bg=COLORS['background'],
                                   fg=COLORS['text_secondary'])
        subtitle_label.pack()

        # Login form frame - single column container
        form_frame = tk.Frame(main_frame, bg=COLORS['background'])
        form_frame.pack(fill=tk.BOTH, expand=True)

        # Username field
        username_label = tk.Label(form_frame, text="Username",
                                   font=FONTS['body_bold'],
                                   bg=COLORS['background'],
                                   fg=COLORS['text_primary'])
        username_label.pack(anchor=tk.W, pady=(0, SPACING['sm']))

        self.username_entry = ttk.Entry(form_frame, font=FONTS['body'])
        self.username_entry.pack(fill=tk.X, ipady=SPACING['sm'], pady=(0, SPACING['md']))
        self.username_entry.focus()

        # Password field
        password_label = tk.Label(form_frame, text="Password",
                                   font=FONTS['body_bold'],
                                   bg=COLORS['background'],
                                   fg=COLORS['text_primary'])
        password_label.pack(anchor=tk.W, pady=(0, SPACING['sm']))

        self.password_entry = ttk.Entry(form_frame, font=FONTS['body'], show="●")
        self.password_entry.pack(fill=tk.X, ipady=SPACING['sm'], pady=(0, SPACING['md']))

        # Show password checkbox
        self.show_password_var = tk.BooleanVar()
        show_password_check = ttk.Checkbutton(form_frame, text="Show password",
                                             variable=self.show_password_var,
                                             command=self.toggle_password)
        show_password_check.pack(anchor=tk.W, pady=(0, SPACING['md']))

        # Company dropdown (Optional)
        company_label = tk.Label(form_frame, text="Company (Optional)",
                                 font=FONTS['body_bold'],
                                 bg=COLORS['background'],
                                 fg=COLORS['text_primary'])
        company_label.pack(anchor=tk.W, pady=(0, SPACING['sm']))

        self.company_var = tk.StringVar()
        self.company_combo = ttk.Combobox(form_frame, textvariable=self.company_var,
                                         font=FONTS['body'], state="readonly")
        self.company_combo.pack(fill=tk.X, ipady=SPACING['sm'], pady=(0, SPACING['lg']))
        self.company_combo.set("-- Select Company --")

        # Login button
        self.login_button = tk.Button(form_frame, text="Login")
        self.login_button.config(
            font=FONTS['button'],
            bg=COLORS['primary'],
            fg='white',
            activebackground=COLORS['primary_hover'],
            activeforeground='white',
            cursor='hand2',
            relief=tk.FLAT,
            pady=SPACING['sm'],
            command=self.handle_login
        )
        self.login_button.pack(fill=tk.X)

        # Add hover effect
        self.login_button.bind('<Enter>', lambda e: self.login_button.config(bg=COLORS['primary_hover']))
        self.login_button.bind('<Leave>', lambda e: self.login_button.config(bg=COLORS['primary']))

        # Bind Enter key to login
        self.bind('<Return>', lambda e: self.handle_login())
    
    def toggle_password(self):
        """Toggle password visibility"""
        if self.show_password_var.get():
            self.password_entry.config(show="")
        else:
            self.password_entry.config(show="●")
    
    def load_companies(self):
        """Load companies from database into dropdown"""
        companies = self.auth_handler.get_all_companies()
        
        if companies:
            company_names = ["-- Select Company --"] + [comp['name'] for comp in companies]
            self.company_combo['values'] = company_names
        else:
            self.company_combo['values'] = ["-- Select Company --", "No companies available"]
    
    def handle_login(self):
        """Handle login button click"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        company = self.company_var.get()
        
        # Validate inputs
        if not username:
            messagebox.showwarning("Input Error", "Please enter your username")
            self.username_entry.focus()
            return
        
        if not password:
            messagebox.showwarning("Input Error", "Please enter your password")
            self.password_entry.focus()
            return
        
        # Handle optional company selection
        if company == "-- Select Company --":
            company = None
        
        # Attempt login
        user = self.auth_handler.authenticate_user(username, password, company)
        
        if user:
            self.logged_in_user = user

            # Print login info
            print(f"✓ User logged in: {user['username']}")
            print(f"  Full Name: {user['full_name']}")
            print(f"  Email: {user['email']}")
            if user.get('company_name'):
                print(f"  Company: {user['company_name']}")

            # Close login window and open dashboard
            self.open_dashboard(user)
            
        else:
            messagebox.showerror("Login Failed", 
                               "Invalid username, password, or company selection.\n"
                               "Please try again.")
            self.password_entry.delete(0, tk.END)
            self.password_entry.focus()
    
    def clear_form(self):
        """Clear form fields"""
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        self.company_combo.set("-- Select Company --")
        self.username_entry.focus()
    
    def open_registration(self):
        """Open registration window"""
        try:
            from register_screen import RegistrationScreen
            reg_window = RegistrationScreen(self)
            reg_window.grab_set()  # Make it modal
        except Exception as e:
            messagebox.showerror("Error", f"Could not open registration: {e}")

    def open_dashboard(self, user_data):
        """Open main dashboard after successful login"""
        try:
            # Add role to user data (default to Administrator)
            user_data['role'] = user_data.get('role', 'Administrator')

            # Close database connection
            self.auth_handler.disconnect()

            # Destroy login window
            self.destroy()

            # Open dashboard
            from dashboard import Dashboard
            dashboard = Dashboard(user_data)
            dashboard.mainloop()

        except Exception as e:
            messagebox.showerror("Error", f"Could not open dashboard: {e}")

    def on_closing(self):
        """Handle window closing event"""
        self.auth_handler.disconnect()
        self.destroy()


if __name__ == "__main__":
    print("\n" + "="*50)
    print("[START] Starting Login Application")
    print("="*50)
    print("\n[INFO] Test Credentials:")
    print("   Username: admin")
    print("   Password: password123")
    print("   Company: Tech Solutions Inc (optional)")
    print("\n" + "="*50 + "\n")
    
    app = LoginScreen()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()