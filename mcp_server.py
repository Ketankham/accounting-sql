#!/usr/bin/env python3
"""
Enhanced Tkinter MCP Server with Application Plan Support
Understands your complete application structure and auto-generates:
- Database schemas with relationships
- CRUD forms (Create/Read/Update/Delete)
- Table viewers with edit capability
- Complete database operations
"""

import os
import sys
import json
from pathlib import Path
from typing import List, Dict
from datetime import datetime
from dataclasses import dataclass, asdict

try:
    from mcp.server.fastmcp import FastMCP
except ImportError:
    print("Error: FastMCP package not installed. Install with: pip install fastmcp")
    sys.exit(1)


@dataclass
class Entity:
    """Represents a database entity/table"""
    name: str  # e.g., "users", "products"
    fields: Dict[str, str]  # {field_name: field_type}
    description: str = ""
    operations: List[str] = None  # ['create', 'read', 'update', 'delete']

    def __post_init__(self):
        if self.operations is None:
            self.operations = ['create', 'read', 'update', 'delete']


@dataclass
class ApplicationPlan:
    """Represents the complete application plan"""
    app_name: str
    description: str
    entities: List[Entity]  # Your tables/forms
    relationships: Dict[str, str] = None  # {table1: table2, ...}
    created_at: str = None

    def __post_init__(self):
        if self.relationships is None:
            self.relationships = {}
        if self.created_at is None:
            self.created_at = datetime.now().isoformat()


class ApplicationPlanManager:
    """Manages your application plan"""

    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.plan_file = self.project_root / "app_plan.json"

    def save_plan(self, plan: ApplicationPlan) -> str:
        """Save application plan to file"""
        plan_dict = {
            "app_name": plan.app_name,
            "description": plan.description,
            "entities": [
                {
                    "name": e.name,
                    "fields": e.fields,
                    "description": e.description,
                    "operations": e.operations
                }
                for e in plan.entities
            ],
            "relationships": plan.relationships,
            "created_at": plan.created_at
        }

        with open(self.plan_file, 'w') as f:
            json.dump(plan_dict, f, indent=2)

        return str(self.plan_file)

    def load_plan(self) -> ApplicationPlan:
        """Load application plan from file"""
        if not self.plan_file.exists():
            return None

        with open(self.plan_file, 'r') as f:
            data = json.load(f)

        entities = [
            Entity(
                name=e["name"],
                fields=e["fields"],
                description=e.get("description", ""),
                operations=e.get("operations", ['create', 'read', 'update', 'delete'])
            )
            for e in data["entities"]
        ]

        return ApplicationPlan(
            app_name=data["app_name"],
            description=data["description"],
            entities=entities,
            relationships=data.get("relationships", {}),
            created_at=data.get("created_at")
        )


