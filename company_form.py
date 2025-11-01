"""
Company Form - Create and Edit Company
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
from ui_config import COLORS, FONTS, SPACING, LAYOUT, INPUT_STYLES


class CompanyForm(tk.Frame):
    def __init__(self, parent, colors, company_handler, company_data, on_save, on_cancel):
        super().__init__(parent, bg=COLORS['background'])
        self.colors = COLORS  # Use unified colors
        self.company_handler = company_handler
        self.company_data = company_data
        self.on_save_callback = on_save
        self.on_cancel_callback = on_cancel

        self.is_edit_mode = company_data is not None

        # Form data
        self.form_vars = {}

        # Create UI
        self.create_widgets()

        # Load data if edit mode
        if self.is_edit_mode:
            self.load_company_data()

    def create_widgets(self):
        """Create the form UI"""
        # Scrollable form container
        canvas = tk.Canvas(self, bg=self.colors['background'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)

        form_container = tk.Frame(canvas, bg=self.colors['background'])

        form_container.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=form_container, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Enable mousewheel scrolling
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")

        canvas.bind_all("<MouseWheel>", _on_mousewheel)

        # Form content
        self.create_form_content(form_container)

    def create_form_content(self, parent):
        """Create form fields - all stacked vertically in single column"""
        # Form frame with padding
        form_frame = tk.Frame(parent, bg=self.colors['background'])
        form_frame.pack(fill=tk.BOTH, expand=True, padx=SPACING['xxl'], pady=SPACING['xl'])

        # Single column layout - all fields stacked vertically
        form_frame.grid_columnconfigure(0, weight=1)

        current_row = 0

        # --- Company Code ---
        self.create_field(form_frame, "Company Code", "company_code",
                         placeholder="e.g., COMP-001", required=True, row=current_row)
        current_row += 2

        # --- Company Name ---
        self.create_field(form_frame, "Company Name", "company_name",
                         placeholder="Enter company name", required=True, row=current_row)
        current_row += 2

        # --- GST Number ---
        self.create_field(form_frame, "GST Number", "gst_number",
                         placeholder="Enter GST number", row=current_row)
        current_row += 2

        # --- PAN Number ---
        self.create_field(form_frame, "PAN Number", "pan_number",
                         placeholder="Enter PAN number", row=current_row)
        current_row += 2

        # --- Bill To Address ---
        self.create_textarea(form_frame, "Bill To Address", "bill_to_address",
                            placeholder="Enter billing address", row=current_row)
        current_row += 2

        # --- Ship To Address ---
        self.create_textarea(form_frame, "Ship To Address", "ship_to_address",
                            placeholder="Enter shipping address", row=current_row)
        current_row += 2

        # --- State ---
        self.create_dropdown(form_frame, "State", "state",
                            self.company_handler.get_states(), row=current_row)
        current_row += 2

        # --- City ---
        self.create_field(form_frame, "City", "city",
                         placeholder="Enter city", row=current_row)
        current_row += 2

        # --- Landline Number ---
        self.create_field(form_frame, "Landline Number", "landline_number",
                         placeholder="Enter landline number", row=current_row)
        current_row += 2

        # --- Mobile Number ---
        self.create_field(form_frame, "Mobile Number", "mobile_number",
                         placeholder="Enter mobile number", row=current_row)
        current_row += 2

        # --- Email Address ---
        self.create_field(form_frame, "Email Address", "email_address",
                         placeholder="Enter email address", row=current_row)
        current_row += 2

        # --- Website ---
        self.create_field(form_frame, "Website", "website",
                         placeholder="Enter website URL", row=current_row)
        current_row += 2

        # --- Logo Upload ---
        self.create_file_upload(form_frame, "Attach Logo", "logo_path", row=current_row)
        current_row += 2

        # --- Status ---
        self.create_dropdown(form_frame, "Status", "status",
                            ["Active", "Inactive"], row=current_row)
        current_row += 2

        # --- BUTTONS ---
        button_frame = tk.Frame(parent, bg=self.colors['background'])
        button_frame.pack(fill=tk.X, padx=SPACING['xxl'], pady=(SPACING['lg'], SPACING['xl']))

        # Save button
        save_btn = tk.Button(button_frame,
                            text="Save")
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

        # Cancel button
        cancel_btn = tk.Button(button_frame,
                              text="Cancel")
        cancel_btn.config(
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
        cancel_btn.pack(side=tk.LEFT, padx=(0, SPACING['md']))

        # Back to Main Menu link
        back_link = tk.Label(button_frame,
                            text="Back to Main Menu",
                            font=FONTS['body'],
                            fg=self.colors['primary'],
                            bg=self.colors['background'],
                            cursor='hand2')
        back_link.pack(side=tk.RIGHT)
        back_link.bind('<Button-1>', lambda e: self.handle_cancel())

    def create_field(self, parent, label_text, field_name, placeholder="", required=False, row=0):
        """Create a text input field - stacked vertically"""
        # Label
        label = tk.Label(parent,
                        text=label_text + (" *" if required else ""),
                        font=FONTS['body_bold'],
                        bg=self.colors['background'],
                        fg=self.colors['text_primary'],
                        anchor='w')
        label.grid(row=row, column=0, sticky=tk.W, pady=(0, SPACING['sm']))

        # Entry (with equal width)
        entry = ttk.Entry(parent, font=FONTS['body'])
        entry.grid(row=row+1, column=0, sticky=tk.EW, ipady=SPACING['md'], pady=(0, SPACING['lg']))

        # Placeholder
        if placeholder:
            entry.insert(0, placeholder)
            entry.config(foreground='gray')

            def on_focus_in(event):
                if entry.get() == placeholder:
                    entry.delete(0, tk.END)
                    entry.config(foreground='black')

            def on_focus_out(event):
                if not entry.get():
                    entry.insert(0, placeholder)
                    entry.config(foreground='gray')

            entry.bind('<FocusIn>', on_focus_in)
            entry.bind('<FocusOut>', on_focus_out)

        # Store reference
        self.form_vars[field_name] = {
            'widget': entry,
            'type': 'entry',
            'required': required
        }

    def create_textarea(self, parent, label_text, field_name, placeholder="", row=0):
        """Create a multiline text area - stacked vertically"""
        # Label
        label = tk.Label(parent,
                        text=label_text,
                        font=FONTS['body_bold'],
                        bg=self.colors['background'],
                        fg=self.colors['text_primary'],
                        anchor='w')
        label.grid(row=row, column=0, sticky=tk.W, pady=(0, SPACING['sm']))

        # Text widget (with equal width)
        text_widget = tk.Text(parent,
                             font=FONTS['body'],
                             height=4,
                             wrap=tk.WORD,
                             relief=tk.SOLID,
                             borderwidth=2,
                             padx=SPACING['sm'],
                             pady=SPACING['sm'])
        text_widget.grid(row=row+1, column=0, sticky=tk.EW, pady=(0, SPACING['lg']))

        # Placeholder
        if placeholder:
            text_widget.insert('1.0', placeholder)
            text_widget.config(foreground='gray')

            def on_focus_in(event):
                if text_widget.get('1.0', tk.END).strip() == placeholder:
                    text_widget.delete('1.0', tk.END)
                    text_widget.config(foreground='black')

            def on_focus_out(event):
                if not text_widget.get('1.0', tk.END).strip():
                    text_widget.insert('1.0', placeholder)
                    text_widget.config(foreground='gray')

            text_widget.bind('<FocusIn>', on_focus_in)
            text_widget.bind('<FocusOut>', on_focus_out)

        # Store reference
        self.form_vars[field_name] = {
            'widget': text_widget,
            'type': 'text'
        }

    def create_dropdown(self, parent, label_text, field_name, values, row=0):
        """Create a dropdown field - stacked vertically"""
        # Label
        label = tk.Label(parent,
                        text=label_text,
                        font=FONTS['body_bold'],
                        bg=self.colors['background'],
                        fg=self.colors['text_primary'],
                        anchor='w')
        label.grid(row=row, column=0, sticky=tk.W, pady=(0, SPACING['sm']))

        # Combobox (with equal width)
        combo = ttk.Combobox(parent,
                            font=FONTS['body'],
                            state="readonly" if values else "normal",
                            values=values)
        combo.grid(row=row+1, column=0, sticky=tk.EW, ipady=SPACING['md'], pady=(0, SPACING['lg']))

        if values:
            if field_name == 'status':
                combo.set('Active')
            else:
                combo.set(f"Select {label_text}")

        # Store reference
        self.form_vars[field_name] = {
            'widget': combo,
            'type': 'combobox'
        }

    def create_file_upload(self, parent, label_text, field_name, row=0):
        """Create a file upload field - stacked vertically"""
        # Label
        label = tk.Label(parent,
                        text=label_text,
                        font=FONTS['body_bold'],
                        bg=self.colors['background'],
                        fg=self.colors['text_primary'],
                        anchor='w')
        label.grid(row=row, column=0, sticky=tk.W, pady=(0, SPACING['sm']))

        # Upload frame (with equal width)
        upload_frame = tk.Frame(parent, bg=self.colors['background'], relief=tk.SOLID, borderwidth=2)
        upload_frame.grid(row=row+1, column=0, sticky=tk.EW, ipady=SPACING['md'], pady=(0, SPACING['lg']))
        upload_frame.grid_columnconfigure(0, weight=1)

        # File path label
        path_var = tk.StringVar(value="No file selected")
        path_label = tk.Label(upload_frame,
                             textvariable=path_var,
                             font=FONTS['body'],
                             bg=self.colors['background'],
                             fg=self.colors['text_tertiary'],
                             anchor='w',
                             padx=SPACING['md'])
        path_label.grid(row=0, column=0, sticky=tk.EW)

        # Browse button
        def browse_file():
            filename = filedialog.askopenfilename(
                title="Select Logo",
                filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif"), ("All files", "*.*")]
            )
            if filename:
                path_var.set(os.path.basename(filename))
                path_label.config(fg=self.colors['text_primary'])

        browse_btn = tk.Button(upload_frame,
                              text="Attach Logo")
        browse_btn.config(
            font=FONTS['small_bold'],
            bg=self.colors['surface'],
            fg=self.colors['text_primary'],
            activebackground=self.colors['border'],
            activeforeground=self.colors['text_primary'],
            cursor='hand2',
            relief=tk.FLAT,
            padx=SPACING['md'],
            pady=SPACING['sm'],
            command=browse_file
        )
        browse_btn.grid(row=0, column=1, padx=SPACING['sm'])

        # Store reference
        self.form_vars[field_name] = {
            'widget': path_var,
            'type': 'file',
            'path_label': path_label
        }

    def load_company_data(self):
        """Load existing company data into form"""
        if not self.company_data:
            return

        for field_name, field_info in self.form_vars.items():
            widget = field_info['widget']
            field_type = field_info['type']
            value = self.company_data.get(field_name, '')

            if value is None:
                value = ''

            if field_type == 'entry':
                # Clear placeholder first
                if widget.get() and widget.cget('foreground') == 'gray':
                    widget.delete(0, tk.END)
                    widget.config(foreground='black')
                widget.delete(0, tk.END)
                widget.insert(0, str(value))

            elif field_type == 'text':
                # Clear placeholder first
                current_text = widget.get('1.0', tk.END).strip()
                if current_text and widget.cget('foreground') == 'gray':
                    widget.delete('1.0', tk.END)
                    widget.config(foreground='black')
                widget.delete('1.0', tk.END)
                widget.insert('1.0', str(value))

            elif field_type == 'combobox':
                widget.set(str(value))

            elif field_type == 'file':
                if value:
                    widget.set(value)
                    field_info['path_label'].config(foreground='black')

    def get_form_data(self):
        """Get all form data"""
        data = {}

        for field_name, field_info in self.form_vars.items():
            widget = field_info['widget']
            field_type = field_info['type']

            if field_type == 'entry':
                value = widget.get()
                # Check if it's a placeholder
                if widget.cget('foreground') == 'gray':
                    value = ''
                data[field_name] = value.strip()

            elif field_type == 'text':
                value = widget.get('1.0', tk.END)
                # Check if it's a placeholder
                if widget.cget('foreground') == 'gray':
                    value = ''
                data[field_name] = value.strip()

            elif field_type == 'combobox':
                value = widget.get()
                # Check if it's a placeholder
                if value.startswith("Select"):
                    value = ''
                data[field_name] = value.strip()

            elif field_type == 'file':
                value = widget.get()
                if value == "No file selected":
                    value = ''
                data[field_name] = value

        return data

    def validate_form(self, data):
        """Validate form data"""
        # Check required fields
        if not data.get('company_code'):
            messagebox.showerror("Validation Error", "Company Code is required")
            return False

        if not data.get('company_name'):
            messagebox.showerror("Validation Error", "Company Name is required")
            return False

        return True

    def handle_save(self):
        """Handle save button click"""
        # Get form data
        data = self.get_form_data()

        # Validate
        if not self.validate_form(data):
            return

        # Save to database
        if self.is_edit_mode:
            # Update existing company
            success, message = self.company_handler.update_company(
                self.company_data['id'],
                data
            )
        else:
            # Create new company
            success, message, company_id = self.company_handler.create_company(data)

        if success:
            messagebox.showinfo("Success", message)
            self.on_save_callback()
        else:
            messagebox.showerror("Error", message)

    def handle_cancel(self):
        """Handle cancel button click"""
        result = messagebox.askyesno("Confirm",
                                     "Are you sure you want to cancel? Any unsaved changes will be lost.")
        if result:
            self.on_cancel_callback()