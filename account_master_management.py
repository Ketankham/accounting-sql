"""
Account Master Management Screen - List, Create, Edit Accounts
"""

import tkinter as tk
from tkinter import ttk, messagebox
from database.account_master_handler import AccountMasterHandler
from ui_config import COLORS, FONTS, SPACING, LAYOUT, BUTTON_STYLES


class AccountMasterManagement(tk.Frame):
    def __init__(self, parent, colors):
        super().__init__(parent, bg=COLORS['background'])
        self.colors = COLORS
        self.account_master_handler = AccountMasterHandler()

        # Connect to database
        if not self.account_master_handler.connect():
            messagebox.showerror("Database Error",
                               "Failed to connect to database.")
            return

        # Current view state
        self.current_view = 'list'  # 'list' or 'form'
        self.edit_account_id = None

        # Create UI
        self.create_widgets()
        self.load_accounts()

    def create_widgets(self):
        """Create the account master management UI"""
        # Header
        header_frame = tk.Frame(self, bg=self.colors['background'])
        header_frame.pack(fill=tk.X, padx=SPACING['xl'], pady=(SPACING['lg'], SPACING['md']))

        self.title_label = tk.Label(header_frame,
                                    text="Account Master",
                                    font=FONTS['h1'],
                                    bg=self.colors['background'],
                                    fg=self.colors['text_primary'])
        self.title_label.pack(side=tk.LEFT)

        self.create_btn = tk.Button(header_frame,
                                    text="Create New Account")
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
        """Create the table view for accounts"""
        # Clear content container
        for widget in self.content_container.winfo_children():
            widget.destroy()

        # Table container with border
        table_frame = tk.Frame(self.content_container,
                              bg=self.colors['border'],
                              relief=tk.SOLID,
                              bd=2)
        table_frame.pack(fill=tk.BOTH, expand=True)

        # Table header
        header_frame = tk.Frame(table_frame, bg=self.colors['surface'], height=LAYOUT['table_header_height'])
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)

        headers = [
            ("Sr.", 3),
            ("Account Code", 8),
            ("Account Name", 15),
            ("Account Group", 12),
            ("Book Code", 10),
            ("Account Type", 10),
            ("Opening Balance", 10),
            ("Status", 6),
            ("Action", 4)
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
            header_label.pack(side=tk.LEFT, padx=SPACING['xs'])

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

        # Create window with proper width binding
        self.canvas_window = canvas.create_window((0, 0), window=self.table_body, anchor="nw")

        # Bind canvas width to table_body width
        def on_canvas_configure(event):
            canvas.itemconfig(self.canvas_window, width=event.width)
        canvas.bind("<Configure>", on_canvas_configure)
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Enable mousewheel scrolling
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")

        canvas.bind_all("<MouseWheel>", _on_mousewheel)

    def load_accounts(self):
        """Load accounts from database and display in table grouped by book code"""
        # Clear existing rows
        for widget in self.table_body.winfo_children():
            widget.destroy()

        # Get accounts
        accounts = self.account_master_handler.get_all_accounts()

        if not accounts:
            # No accounts found
            no_data_label = tk.Label(self.table_body,
                                    text="No accounts found. Click 'Create New Account' to add one.",
                                    font=FONTS['body'],
                                    bg=self.colors['background'],
                                    fg=self.colors['text_tertiary'],
                                    pady=SPACING['xxl'])
            no_data_label.pack(fill=tk.BOTH)
            return

        # Group accounts by book code
        from collections import defaultdict
        grouped_accounts = defaultdict(list)
        for account in accounts:
            book_code_id = account.get('book_code_id', 0)
            book_code_name = account.get('book_code_name', 'Unknown')
            grouped_accounts[(book_code_id, book_code_name)].append(account)

        # Sort book codes by ID
        sorted_book_codes = sorted(grouped_accounts.keys(), key=lambda x: x[0])

        # Display accounts grouped by book code
        sr_no = 1
        for book_code_id, book_code_name in sorted_book_codes:
            # Book code header (optional visual separator)
            # Accounts under this book code
            for account in grouped_accounts[(book_code_id, book_code_name)]:
                self.create_table_row(sr_no, account)
                sr_no += 1

    def create_table_row(self, sr_no, account):
        """Create a single table row"""
        # Alternating row colors
        row_bg = self.colors['background'] if sr_no % 2 == 0 else self.colors['surface']

        row_frame = tk.Frame(self.table_body, bg=row_bg, height=LAYOUT['table_row_height'])
        row_frame.pack(fill=tk.X, pady=1)
        row_frame.pack_propagate(False)

        # Hover effect
        def on_enter(e):
            row_frame.config(bg='#DBEAFE')
            for widget in row_frame.winfo_children():
                if isinstance(widget, (tk.Label, tk.Frame)) and widget != edit_btn:
                    widget.config(bg='#DBEAFE')

        def on_leave(e):
            row_frame.config(bg=row_bg)
            for widget in row_frame.winfo_children():
                if isinstance(widget, (tk.Label, tk.Frame)) and widget != edit_btn:
                    widget.config(bg=row_bg)

        row_frame.bind('<Enter>', on_enter)
        row_frame.bind('<Leave>', on_leave)

        # Serial number
        sr_label = tk.Label(row_frame, text=str(sr_no),
                           font=FONTS['body'],
                           bg=row_bg,
                           fg=self.colors['text_primary'],
                           width=3,
                           anchor='w',
                           padx=SPACING['md'])
        sr_label.pack(side=tk.LEFT, padx=SPACING['xs'])
        sr_label.bind('<Enter>', on_enter)
        sr_label.bind('<Leave>', on_leave)

        # Account Code
        code_label = tk.Label(row_frame, text=account.get('account_code', 'N/A'),
                             font=FONTS['body'],
                             bg=row_bg,
                             fg=self.colors['text_primary'],
                             width=8,
                             anchor='w',
                             padx=SPACING['md'])
        code_label.pack(side=tk.LEFT, padx=SPACING['xs'])
        code_label.bind('<Enter>', on_enter)
        code_label.bind('<Leave>', on_leave)

        # Account Name
        name_label = tk.Label(row_frame, text=account.get('account_name', 'N/A'),
                             font=FONTS['body'],
                             bg=row_bg,
                             fg=self.colors['text_primary'],
                             width=15,
                             anchor='w',
                             padx=SPACING['md'])
        name_label.pack(side=tk.LEFT, padx=SPACING['xs'])
        name_label.bind('<Enter>', on_enter)
        name_label.bind('<Leave>', on_leave)

        # Account Group
        ag_label = tk.Label(row_frame, text=account.get('account_group_name', 'N/A'),
                           font=FONTS['body'],
                           bg=row_bg,
                           fg=self.colors['text_primary'],
                           width=12,
                           anchor='w',
                           padx=SPACING['md'])
        ag_label.pack(side=tk.LEFT, padx=SPACING['xs'])
        ag_label.bind('<Enter>', on_enter)
        ag_label.bind('<Leave>', on_leave)

        # Book Code
        bc_label = tk.Label(row_frame, text=account.get('book_code_name', 'N/A'),
                           font=FONTS['body'],
                           bg=row_bg,
                           fg=self.colors['text_primary'],
                           width=10,
                           anchor='w',
                           padx=SPACING['md'])
        bc_label.pack(side=tk.LEFT, padx=SPACING['xs'])
        bc_label.bind('<Enter>', on_enter)
        bc_label.bind('<Leave>', on_leave)

        # Account Type
        at_label = tk.Label(row_frame, text=account.get('account_type_name', 'N/A'),
                           font=FONTS['body'],
                           bg=row_bg,
                           fg=self.colors['text_primary'],
                           width=10,
                           anchor='w',
                           padx=SPACING['md'])
        at_label.pack(side=tk.LEFT, padx=SPACING['xs'])
        at_label.bind('<Enter>', on_enter)
        at_label.bind('<Leave>', on_leave)

        # Opening Balance
        balance_text = f"{account.get('opening_balance', 0)} {account.get('balance_type', 'Debit')[0]}"
        balance_label = tk.Label(row_frame, text=balance_text,
                                font=FONTS['body'],
                                bg=row_bg,
                                fg=self.colors['text_primary'],
                                width=10,
                                anchor='w',
                                padx=SPACING['md'])
        balance_label.pack(side=tk.LEFT, padx=SPACING['xs'])
        balance_label.bind('<Enter>', on_enter)
        balance_label.bind('<Leave>', on_leave)

        # Status
        status = account.get('status', 'N/A')
        status_color = '#10B981' if status == 'Active' else '#EF4444'
        status_label = tk.Label(row_frame, text=status,
                               font=FONTS['body'],
                               bg=row_bg,
                               fg=status_color,
                               width=6,
                               anchor='w',
                               padx=SPACING['md'])
        status_label.pack(side=tk.LEFT, padx=SPACING['xs'])
        status_label.bind('<Enter>', on_enter)
        status_label.bind('<Leave>', on_leave)

        # Action buttons container
        action_frame = tk.Frame(row_frame, bg=row_bg)
        action_frame.pack(side=tk.LEFT, padx=SPACING['md'])
        action_frame.bind('<Enter>', on_enter)
        action_frame.bind('<Leave>', on_leave)

        # Edit button only (delete moved to edit form)
        edit_btn = tk.Button(action_frame, text="Edit",
                            font=FONTS['small'],
                            bg=self.colors['primary'],
                            fg='white',
                            activebackground=self.colors['primary_hover'],
                            activeforeground='white',
                            cursor='hand2',
                            relief=tk.FLAT,
                            padx=SPACING['sm'],
                            pady=SPACING['xs'],
                            command=lambda: self.show_edit_form(account['id']))
        edit_btn.pack(side=tk.LEFT)

    def show_create_form(self):
        """Show create account form"""
        # Clear content container
        for widget in self.content_container.winfo_children():
            widget.destroy()

        # Update title
        self.title_label.config(text="Create New Account")

        # Hide create button
        self.create_btn.pack_forget()

        # Import and create form
        from account_master_form import AccountMasterForm

        form = AccountMasterForm(
            self.content_container,
            self.colors,
            self.account_master_handler,
            None,  # No existing data
            on_save=self.on_form_save,
            on_cancel=self.on_form_cancel
        )
        form.pack(fill=tk.BOTH, expand=True)

        self.current_view = 'form'

    def show_edit_form(self, account_id):
        """Show edit account form"""
        # Get account data
        account_data = self.account_master_handler.get_account_by_id(account_id)

        if not account_data:
            messagebox.showerror("Error", "Account not found")
            return

        # Clear content container
        for widget in self.content_container.winfo_children():
            widget.destroy()

        # Update title
        self.title_label.config(text=f"Edit Account: {account_data['account_name']}")

        # Hide create button
        self.create_btn.pack_forget()

        # Import and create form
        from account_master_form import AccountMasterForm

        form = AccountMasterForm(
            self.content_container,
            self.colors,
            self.account_master_handler,
            account_data,
            on_save=self.on_form_save,
            on_cancel=self.on_form_cancel,
            on_delete=self.delete_account  # Pass delete callback for edit mode
        )
        form.pack(fill=tk.BOTH, expand=True)

        self.current_view = 'form'
        self.edit_account_id = account_id

    def on_form_save(self):
        """Handle form save"""
        # Return to list view
        self.on_form_cancel()

    def on_form_cancel(self):
        """Handle form cancel"""
        # Update title
        self.title_label.config(text="Account Master")

        # Show create button
        self.create_btn.pack(side=tk.RIGHT)

        # Recreate table view
        self.create_table_view()
        self.load_accounts()

        self.current_view = 'list'
        self.edit_account_id = None

    def delete_account(self, account_id, account_name):
        """Delete an account"""
        result = messagebox.askyesno("Confirm Delete",
                                     f"Are you sure you want to delete '{account_name}'?\n\n" +
                                     "This action cannot be undone.")

        if result:
            success, message = self.account_master_handler.delete_account(account_id)
            if success:
                messagebox.showinfo("Success", message)
                self.load_accounts()
            else:
                messagebox.showerror("Error", message)
