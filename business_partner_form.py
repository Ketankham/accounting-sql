"""
Business Partner Form - Create and Edit Business Partner
"""

import tkinter as tk
from tkinter import ttk, messagebox
from ui_config import COLORS, FONTS, SPACING, LAYOUT


class BusinessPartnerForm(tk.Frame):
    def __init__(self, parent, colors, bp_handler, bp_data, on_save, on_cancel):
        super().__init__(parent, bg=COLORS['background'])
        self.colors = COLORS
        self.bp_handler = bp_handler
        self.bp_data = bp_data
        self.on_save_callback = on_save
        self.on_cancel_callback = on_cancel

        self.is_edit_mode = bp_data is not None

        # Form data
        self.form_vars = {}

        # Dropdown data
        self.account_groups = []
        self.book_codes = []
        self.account_types = []
        self.cities = []
        self.states = []

        # Create UI
        self.create_widgets()

        # Load data if edit mode
        if self.is_edit_mode:
            self.load_bp_data()

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

        # --- BP Code (Read-only in edit mode, hidden in create mode) ---
        if self.is_edit_mode:
            self.create_readonly_field(form_container, "BP Code", "bp_code", row=current_row)
            current_row += 2

        # --- Business Partner Name (*) ---
        self.create_field(form_container, "Business Partner Name", "bp_name",
                         placeholder="e.g., ABC Company Pvt Ltd", required=True, row=current_row)
        current_row += 2

        # --- Bill To Address ---
        self.create_textarea(form_container, "Bill To Address", "bill_to_address",
                           placeholder="Enter billing address", row=current_row)
        current_row += 2

        # --- Ship To Address ---
        self.create_textarea(form_container, "Ship To Address", "ship_to_address",
                           placeholder="Enter shipping address", row=current_row)
        current_row += 2

        # --- City (*) ---
        self.cities = self.bp_handler.get_active_cities()
        city_values = [f"{city['name']} ({city['city_code']})" for city in self.cities]
        self.create_dropdown(form_container, "City", "city",
                            city_values, required=True, row=current_row)
        current_row += 2

        # --- State (*) ---
        self.states = self.bp_handler.get_active_states()
        state_values = [f"{state['name']} ({state['state_code']})" for state in self.states]
        self.create_dropdown(form_container, "State", "state",
                            state_values, required=True, row=current_row)
        current_row += 2

        # --- Mobile ---
        self.create_field(form_container, "Mobile", "mobile",
                         placeholder="Enter 10-digit mobile number", row=current_row)
        current_row += 2

        # --- Account Group (*) ---
        self.account_groups = self.bp_handler.get_active_account_groups()
        account_group_values = [f"{ag['name']} ({ag['ag_code']})" for ag in self.account_groups]
        self.create_dropdown(form_container, "Account Group", "account_group",
                            account_group_values, required=True, row=current_row)
        current_row += 2

        # --- Book Code (*) ---
        self.book_codes = self.bp_handler.get_active_book_codes()
        book_code_values = [f"{bc['book_number']}-{bc['name']}" for bc in self.book_codes]
        self.create_dropdown(form_container, "Book Code", "book_code",
                            book_code_values, required=True, row=current_row)
        current_row += 2

        # --- Account Type (*) ---
        self.account_types = self.bp_handler.get_active_account_types()
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

        # Add info text about BP code generation
        if not self.is_edit_mode:
            info_frame = tk.Frame(form_container, bg='#F5F5F5', relief=tk.FLAT, borderwidth=0)
            info_frame.grid(row=current_row, column=0, sticky=tk.EW, pady=(0, SPACING['lg']))

            info_label = tk.Label(info_frame,
                                 text="ℹ BP Code will be auto-generated based on Business Partner Name and Account Group",
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
                            text="Create Business Partner" if not self.is_edit_mode else "Update Business Partner")
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

    def create_textarea(self, parent, label_text, field_name, placeholder="", row=0):
        """Create a textarea field"""
        # Label
        label = tk.Label(parent,
                        text=label_text,
                        font=FONTS['body_bold'],
                        bg=self.colors['background'],
                        fg=self.colors['text_primary'],
                        anchor='w')
        label.grid(row=row, column=0, sticky=tk.W, pady=(0, SPACING['sm']))

        # Text widget
        text_widget = tk.Text(parent,
                             font=FONTS['body'],
                             relief=tk.SOLID,
                             borderwidth=1,
                             height=3,
                             wrap=tk.WORD)
        text_widget.grid(row=row+1, column=0, sticky=tk.EW, pady=(0, SPACING['lg']))

        # Placeholder behavior
        if placeholder:
            text_widget.insert('1.0', placeholder)
            text_widget.config(fg=self.colors['text_tertiary'])

            def on_focus_in(event):
                if text_widget.get('1.0', 'end-1c') == placeholder:
                    text_widget.delete('1.0', tk.END)
                    text_widget.config(fg=self.colors['text_primary'])

            def on_focus_out(event):
                if not text_widget.get('1.0', 'end-1c'):
                    text_widget.insert('1.0', placeholder)
                    text_widget.config(fg=self.colors['text_tertiary'])

            text_widget.bind('<FocusIn>', on_focus_in)
            text_widget.bind('<FocusOut>', on_focus_out)

        # Store reference
        self.form_vars[field_name] = {
            'widget': text_widget,
            'type': 'textarea',
            'placeholder': placeholder,
            'required': False
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

        # Validate numeric input (allow decimals)
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

    def load_bp_data(self):
        """Load existing business partner data into form"""
        if not self.bp_data:
            return

        # BP Code
        if 'bp_code' in self.bp_data and 'bp_code' in self.form_vars:
            self.form_vars['bp_code']['var'].set(self.bp_data['bp_code'])

        # BP Name
        if 'bp_name' in self.bp_data:
            self.form_vars['bp_name']['var'].set(self.bp_data['bp_name'])
            self.form_vars['bp_name']['widget'].config(fg=self.colors['text_primary'])

        # Bill To Address
        if 'bill_to_address' in self.bp_data and self.bp_data['bill_to_address']:
            self.form_vars['bill_to_address']['widget'].delete('1.0', tk.END)
            self.form_vars['bill_to_address']['widget'].insert('1.0', self.bp_data['bill_to_address'])
            self.form_vars['bill_to_address']['widget'].config(fg=self.colors['text_primary'])

        # Ship To Address
        if 'ship_to_address' in self.bp_data and self.bp_data['ship_to_address']:
            self.form_vars['ship_to_address']['widget'].delete('1.0', tk.END)
            self.form_vars['ship_to_address']['widget'].insert('1.0', self.bp_data['ship_to_address'])
            self.form_vars['ship_to_address']['widget'].config(fg=self.colors['text_primary'])

        # City
        if 'city_id' in self.bp_data and self.bp_data['city_id']:
            for city in self.cities:
                if city['id'] == self.bp_data['city_id']:
                    self.form_vars['city']['var'].set(f"{city['name']} ({city['city_code']})")
                    break

        # State
        if 'state_id' in self.bp_data and self.bp_data['state_id']:
            for state in self.states:
                if state['id'] == self.bp_data['state_id']:
                    self.form_vars['state']['var'].set(f"{state['name']} ({state['state_code']})")
                    break

        # Mobile
        if 'mobile' in self.bp_data and self.bp_data['mobile']:
            self.form_vars['mobile']['var'].set(self.bp_data['mobile'])
            self.form_vars['mobile']['widget'].config(fg=self.colors['text_primary'])

        # Account Group
        if 'account_group_id' in self.bp_data:
            for ag in self.account_groups:
                if ag['id'] == self.bp_data['account_group_id']:
                    self.form_vars['account_group']['var'].set(f"{ag['name']} ({ag['ag_code']})")
                    break

        # Book Code
        if 'book_code_id' in self.bp_data:
            for bc in self.book_codes:
                if bc['id'] == self.bp_data['book_code_id']:
                    self.form_vars['book_code']['var'].set(f"{bc['book_number']}-{bc['name']}")
                    break

        # Account Type
        if 'account_type_id' in self.bp_data:
            for at in self.account_types:
                if at['id'] == self.bp_data['account_type_id']:
                    self.form_vars['account_type']['var'].set(f"{at['code']} - {at['name']}")
                    break

        # Opening Balance
        if 'opening_balance' in self.bp_data:
            self.form_vars['opening_balance']['var'].set(str(self.bp_data['opening_balance']))

        # Balance Type
        if 'balance_type' in self.bp_data:
            self.form_vars['balance_type']['var'].set(self.bp_data['balance_type'])

        # Status
        if 'status' in self.bp_data:
            self.form_vars['status']['var'].set(self.bp_data['status'])

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

        # BP Name
        data['bp_name'] = self.form_vars['bp_name']['var'].get()

        # Bill To Address
        bill_to_text = self.form_vars['bill_to_address']['widget'].get('1.0', 'end-1c')
        placeholder = self.form_vars['bill_to_address']['placeholder']
        data['bill_to_address'] = bill_to_text if bill_to_text != placeholder else ''

        # Ship To Address
        ship_to_text = self.form_vars['ship_to_address']['widget'].get('1.0', 'end-1c')
        placeholder = self.form_vars['ship_to_address']['placeholder']
        data['ship_to_address'] = ship_to_text if ship_to_text != placeholder else ''

        # City (extract ID)
        city_display = self.form_vars['city']['var'].get()
        for city in self.cities:
            if f"{city['name']} ({city['city_code']})" == city_display:
                data['city_id'] = city['id']
                break

        # State (extract ID)
        state_display = self.form_vars['state']['var'].get()
        for state in self.states:
            if f"{state['name']} ({state['state_code']})" == state_display:
                data['state_id'] = state['id']
                break

        # Mobile
        mobile = self.form_vars['mobile']['var'].get()
        placeholder = self.form_vars['mobile']['placeholder']
        data['mobile'] = mobile if mobile != placeholder else ''

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
            success, message = self.bp_handler.update_business_partner(
                self.bp_data['id'],
                data
            )
        else:
            success, message, bp_id = self.bp_handler.create_business_partner(data)

        if success:
            messagebox.showinfo("Success", message)
            self.on_save_callback()
        else:
            messagebox.showerror("Error", message)

    def handle_cancel(self):
        """Handle cancel/back button click"""
        self.on_cancel_callback()
