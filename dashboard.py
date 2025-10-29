"""
Main Dashboard - Navigation Hub
Displays after successful login
"""

import tkinter as tk
from tkinter import ttk, messagebox
from ui_config import COLORS, FONTS, SPACING, LAYOUT, BUTTON_STYLES, get_hover_handlers


class Dashboard(tk.Tk):
    def __init__(self, user_data):
        super().__init__()

        self.user_data = user_data

        # Window configuration
        self.title("Dashboard - Application")
        self.geometry(f"{LAYOUT['dashboard_width']}x{LAYOUT['dashboard_height']}")
        self.resizable(True, True)

        # Center the window on screen
        self.center_window()

        # Current module and submenu tracking
        self.current_module = None
        self.current_submenu = None

        # Use unified color scheme from ui_config
        self.colors = COLORS

        # Create UI
        self.create_widgets()

    def center_window(self):
        """Center the window on the screen"""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')

    def create_widgets(self):
        """Create the dashboard UI components"""
        # Header
        self.create_header()

        # Main container
        main_container = tk.Frame(self, bg=self.colors['background'])
        main_container.pack(fill=tk.BOTH, expand=True)

        # Sidebar
        self.create_sidebar(main_container)

        # Content area
        self.content_frame = tk.Frame(main_container, bg=self.colors['background'])
        self.content_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Default content
        self.show_default_content()

        # Footer
        self.create_footer()

    def create_header(self):
        """Create header with user info and logout"""
        header_frame = tk.Frame(self, bg=self.colors['background'], height=LAYOUT['header_height'])
        header_frame.pack(fill=tk.X, side=tk.TOP)
        header_frame.pack_propagate(False)

        # Left side - App title
        title_label = tk.Label(header_frame, text="Main Menu",
                              font=FONTS['h1'],
                              bg=self.colors['background'],
                              fg=self.colors['text_primary'])
        title_label.pack(side=tk.LEFT, padx=SPACING['xl'], pady=SPACING['lg'])

        # Right side - User info and logout
        user_info_frame = tk.Frame(header_frame, bg=self.colors['background'])
        user_info_frame.pack(side=tk.RIGHT, padx=SPACING['xl'], pady=SPACING['lg'])

        # User role/name
        role = self.user_data.get('role', 'Administrator')
        user_label = tk.Label(user_info_frame,
                             text=f"Logged-in user ({role})",
                             font=FONTS['body'],
                             bg=self.colors['background'],
                             fg=self.colors['text_secondary'])
        user_label.pack(side=tk.LEFT, padx=(0, SPACING['lg']))

        # Logout button
        logout_btn = tk.Button(user_info_frame, text="Logout")
        logout_btn.config(
            font=FONTS['button'],
            bg=self.colors['primary'],
            fg='white',
            activebackground=self.colors['primary_hover'],
            activeforeground='white',
            cursor='hand2',
            relief=tk.FLAT,
            padx=SPACING['lg'],
            pady=SPACING['md'],
            command=self.handle_logout
        )
        logout_btn.pack(side=tk.LEFT)

        # Add hover effect
        on_enter, on_leave = get_hover_handlers(logout_btn, self.colors['primary'], self.colors['primary_hover'])
        logout_btn.bind('<Enter>', on_enter)
        logout_btn.bind('<Leave>', on_leave)

        # Separator
        separator = tk.Frame(self, bg=self.colors['border'], height=2)
        separator.pack(fill=tk.X)

    def create_sidebar(self, parent):
        """Create sidebar with menu items"""
        sidebar_frame = tk.Frame(parent, bg=self.colors['sidebar'], width=LAYOUT['sidebar_width'])
        sidebar_frame.pack(side=tk.LEFT, fill=tk.Y)
        sidebar_frame.pack_propagate(False)

        # Separator (thicker border for better visibility)
        separator = tk.Frame(sidebar_frame, bg=self.colors['border'], width=2)
        separator.pack(side=tk.RIGHT, fill=tk.Y)

        # Menu items container
        menu_container = tk.Frame(sidebar_frame, bg=self.colors['sidebar'])
        menu_container.pack(fill=tk.BOTH, expand=True, padx=0, pady=SPACING['md'])

        # Define menu structure
        menus = [
            {
                'name': 'Sales',
                'icon': '📊',
                'submenus': [
                    'Sales Invoice',
                    'Sales Return',
                    'Debit Note',
                    'Credit Note'
                ]
            },
            {
                'name': 'Purchase',
                'icon': '🛒',
                'submenus': []
            },
            {
                'name': 'Accounting',
                'icon': '💰',
                'submenus': []
            },
            {
                'name': 'Master Data',
                'icon': '📁',
                'submenus': []
            },
            {
                'name': 'Utilities',
                'icon': '⚙️',
                'submenus': [
                    'Companies'
                ]
            }
        ]

        # Create menu items
        for menu in menus:
            self.create_menu_item(menu_container, menu)

    def create_menu_item(self, parent, menu_data):
        """Create a menu item with optional submenus"""
        # Main menu button
        menu_frame = tk.Frame(parent, bg=self.colors['sidebar'])
        menu_frame.pack(fill=tk.X, padx=SPACING['md'], pady=SPACING['xs'])

        # Button frame
        btn_frame = tk.Frame(menu_frame, bg=self.colors['primary'], cursor='hand2')
        btn_frame.pack(fill=tk.X)

        # Icon and label
        content_frame = tk.Frame(btn_frame, bg=self.colors['primary'])
        content_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Menu label with icon (larger text, better spacing)
        menu_label = tk.Label(content_frame,
                             text=f"  {menu_data['icon']}  {menu_data['name']}",
                             font=FONTS['menu'],
                             bg=self.colors['primary'],
                             fg='white',
                             anchor='w',
                             padx=SPACING['md'],
                             pady=SPACING['md'])
        menu_label.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Arrow indicator if has submenus
        if menu_data['submenus']:
            arrow_label = tk.Label(content_frame, text="▼",
                                  font=FONTS['small'],
                                  bg=self.colors['primary'],
                                  fg='white',
                                  padx=SPACING['md'])
            arrow_label.pack(side=tk.RIGHT)

        # Submenu container (initially hidden)
        submenu_container = tk.Frame(menu_frame, bg=self.colors['sidebar'])

        # Click handler
        def toggle_menu(event=None):
            if menu_data['submenus']:
                # Toggle submenu
                if submenu_container.winfo_ismapped():
                    submenu_container.pack_forget()
                else:
                    submenu_container.pack(fill=tk.X, pady=(0, 5))
                    self.current_module = menu_data['name']
                    self.show_module_content(menu_data['name'])
            else:
                # No submenu, just select module
                self.current_module = menu_data['name']
                self.show_module_content(menu_data['name'])

        btn_frame.bind('<Button-1>', toggle_menu)
        menu_label.bind('<Button-1>', toggle_menu)

        # Create submenus
        for submenu in menu_data['submenus']:
            self.create_submenu_item(submenu_container, submenu, menu_data['name'])

    def create_submenu_item(self, parent, submenu_name, module_name):
        """Create a submenu item"""
        submenu_frame = tk.Frame(parent, bg=self.colors['background'], cursor='hand2')
        submenu_frame.pack(fill=tk.X, padx=SPACING['md'], pady=SPACING['xs'])

        submenu_label = tk.Label(submenu_frame,
                                text=f"     ›  {submenu_name}",
                                font=FONTS['submenu'],
                                bg=self.colors['background'],
                                fg=self.colors['text_secondary'],
                                anchor='w',
                                padx=SPACING['md'],
                                pady=SPACING['md'])
        submenu_label.pack(fill=tk.X)

        # Click handler
        def select_submenu(event=None):
            self.current_module = module_name
            self.current_submenu = submenu_name
            self.show_submenu_content(module_name, submenu_name)

        submenu_frame.bind('<Button-1>', select_submenu)
        submenu_label.bind('<Button-1>', select_submenu)

        # Hover effects with better contrast
        on_enter_frame, on_leave_frame = get_hover_handlers(
            submenu_frame,
            self.colors['background'],
            self.colors['primary_light']
        )
        on_enter_label, on_leave_label = get_hover_handlers(
            submenu_label,
            self.colors['background'],
            self.colors['primary_light']
        )

        submenu_frame.bind('<Enter>', lambda e: [on_enter_frame(e), on_enter_label(e)])
        submenu_label.bind('<Enter>', lambda e: [on_enter_frame(e), on_enter_label(e)])
        submenu_frame.bind('<Leave>', lambda e: [on_leave_frame(e), on_leave_label(e)])
        submenu_label.bind('<Leave>', lambda e: [on_leave_frame(e), on_leave_label(e)])

    def show_default_content(self):
        """Show default content when no module is selected"""
        # Clear content
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        # Create centered message
        center_frame = tk.Frame(self.content_frame, bg=self.colors['background'])
        center_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        message_label = tk.Label(center_frame,
                                text="Sales Module selected. Choose a sub-menu to view content.",
                                font=FONTS['body_large'],
                                bg=self.colors['background'],
                                fg=self.colors['text_tertiary'])
        message_label.pack()

    def show_module_content(self, module_name):
        """Show content for a selected module"""
        # Clear content
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        # Create centered message
        center_frame = tk.Frame(self.content_frame, bg=self.colors['background'])
        center_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        message_label = tk.Label(center_frame,
                                text=f"{module_name} Module selected. Choose a sub-menu to view content.",
                                font=FONTS['body_large'],
                                bg=self.colors['background'],
                                fg=self.colors['text_tertiary'])
        message_label.pack()

    def show_submenu_content(self, module_name, submenu_name):
        """Show content for a selected submenu"""
        # Clear content
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        # Handle specific submenus
        if module_name == 'Utilities' and submenu_name == 'Companies':
            self.show_companies_management()
        else:
            # Default placeholder
            center_frame = tk.Frame(self.content_frame, bg=self.colors['background'])
            center_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

            message_label = tk.Label(center_frame,
                                    text=f"{submenu_name} - Coming Soon",
                                    font=FONTS['body_large'],
                                    bg=self.colors['background'],
                                    fg=self.colors['text_tertiary'])
            message_label.pack()

    def show_companies_management(self):
        """Show companies management screen"""
        try:
            from company_management import CompanyManagement

            # Clear content
            for widget in self.content_frame.winfo_children():
                widget.destroy()

            # Create company management widget
            company_mgmt = CompanyManagement(self.content_frame, self.colors)
            company_mgmt.pack(fill=tk.BOTH, expand=True)

        except Exception as e:
            messagebox.showerror("Error", f"Could not load Companies module: {e}")

    def create_footer(self):
        """Create footer"""
        # Separator
        separator = tk.Frame(self, bg=self.colors['border'], height=2)
        separator.pack(fill=tk.X, side=tk.BOTTOM)

        footer_frame = tk.Frame(self, bg=self.colors['surface'], height=LAYOUT['footer_height'])
        footer_frame.pack(fill=tk.X, side=tk.BOTTOM)
        footer_frame.pack_propagate(False)

        footer_label = tk.Label(footer_frame,
                               text="Software By [Company Name]",
                               font=FONTS['small'],
                               bg=self.colors['surface'],
                               fg=self.colors['text_tertiary'])
        footer_label.pack(pady=SPACING['md'])

    def handle_logout(self):
        """Handle logout button click"""
        result = messagebox.askyesno("Logout",
                                     "Are you sure you want to logout?")
        if result:
            self.destroy()
            # Reopen login screen
            try:
                from login_screen import LoginScreen
                login = LoginScreen()
                login.mainloop()
            except Exception as e:
                print(f"Error reopening login: {e}")


if __name__ == "__main__":
    # Test data
    test_user = {
        'id': 1,
        'username': 'admin',
        'full_name': 'Admin User',
        'email': 'admin@example.com',
        'role': 'Administrator'
    }

    app = Dashboard(test_user)
    app.mainloop()
