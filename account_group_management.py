"""
Account Group Management Screen - List, Create, Edit Account Groups
"""

import tkinter as tk
from tkinter import ttk, messagebox
from database.account_group_handler import AccountGroupHandler
from ui_config import COLORS, FONTS, SPACING, LAYOUT, BUTTON_STYLES


class AccountGroupManagement(tk.Frame):
    def __init__(self, parent, colors):
        super().__init__(parent, bg=COLORS['background'])
        self.colors = COLORS  # Use unified colors
        self.account_group_handler = AccountGroupHandler()

        # Connect to database
        if not self.account_group_handler.connect():
            messagebox.showerror("Database Error",
                               "Failed to connect to database.")
            return

        # Current view state
        self.current_view = 'list'  # 'list' or 'form'
        self.edit_account_group_id = None

        # Create UI
        self.create_widgets()
        self.load_account_groups()

    def create_widgets(self):
        """Create the account group management UI"""
        # Header
        header_frame = tk.Frame(self, bg=self.colors['background'])
        header_frame.pack(fill=tk.X, padx=SPACING['xl'], pady=(SPACING['lg'], SPACING['md']))

        self.title_label = tk.Label(header_frame,
                                    text="Account Group Master",
                                    font=FONTS['h1'],
                                    bg=self.colors['background'],
                                    fg=self.colors['text_primary'])
        self.title_label.pack(side=tk.LEFT)

        self.create_btn = tk.Button(header_frame,
                                    text="Create New Account Group")
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
        """Create the table view for account groups"""
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
            ("Sr.", 4),
            ("Name", 25),
            ("Account Group Type", 20),
            ("AG Code", 10),
            ("Status", 8),
            ("Action", 6)
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

    def load_account_groups(self):
        """Load account groups from database and display in table"""
        # Clear existing rows
        for widget in self.table_body.winfo_children():
            widget.destroy()

        # Get account groups
        account_groups = self.account_group_handler.get_all_account_groups()

        if not account_groups:
            # No account groups found
            no_data_label = tk.Label(self.table_body,
                                    text="No account groups found. Click 'Create New Account Group' to add one.",
                                    font=FONTS['body'],
                                    bg=self.colors['background'],
                                    fg=self.colors['text_tertiary'],
                                    pady=SPACING['xxl'])
            no_data_label.pack(fill=tk.BOTH)
            return

        # Display account groups
        for idx, account_group in enumerate(account_groups, 1):
            self.create_table_row(idx, account_group)

    def create_table_row(self, sr_no, account_group):
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
                           width=4,
                           anchor='w',
                           padx=SPACING['md'])
        sr_label.pack(side=tk.LEFT, padx=SPACING['sm'])
        sr_label.bind('<Enter>', on_enter)
        sr_label.bind('<Leave>', on_leave)

        # Account Group Name
        name_label = tk.Label(row_frame, text=account_group['name'],
                             font=FONTS['body'],
                             bg=row_bg,
                             fg=self.colors['text_primary'],
                             width=25,
                             anchor='w',
                             padx=SPACING['md'])
        name_label.pack(side=tk.LEFT, padx=SPACING['sm'])
        name_label.bind('<Enter>', on_enter)
        name_label.bind('<Leave>', on_leave)

        # Account Group Type
        type_label = tk.Label(row_frame, text=account_group['account_group_type'],
                             font=FONTS['body'],
                             bg=row_bg,
                             fg=self.colors['text_primary'],
                             width=20,
                             anchor='w',
                             padx=SPACING['md'])
        type_label.pack(side=tk.LEFT, padx=SPACING['sm'])
        type_label.bind('<Enter>', on_enter)
        type_label.bind('<Leave>', on_leave)

        # AG Code
        code_label = tk.Label(row_frame, text=account_group['ag_code'],
                             font=FONTS['body_bold'],
                             bg=row_bg,
                             fg=self.colors['primary'],
                             width=10,
                             anchor='w',
                             padx=SPACING['md'])
        code_label.pack(side=tk.LEFT, padx=SPACING['sm'])
        code_label.bind('<Enter>', on_enter)
        code_label.bind('<Leave>', on_leave)

        # Status
        status_color = self.colors['success'] if account_group['status'] == 'Active' else self.colors['error']
        status_label = tk.Label(row_frame,
                               text=account_group['status'],
                               font=FONTS['body_bold'],
                               bg=row_bg,
                               fg=status_color,
                               width=8,
                               anchor='w',
                               padx=SPACING['md'])
        status_label.pack(side=tk.LEFT, padx=SPACING['sm'])
        status_label.bind('<Enter>', on_enter)
        status_label.bind('<Leave>', on_leave)

        # Edit button
        edit_btn = tk.Button(row_frame,
                            text="Edit",
                            font=FONTS['small_bold'],
                            bg=self.colors['primary'],
                            fg='white',
                            activebackground=self.colors['primary_hover'],
                            activeforeground='white',
                            cursor='hand2',
                            relief=tk.FLAT,
                            width=6,
                            padx=SPACING['sm'],
                            pady=SPACING['xs'],
                            command=lambda: self.show_edit_form(account_group['id']))
        edit_btn.pack(side=tk.LEFT, padx=SPACING['md'])

        # Hover effect for edit button
        def on_btn_enter(e):
            edit_btn.config(bg=self.colors['primary_hover'])
        def on_btn_leave(e):
            edit_btn.config(bg=self.colors['primary'])

        edit_btn.bind('<Enter>', on_btn_enter)
        edit_btn.bind('<Leave>', on_btn_leave)

    def show_create_form(self):
        """Show the create account group form"""
        self.current_view = 'form'
        self.edit_account_group_id = None

        # Hide create button and change title
        self.create_btn.pack_forget()
        self.title_label.config(text="Create New Account Group")

        # Show form
        from account_group_form import AccountGroupForm
        self.show_form(None)

    def show_edit_form(self, account_group_id):
        """Show the edit account group form"""
        self.current_view = 'form'
        self.edit_account_group_id = account_group_id

        # Hide create button and change title
        self.create_btn.pack_forget()
        self.title_label.config(text="Edit Account Group")

        # Get account group data
        account_group_data = self.account_group_handler.get_account_group_by_id(account_group_id)

        if not account_group_data:
            messagebox.showerror("Error", "Account Group not found")
            self.show_list_view()
            return

        # Show form
        self.show_form(account_group_data)

    def show_form(self, account_group_data):
        """Show account group form (create or edit)"""
        # Clear content container
        for widget in self.content_container.winfo_children():
            widget.destroy()

        # Import and create form
        from account_group_form import AccountGroupForm

        form = AccountGroupForm(
            self.content_container,
            self.colors,
            self.account_group_handler,
            account_group_data,
            self.on_form_save,
            self.on_form_cancel
        )
        form.pack(fill=tk.BOTH, expand=True)

    def on_form_save(self):
        """Callback when form is saved"""
        self.show_list_view()
        self.load_account_groups()

    def on_form_cancel(self):
        """Callback when form is cancelled"""
        self.show_list_view()

    def show_list_view(self):
        """Show the list view"""
        self.current_view = 'list'
        self.edit_account_group_id = None

        # Show create button and restore title
        self.create_btn.pack(side=tk.RIGHT)
        self.title_label.config(text="Account Group Master")

        # Recreate table view
        self.create_table_view()
        self.load_account_groups()

    def __del__(self):
        """Cleanup when widget is destroyed"""
        if hasattr(self, 'account_group_handler'):
            self.account_group_handler.disconnect()
