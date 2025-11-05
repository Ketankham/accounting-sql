"""
Financial Year Form - Create and Edit Financial Year
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from tkcalendar import DateEntry
from ui_config import COLORS, FONTS, SPACING, LAYOUT, INPUT_STYLES


class FinancialYearForm(tk.Frame):
    def __init__(self, parent, colors, fy_handler, fy_data, on_save, on_cancel):
        super().__init__(parent, bg=COLORS['background'])
        self.colors = COLORS
        self.fy_handler = fy_handler
        self.fy_data = fy_data
        self.on_save_callback = on_save
        self.on_cancel_callback = on_cancel

        self.is_edit_mode = fy_data is not None

        # Form data
        self.form_vars = {}

        # Create UI
        self.create_widgets()

        # Load data if edit mode
        if self.is_edit_mode:
            self.load_fy_data()

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

        # Create canvas window with width binding (same fix as table view)
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

        # --- Financial Year Code ---
        self.create_field(form_container, "FY Code", "fy_code",
                         placeholder="e.g., FY2425", required=True,
                         max_length=6, row=current_row)
        current_row += 2

        # --- Display Name ---
        self.create_field(form_container, "Display Name", "display_name",
                         placeholder="e.g., Financial year 2024-2025", required=True,
                         row=current_row)
        current_row += 2

        # --- Start Date ---
        self.create_date_field(form_container, "Start Date", "start_date",
                              required=True, row=current_row)
        current_row += 2

        # --- End Date ---
        self.create_date_field(form_container, "End Date", "end_date",
                              required=True, row=current_row)
        current_row += 2

        # --- Status ---
        self.create_dropdown(form_container, "Status", "status",
                            ["Active", "Inactive"], row=current_row)
        current_row += 2

        # --- BUTTONS (inside scrollable area) ---
        button_frame = tk.Frame(scrollable_frame, bg=self.colors['background'])
        button_frame.pack(fill=tk.X, padx=SPACING['xxl'], pady=(SPACING['lg'], SPACING['xl']))

        # Save button (left side)
        save_btn = tk.Button(button_frame,
                            text="Create Financial Year" if not self.is_edit_mode else "Update Financial Year")
        save_btn.config(
            font=FONTS['button'],
            bg=self.colors['primary'],
            fg='white',
            activebackground=self.colors['primary_hover'],
            activeforeground='white',
            cursor='hand2',
            relief=tk.FLAT,
            padx=SPACING['lg'],
            pady=SPACING['md'],
            command=self.handle_save
        )
        save_btn.pack(side=tk.LEFT)

        # Hover effect
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
            padx=SPACING['lg'],
            pady=SPACING['md'],
            command=self.handle_cancel
        )
        back_btn.pack(side=tk.RIGHT)

        # Hover effect
        back_btn.bind('<Enter>', lambda e: back_btn.config(bg=self.colors['border']))
        back_btn.bind('<Leave>', lambda e: back_btn.config(bg=self.colors['surface']))

    def create_field(self, parent, label_text, field_name, placeholder="", required=False, max_length=None, row=0):
        """Create a text input field"""
        # Label with required indicator
        label_display = f"{label_text} *" if required else label_text
        label = tk.Label(parent,
                        text=label_display,
                        font=FONTS['body_bold'],
                        bg=self.colors['background'],
                        fg=self.colors['text_primary'],
                        anchor='w')
        label.grid(row=row, column=0, sticky='w', pady=(SPACING['md'], SPACING['xs']))

        # Entry
        entry_var = tk.StringVar()
        entry = tk.Entry(parent,
                        textvariable=entry_var,
                        font=FONTS['body'],
                        bg='white',
                        fg=self.colors['text_primary'],
                        relief=tk.SOLID,
                        bd=1,
                        highlightthickness=2,
                        highlightcolor=self.colors['primary'],
                        highlightbackground=self.colors['border'])

        # Character limit validation
        if max_length:
            def validate_length(text):
                return len(text) <= max_length
            vcmd = (entry.register(validate_length), '%P')
            entry.config(validate='key', validatecommand=vcmd)

        entry.grid(row=row+1, column=0, sticky='ew', pady=(0, SPACING['md']))
        entry.insert(0, placeholder)
        entry.config(fg=self.colors['text_tertiary'])

        # Placeholder behavior
        def on_focus_in(event):
            if entry.get() == placeholder:
                entry.delete(0, tk.END)
                entry.config(fg=self.colors['text_primary'])

        def on_focus_out(event):
            if entry.get() == "":
                entry.insert(0, placeholder)
                entry.config(fg=self.colors['text_tertiary'])

        entry.bind('<FocusIn>', on_focus_in)
        entry.bind('<FocusOut>', on_focus_out)

        self.form_vars[field_name] = {
            'var': entry_var,
            'widget': entry,
            'required': required,
            'placeholder': placeholder
        }

    def create_date_field(self, parent, label_text, field_name, required=False, row=0):
        """Create a date picker field"""
        # Label with required indicator
        label_display = f"{label_text} *" if required else label_text
        label = tk.Label(parent,
                        text=label_display,
                        font=FONTS['body_bold'],
                        bg=self.colors['background'],
                        fg=self.colors['text_primary'],
                        anchor='w')
        label.grid(row=row, column=0, sticky='w', pady=(SPACING['md'], SPACING['xs']))

        # DateEntry widget with year/month selection
        from datetime import date
        date_entry = DateEntry(parent,
                              font=FONTS['body'],
                              bg='white',
                              fg=self.colors['text_primary'],
                              borderwidth=2,
                              date_pattern='yyyy-mm-dd',
                              state='normal',
                              year=datetime.now().year,
                              mindate=date(1900, 1, 1),
                              maxdate=date(2100, 12, 31),
                              showweeknumbers=False,
                              showothermonthdays=False)
        date_entry.grid(row=row+1, column=0, sticky='ew', pady=(0, SPACING['md']))

        self.form_vars[field_name] = {
            'widget': date_entry,
            'required': required,
            'type': 'date'
        }

    def create_dropdown(self, parent, label_text, field_name, options, row=0):
        """Create a dropdown/combobox field"""
        label = tk.Label(parent,
                        text=label_text,
                        font=FONTS['body_bold'],
                        bg=self.colors['background'],
                        fg=self.colors['text_primary'],
                        anchor='w')
        label.grid(row=row, column=0, sticky='w', pady=(SPACING['md'], SPACING['xs']))

        # Combobox
        combo_var = tk.StringVar()
        combo = ttk.Combobox(parent,
                            textvariable=combo_var,
                            values=options,
                            font=FONTS['body'],
                            state='readonly')
        combo.grid(row=row+1, column=0, sticky='ew', pady=(0, SPACING['md']))

        if options:
            combo.set(options[0])

        self.form_vars[field_name] = {
            'var': combo_var,
            'widget': combo,
            'required': False
        }

    def load_fy_data(self):
        """Load financial year data into form (edit mode)"""
        if not self.fy_data:
            return

        # Load text fields
        for field_name, field_info in self.form_vars.items():
            if field_info.get('type') == 'date':
                # Date field
                if field_name in self.fy_data and self.fy_data[field_name]:
                    date_value = self.fy_data[field_name]
                    if isinstance(date_value, str):
                        date_value = datetime.strptime(date_value, '%Y-%m-%d').date()
                    field_info['widget'].set_date(date_value)

            elif 'var' in field_info:
                # Text/dropdown field
                value = self.fy_data.get(field_name, '')
                if value and value != field_info.get('placeholder', ''):
                    field_info['var'].set(value)

                    if 'widget' in field_info:
                        widget = field_info['widget']
                        # Only set fg color for tk.Entry, NOT for ttk.Combobox
                        if isinstance(widget, tk.Entry) and not isinstance(widget, ttk.Combobox):
                            widget.config(fg=self.colors['text_primary'])

    def validate_form(self):
        """Validate form data"""
        errors = []

        for field_name, field_info in self.form_vars.items():
            if field_info.get('required'):
                if field_info.get('type') == 'date':
                    # Date fields are always filled
                    continue
                else:
                    value = field_info['var'].get().strip()
                    placeholder = field_info.get('placeholder', '')
                    if not value or value == placeholder:
                        label = field_name.replace('_', ' ').title()
                        errors.append(f"{label} is required")

        # Additional validation for FY Code
        if 'fy_code' in self.form_vars:
            fy_code = self.form_vars['fy_code']['var'].get().strip()
            if len(fy_code) > 6:
                errors.append("FY Code must be maximum 6 characters")

        # Date validation
        if 'start_date' in self.form_vars and 'end_date' in self.form_vars:
            start_date = self.form_vars['start_date']['widget'].get_date()
            end_date = self.form_vars['end_date']['widget'].get_date()

            if start_date >= end_date:
                errors.append("End Date must be after Start Date")

        return errors

    def get_form_data(self):
        """Get form data as dictionary"""
        data = {}

        for field_name, field_info in self.form_vars.items():
            if field_info.get('type') == 'date':
                # Date field
                date_value = field_info['widget'].get_date()
                data[field_name] = date_value.strftime('%Y-%m-%d')
            elif 'var' in field_info:
                # Text/dropdown field
                value = field_info['var'].get().strip()
                placeholder = field_info.get('placeholder', '')
                data[field_name] = value if value != placeholder else ''

        return data

    def handle_save(self):
        """Handle save button click"""
        # Validate
        errors = self.validate_form()
        if errors:
            messagebox.showerror("Validation Error", "\n".join(errors))
            return

        # Get data
        data = self.get_form_data()

        # Save
        if self.is_edit_mode:
            success, message = self.fy_handler.update_financial_year(
                self.fy_data['id'],
                data
            )
        else:
            success, message, _ = self.fy_handler.create_financial_year(data)

        if success:
            messagebox.showinfo("Success", message)
            self.on_save_callback()
        else:
            messagebox.showerror("Error", message)

    def handle_cancel(self):
        """Handle cancel/back button click"""
        self.on_cancel_callback()
