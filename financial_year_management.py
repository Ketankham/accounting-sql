"""
Financial Year Management Screen - List, Create, Edit Financial Years
Fully Fixed & Enhanced Version
"""

import tkinter as tk
from tkinter import ttk, messagebox
from database.financial_year_handler import FinancialYearHandler
from ui_config import COLORS, FONTS, SPACING, LAYOUT


class FinancialYearManagement(tk.Frame):
    def __init__(self, parent, colors):
        # print("\n[DEBUG] === FinancialYearManagement.__init__() START ===")
        super().__init__(parent, bg=COLORS['background'])
        self.colors = COLORS  # Use unified colors
        self.fy_handler = FinancialYearHandler()

        # Connect to database
        if not self.fy_handler.connect():
            messagebox.showerror("Database Error", "Failed to connect to SQLite database.")
            return

        # View state
        self.current_view = 'list'
        self.edit_fy_id = None

        # Create UI
        # print("[DEBUG] Calling create_widgets()...")
        self.create_widgets()
        # print("[DEBUG] create_widgets() completed")

        # print("[DEBUG] Calling load_financial_years()...")
        self.load_financial_years()
        # print("[DEBUG] === FinancialYearManagement.__init__() END ===")

    # -------------------------------------------------------------------------
    # UI Creation
    # -------------------------------------------------------------------------
    def create_widgets(self):
        """Create the main UI elements"""
        header_frame = tk.Frame(self, bg=self.colors['background'])
        header_frame.pack(fill=tk.X, padx=SPACING['xl'], pady=(SPACING['lg'], SPACING['md']))

        self.title_label = tk.Label(
            header_frame,
            text="Financial Year Management",
            font=FONTS['h1'],
            bg=self.colors['background'],
            fg=self.colors['text_primary']
        )
        self.title_label.pack(side=tk.LEFT)

        self.create_btn = tk.Button(
            header_frame,
            text="Create New Financial Year",
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

        # Hover effect
        self.create_btn.bind('<Enter>', lambda e: self.create_btn.config(bg=self.colors['primary_hover']))
        self.create_btn.bind('<Leave>', lambda e: self.create_btn.config(bg=self.colors['primary']))

        # Content container
        self.content_container = tk.Frame(self, bg=self.colors['background'])
        self.content_container.pack(fill=tk.BOTH, expand=True, padx=SPACING['xl'], pady=SPACING['md'])

        # Create table
        self.create_table_view()

    # -------------------------------------------------------------------------
    # Table View
    # -------------------------------------------------------------------------
    def create_table_view(self):
        """Create the table view for financial years"""
        # print("\n[DEBUG] === create_table_view() START ===")

        # Clear content
        # print("[DEBUG] Clearing content_container...")
        for widget in self.content_container.winfo_children():
            widget.destroy()
        # print(f"[DEBUG] content_container cleared. Children: {len(self.content_container.winfo_children())}")

        table_frame = tk.Frame(self.content_container, bg=self.colors['border'], relief=tk.SOLID, bd=2)
        table_frame.pack(fill=tk.BOTH, expand=True)
        # print(f"[DEBUG] table_frame created and packed: {table_frame}")

        # Header
        header_frame = tk.Frame(table_frame, bg=self.colors['surface'], height=LAYOUT['table_header_height'])
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)

        headers = [
            ("Sr.", 4),
            ("FY Code", 8),
            ("Display Name", 28),
            ("Start Date", 12),
            ("End Date", 12),
            ("Status", 8),
            ("Action", 8)
        ]

        for header_text, width in headers:
            header_label = tk.Label(
                header_frame,
                text=header_text,
                font=FONTS['body_bold'],
                bg=self.colors['surface'],
                fg=self.colors['text_primary'],
                anchor='w',
                width=width,
                padx=SPACING['md']
            )
            header_label.pack(side=tk.LEFT, padx=SPACING['sm'])

        # Canvas for scrollable area
        # print("[DEBUG] Creating canvas and scrollbar...")
        table_canvas_frame = tk.Frame(table_frame, bg=self.colors['background'])
        table_canvas_frame.pack(fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(table_canvas_frame, bg=self.colors['background'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(table_canvas_frame, orient="vertical", command=self.canvas.yview)
        self.table_body = tk.Frame(self.canvas, bg=self.colors['background'])

        self.table_body.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        # CRITICAL FIX: Create window with proper width binding to prevent 1px wide frame
        # See TKINTER_CANVAS_TABLE_FIX.md for details
        self.canvas_window = self.canvas.create_window((0, 0), window=self.table_body, anchor="nw")

        # Bind canvas width to table_body width so it expands horizontally
        def on_canvas_configure(event):
            self.canvas.itemconfig(self.canvas_window, width=event.width)
        self.canvas.bind("<Configure>", on_canvas_configure)

        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Mousewheel scroll
        def _on_mousewheel(event):
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        self.canvas.bind("<Enter>", lambda e: self.canvas.bind_all("<MouseWheel>", _on_mousewheel))
        self.canvas.bind("<Leave>", lambda e: self.canvas.unbind_all("<MouseWheel>"))

    # -------------------------------------------------------------------------
    # Data Loading
    # -------------------------------------------------------------------------
    def load_financial_years(self):
        """Load financial years from database and display in table"""
        # Check if table_body exists
        if not hasattr(self, 'table_body'):
            print("[ERROR] table_body does not exist!")
            return

        # Clear previous rows
        for widget in self.table_body.winfo_children():
            widget.destroy()

        # Load financial years from database
        financial_years = self.fy_handler.get_all_financial_years()

        if not financial_years:
            no_data_label = tk.Label(
                self.table_body,
                text="No financial years found. Click 'Create New Financial Year' to add one.",
                font=FONTS['body'],
                bg=self.colors['background'],
                fg=self.colors['text_secondary'],
                pady=SPACING['xl']
            )
            no_data_label.pack(fill=tk.BOTH, expand=True)
            return

        # Create rows
        for idx, fy in enumerate(financial_years, 1):
            self.create_table_row(idx, fy)

        # Refresh canvas scroll area
        self.table_body.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))


    # -------------------------------------------------------------------------
    # Table Row Creation
    # -------------------------------------------------------------------------
    def create_table_row(self, sr_no, fy):
        """Create a single financial year row"""
        bg_color = self.colors['background'] if sr_no % 2 == 0 else self.colors['surface']
        row_frame = tk.Frame(self.table_body, bg=bg_color, height=LAYOUT['table_row_height'])
        row_frame.pack(fill=tk.X, pady=SPACING['xs'])
        row_frame.pack_propagate(False)

        # Hover highlight
        def on_enter(e): row_frame.config(bg=self.colors['primary_light'])
        def on_leave(e): row_frame.config(bg=bg_color)
        row_frame.bind("<Enter>", on_enter)
        row_frame.bind("<Leave>", on_leave)

        # Serial number
        tk.Label(
            row_frame, text=str(sr_no),
            font=FONTS['body'],
            bg=bg_color,
            fg=self.colors['text_primary'],
            width=4, anchor='w', padx=SPACING['md']
        ).pack(side=tk.LEFT, padx=SPACING['sm'])

        # FY Code
        tk.Label(
            row_frame, text=fy['fy_code'],
            font=FONTS['body'],
            bg=bg_color,
            fg=self.colors['text_primary'],
            width=8, anchor='w', padx=SPACING['md']
        ).pack(side=tk.LEFT, padx=SPACING['sm'])

        # Display Name
        tk.Label(
            row_frame, text=fy['display_name'],
            font=FONTS['body'],
            bg=bg_color,
            fg=self.colors['text_primary'],
            width=28, anchor='w', padx=SPACING['md']
        ).pack(side=tk.LEFT, padx=SPACING['sm'])

        # Start Date
        tk.Label(
            row_frame, text=str(fy['start_date']),
            font=FONTS['body'],
            bg=bg_color,
            fg=self.colors['text_primary'],
            width=12, anchor='w', padx=SPACING['md']
        ).pack(side=tk.LEFT, padx=SPACING['sm'])

        # End Date
        tk.Label(
            row_frame, text=str(fy['end_date']),
            font=FONTS['body'],
            bg=bg_color,
            fg=self.colors['text_primary'],
            width=12, anchor='w', padx=SPACING['md']
        ).pack(side=tk.LEFT, padx=SPACING['sm'])

        # Status
        status_color = self.colors['success'] if fy['status'] == 'Active' else self.colors['error']
        tk.Label(
            row_frame, text=fy['status'],
            font=FONTS['body_bold'],
            bg=bg_color,
            fg=status_color,
            width=8, anchor='w', padx=SPACING['md']
        ).pack(side=tk.LEFT, padx=SPACING['sm'])

        # Edit button
        edit_btn = tk.Button(
            row_frame, text="Edit",
            font=FONTS['small_bold'],
            bg=self.colors['primary'],
            fg='white',
            activebackground=self.colors['primary_hover'],
            activeforeground='white',
            cursor='hand2',
            relief=tk.FLAT,
            padx=SPACING['sm'],
            pady=SPACING['xs'],
            width=6,
            command=lambda: self.show_edit_form(fy['id'])
        )
        edit_btn.pack(side=tk.LEFT, padx=SPACING['sm'])

        # Hover effect for edit button
        edit_btn.bind('<Enter>', lambda e: edit_btn.config(bg=self.colors['primary_hover']))
        edit_btn.bind('<Leave>', lambda e: edit_btn.config(bg=self.colors['primary']))

    # -------------------------------------------------------------------------
    # Form Handlers
    # -------------------------------------------------------------------------
    def show_create_form(self):
        """Open create financial year form"""
        self.current_view = 'form'
        self.edit_fy_id = None
        self.create_btn.pack_forget()
        self.title_label.config(text="Create New Financial Year")
        self.show_form(None)

    def show_edit_form(self, fy_id):
        """Open edit financial year form"""
        self.current_view = 'form'
        self.edit_fy_id = fy_id
        self.create_btn.pack_forget()
        self.title_label.config(text="Edit Financial Year")

        fy_data = self.fy_handler.get_financial_year_by_id(fy_id)

        if not fy_data:
            messagebox.showerror("Error", "Financial Year not found.")
            self.show_list_view()
            return

        self.show_form(fy_data)

    def show_form(self, fy_data):
        """Show financial year form"""
        for widget in self.content_container.winfo_children():
            widget.destroy()

        from financial_year_form import FinancialYearForm
        form = FinancialYearForm(
            self.content_container,
            self.colors,
            self.fy_handler,
            fy_data,
            self.on_form_save,
            self.on_form_cancel
        )
        form.pack(fill=tk.BOTH, expand=True)

    def on_form_save(self):
        """After saving a form"""
        self.show_list_view()
        self.load_financial_years()

    def on_form_cancel(self):
        """On cancel"""
        self.show_list_view()

    def show_list_view(self):
        """Return to list view"""
        self.current_view = 'list'
        self.edit_fy_id = None
        self.create_btn.pack(side=tk.RIGHT)
        self.title_label.config(text="Financial Year Management")
        self.create_table_view()
        self.load_financial_years()

    # -------------------------------------------------------------------------
    # Cleanup
    # -------------------------------------------------------------------------
    def __del__(self):
        if hasattr(self, 'fy_handler'):
            self.fy_handler.disconnect()
