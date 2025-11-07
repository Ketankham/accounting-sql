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
                'submenus': [
                    'Account Group Master',
                    'Account Master',
                    'Business Partner',
                    'Item Group Master',
                    'Item Type Master',
                    'Manufacturer Master',
                    'Item Master',
                    'UoM Master',
                    'City Master',
                    'State Master'
                ]
            },
            {
                'name': 'Utilities',
                'icon': '⚙️',
                'submenus': [
                    'Companies',
                    'Financial Years'
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

        # Submenu container with scrollbar (initially hidden)
        submenu_outer = tk.Frame(menu_frame, bg=self.colors['sidebar'])

        # Create canvas for scrollable submenu
        submenu_canvas = tk.Canvas(submenu_outer, bg=self.colors['sidebar'],
                                   highlightthickness=0, bd=0)
        submenu_scrollbar = ttk.Scrollbar(submenu_outer, orient="vertical",
                                         command=submenu_canvas.yview)
        submenu_container = tk.Frame(submenu_canvas, bg=self.colors['sidebar'])

        submenu_canvas.configure(yscrollcommand=submenu_scrollbar.set)

        # Create window in canvas - set width to sidebar width minus scrollbar
        canvas_window = submenu_canvas.create_window((0, 0), window=submenu_container,
                                                     anchor='nw', width=LAYOUT['sidebar_width']-30)

        # Update scroll region when container size changes
        def update_scroll_region(_event=None):
            # Update the scroll region to match the container size
            submenu_canvas.update_idletasks()
            submenu_canvas.configure(scrollregion=submenu_canvas.bbox("all"))

            # Get the actual height needed
            items_height = submenu_container.winfo_reqheight()

            # Limit max height to 250px to ensure scrollbar appears when needed
            max_height = min(items_height, 250)
            submenu_canvas.configure(height=max_height)

        submenu_container.bind('<Configure>', update_scroll_region)

        # Mouse wheel scrolling - only when hovering over submenu
        def on_mousewheel(event):
            if submenu_canvas.winfo_exists() and submenu_outer.winfo_ismapped():
                submenu_canvas.yview_scroll(int(-1*(event.delta/120)), "units")

        def bind_mousewheel_enter(_event):
            submenu_canvas.bind_all("<MouseWheel>", on_mousewheel)

        def unbind_mousewheel_leave(_event):
            submenu_canvas.unbind_all("<MouseWheel>")

        submenu_outer.bind("<Enter>", bind_mousewheel_enter)
        submenu_outer.bind("<Leave>", unbind_mousewheel_leave)

        # Click handler
        def toggle_menu(event=None):
            if menu_data['submenus']:
                # Toggle submenu
                if submenu_outer.winfo_ismapped():
                    submenu_outer.pack_forget()
                    unbind_mousewheel_leave(None)
                else:
                    # Pack canvas and scrollbar
                    submenu_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
                    submenu_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
                    submenu_outer.pack(fill=tk.X, pady=(0, 5))
                    self.current_module = menu_data['name']
                    self.show_module_content(menu_data['name'])
                    # Force update of scroll region after a short delay
                    self.after(100, update_scroll_region)
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
        elif module_name == 'Utilities' and submenu_name == 'Financial Years':
            self.show_financial_years_management()
        elif module_name == 'Master Data' and submenu_name == 'Account Group Master':
            self.show_account_group_management()
        elif module_name == 'Master Data' and submenu_name == 'Account Master':
            self.show_account_master_management()
        elif module_name == 'Master Data' and submenu_name == 'Business Partner':
            self.show_business_partner_management()
        elif module_name == 'Master Data' and submenu_name == 'Item Group Master':
            self.show_item_group_management()
        elif module_name == 'Master Data' and submenu_name == 'Item Type Master':
            self.show_item_type_management()
        elif module_name == 'Master Data' and submenu_name == 'Manufacturer Master':
            self.show_item_company_management()
        elif module_name == 'Master Data' and submenu_name == 'Item Master':
            self.show_item_management()
        elif module_name == 'Master Data' and submenu_name == 'UoM Master':
            self.show_uom_management()
        elif module_name == 'Master Data' and submenu_name == 'City Master':
            self.show_city_management()
        elif module_name == 'Master Data' and submenu_name == 'State Master':
            self.show_state_management()
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

    def show_financial_years_management(self):
        """Show financial years management screen"""
        try:
            from financial_year_management import FinancialYearManagement

            # Clear content
            for widget in self.content_frame.winfo_children():
                widget.destroy()

            # Create financial year management widget
            fy_mgmt = FinancialYearManagement(self.content_frame, self.colors)
            fy_mgmt.pack(fill=tk.BOTH, expand=True)

        except Exception as e:
            messagebox.showerror("Error", f"Could not load Financial Years module: {e}")

    def show_account_group_management(self):
        """Show account group management screen"""
        try:
            from account_group_management import AccountGroupManagement

            # Clear content
            for widget in self.content_frame.winfo_children():
                widget.destroy()

            # Create account group management widget
            ag_mgmt = AccountGroupManagement(self.content_frame, self.colors)
            ag_mgmt.pack(fill=tk.BOTH, expand=True)

        except Exception as e:
            messagebox.showerror("Error", f"Could not load Account Group Master module: {e}")

    def show_item_group_management(self):
        """Show item group management screen"""
        try:
            from item_group_management import ItemGroupManagement

            # Clear content
            for widget in self.content_frame.winfo_children():
                widget.destroy()

            # Create item group management widget
            ig_mgmt = ItemGroupManagement(self.content_frame, self.colors)
            ig_mgmt.pack(fill=tk.BOTH, expand=True)

        except Exception as e:
            messagebox.showerror("Error", f"Could not load Item Group Master module: {e}")

    def show_item_type_management(self):
        """Show item type management screen"""
        try:
            from item_type_management import ItemTypeManagement

            # Clear content
            for widget in self.content_frame.winfo_children():
                widget.destroy()

            # Create item type management widget
            it_mgmt = ItemTypeManagement(self.content_frame, self.colors)
            it_mgmt.pack(fill=tk.BOTH, expand=True)

        except Exception as e:
            messagebox.showerror("Error", f"Could not load Item Type Master module: {e}")

    def show_item_company_management(self):
        """Show manufacturer management screen"""
        try:
            from item_company_management import ItemCompanyManagement

            # Clear content
            for widget in self.content_frame.winfo_children():
                widget.destroy()

            # Create manufacturer management widget
            ic_mgmt = ItemCompanyManagement(self.content_frame, self.colors)
            ic_mgmt.pack(fill=tk.BOTH, expand=True)

        except Exception as e:
            messagebox.showerror("Error", f"Could not load Manufacturer Master module: {e}")

    def show_city_management(self):
        """Show city management screen"""
        try:
            from city_management import CityManagement

            # Clear content
            for widget in self.content_frame.winfo_children():
                widget.destroy()

            # Create city management widget
            city_mgmt = CityManagement(self.content_frame, self.colors)
            city_mgmt.pack(fill=tk.BOTH, expand=True)

        except Exception as e:
            messagebox.showerror("Error", f"Could not load City Master module: {e}")

    def show_state_management(self):
        """Show state management screen"""
        try:
            from state_management import StateManagement

            # Clear content
            for widget in self.content_frame.winfo_children():
                widget.destroy()

            # Create state management widget
            state_mgmt = StateManagement(self.content_frame, self.colors)
            state_mgmt.pack(fill=tk.BOTH, expand=True)

        except Exception as e:
            messagebox.showerror("Error", f"Could not load State Master module: {e}")

    def show_uom_management(self):
        """Show UoM (Unit of Measure) management screen"""
        try:
            from uom_management import UoMManagement

            # Clear content
            for widget in self.content_frame.winfo_children():
                widget.destroy()

            # Create UoM management widget
            uom_mgmt = UoMManagement(self.content_frame, self.colors)
            uom_mgmt.pack(fill=tk.BOTH, expand=True)

        except Exception as e:
            messagebox.showerror("Error", f"Could not load UoM Master module: {e}")

    def show_item_management(self):
        """Show Item Master management screen"""
        try:
            from item_management import ItemManagement

            # Clear content
            for widget in self.content_frame.winfo_children():
                widget.destroy()

            # Create item management widget
            item_mgmt = ItemManagement(self.content_frame, self.colors)
            item_mgmt.pack(fill=tk.BOTH, expand=True)

        except Exception as e:
            messagebox.showerror("Error", f"Could not load Item Master module: {e}")

    def show_account_master_management(self):
        """Show account master management screen"""
        try:
            from account_master_management import AccountMasterManagement

            # Clear content
            for widget in self.content_frame.winfo_children():
                widget.destroy()

            # Create account master management widget
            am_mgmt = AccountMasterManagement(self.content_frame, self.colors)
            am_mgmt.pack(fill=tk.BOTH, expand=True)

        except Exception as e:
            messagebox.showerror("Error", f"Could not load Account Master module: {e}")

    def show_business_partner_management(self):
        """Show business partner management screen"""
        try:
            from business_partner_management import BusinessPartnerManagement

            # Clear content
            for widget in self.content_frame.winfo_children():
                widget.destroy()

            # Create business partner management widget
            bp_mgmt = BusinessPartnerManagement(self.content_frame, self.colors)
            bp_mgmt.pack(fill=tk.BOTH, expand=True)

        except Exception as e:
            messagebox.showerror("Error", f"Could not load Business Partner module: {e}")

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
    def load_generated_module(self, module_path):
        """Dynamically load a generated module"""
        try:
            # module_path should be like 'tables.ProductsTable'
            parts = module_path.rsplit('.', 1)
            module_name = parts[0]
            class_name = parts[1]
            
            # Import module
            module = __import__(module_name, fromlist=[class_name])
            widget_class = getattr(module, class_name)
            
            # Create instance
            from database.company_handler import CompanyHandler
            handler = CompanyHandler()  # Or use the appropriate handler
            
            widget = widget_class(self.content_frame, handler)
            widget.pack(fill=tk.BOTH, expand=True)
            return True
        except Exception as e:
            messagebox.showerror("Error", f"Could not load module: {e}")
            return False    


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
