"""
Financial Year Management Screen - List, Create, Edit Financial Years
"""

import tkinter as tk
from tkinter import ttk, messagebox
from database.financial_year_handler import FinancialYearHandler
from ui_config import COLORS, FONTS, SPACING, LAYOUT, BUTTON_STYLES


class FinancialYearManagement(tk.Frame):
    def __init__(self, parent, colors):
        super().__init__(parent, bg=COLORS['background'])
        self.colors = COLORS  # Use unified colors
        self.fy_handler = FinancialYearHandler()

        # Connect to database
        if not self.fy_handler.connect():
            messagebox.showerror("Database Error",
                               "Failed to connect to database.")
            return

        # Current view state
        self.current_view = 'list'  # 'list' or 'form'
        self.edit_fy_id = None

        # Create UI
        self.create_widgets()
        self.load_financial_years()

    def create_widgets(self):
        """Create the financial year management UI"""
        # Header
        header_frame = tk.Frame(self, bg=self.colors['background'])
        header_frame.pack(fill=tk.X, padx=SPACING['xl'], pady=(SPACING['lg'], SPACING['md']))

        self.title_label = tk.Label(header_frame,
                                    text="Financial Year Management",
                                    font=FONTS['h1'],
                                    bg=self.colors['background'],
                                    fg=self.colors['text_primary'])
        self.title_label.pack(side=tk.LEFT)

        self.create_btn = tk.Button(header_frame,
                                    text="Create New Financial Year")
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
        """Create the table view for financial years"""
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
            ("Sr.", 5),
            ("FY Code", 10),
            ("Display Name", 30),
            ("Start Date", 15),
            ("End Date", 15),
            ("Status", 10),
            ("Action", 10)
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

        self.canvas = tk.Canvas(table_canvas_frame, bg=self.colors['background'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(table_canvas_frame, orient="vertical", command=self.canvas.yview)

        self.table_body = tk.Frame(self.canvas, bg=self.colors['background'])

        self.table_body.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.table_body, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Enable mousewheel scrolling
        def _on_mousewheel(event):
            self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

        self.canvas.bind_all("<MouseWheel>", _on_mousewheel)

    def load_financial_years(self):
        """Load financial years from database and display in table"""
        print("\n" + "="*70)
        print("[UI] load_financial_years() called")
        print("="*70)

        # Clear existing rows
        for widget in self.table_body.winfo_children():
            widget.destroy()
        print("[UI] Cleared existing table rows")

        # Get financial years
        print("[UI] Calling fy_handler.get_all_financial_years()...")
        financial_years = self.fy_handler.get_all_financial_years()

        # DEBUG: Print what we got from database
        print(f"\n[UI] ✓ Retrieved {len(financial_years) if financial_years else 0} financial years from handler")
        if financial_years:
            print(f"[UI] Data type: {type(financial_years)}")
            print(f"[UI] First item type: {type(financial_years[0])}")
            print(f"[UI] First FY data: {financial_years[0]}")
        else:
            print("[UI] ⚠ No financial years returned!")

        if not financial_years:
            # No financial years found
            print("[UI] Showing 'No data' message\n")
            no_data_label = tk.Label(self.table_body,
                                    text="No financial years found. Click 'Create New Financial Year' to add one.",
                                    font=FONTS['body'],
                                    bg=self.colors['background'],
                                    fg=self.colors['text_tertiary'],
                                    pady=SPACING['xxl'])
            no_data_label.pack(fill=tk.BOTH)
            print("="*70 + "\n")
            return

        # Display financial years
        print(f"\n[UI] Creating {len(financial_years)} table rows...")
        for idx, fy in enumerate(financial_years, 1):
            print(f"[UI] Creating row {idx}: {fy.get('fy_code')} - {fy.get('display_name')}")
            self.create_table_row(idx, fy)
        print(f"[UI] ✓ All {len(financial_years)} rows created!")

        # Force canvas to update and recalculate scroll region
        if hasattr(self, 'canvas'):
            self.table_body.update_idletasks()
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))
            bbox = self.canvas.bbox("all")
            print(f"[UI] Canvas scroll region updated: {bbox}")
            if bbox:
                print(f"[UI] Canvas content size: {bbox[2]}x{bbox[3]} pixels")

        print("="*70 + "\n")

    def create_table_row(self, sr_no, fy):
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
                           width=5,
                           anchor='w',
                           padx=SPACING['md'])
        sr_label.pack(side=tk.LEFT, padx=SPACING['sm'])

        # FY Code
        code_label = tk.Label(row_frame, text=fy['fy_code'],
                             font=FONTS['body'],
                             bg=self.colors['background'],
                             fg=self.colors['text_primary'],
                             width=10,
                             anchor='w',
                             padx=SPACING['md'])
        code_label.pack(side=tk.LEFT, padx=SPACING['sm'])

        # Display Name
        name_label = tk.Label(row_frame, text=fy['display_name'],
                             font=FONTS['body'],
                             bg=self.colors['background'],
                             fg=self.colors['text_primary'],
                             width=30,
                             anchor='w',
                             padx=SPACING['md'])
        name_label.pack(side=tk.LEFT, padx=SPACING['sm'])

        # Start Date
        start_date = str(fy['start_date']) if fy['start_date'] else ''
        start_label = tk.Label(row_frame, text=start_date,
                              font=FONTS['body'],
                              bg=self.colors['background'],
                              fg=self.colors['text_primary'],
                              width=15,
                              anchor='w',
                              padx=SPACING['md'])
        start_label.pack(side=tk.LEFT, padx=SPACING['sm'])

        # End Date
        end_date = str(fy['end_date']) if fy['end_date'] else ''
        end_label = tk.Label(row_frame, text=end_date,
                            font=FONTS['body'],
                            bg=self.colors['background'],
                            fg=self.colors['text_primary'],
                            width=15,
                            anchor='w',
                            padx=SPACING['md'])
        end_label.pack(side=tk.LEFT, padx=SPACING['sm'])

        # Status
        status_label = tk.Label(row_frame,
                               text=fy['status'],
                               font=FONTS['body_bold'],
                               bg=self.colors['background'],
                               fg=self.colors['success'] if fy['status'] == 'Active' else self.colors['error'],
                               width=10,
                               anchor='w',
                               padx=SPACING['md'])
        status_label.pack(side=tk.LEFT, padx=SPACING['sm'])

        # Action button (better contrast and size)
        edit_btn = tk.Button(row_frame,
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
                            command=lambda: self.show_edit_form(fy['id']))
        edit_btn.pack(side=tk.LEFT, padx=SPACING['md'])

    def show_create_form(self):
        """Show the create financial year form"""
        self.current_view = 'form'
        self.edit_fy_id = None

        # Hide create button and change title
        self.create_btn.pack_forget()
        self.title_label.config(text="Create New Financial Year")

        # Show form
        from financial_year_form import FinancialYearForm
        self.show_form(None)

    def show_edit_form(self, fy_id):
        """Show the edit financial year form"""
        self.current_view = 'form'
        self.edit_fy_id = fy_id

        # Hide create button and change title
        self.create_btn.pack_forget()
        self.title_label.config(text="Edit Financial Year")

        # Get financial year data
        fy_data = self.fy_handler.get_financial_year_by_id(fy_id)

        if not fy_data:
            messagebox.showerror("Error", "Financial Year not found")
            self.show_list_view()
            return

        # Show form
        self.show_form(fy_data)

    def show_form(self, fy_data):
        """Show financial year form (create or edit)"""
        # Clear content container
        for widget in self.content_container.winfo_children():
            widget.destroy()

        # Import and create form
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
        """Callback when form is saved"""
        self.show_list_view()
        self.load_financial_years()

    def on_form_cancel(self):
        """Callback when form is cancelled"""
        self.show_list_view()

    def show_list_view(self):
        """Show the list view"""
        self.current_view = 'list'
        self.edit_fy_id = None

        # Show create button and restore title
        self.create_btn.pack(side=tk.RIGHT)
        self.title_label.config(text="Financial Year Management")

        # Recreate table view
        self.create_table_view()
        self.load_financial_years()

    def __del__(self):
        """Cleanup when widget is destroyed"""
        if hasattr(self, 'fy_handler'):
            self.fy_handler.disconnect()