class CRUDGenerator:
    """Generates complete CRUD interface for an entity"""

    @staticmethod
    def generate_form_with_operations(entity: Entity) -> str:
        """Generate form class for CREATE/EDIT with all CRUD operations"""

        form_name = f"{entity.name.title()}Form"
        entity_name = entity.name
        entity_title = entity.name.title()

        code = f'''import tkinter as tk
from tkinter import ttk, messagebox
from database.connection import Database


class {form_name}:
    """Auto-generated CRUD form for {entity_name}"""

    def __init__(self, parent, db: Database = None, entry_id: int = None):
        """
        Initialize form

        Args:
            parent: Parent window
            db: Database connection
            entry_id: ID of entry to edit (None for create)
        """
        self.parent = parent
        self.db = db or Database()
        self.entry_id = entry_id
        self.is_edit_mode = entry_id is not None

        # Create main frame
        self.frame = ttk.Frame(parent, padding="10")
        self.frame.pack(fill="both", expand=True)

        # Title
        title = "Edit {entity_title}" if self.is_edit_mode else "New {entity_title}"
        ttk.Label(self.frame, text=title, font=("Arial", 14, "bold")).grid(
            row=0, column=0, columnspan=2, pady=10
        )

        # Form fields
        self.field_vars = {{}}
        self.setup_fields()

        # Load existing data if editing
        if self.is_edit_mode:
            self.load_data()

        # Buttons
        self.setup_buttons()

    def setup_fields(self):
        """Create form fields"""
'''

        row = 1
        for field_name, field_type in entity.fields.items():
            if field_name in ['id', 'created_at', 'updated_at']:
                continue  # Skip auto fields

            label = field_name.replace('_', ' ').title()
            code += f'''
        # {label}
        ttk.Label(self.frame, text="{label}:").grid(row={row}, column=0, sticky="w", padx=5, pady=5)
        self.field_vars["{field_name}"] = tk.StringVar()
'''

            # Different input types based on field_type
            if 'int' in field_type.lower() or 'real' in field_type.lower():
                code += f'''        ttk.Entry(self.frame, textvariable=self.field_vars["{field_name}"]).grid(
            row={row}, column=1, sticky="ew", padx=5, pady=5
        )
'''
            elif 'bool' in field_type.lower():
                code += f'''        ttk.Checkbutton(
            self.frame, variable=self.field_vars["{field_name}"]
        ).grid(row={row}, column=1, sticky="w", padx=5, pady=5)
'''
            else:
                code += f'''        ttk.Entry(self.frame, textvariable=self.field_vars["{field_name}"]).grid(
            row={row}, column=1, sticky="ew", padx=5, pady=5
        )
'''

            row += 1

        code += f'''
        self.frame.columnconfigure(1, weight=1)

    def setup_buttons(self):
        """Create action buttons"""
        button_frame = ttk.Frame(self.frame)
        button_frame.grid(row={row}, column=0, columnspan=2, pady=20)

        if self.is_edit_mode:
            ttk.Button(button_frame, text="Update", command=self.on_update).pack(side="left", padx=5)
            ttk.Button(button_frame, text="Delete", command=self.on_delete).pack(side="left", padx=5)
        else:
            ttk.Button(button_frame, text="Create", command=self.on_create).pack(side="left", padx=5)

        ttk.Button(button_frame, text="Cancel", command=self.on_cancel).pack(side="left", padx=5)

    def load_data(self):
        """Load existing entry data for editing"""
        query = "SELECT * FROM {entity_name} WHERE id = ?"
        result = self.db.execute(query, (self.entry_id,))

        if result:
            row = result[0]
            for field_name in self.field_vars.keys():
                if field_name in row.keys():
                    self.field_vars[field_name].set(str(row[field_name]))

    def get_data(self) -> dict:
        """Get form data as dictionary"""
        return {{
            field_name: self.field_vars[field_name].get()
            for field_name in self.field_vars.keys()
        }}

    def on_create(self):
        """Handle create operation"""
        data = self.get_data()

        # Validate
        if not all(data.values()):
            messagebox.showwarning("Validation", "All fields are required")
            return

        # Build INSERT query
        columns = ", ".join(data.keys())
        placeholders = ", ".join(["?" for _ in data])
        query = f"INSERT INTO {entity_name} ({{columns}}) VALUES ({{placeholders}})"

        try:
            self.db.execute(query, tuple(data.values()))
            messagebox.showinfo("Success", "{entity_title} created successfully")
            self.on_cancel()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create: {{str(e)}}")

    def on_update(self):
        """Handle update operation"""
        data = self.get_data()

        # Validate
        if not all(data.values()):
            messagebox.showwarning("Validation", "All fields are required")
            return

        # Build UPDATE query
        set_clause = ", ".join([f"{{col}} = ?" for col in data.keys()])
        query = f"UPDATE {entity_name} SET {{set_clause}} WHERE id = ?"

        try:
            values = list(data.values()) + [self.entry_id]
            self.db.execute(query, tuple(values))
            messagebox.showinfo("Success", "{entity_title} updated successfully")
            self.on_cancel()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update: {{str(e)}}")

    def on_delete(self):
        """Handle delete operation"""
        if messagebox.askyesno("Confirm Delete", "Are you sure?"):
            query = f"DELETE FROM {entity_name} WHERE id = ?"
            try:
                self.db.execute(query, (self.entry_id,))
                messagebox.showinfo("Success", "{entity_title} deleted successfully")
                self.on_cancel()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete: {{str(e)}}")

    def on_cancel(self):
        """Close form"""
        self.frame.destroy()
'''

        return code

    @staticmethod
    def generate_table_viewer(entity: Entity) -> str:
        """Generate table viewer with edit capability"""

        viewer_name = f"{entity.name.title()}Table"
        entity_name = entity.name
        entity_title = entity.name.title()
        fields_list = str(list(entity.fields.keys()))

        code = f'''import tkinter as tk
from tkinter import ttk
from database.connection import Database
from forms.{entity_title}Form import {entity_title}Form


class {viewer_name}:
    """Auto-generated table viewer for {entity_name}"""

    def __init__(self, parent, db: Database = None):
        """
        Initialize table viewer

        Args:
            parent: Parent window
            db: Database connection
        """
        self.parent = parent
        self.db = db or Database()
        self.selected_id = None

        # Create main frame
        self.frame = ttk.Frame(parent, padding="10")
        self.frame.pack(fill="both", expand=True)

        # Title and buttons
        self.setup_header()

        # Table
        self.setup_table()

        # Load data
        self.refresh_data()

    def setup_header(self):
        """Create header with buttons"""
        header_frame = ttk.Frame(self.frame)
        header_frame.pack(fill="x", pady=10)

        ttk.Label(header_frame, text="{entity_title} List", font=("Arial", 12, "bold")).pack(side="left")

        ttk.Button(header_frame, text="+ New", command=self.on_new).pack(side="right", padx=5)
        ttk.Button(header_frame, text="Edit", command=self.on_edit).pack(side="right", padx=5)
        ttk.Button(header_frame, text="Refresh", command=self.refresh_data).pack(side="right", padx=5)

    def setup_table(self):
        """Create Treeview table"""
        # Define columns
        all_columns = {fields_list}
        columns = [col for col in all_columns if col not in ['created_at', 'updated_at']]

        self.tree = ttk.Treeview(self.frame, columns=columns, height=15)
        self.tree.column("#0", width=0, stretch=tk.NO)
        self.tree.heading("#0", text="")

        # Configure columns
        for col in columns:
            self.tree.column(col, anchor=tk.W, width=100)
            self.tree.heading(col, text=col.title())

        # Scrollbars
        scrollbar = ttk.Scrollbar(self.frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)

        # Pack
        self.tree.pack(fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Bind events
        self.tree.bind("<Button-1>", self.on_row_select)
        self.tree.bind("<Double-1>", self.on_row_double_click)

    def refresh_data(self):
        """Load data from database"""
        # Clear existing
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Query
        query = f"SELECT * FROM {entity_name}"
        try:
            results = self.db.execute(query)

            for row in results:
                values = [row[i] for i in range(len({fields_list}))]
                self.tree.insert("", tk.END, values=values)
        except Exception as e:
            print(f"Error loading data: {{e}}")

    def on_row_select(self, event):
        """Handle row selection"""
        selection = self.tree.selection()
        if selection:
            item = selection[0]
            values = self.tree.item(item)['values']
            self.selected_id = values[0]  # Assuming first column is ID

    def on_row_double_click(self, event):
        """Open edit form on double-click"""
        self.on_edit()

    def on_new(self):
        """Open new entry form"""
        new_window = tk.Toplevel(self.parent)
        new_window.title("New {entity_title}")
        new_window.geometry("400x300")

        form = {entity_title}Form(new_window, self.db)

        # Refresh after close
        new_window.wait_window()
        self.refresh_data()

    def on_edit(self):
        """Open edit form for selected entry"""
        if not self.selected_id:
            return

        edit_window = tk.Toplevel(self.parent)
        edit_window.title("Edit {entity_title}")
        edit_window.geometry("400x300")

        form = {entity_title}Form(edit_window, self.db, self.selected_id)

        # Refresh after close
        edit_window.wait_window()
        self.refresh_data()
'''

        return code


