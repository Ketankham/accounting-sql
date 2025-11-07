"""
Item Group Management Screen - List, Create, Edit Item Groups
"""

import tkinter as tk
from tkinter import ttk, messagebox
from database.item_group_handler import ItemGroupHandler
from ui_config import COLORS, FONTS, SPACING, LAYOUT, BUTTON_STYLES


class ItemGroupManagement(tk.Frame):
    def __init__(self, parent, colors):
        super().__init__(parent, bg=COLORS['background'])
        self.colors = COLORS  # Use unified colors
        self.item_group_handler = ItemGroupHandler()

        # Connect to database
        if not self.item_group_handler.connect():
            messagebox.showerror("Database Error",
                               "Failed to connect to database.")
            return

        # Current view state
        self.current_view = 'list'  # 'list' or 'form'
        self.edit_item_group_id = None

        # Create UI
        self.create_widgets()
        self.load_item_groups()

    def create_widgets(self):
        """Create the item group management UI"""
        # Header
        header_frame = tk.Frame(self, bg=self.colors['background'])
        header_frame.pack(fill=tk.X, padx=SPACING['xl'], pady=(SPACING['lg'], SPACING['md']))

        self.title_label = tk.Label(header_frame,
                                    text="Item Group Master",
                                    font=FONTS['h1'],
                                    bg=self.colors['background'],
                                    fg=self.colors['text_primary'])
        self.title_label.pack(side=tk.LEFT)

        self.create_btn = tk.Button(header_frame,
                                    text="Create New Item Group")
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
        """Create the table view for item groups"""
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
            ("Item Group Code", 15),
            ("Item Group Name", 40),
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

    def load_item_groups(self):
        """Load item groups from database and display in table"""
        # Clear existing rows
        for widget in self.table_body.winfo_children():
            widget.destroy()

        # Get item groups
        item_groups = self.item_group_handler.get_all_item_groups()

        if not item_groups:
            # No item groups found
            no_data_label = tk.Label(self.table_body,
                                    text="No item groups found. Click 'Create New Item Group' to add one.",
                                    font=FONTS['body'],
                                    bg=self.colors['background'],
                                    fg=self.colors['text_tertiary'],
                                    pady=SPACING['xxl'])
            no_data_label.pack(fill=tk.BOTH)
            return

        # Display item groups
        for idx, item_group in enumerate(item_groups, 1):
            self.create_table_row(idx, item_group)

    def create_table_row(self, sr_no, item_group):
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

        # Item Group Code
        code_label = tk.Label(row_frame, text=item_group['item_group_code'],
                             font=FONTS['body_bold'],
                             bg=row_bg,
                             fg=self.colors['primary'],
                             width=15,
                             anchor='w',
                             padx=SPACING['md'])
        code_label.pack(side=tk.LEFT, padx=SPACING['sm'])
        code_label.bind('<Enter>', on_enter)
        code_label.bind('<Leave>', on_leave)

        # Item Group Name
        name_label = tk.Label(row_frame, text=item_group['item_group_name'],
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
        status_color = self.colors['success'] if item_group['status'] == 'Active' else self.colors['error']
        status_label = tk.Label(row_frame,
                               text=item_group['status'],
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
                            command=lambda: self.show_edit_form(item_group['id']))
        edit_btn.pack(side=tk.LEFT, padx=SPACING['md'])

        # Hover effect for edit button
        def on_btn_enter(e):
            edit_btn.config(bg=self.colors['primary_hover'])
        def on_btn_leave(e):
            edit_btn.config(bg=self.colors['primary'])

        edit_btn.bind('<Enter>', on_btn_enter)
        edit_btn.bind('<Leave>', on_btn_leave)

    def show_create_form(self):
        """Show the create item group form"""
        self.current_view = 'form'
        self.edit_item_group_id = None

        # Hide create button and change title
        self.create_btn.pack_forget()
        self.title_label.config(text="Create New Item Group")

        # Show form
        from item_group_form import ItemGroupForm
        self.show_form(None)

    def show_edit_form(self, item_group_id):
        """Show the edit item group form"""
        self.current_view = 'form'
        self.edit_item_group_id = item_group_id

        # Hide create button and change title
        self.create_btn.pack_forget()
        self.title_label.config(text="Edit Item Group")

        # Get item group data
        item_group_data = self.item_group_handler.get_item_group_by_id(item_group_id)

        if not item_group_data:
            messagebox.showerror("Error", "Item Group not found")
            self.show_list_view()
            return

        # Show form
        self.show_form(item_group_data)

    def show_form(self, item_group_data):
        """Show item group form (create or edit)"""
        # Clear content container
        for widget in self.content_container.winfo_children():
            widget.destroy()

        # Import and create form
        from item_group_form import ItemGroupForm

        form = ItemGroupForm(
            self.content_container,
            self.colors,
            self.item_group_handler,
            item_group_data,
            self.on_form_save,
            self.on_form_cancel
        )
        form.pack(fill=tk.BOTH, expand=True)

    def on_form_save(self):
        """Callback when form is saved"""
        self.show_list_view()
        self.load_item_groups()

    def on_form_cancel(self):
        """Callback when form is cancelled"""
        self.show_list_view()

    def show_list_view(self):
        """Show the list view"""
        self.current_view = 'list'
        self.edit_item_group_id = None

        # Show create button and restore title
        self.create_btn.pack(side=tk.RIGHT)
        self.title_label.config(text="Item Group Master")

        # Recreate table view
        self.create_table_view()
        self.load_item_groups()

    def __del__(self):
        """Cleanup when widget is destroyed"""
        if hasattr(self, 'item_group_handler'):
            self.item_group_handler.disconnect()
