"""
UoM Form - Create and Edit Unit of Measure
"""

import tkinter as tk
from tkinter import ttk, messagebox
from ui_config import COLORS, FONTS, SPACING, LAYOUT


class UoMForm(tk.Frame):
    def __init__(self, parent, colors, uom_handler, uom_data, on_save, on_cancel):
        super().__init__(parent, bg=COLORS['background'])
        self.colors = COLORS
        self.uom_handler = uom_handler
        self.uom_data = uom_data
        self.on_save_callback = on_save
        self.on_cancel_callback = on_cancel

        self.is_edit_mode = uom_data is not None

        # Form data
        self.form_vars = {}

        # Create UI
        self.create_widgets()

        # Load data if edit mode
        if self.is_edit_mode:
            self.load_uom_data()

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

        # --- UoM Code (*) ---
        if not self.is_edit_mode:
            self.create_field(form_container, "UoM Code", "uom_code",
                             placeholder="e.g., KG, LTR, PCS (max 10 characters)", required=True, row=current_row)
        else:
            # Read-only in edit mode
            self.create_readonly_field(form_container, "UoM Code", "uom_code", row=current_row)
        current_row += 2

        # --- UoM Name (*) ---
        self.create_field(form_container, "UoM Name", "uom_name",
                         placeholder="e.g., Kilogram, Litre, Pieces", required=True, row=current_row)
        current_row += 2

        # --- Status (*) ---
        self.create_dropdown(form_container, "Status", "status",
                            ["Active", "Inactive"], required=True, row=current_row)
        current_row += 2

        # Add info text about code in create mode
        if not self.is_edit_mode:
            info_frame = tk.Frame(form_container, bg='#F5F5F5', relief=tk.FLAT, borderwidth=0)
            info_frame.grid(row=current_row, column=0, sticky=tk.EW, pady=(0, SPACING['lg']))

            info_label = tk.Label(info_frame,
                                 text="ℹ UoM Code must be alphanumeric and maximum 10 characters. Common examples: KG, LTR, MTR, PCS, NOS",
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
                            text="Create UoM" if not self.is_edit_mode else "Update UoM")
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

        # Validation for uom_code - max 10 characters
        if field_name == 'uom_code':
            def validate_length(new_value):
                return len(new_value) <= 10
            vcmd = (parent.register(validate_length), '%P')
            entry.config(validate='key', validatecommand=vcmd)

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

    def load_uom_data(self):
        """Load existing UoM data into form"""
        if not self.uom_data:
            return

        for field_name, field_info in self.form_vars.items():
            value = self.uom_data.get(field_name, '')

            if value is None:
                value = ''

            if field_info['type'] == 'entry':
                # Entry field
                field_info['var'].set(value)
                if isinstance(field_info['widget'], tk.Entry):
                    field_info['widget'].config(fg=self.colors['text_primary'])

            elif field_info['type'] == 'dropdown':
                # Dropdown
                field_info['var'].set(value if value else field_info.get('placeholder', ''))

            elif field_info['type'] == 'readonly':
                # Read-only field
                field_info['var'].set(value)

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
                    elif field_name == 'uom_code':
                        # Additional validation for UoM code
                        is_valid, message = self.uom_handler.validate_uom_code(value)
                        if not is_valid:
                            errors.append(message)

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

        for field_name, field_info in self.form_vars.items():
            # Skip readonly fields in edit mode
            if field_info['type'] == 'readonly':
                continue

            if field_info['type'] == 'entry':
                value = field_info['var'].get()
                placeholder = field_info.get('placeholder', '')
                data[field_name] = value if value != placeholder else ''

            elif field_info['type'] == 'dropdown':
                value = field_info['var'].get()
                placeholder = field_info.get('placeholder', '')
                if value and not value.startswith('Select'):
                    data[field_name] = value
                else:
                    data[field_name] = ''

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
            success, message = self.uom_handler.update_uom(
                self.uom_data['id'],
                data
            )
        else:
            success, message, uom_id = self.uom_handler.create_uom(data)

        if success:
            messagebox.showinfo("Success", message)
            self.on_save_callback()
        else:
            messagebox.showerror("Error", message)

    def handle_cancel(self):
        """Handle cancel/back button click"""
        self.on_cancel_callback()
