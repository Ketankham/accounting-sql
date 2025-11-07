"""
Item Management Screen - List, Create, Edit Items
"""

import tkinter as tk
from tkinter import ttk, messagebox
from database.item_handler import ItemHandler
from ui_config import COLORS, FONTS, SPACING, LAYOUT


class ItemManagement(tk.Frame):
    def __init__(self, parent, colors):
        super().__init__(parent, bg=COLORS['background'])
        self.colors = colors
        self.item_handler = ItemHandler()

        # Connect to database
        if not self.item_handler.connect():
            messagebox.showerror("Database Error",
                               "Failed to connect to database.")
            return

        # Current view state
        self.current_view = 'list'  # 'list' or 'form'
        self.edit_item_id = None

        # Create UI
        self.create_widgets()
        self.load_items()

    def create_widgets(self):
        """Create the item management UI"""
        # Header
        header_frame = tk.Frame(self, bg=self.colors['background'])
        header_frame.pack(fill=tk.X, padx=SPACING['xl'], pady=(SPACING['lg'], SPACING['md']))

        self.title_label = tk.Label(header_frame,
                                    text="Item Master",
                                    font=FONTS['h1'],
                                    bg=self.colors['background'],
                                    fg=self.colors['text_primary'])
        self.title_label.pack(side=tk.LEFT)

        self.create_btn = tk.Button(header_frame,
                                    text="Create New Item")
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
        self.create_btn.bind('<Enter>', lambda _e: self.create_btn.config(bg=self.colors['primary_hover']))
        self.create_btn.bind('<Leave>', lambda _e: self.create_btn.config(bg=self.colors['primary']))

        # Content container (will hold either table or form)
        self.content_container = tk.Frame(self, bg=self.colors['background'])
        self.content_container.pack(fill=tk.BOTH, expand=True, padx=SPACING['xl'], pady=SPACING['md'])

        # Create table view
        self.create_table_view()

    def create_table_view(self):
        """Create the table view for items"""
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
            ("Item Code", 15),
            ("Item Name", 45),
            ("MRP", 15),
            ("Status", 12),
            ("Actions", 10)
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

        self.canvas = tk.Canvas(table_canvas_frame, bg=self.colors['background'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(table_canvas_frame, orient="vertical", command=self.canvas.yview)

        self.table_body = tk.Frame(self.canvas, bg=self.colors['background'])

        self.table_body.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        # Create window with proper width binding
        self.canvas_window = self.canvas.create_window((0, 0), window=self.table_body, anchor="nw")

        # Bind canvas width to table_body width
        def on_canvas_configure(event):
            self.canvas.itemconfig(self.canvas_window, width=event.width)
        self.canvas.bind("<Configure>", on_canvas_configure)
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Enable mousewheel scrolling
        def _on_mousewheel(event):
            self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

        self.canvas.bind_all("<MouseWheel>", _on_mousewheel)

    def load_items(self):
        """Load items from database and display in table"""
        # Clear existing rows
        for widget in self.table_body.winfo_children():
            widget.destroy()

        # Get items
        items = self.item_handler.get_all_items()

        if not items:
            # No items found
            no_data_label = tk.Label(self.table_body,
                                    text="No items found. Click 'Create New Item' to add one.",
                                    font=FONTS['body'],
                                    bg=self.colors['background'],
                                    fg=self.colors['text_tertiary'],
                                    pady=SPACING['xxl'])
            no_data_label.pack(fill=tk.BOTH)
            return

        # Display items
        for idx, item in enumerate(items, 1):
            self.create_table_row(idx, item)

        # Update canvas scroll region after all items are added
        self.table_body.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def create_table_row(self, sr_no, item):
        """Create a single table row"""
        # Alternating row colors
        row_bg = self.colors['background'] if sr_no % 2 == 0 else self.colors['surface']

        row_frame = tk.Frame(self.table_body, bg=row_bg, height=LAYOUT['table_row_height'])
        row_frame.pack(fill=tk.X, pady=1)
        row_frame.pack_propagate(False)

        # Hover effect
        def on_enter(_e):
            row_frame.config(bg='#DBEAFE')
            for widget in row_frame.winfo_children():
                if isinstance(widget, (tk.Label, tk.Frame)) and widget != edit_btn:
                    widget.config(bg='#DBEAFE')

        def on_leave(_e):
            row_frame.config(bg=row_bg)
            for widget in row_frame.winfo_children():
                if isinstance(widget, (tk.Label, tk.Frame)) and widget != edit_btn:
                    widget.config(bg=row_bg)

        row_frame.bind('<Enter>', on_enter)
        row_frame.bind('<Leave>', on_leave)

        # Item Code
        code_label = tk.Label(row_frame, text=item.get('item_code', 'N/A'),
                             font=FONTS['body'],
                             bg=row_bg,
                             fg=self.colors['text_primary'],
                             width=15,
                             anchor='w',
                             padx=SPACING['md'])
        code_label.pack(side=tk.LEFT, padx=SPACING['xs'])
        code_label.bind('<Enter>', on_enter)
        code_label.bind('<Leave>', on_leave)

        # Item Name
        name_label = tk.Label(row_frame, text=item.get('item_name', 'N/A'),
                             font=FONTS['body'],
                             bg=row_bg,
                             fg=self.colors['text_primary'],
                             width=45,
                             anchor='w',
                             padx=SPACING['md'])
        name_label.pack(side=tk.LEFT, padx=SPACING['xs'])
        name_label.bind('<Enter>', on_enter)
        name_label.bind('<Leave>', on_leave)

        # MRP
        mrp = item.get('mrp', 0)
        mrp_label = tk.Label(row_frame, text=f"Rs. {mrp:.2f}" if mrp else "Rs. 0.00",
                            font=FONTS['body'],
                            bg=row_bg,
                            fg=self.colors['text_primary'],
                            width=15,
                            anchor='w',
                            padx=SPACING['md'])
        mrp_label.pack(side=tk.LEFT, padx=SPACING['xs'])
        mrp_label.bind('<Enter>', on_enter)
        mrp_label.bind('<Leave>', on_leave)

        # Status
        status = item.get('status', 'N/A')
        status_color = '#10B981' if status == 'Active' else '#EF4444'
        status_label = tk.Label(row_frame, text=status,
                               font=FONTS['body'],
                               bg=row_bg,
                               fg=status_color,
                               width=12,
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
                            font=FONTS['body'],
                            bg=self.colors['primary'],
                            fg='white',
                            activebackground=self.colors['primary_hover'],
                            activeforeground='white',
                            cursor='hand2',
                            relief=tk.FLAT,
                            padx=SPACING['lg'],
                            pady=SPACING['sm'],
                            width=6,
                            command=lambda: self.show_edit_form(item['id']))
        edit_btn.pack(side=tk.LEFT)

    def show_create_form(self):
        """Show create item form"""
        # Clear content container
        for widget in self.content_container.winfo_children():
            widget.destroy()

        # Update title
        self.title_label.config(text="Create New Item")

        # Hide create button
        self.create_btn.pack_forget()

        # Import and create form
        from item_form import ItemForm

        form = ItemForm(
            self.content_container,
            self.colors,
            self.item_handler,
            None,  # No existing data
            on_save=self.on_form_save,
            on_cancel=self.on_form_cancel
        )
        form.pack(fill=tk.BOTH, expand=True)

        self.current_view = 'form'

    def show_edit_form(self, item_id):
        """Show edit item form"""
        # Get item data
        item_data = self.item_handler.get_item_by_id(item_id)

        if not item_data:
            messagebox.showerror("Error", "Item not found")
            return

        # Clear content container
        for widget in self.content_container.winfo_children():
            widget.destroy()

        # Update title
        self.title_label.config(text=f"Edit Item: {item_data['item_name']}")

        # Hide create button
        self.create_btn.pack_forget()

        # Import and create form
        from item_form import ItemForm

        form = ItemForm(
            self.content_container,
            self.colors,
            self.item_handler,
            item_data,
            on_save=self.on_form_save,
            on_cancel=self.on_form_cancel,
            on_delete=self.delete_item  # Pass delete callback for edit mode
        )
        form.pack(fill=tk.BOTH, expand=True)

        self.current_view = 'form'
        self.edit_item_id = item_id

    def on_form_save(self):
        """Handle form save"""
        # Return to list view
        self.on_form_cancel()

    def on_form_cancel(self):
        """Handle form cancel"""
        # Update title
        self.title_label.config(text="Item Master")

        # Show create button
        self.create_btn.pack(side=tk.RIGHT)

        # Recreate table view
        self.create_table_view()
        self.load_items()

        self.current_view = 'list'
        self.edit_item_id = None

    def delete_item(self, item_id, item_name):
        """Delete an item"""
        result = messagebox.askyesno("Confirm Delete",
                                     f"Are you sure you want to delete '{item_name}'?\n\n" +
                                     "This action cannot be undone.")

        if result:
            success, message = self.item_handler.delete_item(item_id)
            if success:
                messagebox.showinfo("Success", message)
                self.load_items()
            else:
                messagebox.showerror("Error", message)
