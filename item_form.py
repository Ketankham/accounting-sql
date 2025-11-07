"""
Item Form - Create and Edit Item
"""

import tkinter as tk
from tkinter import ttk, messagebox
from database.item_group_handler import ItemGroupHandler
from database.item_type_handler import ItemTypeHandler
from database.uom_handler import UoMHandler
from database.item_company_handler import ItemCompanyHandler
from database.account_master_handler import AccountMasterHandler
from ui_config import COLORS, FONTS, SPACING


class ItemForm(tk.Frame):
    def __init__(self, parent, colors, item_handler, item_data, on_save, on_cancel, on_delete=None):
        super().__init__(parent, bg=COLORS['background'])
        self.colors = colors
        self.item_handler = item_handler
        self.item_data = item_data
        self.on_save_callback = on_save
        self.on_cancel_callback = on_cancel
        self.on_delete_callback = on_delete

        self.is_edit_mode = item_data is not None

        # Initialize other handlers
        self.item_group_handler = ItemGroupHandler()
        self.item_type_handler = ItemTypeHandler()
        self.uom_handler = UoMHandler()
        self.item_company_handler = ItemCompanyHandler()
        self.account_handler = AccountMasterHandler()

        # Connect to databases
        self.item_group_handler.connect()
        self.item_type_handler.connect()
        self.uom_handler.connect()
        self.item_company_handler.connect()
        self.account_handler.connect()

        self.create_widgets()
        self.pack(fill=tk.BOTH, expand=True)

        # Load existing data if editing
        if self.is_edit_mode:
            self.load_item_data()
        else:
            self.generate_item_code()

    def create_widgets(self):
        """Create form widgets"""
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

        # Form container
        form_frame = tk.Frame(scrollable_frame, bg=self.colors['surface'], relief=tk.SOLID, bd=2)
        form_frame.pack(fill=tk.BOTH, expand=True, padx=SPACING['xl'], pady=SPACING['lg'])

        # Form content with padding
        content_frame = tk.Frame(form_frame, bg=self.colors['surface'])
        content_frame.pack(fill=tk.BOTH, expand=True, padx=SPACING['xl'], pady=SPACING['lg'])

        row = 0

        # Row 1: Item Code and External Code
        tk.Label(content_frame, text="Item Code:", font=FONTS['body'], bg=self.colors['surface'], fg=self.colors['text_primary']).grid(row=row, column=0, sticky='w', pady=SPACING['md'])
        self.item_code_var = tk.StringVar()
        item_code_entry = tk.Entry(content_frame, textvariable=self.item_code_var, font=FONTS['body'], state='readonly', width=20, relief=tk.SOLID, bd=1)
        item_code_entry.grid(row=row, column=1, sticky='ew', pady=SPACING['md'], padx=(0, SPACING['lg']))

        tk.Label(content_frame, text="External Code:", font=FONTS['body'], bg=self.colors['surface'], fg=self.colors['text_primary']).grid(row=row, column=2, sticky='w', pady=SPACING['md'])
        self.external_code_var = tk.StringVar()
        tk.Entry(content_frame, textvariable=self.external_code_var, font=FONTS['body'], width=20, relief=tk.SOLID, bd=1).grid(row=row, column=3, sticky='ew', pady=SPACING['md'])

        row += 1

        # Row 2: Item Name
        tk.Label(content_frame, text="Item Name: *", font=FONTS['body'], bg=self.colors['surface'], fg=self.colors['text_primary']).grid(row=row, column=0, sticky='w', pady=SPACING['md'])
        self.item_name_var = tk.StringVar()
        tk.Entry(content_frame, textvariable=self.item_name_var, font=FONTS['body'], relief=tk.SOLID, bd=1).grid(row=row, column=1, columnspan=3, sticky='ew', pady=SPACING['md'])

        row += 1

        # Row 3: Item Group and UOM
        tk.Label(content_frame, text="Item Group: *", font=FONTS['body'], bg=self.colors['surface'], fg=self.colors['text_primary']).grid(row=row, column=0, sticky='w', pady=SPACING['md'])
        self.item_group_var = tk.StringVar()
        self.item_group_combo = ttk.Combobox(content_frame, textvariable=self.item_group_var, state='readonly', font=FONTS['body'], width=18)
        self.item_group_combo.grid(row=row, column=1, sticky='ew', pady=SPACING['md'], padx=(0, SPACING['lg']))
        self.load_item_groups()

        tk.Label(content_frame, text="UOM: *", font=FONTS['body'], bg=self.colors['surface'], fg=self.colors['text_primary']).grid(row=row, column=2, sticky='w', pady=SPACING['md'])
        self.uom_var = tk.StringVar()
        self.uom_combo = ttk.Combobox(content_frame, textvariable=self.uom_var, state='readonly', font=FONTS['body'], width=18)
        self.uom_combo.grid(row=row, column=3, sticky='ew', pady=SPACING['md'])
        self.load_uoms()

        row += 1

        # Row 4: Item Type and Company
        tk.Label(content_frame, text="Item Type: *", font=FONTS['body'], bg=self.colors['surface'], fg=self.colors['text_primary']).grid(row=row, column=0, sticky='w', pady=SPACING['md'])
        self.item_type_var = tk.StringVar()
        self.item_type_combo = ttk.Combobox(content_frame, textvariable=self.item_type_var, state='readonly', font=FONTS['body'], width=18)
        self.item_type_combo.grid(row=row, column=1, sticky='ew', pady=SPACING['md'], padx=(0, SPACING['lg']))
        self.load_item_types()

        tk.Label(content_frame, text="Company: *", font=FONTS['body'], bg=self.colors['surface'], fg=self.colors['text_primary']).grid(row=row, column=2, sticky='w', pady=SPACING['md'])
        self.company_var = tk.StringVar()
        self.company_combo = ttk.Combobox(content_frame, textvariable=self.company_var, state='readonly', font=FONTS['body'], width=18)
        self.company_combo.grid(row=row, column=3, sticky='ew', pady=SPACING['md'])
        self.load_companies()

        row += 1

        # Row 5: Purchase Rate and MRP
        tk.Label(content_frame, text="Purchase Rate:", font=FONTS['body'], bg=self.colors['surface'], fg=self.colors['text_primary']).grid(row=row, column=0, sticky='w', pady=SPACING['md'])
        self.purchase_rate_var = tk.StringVar(value="0.00")
        purchase_rate_entry = tk.Entry(content_frame, textvariable=self.purchase_rate_var, font=FONTS['body'], width=20, relief=tk.SOLID, bd=1)
        purchase_rate_entry.grid(row=row, column=1, sticky='ew', pady=SPACING['md'], padx=(0, SPACING['lg']))
        purchase_rate_entry.bind('<KeyRelease>', lambda e: self.validate_numeric(self.purchase_rate_var))

        tk.Label(content_frame, text="MRP Rs.:", font=FONTS['body'], bg=self.colors['surface'], fg=self.colors['text_primary']).grid(row=row, column=2, sticky='w', pady=SPACING['md'])
        self.mrp_var = tk.StringVar(value="0.00")
        mrp_entry = tk.Entry(content_frame, textvariable=self.mrp_var, font=FONTS['body'], width=20, relief=tk.SOLID, bd=1)
        mrp_entry.grid(row=row, column=3, sticky='ew', pady=SPACING['md'])
        mrp_entry.bind('<KeyRelease>', lambda e: self.validate_numeric(self.mrp_var))

        row += 1

        # Row 6: GST % and HSN Code
        tk.Label(content_frame, text="GST %:", font=FONTS['body'], bg=self.colors['surface'], fg=self.colors['text_primary']).grid(row=row, column=0, sticky='w', pady=SPACING['md'])
        self.gst_var = tk.StringVar(value="0.00")
        gst_entry = tk.Entry(content_frame, textvariable=self.gst_var, font=FONTS['body'], width=20, relief=tk.SOLID, bd=1)
        gst_entry.grid(row=row, column=1, sticky='ew', pady=SPACING['md'], padx=(0, SPACING['lg']))
        gst_entry.bind('<KeyRelease>', lambda e: self.validate_percentage(self.gst_var))

        tk.Label(content_frame, text="HSN Code:", font=FONTS['body'], bg=self.colors['surface'], fg=self.colors['text_primary']).grid(row=row, column=2, sticky='w', pady=SPACING['md'])
        self.hsn_code_var = tk.StringVar()
        tk.Entry(content_frame, textvariable=self.hsn_code_var, font=FONTS['body'], width=20, relief=tk.SOLID, bd=1).grid(row=row, column=3, sticky='ew', pady=SPACING['md'])

        row += 1

        # Warehouse 1 Section
        tk.Label(content_frame, text="Warehouse-1 Rates", font=FONTS['body_bold'], bg=self.colors['surface'], fg=self.colors['primary']).grid(row=row, column=0, columnspan=4, sticky='w', pady=(SPACING['lg'], SPACING['sm']))

        row += 1

        # Row 7: Sale Rate WH1 and Discount WH1
        tk.Label(content_frame, text="Sale Rate @ WH-1:", font=FONTS['body'], bg=self.colors['surface'], fg=self.colors['text_primary']).grid(row=row, column=0, sticky='w', pady=SPACING['md'])
        self.sale_rate_wh1_var = tk.StringVar(value="0.00")
        sale_rate_wh1_entry = tk.Entry(content_frame, textvariable=self.sale_rate_wh1_var, font=FONTS['body'], width=20, relief=tk.SOLID, bd=1)
        sale_rate_wh1_entry.grid(row=row, column=1, sticky='ew', pady=SPACING['md'], padx=(0, SPACING['lg']))
        sale_rate_wh1_entry.bind('<KeyRelease>', lambda e: self.validate_numeric(self.sale_rate_wh1_var))

        tk.Label(content_frame, text="Discount % @ WH-1:", font=FONTS['body'], bg=self.colors['surface'], fg=self.colors['text_primary']).grid(row=row, column=2, sticky='w', pady=SPACING['md'])
        self.discount_wh1_var = tk.StringVar(value="0.00")
        discount_wh1_entry = tk.Entry(content_frame, textvariable=self.discount_wh1_var, font=FONTS['body'], width=20, relief=tk.SOLID, bd=1)
        discount_wh1_entry.grid(row=row, column=3, sticky='ew', pady=SPACING['md'])
        discount_wh1_entry.bind('<KeyRelease>', lambda e: self.validate_percentage(self.discount_wh1_var))

        row += 1

        # Warehouse 2 Section
        tk.Label(content_frame, text="Warehouse-2 Rates", font=FONTS['body_bold'], bg=self.colors['surface'], fg=self.colors['primary']).grid(row=row, column=0, columnspan=4, sticky='w', pady=(SPACING['lg'], SPACING['sm']))

        row += 1

        # Row 8: Sale Rate WH2 and Discount WH2
        tk.Label(content_frame, text="Sale Rate @ WH-2:", font=FONTS['body'], bg=self.colors['surface'], fg=self.colors['text_primary']).grid(row=row, column=0, sticky='w', pady=SPACING['md'])
        self.sale_rate_wh2_var = tk.StringVar(value="0.00")
        sale_rate_wh2_entry = tk.Entry(content_frame, textvariable=self.sale_rate_wh2_var, font=FONTS['body'], width=20, relief=tk.SOLID, bd=1)
        sale_rate_wh2_entry.grid(row=row, column=1, sticky='ew', pady=SPACING['md'], padx=(0, SPACING['lg']))
        sale_rate_wh2_entry.bind('<KeyRelease>', lambda e: self.validate_numeric(self.sale_rate_wh2_var))

        tk.Label(content_frame, text="Discount % @ WH-2:", font=FONTS['body'], bg=self.colors['surface'], fg=self.colors['text_primary']).grid(row=row, column=2, sticky='w', pady=SPACING['md'])
        self.discount_wh2_var = tk.StringVar(value="0.00")
        discount_wh2_entry = tk.Entry(content_frame, textvariable=self.discount_wh2_var, font=FONTS['body'], width=20, relief=tk.SOLID, bd=1)
        discount_wh2_entry.grid(row=row, column=3, sticky='ew', pady=SPACING['md'])
        discount_wh2_entry.bind('<KeyRelease>', lambda e: self.validate_percentage(self.discount_wh2_var))

        row += 1

        # Account Section
        tk.Label(content_frame, text="Account Information", font=FONTS['body_bold'], bg=self.colors['surface'], fg=self.colors['primary']).grid(row=row, column=0, columnspan=4, sticky='w', pady=(SPACING['lg'], SPACING['sm']))

        row += 1

        # Row 9: Sales Account and Purchase Account
        tk.Label(content_frame, text="Sales A/c:", font=FONTS['body'], bg=self.colors['surface'], fg=self.colors['text_primary']).grid(row=row, column=0, sticky='w', pady=SPACING['md'])
        self.sales_account_var = tk.StringVar()
        self.sales_account_combo = ttk.Combobox(content_frame, textvariable=self.sales_account_var, state='readonly', font=FONTS['body'], width=18)
        self.sales_account_combo.grid(row=row, column=1, sticky='ew', pady=SPACING['md'], padx=(0, SPACING['lg']))
        self.load_sales_accounts()

        tk.Label(content_frame, text="Purchase A/c:", font=FONTS['body'], bg=self.colors['surface'], fg=self.colors['text_primary']).grid(row=row, column=2, sticky='w', pady=SPACING['md'])
        self.purchase_account_var = tk.StringVar()
        self.purchase_account_combo = ttk.Combobox(content_frame, textvariable=self.purchase_account_var, state='readonly', font=FONTS['body'], width=18)
        self.purchase_account_combo.grid(row=row, column=3, sticky='ew', pady=SPACING['md'])
        self.load_purchase_accounts()

        row += 1

        # Row 10: Status
        tk.Label(content_frame, text="Status: *", font=FONTS['body'], bg=self.colors['surface'], fg=self.colors['text_primary']).grid(row=row, column=0, sticky='w', pady=SPACING['md'])
        self.status_var = tk.StringVar(value="Active")
        ttk.Combobox(content_frame, textvariable=self.status_var, values=["Active", "Inactive"], state='readonly', font=FONTS['body'], width=18).grid(row=row, column=1, sticky='ew', pady=SPACING['md'])

        row += 1

        # Configure grid weights
        content_frame.columnconfigure(1, weight=1)
        content_frame.columnconfigure(3, weight=1)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Mousewheel scrolling
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind("<Enter>", lambda e: canvas.bind_all("<MouseWheel>", _on_mousewheel))
        canvas.bind("<Leave>", lambda e: canvas.unbind_all("<MouseWheel>"))

        # --- BUTTONS (outside scrollable area) ---
        button_frame = tk.Frame(self, bg=self.colors['background'])
        button_frame.pack(fill=tk.X, padx=SPACING['xxl'], pady=(SPACING['lg'], SPACING['xl']))

        # Save button (left side)
        save_btn = tk.Button(button_frame,
                            text="Create Item" if not self.is_edit_mode else "Update Item")
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
            command=self.save_item
        )
        save_btn.pack(side=tk.LEFT, padx=(0, SPACING['md']))

        # Add hover effect
        save_btn.bind('<Enter>', lambda e: save_btn.config(bg=self.colors['primary_hover']))
        save_btn.bind('<Leave>', lambda e: save_btn.config(bg=self.colors['primary']))

        # Delete button (middle - only in edit mode)
        if self.is_edit_mode and self.on_delete_callback:
            delete_btn = tk.Button(button_frame,
                                  text="Delete Item")
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
            delete_btn.bind('<Enter>', lambda e: delete_btn.config(bg='#DC2626'))
            delete_btn.bind('<Leave>', lambda e: delete_btn.config(bg='#EF4444'))

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
            command=self.on_cancel_callback
        )
        back_btn.pack(side=tk.RIGHT)

    def validate_numeric(self, var):
        """Validate that input is numeric"""
        value = var.get()
        if value == "":
            return True

        # Remove any non-numeric characters except decimal point
        cleaned = ''.join(c for c in value if c.isdigit() or c == '.')

        # Ensure only one decimal point
        if cleaned.count('.') > 1:
            parts = cleaned.split('.')
            cleaned = parts[0] + '.' + ''.join(parts[1:])

        if cleaned != value:
            var.set(cleaned)

        return True

    def validate_percentage(self, var):
        """Validate that input is numeric and between 0-100"""
        value = var.get()
        if value == "":
            return True

        # First validate numeric
        self.validate_numeric(var)
        value = var.get()

        # Check range
        try:
            num_value = float(value)
            if num_value < 0:
                var.set("0.00")
            elif num_value > 100:
                var.set("100.00")
        except ValueError:
            pass

        return True

    def generate_item_code(self):
        """Generate next item code"""
        next_code = self.item_handler.get_next_item_code()
        self.item_code_var.set(next_code)

    def load_item_groups(self):
        """Load active item groups"""
        groups = self.item_group_handler.get_active_item_groups()
        self.item_group_data = {f"{g['item_group_code']} - {g['item_group_name']}": g['item_group_code'] for g in groups}
        self.item_group_combo['values'] = list(self.item_group_data.keys())

    def load_item_types(self):
        """Load active item types only"""
        types = self.item_type_handler.get_active_item_types()
        self.item_type_data = {f"{t['type_code']} - {t['type_name']}": t['type_code'] for t in types}
        self.item_type_combo['values'] = list(self.item_type_data.keys())

    def load_uoms(self):
        """Load active UOMs"""
        uoms = self.uom_handler.get_active_uoms()
        self.uom_data = {f"{u['uom_code']} - {u['uom_name']}": u['uom_code'] for u in uoms}
        self.uom_combo['values'] = list(self.uom_data.keys())

    def load_companies(self):
        """Load active companies"""
        companies = self.item_company_handler.get_active_item_companies()
        self.company_data = {c['company_name']: c['company_name'] for c in companies}
        self.company_combo['values'] = list(self.company_data.keys())

    def load_sales_accounts(self):
        """Load active sales accounts"""
        accounts = self.account_handler.get_active_accounts()
        # Filter for sales accounts
        sales_accounts = [a for a in accounts if 'SALES' in a.get('account_name', '').upper() or a.get('account_code', '').startswith('4')]
        self.sales_account_data = {f"{a['account_code']} - {a['account_name']}": a['account_code'] for a in sales_accounts}
        self.sales_account_combo['values'] = list(self.sales_account_data.keys())

    def load_purchase_accounts(self):
        """Load active purchase accounts"""
        accounts = self.account_handler.get_active_accounts()
        # Filter for purchase accounts
        purchase_accounts = [a for a in accounts if 'PURCHASE' in a.get('account_name', '').upper() or a.get('account_code', '').startswith('5')]
        self.purchase_account_data = {f"{a['account_code']} - {a['account_name']}": a['account_code'] for a in purchase_accounts}
        self.purchase_account_combo['values'] = list(self.purchase_account_data.keys())

    def load_item_data(self):
        """Load existing item data for editing"""
        if not self.item_data:
            return

        item = self.item_data
        self.item_code_var.set(item.get('item_code', ''))
        self.external_code_var.set(item.get('external_code', ''))
        self.item_name_var.set(item.get('item_name', ''))

        # Set dropdowns
        for display, code in self.item_group_data.items():
            if code == item.get('item_group_code'):
                self.item_group_var.set(display)
                break

        for display, code in self.item_type_data.items():
            if code == item.get('item_type_code'):
                self.item_type_var.set(display)
                break

        for display, code in self.uom_data.items():
            if code == item.get('uom_code'):
                self.uom_var.set(display)
                break

        self.company_var.set(item.get('company_name', ''))

        self.purchase_rate_var.set(str(item.get('purchase_rate', 0.0)))
        self.mrp_var.set(str(item.get('mrp', 0.0)))
        self.gst_var.set(str(item.get('gst_percentage', 0.0)))
        self.hsn_code_var.set(item.get('hsn_code', ''))
        self.sale_rate_wh1_var.set(str(item.get('sale_rate_wh1', 0.0)))
        self.sale_rate_wh2_var.set(str(item.get('sale_rate_wh2', 0.0)))
        self.discount_wh1_var.set(str(item.get('discount_wh1', 0.0)))
        self.discount_wh2_var.set(str(item.get('discount_wh2', 0.0)))

        # Set account dropdowns
        for display, code in self.sales_account_data.items():
            if code == item.get('sales_account_code'):
                self.sales_account_var.set(display)
                break

        for display, code in self.purchase_account_data.items():
            if code == item.get('purchase_account_code'):
                self.purchase_account_var.set(display)
                break

        self.status_var.set(item.get('status', 'Active'))

    def save_item(self):
        """Save item to database"""
        # Validate required fields
        if not self.item_name_var.get().strip():
            messagebox.showerror("Error", "Item Name is required")
            return

        if not self.item_group_var.get():
            messagebox.showerror("Error", "Item Group is required")
            return

        if not self.item_type_var.get():
            messagebox.showerror("Error", "Item Type is required")
            return

        if not self.uom_var.get():
            messagebox.showerror("Error", "Unit of Measure is required")
            return

        if not self.company_var.get():
            messagebox.showerror("Error", "Company is required")
            return

        # Get codes from display values
        item_group_code = self.item_group_data.get(self.item_group_var.get(), '')
        item_type_code = self.item_type_data.get(self.item_type_var.get(), '')
        uom_code = self.uom_data.get(self.uom_var.get(), '')
        sales_account_code = self.sales_account_data.get(self.sales_account_var.get(), '')
        purchase_account_code = self.purchase_account_data.get(self.purchase_account_var.get(), '')

        # Prepare item data
        item_data = {
            'item_code': self.item_code_var.get(),
            'external_code': self.external_code_var.get(),
            'item_name': self.item_name_var.get(),
            'item_group_code': item_group_code,
            'item_type_code': item_type_code,
            'uom_code': uom_code,
            'company_name': self.company_var.get(),
            'purchase_rate': float(self.purchase_rate_var.get() or 0),
            'mrp': float(self.mrp_var.get() or 0),
            'gst_percentage': float(self.gst_var.get() or 0),
            'hsn_code': self.hsn_code_var.get(),
            'sale_rate_wh1': float(self.sale_rate_wh1_var.get() or 0),
            'sale_rate_wh2': float(self.sale_rate_wh2_var.get() or 0),
            'discount_wh1': float(self.discount_wh1_var.get() or 0),
            'discount_wh2': float(self.discount_wh2_var.get() or 0),
            'sales_account_code': sales_account_code,
            'purchase_account_code': purchase_account_code,
            'status': self.status_var.get()
        }

        try:
            if self.is_edit_mode:
                # Update existing item
                success, message = self.item_handler.update_item(self.item_data['id'], item_data)
            else:
                # Create new item
                success, message, _ = self.item_handler.create_item(item_data)

            if success:
                messagebox.showinfo("Success", message)
                self.on_save_callback()
            else:
                messagebox.showerror("Error", message)

        except Exception as e:
            messagebox.showerror("Error", f"Error saving item: {str(e)}")

    def handle_delete(self):
        """Handle delete button click"""
        if self.on_delete_callback and self.is_edit_mode:
            item_id = self.item_data['id']
            item_name = self.item_data['item_name']
            self.on_delete_callback(item_id, item_name)
