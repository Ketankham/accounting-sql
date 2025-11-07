"""
Item Type Management Screen - List, Create, Edit Item Types
"""

import tkinter as tk
from tkinter import ttk, messagebox
from database.item_type_handler import ItemTypeHandler
from ui_config import COLORS, FONTS, SPACING, LAYOUT


class ItemTypeManagement(tk.Frame):
    def __init__(self, parent, colors):
        super().__init__(parent, bg=COLORS['background'])
        self.colors = COLORS
        self.item_type_handler = ItemTypeHandler()

        # Connect to database
        if not self.item_type_handler.connect():
            messagebox.showerror("Database Error",
                               "Failed to connect to database.")
            return

        # Current view state
        self.current_view = 'list'  # 'list' or 'form'
        self.edit_item_type_id = None

        # Create UI
        self.create_widgets()
        self.load_item_types()

    def create_widgets(self):
        """Create the item type management UI"""
        # Header
        header_frame = tk.Frame(self, bg=self.colors['background'])
        header_frame.pack(fill=tk.X, padx=SPACING['xl'], pady=(SPACING['lg'], SPACING['md']))

        self.title_label = tk.Label(header_frame,
                                    text="Item Type Master",
                                    font=FONTS['h1'],
                                    bg=self.colors['background'],
                                    fg=self.colors['text_primary'])
        self.title_label.pack(side=tk.LEFT)

        self.create_btn = tk.Button(header_frame,
                                    text="Create New Item Type")
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
        """Create the table view for item types"""
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
            ("Sr.", 8),
            ("Type Code", 15),
            ("Type Name", 40),
            ("Status", 12),
            ("Action", 8)
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

    def load_item_types(self):
        """Load item types from database and display in table"""
        # Clear existing rows
        for widget in self.table_body.winfo_children():
            widget.destroy()

        # Get item types
        item_types = self.item_type_handler.get_all_item_types()

        if not item_types:
            # No item types found
            no_data_label = tk.Label(self.table_body,
                                    text="No item types found. Click 'Create New Item Type' to add one.",
                                    font=FONTS['body'],
                                    bg=self.colors['background'],
                                    fg=self.colors['text_tertiary'],
                                    pady=SPACING['xxl'])
            no_data_label.pack(fill=tk.BOTH)
            return

        # Display item types
        for idx, item_type in enumerate(item_types, 1):
            self.create_table_row(idx, item_type)

    def create_table_row(self, sr_no, item_type):
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
                           width=8,
                           anchor='w',
                           padx=SPACING['md'])
        sr_label.pack(side=tk.LEFT, padx=SPACING['sm'])
        sr_label.bind('<Enter>', on_enter)
        sr_label.bind('<Leave>', on_leave)

        # Type Code
        code_label = tk.Label(row_frame, text=item_type.get('type_code', 'N/A'),
                             font=FONTS['body_bold'],
                             bg=row_bg,
                             fg=self.colors['primary'],
                             width=15,
                             anchor='w',
                             padx=SPACING['md'])
        code_label.pack(side=tk.LEFT, padx=SPACING['sm'])
        code_label.bind('<Enter>', on_enter)
        code_label.bind('<Leave>', on_leave)

        # Type Name
        name_label = tk.Label(row_frame, text=item_type.get('type_name', 'N/A'),
                             font=FONTS['body'],
                             bg=row_bg,
                             fg=self.colors['text_primary'],
                             width=40,
                             anchor='w',
                             padx=SPACING['md'])
        name_label.pack(side=tk.LEFT, padx=SPACING['sm'])
        name_label.bind('<Enter>', on_enter)
        name_label.bind('<Leave>', on_leave)

        # Status
        status = item_type.get('status', 'N/A')
        status_color = '#10B981' if status == 'Active' else '#EF4444'
        status_label = tk.Label(row_frame,
                               text=status,
                               font=FONTS['body_bold'],
                               bg=row_bg,
                               fg=status_color,
                               width=12,
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
                            command=lambda: self.show_edit_form(item_type['id']))
        edit_btn.pack(side=tk.LEFT, padx=SPACING['md'])

        # Hover effect for edit button
        def on_btn_enter(e):
            edit_btn.config(bg=self.colors['primary_hover'])
        def on_btn_leave(e):
            edit_btn.config(bg=self.colors['primary'])

        edit_btn.bind('<Enter>', on_btn_enter)
        edit_btn.bind('<Leave>', on_btn_leave)

    def show_create_form(self):
        """Show create item type form"""
        # Clear content container
        for widget in self.content_container.winfo_children():
            widget.destroy()

        # Update title
        self.title_label.config(text="Create New Item Type")

        # Hide create button
        self.create_btn.pack_forget()

        # Import and create form
        from item_type_form import ItemTypeForm

        form = ItemTypeForm(
            self.content_container,
            self.colors,
            self.item_type_handler,
            None,  # No existing data
            on_save=self.on_form_save,
            on_cancel=self.on_form_cancel
        )
        form.pack(fill=tk.BOTH, expand=True)

        self.current_view = 'form'

    def show_edit_form(self, item_type_id):
        """Show edit item type form"""
        # Get item type data
        item_type_data = self.item_type_handler.get_item_type_by_id(item_type_id)

        if not item_type_data:
            messagebox.showerror("Error", "Item type not found")
            return

        # Clear content container
        for widget in self.content_container.winfo_children():
            widget.destroy()

        # Update title
        self.title_label.config(text=f"Edit Item Type: {item_type_data['type_name']}")

        # Hide create button
        self.create_btn.pack_forget()

        # Import and create form
        from item_type_form import ItemTypeForm

        form = ItemTypeForm(
            self.content_container,
            self.colors,
            self.item_type_handler,
            item_type_data,
            on_save=self.on_form_save,
            on_cancel=self.on_form_cancel,
            on_delete=self.delete_item_type  # Pass delete callback for edit mode
        )
        form.pack(fill=tk.BOTH, expand=True)

        self.current_view = 'form'
        self.edit_item_type_id = item_type_id

    def on_form_save(self):
        """Handle form save"""
        # Return to list view
        self.on_form_cancel()

    def on_form_cancel(self):
        """Handle form cancel"""
        # Update title
        self.title_label.config(text="Item Type Master")

        # Show create button
        self.create_btn.pack(side=tk.RIGHT)

        # Recreate table view
        self.create_table_view()
        self.load_item_types()

        self.current_view = 'list'
        self.edit_item_type_id = None

    def delete_item_type(self, item_type_id, type_name):
        """Delete an item type"""
        result = messagebox.askyesno("Confirm Delete",
                                     f"Are you sure you want to delete '{type_name}'?\n\n" +
                                     "This action cannot be undone.")

        if result:
            success, message = self.item_type_handler.delete_item_type(item_type_id)
            if success:
                messagebox.showinfo("Success", message)
                self.on_form_cancel()
            else:
                messagebox.showerror("Error", message)
