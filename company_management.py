"""
Company Management Screen - List, Create, Edit Companies
"""

import tkinter as tk
from tkinter import ttk, messagebox
from database.company_handler import CompanyHandler
from ui_config import COLORS, FONTS, SPACING, LAYOUT, BUTTON_STYLES


class CompanyManagement(tk.Frame):
    def __init__(self, parent, colors):
        super().__init__(parent, bg=COLORS['background'])
        self.colors = COLORS  # Use unified colors
        self.company_handler = CompanyHandler()

        # Connect to database
        if not self.company_handler.connect():
            messagebox.showerror("Database Error",
                               "Failed to connect to database.")
            return

        # Current view state
        self.current_view = 'list'  # 'list' or 'form'
        self.edit_company_id = None

        # Create UI
        self.create_widgets()
        self.load_companies()

    def create_widgets(self):
        """Create the company management UI"""
        # Header
        header_frame = tk.Frame(self, bg=self.colors['background'])
        header_frame.pack(fill=tk.X, padx=SPACING['xl'], pady=(SPACING['lg'], SPACING['md']))

        self.title_label = tk.Label(header_frame,
                                    text="Company Management",
                                    font=FONTS['h1'],
                                    bg=self.colors['background'],
                                    fg=self.colors['text_primary'])
        self.title_label.pack(side=tk.LEFT)

        self.create_btn = tk.Button(header_frame,
                                    text="Create New Company")
        self.create_btn.config(
            font=FONTS['button'],
            bg=self.colors['primary'],
            fg='white',
            activebackground=self.colors['primary_hover'],
            activeforeground='white',
            cursor='hand2',
            relief=tk.FLAT,
            padx=SPACING['lg'],
            pady=SPACING['md'],
            command=self.show_create_form
        )
        self.create_btn.pack(side=tk.RIGHT)

        # Add hover effect
        self.create_btn.bind('<Enter>', lambda e: self.create_btn.config(bg=self.colors['primary_hover']))
        self.create_btn.bind('<Leave>', lambda e: self.create_btn.config(bg=self.colors['primary']))

        # Content container (will hold either table or form)
        self.content_container = tk.Frame(self, bg=self.colors['background'])
        self.content_container.pack(fill=tk.BOTH, expand=True, padx=SPACING['xl'], pady=SPACING['md'])

        # Create table view
        self.create_table_view()

    def create_table_view(self):
        """Create the table view for companies"""
        # Clear content container
        for widget in self.content_container.winfo_children():
            widget.destroy()

        # Table container with border (thicker, better contrast)
        table_frame = tk.Frame(self.content_container,
                              bg=self.colors['border'],
                              relief=tk.SOLID,
                              bd=2)
        table_frame.pack(fill=tk.BOTH, expand=True)

        # Table header with better height and spacing
        header_frame = tk.Frame(table_frame, bg=self.colors['surface'], height=LAYOUT['table_header_height'])
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)

        headers = [
            ("Sr.", 60),
            ("Company Code", 180),
            ("Company Name", 300),
            ("Status", 140),
            ("Action", 180)
        ]

        for header_text, width in headers:
            header_label = tk.Label(header_frame,
                                   text=header_text,
                                   font=FONTS['body_bold'],
                                   bg=self.colors['surface'],
                                   fg=self.colors['text_primary'],
                                   anchor='w',
                                   width=width,
                                   padx=SPACING['md'])
            header_label.pack(side=tk.LEFT, padx=SPACING['sm'])

        # Scrollable table body
        table_canvas_frame = tk.Frame(table_frame, bg=self.colors['background'])
        table_canvas_frame.pack(fill=tk.BOTH, expand=True)

        canvas = tk.Canvas(table_canvas_frame, bg=self.colors['background'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(table_canvas_frame, orient="vertical", command=canvas.yview)

        self.table_body = tk.Frame(canvas, bg=self.colors['background'])

        self.table_body.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.table_body, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Enable mousewheel scrolling
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")

        canvas.bind_all("<MouseWheel>", _on_mousewheel)

    def load_companies(self):
        """Load companies from database and display in table"""
        # Clear existing rows
        for widget in self.table_body.winfo_children():
            widget.destroy()

        # Get companies
        companies = self.company_handler.get_all_companies()

        if not companies:
            # No companies found
            no_data_label = tk.Label(self.table_body,
                                    text="No companies found. Click 'Create New Company' to add one.",
                                    font=FONTS['body'],
                                    bg=self.colors['background'],
                                    fg=self.colors['text_tertiary'],
                                    pady=SPACING['xxl'])
            no_data_label.pack(fill=tk.BOTH)
            return

        # Display companies
        for idx, company in enumerate(companies, 1):
            self.create_table_row(idx, company)

    def create_table_row(self, sr_no, company):
        """Create a single table row"""
        row_frame = tk.Frame(self.table_body, bg=self.colors['background'], height=LAYOUT['table_row_height'])
        row_frame.pack(fill=tk.X, pady=SPACING['xs'])
        row_frame.pack_propagate(False)

        # Bottom border (more visible)
        border = tk.Frame(row_frame, bg=self.colors['border_light'], height=1)
        border.pack(side=tk.BOTTOM, fill=tk.X)

        # Serial number
        sr_label = tk.Label(row_frame, text=str(sr_no),
                           font=FONTS['body'],
                           bg=self.colors['background'],
                           fg=self.colors['text_primary'],
                           width=60,
                           anchor='w',
                           padx=SPACING['md'])
        sr_label.pack(side=tk.LEFT, padx=SPACING['sm'])

        # Company code
        code_label = tk.Label(row_frame, text=company['company_code'],
                             font=FONTS['body'],
                             bg=self.colors['background'],
                             fg=self.colors['text_primary'],
                             width=180,
                             anchor='w',
                             padx=SPACING['md'])
        code_label.pack(side=tk.LEFT, padx=SPACING['sm'])

        # Company name
        name_label = tk.Label(row_frame, text=company['company_name'],
                             font=FONTS['body'],
                             bg=self.colors['background'],
                             fg=self.colors['text_primary'],
                             width=300,
                             anchor='w',
                             padx=SPACING['md'])
        name_label.pack(side=tk.LEFT, padx=SPACING['sm'])

        # Status
        status_frame = tk.Frame(row_frame, bg=self.colors['background'], width=140)
        status_frame.pack(side=tk.LEFT, padx=SPACING['md'])

        status_color = self.colors['success'] if company['status'] == 'Active' else self.colors['error']
        status_label = tk.Label(status_frame,
                               text=company['status'],
                               font=FONTS['body_bold'],
                               bg=self.colors['background'],
                               fg=status_color)
        status_label.pack()

        # Action button (better contrast and size)
        action_frame = tk.Frame(row_frame, bg=self.colors['background'], width=180)
        action_frame.pack(side=tk.LEFT, padx=SPACING['md'])

        edit_btn = tk.Button(action_frame,
                            text="Edit",
                            font=FONTS['small_bold'],
                            bg=self.colors['surface'],
                            fg=self.colors['text_primary'],
                            activebackground=self.colors['border'],
                            activeforeground=self.colors['text_primary'],
                            cursor='hand2',
                            relief=tk.FLAT,
                            padx=SPACING['md'],
                            pady=SPACING['sm'],
                            command=lambda: self.show_edit_form(company['id']))
        edit_btn.pack()

    def show_create_form(self):
        """Show the create company form"""
        self.current_view = 'form'
        self.edit_company_id = None

        # Hide create button and change title
        self.create_btn.pack_forget()
        self.title_label.config(text="Create New Company")

        # Show form
        from company_form import CompanyForm
        self.show_form(None)

    def show_edit_form(self, company_id):
        """Show the edit company form"""
        self.current_view = 'form'
        self.edit_company_id = company_id

        # Hide create button and change title
        self.create_btn.pack_forget()
        self.title_label.config(text="Edit Company")

        # Get company data
        company_data = self.company_handler.get_company_by_id(company_id)

        if not company_data:
            messagebox.showerror("Error", "Company not found")
            self.show_list_view()
            return

        # Show form
        self.show_form(company_data)

    def show_form(self, company_data):
        """Show company form (create or edit)"""
        # Clear content container
        for widget in self.content_container.winfo_children():
            widget.destroy()

        # Import and create form
        from company_form import CompanyForm

        form = CompanyForm(
            self.content_container,
            self.colors,
            self.company_handler,
            company_data,
            self.on_form_save,
            self.on_form_cancel
        )
        form.pack(fill=tk.BOTH, expand=True)

    def on_form_save(self):
        """Callback when form is saved"""
        self.show_list_view()
        self.load_companies()

    def on_form_cancel(self):
        """Callback when form is cancelled"""
        self.show_list_view()

    def show_list_view(self):
        """Show the list view"""
        self.current_view = 'list'
        self.edit_company_id = None

        # Show create button and restore title
        self.create_btn.pack(side=tk.RIGHT)
        self.title_label.config(text="Company Management")

        # Recreate table view
        self.create_table_view()
        self.load_companies()

    def __del__(self):
        """Cleanup when widget is destroyed"""
        if hasattr(self, 'company_handler'):
            self.company_handler.disconnect()
