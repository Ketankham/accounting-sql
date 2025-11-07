"""
Account Master Form - Create and Edit Account Master
"""

import tkinter as tk
from tkinter import ttk, messagebox
from ui_config import COLORS, FONTS, SPACING, LAYOUT


class AccountMasterForm(tk.Frame):
    def __init__(self, parent, colors, account_master_handler, account_data, on_save, on_cancel, on_delete=None):
        super().__init__(parent, bg=COLORS['background'])
        self.colors = COLORS
        self.account_master_handler = account_master_handler
        self.account_data = account_data
        self.on_save_callback = on_save
        self.on_cancel_callback = on_cancel
        self.on_delete_callback = on_delete  # Delete callback for edit mode

        self.is_edit_mode = account_data is not None

        # Form data
        self.form_vars = {}

        # Dropdown data
        self.account_groups = []
        self.book_codes = []
        self.account_types = []

        # Create UI
        self.create_widgets()

        # Load data if edit mode
        if self.is_edit_mode:
            self.load_account_data()

    def create_widgets(self):
        """Create the form UI"""
        # Main container with canvas for scrolling
        main_container = tk.Frame(self, bg=self.colors['background'])
        main_container.pack(fill=tk.BOTH, expand=True)

        # Create canvas and scrollbar for scrollable form
        canvas = tk.Canvas(main_container, bg=self.colors['background'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_container, orient="vertical", command=canvas.yview)

        # Scrollable frame inside canvas
        scrollable_frame = tk.Frame(canvas, bg=self.colors['background'])

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        # Create canvas window with width binding
        canvas_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        # Bind canvas width to scrollable_frame width
        def on_canvas_configure(event):
            canvas.itemconfig(canvas_window, width=event.width)
        canvas.bind("<Configure>", on_canvas_configure)

        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Mousewheel scrolling
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        canvas.bind("<Enter>", lambda e: canvas.bind_all("<MouseWheel>", _on_mousewheel))
        canvas.bind("<Leave>", lambda e: canvas.unbind_all("<MouseWheel>"))

        # Form content inside scrollable frame
        form_container = tk.Frame(scrollable_frame, bg=self.colors['background'])
        form_container.pack(fill=tk.BOTH, expand=True, padx=SPACING['xxl'], pady=SPACING['xl'])

        # Single column layout
        form_container.grid_columnconfigure(0, weight=1)

        current_row = 0

        # --- Account Name (*) ---
        self.create_field(form_container, "Account Name", "account_name",
                         placeholder="e.g., Cash in Hand, Bank Account", required=True, row=current_row)
        current_row += 2

        # --- Account Group (*) ---
        self.account_groups = self.account_master_handler.get_active_account_groups()
        account_group_values = [f"{ag['name']} ({ag['ag_code']})" for ag in self.account_groups]
        self.create_dropdown(form_container, "Account Group", "account_group",
                            account_group_values, required=True, row=current_row)
        current_row += 2

        # --- Book Code (*) ---
        self.book_codes = self.account_master_handler.get_active_book_codes()
        book_code_values = [f"{bc['book_number']}-{bc['name']}" for bc in self.book_codes]
        self.create_dropdown(form_container, "Book Code", "book_code",
                            book_code_values, required=True, row=current_row)
        current_row += 2

        # --- Account Type (*) ---
        self.account_types = self.account_master_handler.get_active_account_types()
        account_type_values = [f"{at['code']} - {at['name']}" for at in self.account_types]
        self.create_dropdown(form_container, "Account Type", "account_type",
                            account_type_values, required=True, row=current_row)
        current_row += 2

        # --- Opening Balance and Balance Type (on same line) (*) ---
        self.create_opening_balance_field(form_container, current_row)
        current_row += 2

        # --- Status (*) ---
        self.create_dropdown(form_container, "Status", "status",
                            ["Active", "Inactive"], required=True, row=current_row)
        current_row += 2

        # --- Account Code (Read-only in edit mode, hidden in create mode) ---
        if self.is_edit_mode:
            self.create_readonly_field(form_container, "Account Code", "account_code", row=current_row)
            current_row += 2

        # Add info text about Account code generation
        if not self.is_edit_mode:
            info_frame = tk.Frame(form_container, bg='#F5F5F5', relief=tk.FLAT, borderwidth=0)
            info_frame.grid(row=current_row, column=0, sticky=tk.EW, pady=(0, SPACING['lg']))

            info_label = tk.Label(info_frame,
                                 text="ℹ Account Code will be auto-generated based on Account Name and Account Group",
                                 font=FONTS['small_italic'],
                                 bg='#F5F5F5',
                                 fg='#6B7280',
                                 anchor='w',
                                 padx=SPACING['md'],
                                 pady=SPACING['md'])
            info_label.pack(fill=tk.X)
            current_row += 2

        # --- BUTTONS (inside scrollable area) ---
        button_frame = tk.Frame(scrollable_frame, bg=self.colors['background'])
        button_frame.pack(fill=tk.X, padx=SPACING['xxl'], pady=(SPACING['lg'], SPACING['xl']))

        # Save button (left side)
        save_btn = tk.Button(button_frame,
                            text="Create Account" if not self.is_edit_mode else "Update Account")
        save_btn.config(
            font=FONTS['button'],
            bg=self.colors['primary'],
            fg='white',
            activebackground=self.colors['primary_hover'],
            activeforeground='white',
            cursor='hand2',
            relief=tk.FLAT,
            padx=SPACING['xl'],
            pady=SPACING['md'],
            command=self.handle_save
        )
        save_btn.pack(side=tk.LEFT, padx=(0, SPACING['md']))

        # Add hover effect
        save_btn.bind('<Enter>', lambda e: save_btn.config(bg=self.colors['primary_hover']))
        save_btn.bind('<Leave>', lambda e: save_btn.config(bg=self.colors['primary']))

        # Delete button (middle - only in edit mode)
        if self.is_edit_mode and self.on_delete_callback:
            delete_btn = tk.Button(button_frame,
                                  text="Delete Account")
            delete_btn.config(
                font=FONTS['button'],
                bg='#EF4444',
                fg='white',
                activebackground='#DC2626',
                activeforeground='white',
                cursor='hand2',
                relief=tk.FLAT,
                padx=SPACING['xl'],
                pady=SPACING['md'],
                command=self.handle_delete
            )
            delete_btn.pack(side=tk.LEFT, padx=(0, SPACING['md']))

            # Add hover effect
            delete_btn.bind('<Enter>', lambda _e: delete_btn.config(bg='#DC2626'))
            delete_btn.bind('<Leave>', lambda _e: delete_btn.config(bg='#EF4444'))

        # Back button (right side)
        back_btn = tk.Button(button_frame,
                            text="Back")
        back_btn.config(
            font=FONTS['button'],
            bg=self.colors['surface'],
            fg=self.colors['text_primary'],
            activebackground=self.colors['border'],
            activeforeground=self.colors['text_primary'],
            cursor='hand2',
            relief=tk.FLAT,
            padx=SPACING['xl'],
            pady=SPACING['md'],
            command=self.handle_cancel
        )
        back_btn.pack(side=tk.RIGHT)

    def create_field(self, parent, label_text, field_name, placeholder="", required=False, row=0):
        """Create a text input field"""
        # Label
        label = tk.Label(parent,
                        text=label_text + (" *" if required else ""),
                        font=FONTS['body_bold'],
                        bg=self.colors['background'],
                        fg=self.colors['text_primary'],
                        anchor='w')
        label.grid(row=row, column=0, sticky=tk.W, pady=(0, SPACING['sm']))

        # Entry
        var = tk.StringVar()
        entry = tk.Entry(parent,
                        textvariable=var,
                        font=FONTS['body'],
                        relief=tk.SOLID,
                        borderwidth=1)
        entry.grid(row=row+1, column=0, sticky=tk.EW, ipady=SPACING['sm'], pady=(0, SPACING['lg']))

        # Placeholder behavior
        if placeholder:
            var.set(placeholder)
            entry.config(fg=self.colors['text_tertiary'])

            def on_focus_in(event):
                if var.get() == placeholder:
                    var.set('')
                    entry.config(fg=self.colors['text_primary'])

            def on_focus_out(event):
                if not var.get():
                    var.set(placeholder)
                    entry.config(fg=self.colors['text_tertiary'])

            entry.bind('<FocusIn>', on_focus_in)
            entry.bind('<FocusOut>', on_focus_out)

        # Store reference
        self.form_vars[field_name] = {
            'var': var,
            'widget': entry,
            'type': 'entry',
            'placeholder': placeholder,
            'required': required
        }

    def create_readonly_field(self, parent, label_text, field_name, row=0):
        """Create a read-only text field"""
        # Label
        label = tk.Label(parent,
                        text=label_text,
                        font=FONTS['body_bold'],
                        bg=self.colors['background'],
                        fg=self.colors['text_primary'],
                        anchor='w')
        label.grid(row=row, column=0, sticky=tk.W, pady=(0, SPACING['sm']))

        # Entry (read-only)
        var = tk.StringVar()
        entry = tk.Entry(parent,
                        textvariable=var,
                        font=FONTS['body'],
                        relief=tk.SOLID,
                        borderwidth=1,
                        state='readonly')
        entry.grid(row=row+1, column=0, sticky=tk.EW, ipady=SPACING['sm'], pady=(0, SPACING['lg']))

        # Store reference
        self.form_vars[field_name] = {
            'var': var,
            'widget': entry,
            'type': 'readonly',
            'required': False
        }

    def create_dropdown(self, parent, label_text, field_name, values, required=False, row=0):
        """Create a dropdown field"""
        # Label
        label = tk.Label(parent,
                        text=label_text + (" *" if required else ""),
                        font=FONTS['body_bold'],
                        bg=self.colors['background'],
                        fg=self.colors['text_primary'],
                        anchor='w')
        label.grid(row=row, column=0, sticky=tk.W, pady=(0, SPACING['sm']))

        # Combobox
        var = tk.StringVar()
        combo = ttk.Combobox(parent,
                            textvariable=var,
                            font=FONTS['body'],
                            state="readonly",
                            values=values)
        combo.grid(row=row+1, column=0, sticky=tk.EW, ipady=SPACING['sm'], pady=(0, SPACING['lg']))

        # Set default value
        if field_name == 'status':
            var.set('Active')
        else:
            var.set(f"Select {label_text}")

        # Store reference
        self.form_vars[field_name] = {
            'var': var,
            'widget': combo,
            'type': 'dropdown',
            'placeholder': f"Select {label_text}",
            'required': required
        }

    def create_opening_balance_field(self, parent, row):
        """Create opening balance field with amount and balance type on same line"""
        # Label
        label = tk.Label(parent,
                        text="Opening Balance *",
                        font=FONTS['body_bold'],
                        bg=self.colors['background'],
                        fg=self.colors['text_primary'],
                        anchor='w')
        label.grid(row=row, column=0, sticky=tk.W, pady=(0, SPACING['sm']))

        # Container for amount and balance type
        container = tk.Frame(parent, bg=self.colors['background'])
        container.grid(row=row+1, column=0, sticky=tk.EW, pady=(0, SPACING['lg']))
        container.grid_columnconfigure(0, weight=2)
        container.grid_columnconfigure(1, weight=1)

        # Amount entry
        amount_var = tk.StringVar(value="0")
        amount_entry = tk.Entry(container,
                               textvariable=amount_var,
                               font=FONTS['body'],
                               relief=tk.SOLID,
                               borderwidth=1)
        amount_entry.grid(row=0, column=0, sticky=tk.EW, ipady=SPACING['sm'], padx=(0, SPACING['md']))

        # Validate numeric input
        def validate_numeric(text):
            if text == "":
                return True
            try:
                float(text)
                return True
            except ValueError:
                return False

        vcmd = (self.register(validate_numeric), '%P')
        amount_entry.config(validate='key', validatecommand=vcmd)

        # Balance type dropdown
        balance_type_var = tk.StringVar(value="Debit")
        balance_type_combo = ttk.Combobox(container,
                                         textvariable=balance_type_var,
                                         font=FONTS['body'],
                                         state="readonly",
                                         values=["Credit", "Debit"])
        balance_type_combo.grid(row=0, column=1, sticky=tk.EW, ipady=SPACING['sm'])

        # Store references
        self.form_vars['opening_balance'] = {
            'var': amount_var,
            'widget': amount_entry,
            'type': 'entry',
            'placeholder': '',
            'required': True
        }

        self.form_vars['balance_type'] = {
            'var': balance_type_var,
            'widget': balance_type_combo,
            'type': 'dropdown',
            'placeholder': '',
            'required': True
        }

    def load_account_data(self):
        """Load existing account data into form"""
        if not self.account_data:
            return

        # Account Name
        if 'account_name' in self.account_data:
            self.form_vars['account_name']['var'].set(self.account_data['account_name'])
            self.form_vars['account_name']['widget'].config(fg=self.colors['text_primary'])

        # Account Group
        if 'account_group_id' in self.account_data:
            for ag in self.account_groups:
                if ag['id'] == self.account_data['account_group_id']:
                    self.form_vars['account_group']['var'].set(f"{ag['name']} ({ag['ag_code']})")
                    break

        # Book Code
        if 'book_code_id' in self.account_data:
            for bc in self.book_codes:
                if bc['id'] == self.account_data['book_code_id']:
                    self.form_vars['book_code']['var'].set(f"{bc['book_number']}-{bc['name']}")
                    break

        # Account Type
        if 'account_type_id' in self.account_data:
            for at in self.account_types:
                if at['id'] == self.account_data['account_type_id']:
                    self.form_vars['account_type']['var'].set(f"{at['code']} - {at['name']}")
                    break

        # Opening Balance
        if 'opening_balance' in self.account_data:
            self.form_vars['opening_balance']['var'].set(str(self.account_data['opening_balance']))

        # Balance Type
        if 'balance_type' in self.account_data:
            self.form_vars['balance_type']['var'].set(self.account_data['balance_type'])

        # Status
        if 'status' in self.account_data:
            self.form_vars['status']['var'].set(self.account_data['status'])

        # Account Code (readonly)
        if 'account_code' in self.account_data:
            self.form_vars['account_code']['var'].set(self.account_data['account_code'])

    def validate_form(self):
        """Validate form data"""
        errors = []

        for field_name, field_info in self.form_vars.items():
            if field_info.get('required'):
                if field_info['type'] == 'entry':
                    value = field_info['var'].get()
                    placeholder = field_info.get('placeholder', '')
                    if not value or value == placeholder:
                        label_text = field_name.replace('_', ' ').title()
                        errors.append(f"{label_text} is required")

                elif field_info['type'] == 'dropdown':
                    value = field_info['var'].get()
                    placeholder = field_info.get('placeholder', '')
                    if not value or value == placeholder or value.startswith('Select'):
                        label_text = field_name.replace('_', ' ').title()
                        errors.append(f"{label_text} is required")

        if errors:
            messagebox.showerror("Validation Error", "\n".join(errors))
            return False

        return True

    def get_form_data(self):
        """Get all form data"""
        data = {}

        # Account Name
        data['account_name'] = self.form_vars['account_name']['var'].get()

        # Account Group (extract ID)
        account_group_display = self.form_vars['account_group']['var'].get()
        for ag in self.account_groups:
            if f"{ag['name']} ({ag['ag_code']})" == account_group_display:
                data['account_group_id'] = ag['id']
                break

        # Book Code (extract ID from numbered format: 1-Cash, 2-Bank, etc)
        book_code_display = self.form_vars['book_code']['var'].get()
        for bc in self.book_codes:
            if f"{bc['book_number']}-{bc['name']}" == book_code_display:
                data['book_code_id'] = bc['id']
                break

        # Account Type (extract ID)
        account_type_display = self.form_vars['account_type']['var'].get()
        for at in self.account_types:
            if f"{at['code']} - {at['name']}" == account_type_display:
                data['account_type_id'] = at['id']
                break

        # Opening Balance
        try:
            data['opening_balance'] = float(self.form_vars['opening_balance']['var'].get())
        except ValueError:
            data['opening_balance'] = 0

        # Balance Type
        data['balance_type'] = self.form_vars['balance_type']['var'].get()

        # Status
        data['status'] = self.form_vars['status']['var'].get()

        return data

    def handle_save(self):
        """Handle save button click"""
        # Validate form
        if not self.validate_form():
            return

        # Get form data
        data = self.get_form_data()

        # Save to database
        if self.is_edit_mode:
            success, message = self.account_master_handler.update_account(
                self.account_data['id'],
                data
            )
        else:
            success, message, account_id = self.account_master_handler.create_account(data)

        if success:
            messagebox.showinfo("Success", message)
            self.on_save_callback()
        else:
            messagebox.showerror("Error", message)

    def handle_delete(self):
        """Handle delete button click"""
        if self.on_delete_callback and self.is_edit_mode:
            account_id = self.account_data['id']
            account_name = self.account_data['account_name']
            # Call the delete callback from management screen
            self.on_delete_callback(account_id, account_name)

    def handle_cancel(self):
        """Handle cancel/back button click"""
        self.on_cancel_callback()