class SchemaMigrationGenerator:
    """Generates complete database schema from application plan"""

    @staticmethod
    def generate_migration(entities: List[Entity]) -> str:
        """Generate SQL migration for all entities"""

        sql = "-- Auto-generated database schema\n"
        sql += f"-- Generated: {datetime.now().isoformat()}\n\n"

        for entity in entities:
            sql += f"CREATE TABLE IF NOT EXISTS {entity.name} (\n"
            sql += "    id INTEGER PRIMARY KEY AUTOINCREMENT,\n"

            for field_name, field_type in entity.fields.items():
                if field_name not in ['id', 'created_at', 'updated_at']:
                    sql += f"    {field_name} {field_type},\n"

            sql += "    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,\n"
            sql += "    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP\n"
            sql += ");\n\n"

        return sql


# Initialize FastMCP Server
mcp = FastMCP("tkinter-crud-generator")


@mcp.tool()
def save_application_plan(
    project_root: str,
    app_name: str,
    app_description: str,
    entities: List[Dict]
) -> str:
    """Save your complete application plan. Define all entities, fields, and operations."""

    entity_objects = [
        Entity(
            name=e["name"],
            fields=e["fields"],
            description=e.get("description", ""),
            operations=e.get("operations", ['create', 'read', 'update', 'delete'])
        )
        for e in entities
    ]

    plan = ApplicationPlan(
        app_name=app_name,
        description=app_description,
        entities=entity_objects
    )

    manager = ApplicationPlanManager(project_root)
    plan_file = manager.save_plan(plan)

    return f"Application plan saved to: {plan_file}\n\nPlan:\n{json.dumps(asdict(plan), indent=2, default=str)}"


