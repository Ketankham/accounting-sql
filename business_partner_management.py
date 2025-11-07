"""
Business Partner Management Screen - List, Create, Edit Business Partners
"""

import tkinter as tk
from tkinter import ttk, messagebox
from database.business_partner_handler import BusinessPartnerHandler
from ui_config import COLORS, FONTS, SPACING, LAYOUT, BUTTON_STYLES


class BusinessPartnerManagement(tk.Frame):
    def __init__(self, parent, colors):
        super().__init__(parent, bg=COLORS['background'])
        self.colors = COLORS
        self.bp_handler = BusinessPartnerHandler()

        # Connect to database
        if not self.bp_handler.connect():
            messagebox.showerror("Database Error",
                               "Failed to connect to database.")
            return

        # Current view state
        self.current_view = 'list'  # 'list' or 'form'
        self.edit_bp_id = None

        # Create UI
        self.create_widgets()
        self.load_business_partners()

    def create_widgets(self):
        """Create the business partner management UI"""
        # Header
        header_frame = tk.Frame(self, bg=self.colors['background'])
        header_frame.pack(fill=tk.X, padx=SPACING['xl'], pady=(SPACING['lg'], SPACING['md']))

        self.title_label = tk.Label(header_frame,
                                    text="Business Partner",
                                    font=FONTS['h1'],
                                    bg=self.colors['background'],
                                    fg=self.colors['text_primary'])
        self.title_label.pack(side=tk.LEFT)

        self.create_btn = tk.Button(header_frame,
                                    text="Create New Business Partner")
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
        """Create the table view for business partners"""
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
            ("Sr.", 3),
            ("BP Code", 7),
            ("BP Name", 12),
            ("City", 8),
            ("State", 8),
            ("Mobile", 10),
            ("Opening Bal.", 8),
            ("Status", 6),
            ("Action", 6)
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

    def load_business_partners(self):
        """Load business partners from database and display in table"""
        # Clear existing rows
        for widget in self.table_body.winfo_children():
            widget.destroy()

        # Get business partners
        partners = self.bp_handler.get_all_business_partners()

        if not partners:
            # No business partners found
            no_data_label = tk.Label(self.table_body,
                                    text="No business partners found. Click 'Create New Business Partner' to add one.",
                                    font=FONTS['body'],
                                    bg=self.colors['background'],
                                    fg=self.colors['text_tertiary'],
                                    pady=SPACING['xxl'])
            no_data_label.pack(fill=tk.BOTH)
            return

        # Display business partners
        for idx, partner in enumerate(partners, 1):
            self.create_table_row(idx, partner)

    def create_table_row(self, sr_no, partner):
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
                if isinstance(widget, (tk.Label, tk.Frame)) and widget not in [edit_btn, delete_btn]:
                    widget.config(bg='#DBEAFE')

        def on_leave(e):
            row_frame.config(bg=row_bg)
            for widget in row_frame.winfo_children():
                if isinstance(widget, (tk.Label, tk.Frame)) and widget not in [edit_btn, delete_btn]:
                    widget.config(bg=row_bg)

        row_frame.bind('<Enter>', on_enter)
        row_frame.bind('<Leave>', on_leave)

        # Serial number
        sr_label = tk.Label(row_frame, text=str(sr_no),
                           font=FONTS['body'],
                           bg=row_bg,
                           fg=self.colors['text_primary'],
                           width=3,
                           anchor='w',
                           padx=SPACING['md'])
        sr_label.pack(side=tk.LEFT, padx=SPACING['xs'])
        sr_label.bind('<Enter>', on_enter)
        sr_label.bind('<Leave>', on_leave)

        # BP Code
        code_label = tk.Label(row_frame, text=partner.get('bp_code', 'N/A'),
                             font=FONTS['body'],
                             bg=row_bg,
                             fg=self.colors['text_primary'],
                             width=7,
                             anchor='w',
                             padx=SPACING['md'])
        code_label.pack(side=tk.LEFT, padx=SPACING['xs'])
        code_label.bind('<Enter>', on_enter)
        code_label.bind('<Leave>', on_leave)

        # BP Name
        name_label = tk.Label(row_frame, text=partner.get('bp_name', 'N/A'),
                             font=FONTS['body'],
                             bg=row_bg,
                             fg=self.colors['text_primary'],
                             width=12,
                             anchor='w',
                             padx=SPACING['md'])
        name_label.pack(side=tk.LEFT, padx=SPACING['xs'])
        name_label.bind('<Enter>', on_enter)
        name_label.bind('<Leave>', on_leave)

        # City
        city_label = tk.Label(row_frame, text=partner.get('city_name', 'N/A'),
                             font=FONTS['body'],
                             bg=row_bg,
                             fg=self.colors['text_primary'],
                             width=8,
                             anchor='w',
                             padx=SPACING['md'])
        city_label.pack(side=tk.LEFT, padx=SPACING['xs'])
        city_label.bind('<Enter>', on_enter)
        city_label.bind('<Leave>', on_leave)

        # State
        state_label = tk.Label(row_frame, text=partner.get('state_name', 'N/A'),
                              font=FONTS['body'],
                              bg=row_bg,
                              fg=self.colors['text_primary'],
                              width=8,
                              anchor='w',
                              padx=SPACING['md'])
        state_label.pack(side=tk.LEFT, padx=SPACING['xs'])
        state_label.bind('<Enter>', on_enter)
        state_label.bind('<Leave>', on_leave)

        # Mobile
        mobile_label = tk.Label(row_frame, text=partner.get('mobile', 'N/A'),
                               font=FONTS['body'],
                               bg=row_bg,
                               fg=self.colors['text_primary'],
                               width=10,
                               anchor='w',
                               padx=SPACING['md'])
        mobile_label.pack(side=tk.LEFT, padx=SPACING['xs'])
        mobile_label.bind('<Enter>', on_enter)
        mobile_label.bind('<Leave>', on_leave)

        # Opening Balance
        balance_text = f"{partner.get('opening_balance', 0)} {partner.get('balance_type', 'Debit')[0]}"
        balance_label = tk.Label(row_frame, text=balance_text,
                                font=FONTS['body'],
                                bg=row_bg,
                                fg=self.colors['text_primary'],
                                width=8,
                                anchor='w',
                                padx=SPACING['md'])
        balance_label.pack(side=tk.LEFT, padx=SPACING['xs'])
        balance_label.bind('<Enter>', on_enter)
        balance_label.bind('<Leave>', on_leave)

        # Status
        status = partner.get('status', 'N/A')
        status_color = '#10B981' if status == 'Active' else '#EF4444'
        status_label = tk.Label(row_frame, text=status,
                               font=FONTS['body'],
                               bg=row_bg,
                               fg=status_color,
                               width=6,
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

        # Edit button
        edit_btn = tk.Button(action_frame, text="Edit",
                            font=FONTS['small'],
                            bg=self.colors['primary'],
                            fg='white',
                            activebackground=self.colors['primary_hover'],
                            activeforeground='white',
                            cursor='hand2',
                            relief=tk.FLAT,
                            padx=SPACING['sm'],
                            pady=SPACING['xs'],
                            command=lambda: self.show_edit_form(partner['id']))
        edit_btn.pack(side=tk.LEFT, padx=(0, SPACING['xs']))

        # Delete button
        delete_btn = tk.Button(action_frame, text="Delete",
                              font=FONTS['small'],
                              bg='#EF4444',
                              fg='white',
                              activebackground='#DC2626',
                              activeforeground='white',
                              cursor='hand2',
                              relief=tk.FLAT,
                              padx=SPACING['sm'],
                              pady=SPACING['xs'],
                              command=lambda: self.delete_business_partner(partner['id'], partner['bp_name']))
        delete_btn.pack(side=tk.LEFT)

    def show_create_form(self):
        """Show create business partner form"""
        # Clear content container
        for widget in self.content_container.winfo_children():
            widget.destroy()

        # Update title
        self.title_label.config(text="Create New Business Partner")

        # Hide create button
        self.create_btn.pack_forget()

        # Import and create form
        from business_partner_form import BusinessPartnerForm

        form = BusinessPartnerForm(
            self.content_container,
            self.colors,
            self.bp_handler,
            None,  # No existing data
            on_save=self.on_form_save,
            on_cancel=self.on_form_cancel
        )
        form.pack(fill=tk.BOTH, expand=True)

        self.current_view = 'form'

    def show_edit_form(self, bp_id):
        """Show edit business partner form"""
        # Get business partner data
        bp_data = self.bp_handler.get_business_partner_by_id(bp_id)

        if not bp_data:
            messagebox.showerror("Error", "Business Partner not found")
            return

        # Clear content container
        for widget in self.content_container.winfo_children():
            widget.destroy()

        # Update title
        self.title_label.config(text=f"Edit Business Partner: {bp_data['bp_name']}")

        # Hide create button
        self.create_btn.pack_forget()

        # Import and create form
        from business_partner_form import BusinessPartnerForm

        form = BusinessPartnerForm(
            self.content_container,
            self.colors,
            self.bp_handler,
            bp_data,
            on_save=self.on_form_save,
            on_cancel=self.on_form_cancel
        )
        form.pack(fill=tk.BOTH, expand=True)

        self.current_view = 'form'
        self.edit_bp_id = bp_id

    def on_form_save(self):
        """Handle form save"""
        # Return to list view
        self.on_form_cancel()

    def on_form_cancel(self):
        """Handle form cancel"""
        # Update title
        self.title_label.config(text="Business Partner")

        # Show create button
        self.create_btn.pack(side=tk.RIGHT)

        # Recreate table view
        self.create_table_view()
        self.load_business_partners()

        self.current_view = 'list'
        self.edit_bp_id = None

    def delete_business_partner(self, bp_id, bp_name):
        """Delete a business partner"""
        result = messagebox.askyesno("Confirm Delete",
                                     f"Are you sure you want to delete '{bp_name}'?\n\n" +
                                     "This action cannot be undone.")

        if result:
            success, message = self.bp_handler.delete_business_partner(bp_id)
            if success:
                messagebox.showinfo("Success", message)
                self.load_business_partners()
            else:
                messagebox.showerror("Error", message)
