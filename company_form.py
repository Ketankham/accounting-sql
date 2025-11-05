"""
Company Form - Create and Edit Company (Scrollable with Canvas Width Binding)
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
from ui_config import COLORS, FONTS, SPACING, LAYOUT


class CompanyForm(tk.Frame):
    def __init__(self, parent, colors, company_handler, company_data, on_save, on_cancel):
        super().__init__(parent, bg=COLORS['background'])
        self.colors = COLORS
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
        """Create the form UI with scrollable canvas"""
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

        # CRITICAL FIX: Create canvas window with width binding (same fix as table view)
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

        # --- Company Code (*) ---
        self.create_field(form_container, "Company Code", "company_code",
                         placeholder="e.g., COMP001", required=True, row=current_row, max_length=20)
        current_row += 2

        # --- Company Name (*) ---
        self.create_field(form_container, "Company Name", "company_name",
                         placeholder="Enter company name", required=True, row=current_row)
        current_row += 2

        # --- Bill To Address (*) ---
        self.create_textarea(form_container, "Bill To Address", "bill_to_address",
                            placeholder="Enter billing address", required=True, row=current_row)
        current_row += 2

        # --- Ship To Address (*) ---
        self.create_textarea(form_container, "Ship To Address", "ship_to_address",
                            placeholder="Enter shipping address", required=True, row=current_row)
        current_row += 2

        # --- State (*) ---
        self.create_dropdown(form_container, "State", "state",
                            self.company_handler.get_states(), required=True, row=current_row)
        current_row += 2

        # --- City (*) ---
        self.create_field(form_container, "City", "city",
                         placeholder="Enter city", required=True, row=current_row)
        current_row += 2

        # --- GST Number (*) ---
        self.create_field(form_container, "GST Number", "gst_number",
                         placeholder="e.g., 22AAAAA0000A1Z5", required=True, row=current_row, max_length=15)
        current_row += 2

        # --- PAN Number (*) ---
        self.create_field(form_container, "PAN Number", "pan_number",
                         placeholder="e.g., AAAAA0000A", required=True, row=current_row, max_length=10)
        current_row += 2

        # --- Landline Number (Optional) ---
        self.create_field(form_container, "Landline Number", "landline_number",
                         placeholder="e.g., 022-12345678", row=current_row)
        current_row += 2

        # --- Mobile Number (Optional) ---
        self.create_field(form_container, "Mobile Number", "mobile_number",
                         placeholder="e.g., +91 9876543210", row=current_row)
        current_row += 2

        # --- Email Address (Optional) ---
        self.create_field(form_container, "Email Address", "email_address",
                         placeholder="e.g., info@company.com", row=current_row)
        current_row += 2

        # --- Website (Optional) ---
        self.create_field(form_container, "Website", "website",
                         placeholder="e.g., www.company.com", row=current_row)
        current_row += 2

        # --- Logo Path (*) ---
        self.create_file_upload(form_container, "Company Logo", "logo_path",
                               required=True, row=current_row)
        current_row += 2

        # --- Status (*) ---
        self.create_dropdown(form_container, "Status", "status",
                            ["Active", "Inactive"], required=True, row=current_row)
        current_row += 2

        # --- BUTTONS (inside scrollable area) ---
        button_frame = tk.Frame(scrollable_frame, bg=self.colors['background'])
        button_frame.pack(fill=tk.X, padx=SPACING['xxl'], pady=(SPACING['lg'], SPACING['xl']))

        # Save button (left side)
        save_btn = tk.Button(button_frame,
                            text="Create Company" if not self.is_edit_mode else "Update Company")
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

    def create_field(self, parent, label_text, field_name, placeholder="", required=False, row=0, max_length=None):
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

    def create_textarea(self, parent, label_text, field_name, placeholder="", required=False, row=0):
        """Create a multiline text area"""
        # Label
        label = tk.Label(parent,
                        text=label_text + (" *" if required else ""),
                        font=FONTS['body_bold'],
                        bg=self.colors['background'],
                        fg=self.colors['text_primary'],
                        anchor='w')
        label.grid(row=row, column=0, sticky=tk.W, pady=(0, SPACING['sm']))

        # Text widget
        text_widget = tk.Text(parent,
                             font=FONTS['body'],
                             height=3,
                             wrap=tk.WORD,
                             relief=tk.SOLID,
                             borderwidth=1,
                             padx=SPACING['sm'],
                             pady=SPACING['sm'])
        text_widget.grid(row=row+1, column=0, sticky=tk.EW, pady=(0, SPACING['lg']))

        # Placeholder behavior
        if placeholder:
            text_widget.insert('1.0', placeholder)
            text_widget.config(fg=self.colors['text_tertiary'])

            def on_focus_in(event):
                if text_widget.get('1.0', tk.END).strip() == placeholder:
                    text_widget.delete('1.0', tk.END)
                    text_widget.config(fg=self.colors['text_primary'])

            def on_focus_out(event):
                if not text_widget.get('1.0', tk.END).strip():
                    text_widget.insert('1.0', placeholder)
                    text_widget.config(fg=self.colors['text_tertiary'])

            text_widget.bind('<FocusIn>', on_focus_in)
            text_widget.bind('<FocusOut>', on_focus_out)

        # Store reference
        self.form_vars[field_name] = {
            'widget': text_widget,
            'type': 'text',
            'placeholder': placeholder,
            'required': required
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

    def create_file_upload(self, parent, label_text, field_name, required=False, row=0):
        """Create a file upload field"""
        # Label
        label = tk.Label(parent,
                        text=label_text + (" *" if required else ""),
                        font=FONTS['body_bold'],
                        bg=self.colors['background'],
                        fg=self.colors['text_primary'],
                        anchor='w')
        label.grid(row=row, column=0, sticky=tk.W, pady=(0, SPACING['sm']))

        # Upload frame
        upload_frame = tk.Frame(parent, bg=self.colors['surface'], relief=tk.SOLID, borderwidth=1)
        upload_frame.grid(row=row+1, column=0, sticky=tk.EW, pady=(0, SPACING['lg']))
        upload_frame.grid_columnconfigure(0, weight=1)

        # File path variable
        path_var = tk.StringVar(value="No file selected")

        # File path label
        path_label = tk.Label(upload_frame,
                             textvariable=path_var,
                             font=FONTS['body'],
                             bg=self.colors['surface'],
                             fg=self.colors['text_tertiary'],
                             anchor='w',
                             padx=SPACING['md'],
                             pady=SPACING['sm'])
        path_label.grid(row=0, column=0, sticky=tk.EW)

        # Browse button
        def browse_file():
            filename = filedialog.askopenfilename(
                title="Select Logo",
                filetypes=[("Image files", "*.png *.jpg *.jpeg *.gif"), ("All files", "*.*")]
            )
            if filename:
                path_var.set(filename)
                path_label.config(fg=self.colors['text_primary'])

        browse_btn = tk.Button(upload_frame,
                              text="Browse")
        browse_btn.config(
            font=FONTS['small_bold'],
            bg=self.colors['primary'],
            fg='white',
            activebackground=self.colors['primary_hover'],
            activeforeground='white',
            cursor='hand2',
            relief=tk.FLAT,
            padx=SPACING['md'],
            pady=SPACING['sm'],
            command=browse_file
        )
        browse_btn.grid(row=0, column=1, padx=SPACING['sm'], pady=SPACING['sm'])

        # Store reference
        self.form_vars[field_name] = {
            'var': path_var,
            'widget': path_label,
            'type': 'file',
            'required': required
        }

    def load_company_data(self):
        """Load existing company data into form"""
        if not self.company_data:
            return

        for field_name, field_info in self.form_vars.items():
            value = self.company_data.get(field_name, '')

            if value is None:
                value = ''

            if field_info['type'] == 'entry':
                # Entry field
                field_info['var'].set(value)
                # Only set fg color for tk.Entry, NOT for ttk.Combobox
                if isinstance(field_info['widget'], tk.Entry):
                    field_info['widget'].config(fg=self.colors['text_primary'])

            elif field_info['type'] == 'text':
                # Text area
                widget = field_info['widget']
                widget.delete('1.0', tk.END)
                widget.insert('1.0', value)
                widget.config(fg=self.colors['text_primary'])

            elif field_info['type'] == 'dropdown':
                # Dropdown
                field_info['var'].set(value if value else field_info.get('placeholder', ''))

            elif field_info['type'] == 'file':
                # File upload
                if value:
                    field_info['var'].set(value)
                    field_info['widget'].config(fg=self.colors['text_primary'])

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

                elif field_info['type'] == 'text':
                    value = field_info['widget'].get('1.0', tk.END).strip()
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

                elif field_info['type'] == 'file':
                    value = field_info['var'].get()
                    if not value or value == "No file selected":
                        label_text = field_name.replace('_', ' ').title()
                        errors.append(f"{label_text} is required")

        if errors:
            messagebox.showerror("Validation Error", "\n".join(errors))
            return False

        return True

    def get_form_data(self):
        """Get all form data"""
        data = {}

        for field_name, field_info in self.form_vars.items():
            if field_info['type'] == 'entry':
                value = field_info['var'].get()
                placeholder = field_info.get('placeholder', '')
                data[field_name] = value if value != placeholder else ''

            elif field_info['type'] == 'text':
                value = field_info['widget'].get('1.0', tk.END).strip()
                placeholder = field_info.get('placeholder', '')
                data[field_name] = value if value != placeholder else ''

            elif field_info['type'] == 'dropdown':
                value = field_info['var'].get()
                placeholder = field_info.get('placeholder', '')
                if value and not value.startswith('Select'):
                    data[field_name] = value
                else:
                    data[field_name] = ''

            elif field_info['type'] == 'file':
                value = field_info['var'].get()
                data[field_name] = value if value != "No file selected" else ''

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
            success, message = self.company_handler.update_company(
                self.company_data['id'],
                data
            )
        else:
            success, message, company_id = self.company_handler.create_company(data)

        if success:
            messagebox.showinfo("Success", message)
            self.on_save_callback()
        else:
            messagebox.showerror("Error", message)

    def handle_cancel(self):
        """Handle cancel/back button click"""
        self.on_cancel_callback()