@mcp.tool()
def load_application_plan(project_root: str) -> str:
    """Load your saved application plan"""

    manager = ApplicationPlanManager(project_root)
    plan = manager.load_plan()

    if not plan:
        return "No application plan found. Use save_application_plan first."

    return f"Loaded plan:\n{json.dumps(asdict(plan), indent=2, default=str)}"


@mcp.tool()
def generate_crud_forms(project_root: str) -> str:
    """Generate complete CRUD forms for all entities in your plan"""

    manager = ApplicationPlanManager(project_root)
    plan = manager.load_plan()

    if not plan:
        raise ValueError("No application plan found.")

    forms_dir = Path(project_root) / "forms"
    forms_dir.mkdir(exist_ok=True)

    created_files = []
    for entity in plan.entities:
        if 'create' in entity.operations or 'update' in entity.operations:
            form_code = CRUDGenerator.generate_form_with_operations(entity)
            form_file = forms_dir / f"{entity.name.title()}Form.py"
            with open(form_file, 'w') as f:
                f.write(form_code)
            created_files.append(str(form_file))

    return f"Generated {len(created_files)} CRUD forms:\n" + "\n".join(created_files)


@mcp.tool()
def generate_table_viewers(project_root: str) -> str:
    """Generate table viewers with edit capability for all entities"""

    manager = ApplicationPlanManager(project_root)
    plan = manager.load_plan()

    if not plan:
        raise ValueError("No application plan found.")

    tables_dir = Path(project_root) / "tables"
    tables_dir.mkdir(exist_ok=True)

    created_files = []
    for entity in plan.entities:
        if 'read' in entity.operations:
            table_code = CRUDGenerator.generate_table_viewer(entity)
            table_file = tables_dir / f"{entity.name.title()}Table.py"
            with open(table_file, 'w') as f:
                f.write(table_code)
            created_files.append(str(table_file))

    return f"Generated {len(created_files)} table viewers:\n" + "\n".join(created_files)


@mcp.tool()
def generate_database_schema(project_root: str) -> str:
    """Generate complete database schema migration from your plan"""

    manager = ApplicationPlanManager(project_root)
    plan = manager.load_plan()

    if not plan:
        raise ValueError("No application plan found.")

    schema_sql = SchemaMigrationGenerator.generate_migration(plan.entities)

    migrations_dir = Path(project_root) / "migrations"
    migrations_dir.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    migration_file = migrations_dir / f"{timestamp}_create_schema.sql"

    with open(migration_file, 'w') as f:
        f.write(schema_sql)

    return f"Schema migration created:\n{migration_file}\n\n{schema_sql}"


@mcp.tool()
def generate_complete_crud_system(project_root: str) -> str:
    """One-shot: Generate forms + tables + schema for entire application"""

    manager = ApplicationPlanManager(project_root)
    plan = manager.load_plan()

    if not plan:
        raise ValueError("No application plan found.")

    results = []

    # Generate forms
    forms_dir = Path(project_root) / "forms"
    forms_dir.mkdir(exist_ok=True)
    for entity in plan.entities:
        form_code = CRUDGenerator.generate_form_with_operations(entity)
        form_file = forms_dir / f"{entity.name.title()}Form.py"
        with open(form_file, 'w') as f:
            f.write(form_code)
        results.append(f"✓ Form: {form_file.name}")

    # Generate tables
    tables_dir = Path(project_root) / "tables"
    tables_dir.mkdir(exist_ok=True)
    for entity in plan.entities:
        table_code = CRUDGenerator.generate_table_viewer(entity)
        table_file = tables_dir / f"{entity.name.title()}Table.py"
        with open(table_file, 'w') as f:
            f.write(table_code)
        results.append(f"✓ Table: {table_file.name}")

    # Generate schema
    schema_sql = SchemaMigrationGenerator.generate_migration(plan.entities)
    migrations_dir = Path(project_root) / "migrations"
    migrations_dir.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    migration_file = migrations_dir / f"{timestamp}_create_schema.sql"
    with open(migration_file, 'w') as f:
        f.write(schema_sql)
    results.append(f"✓ Schema: {migration_file.name}")

    return f"✅ Complete CRUD system generated!\n\n" + "\n".join(results) + f"\n\nYour project now has:\n- {len(plan.entities)} forms\n- {len(plan.entities)} table viewers\n- 1 database schema"


if __name__ == "__main__":
    mcp.run()
