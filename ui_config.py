"""
UI Configuration - Comfort-Oriented Unified Design System (Tkinter-Compatible)
Optimized for long-term daily use with low-contrast neutrals and ergonomic typography.
"""

# =============================================================================
# COLOR PALETTE — Eye-Friendly Neutrals + Muted Accents
# =============================================================================

COLORS = {
    'primary': '#3A7BD5',           # Calm blue
    'primary_hover': '#2E66B2',     # Darker blue
    'primary_light': '#E6F0FB',     # Gentle light blue
    'primary_dark': '#224E7A',      # Deep navy

    'background': '#F4F6F8',        # Neutral light gray (reduced glare)
    'surface': '#FFFFFF',           # Clean white surface
    'sidebar': '#ECEFF3',           # Light gray-blue sidebar

    'border': '#CDD5DF',            # Neutral soft border
    'border_light': '#E3E7ED',      # Subtle light border
    'border_dark': '#9AA5B1',       # For dividers or tables

    'text_primary': '#1E293B',      # Off-black
    'text_secondary': '#475569',    # Medium gray-blue
    'text_tertiary': '#64748B',     # Muted blue-gray
    'text_disabled': '#94A3B8',     # Dimmed gray

    'success': '#22C55E',
    'success_bg': '#DCFCE7',
    'error': '#EF4444',
    'error_bg': '#FEE2E2',
    'warning': '#F59E0B',
    'warning_bg': '#FEF3C7',
    'info': '#3B82F6',
    'info_bg': '#DBEAFE',
}


# =============================================================================
# SPACING
# =============================================================================

SPACING = {
    'xs': 4,
    'sm': 8,
    'md': 16,
    'lg': 24,
    'xl': 32,
    'xxl': 48,
}


# =============================================================================
# TYPOGRAPHY — Tkinter-Compatible
# =============================================================================

# ⚠️ Tkinter supports only: weight=("normal" | "bold")
# We’ll use “bold” sparingly and default to “normal” for most text

FONTS = {
    'display': ('Segoe UI', 22, 'bold'),
    'h1': ('Segoe UI', 18, 'bold'),
    'h2': ('Segoe UI', 14, 'bold'),
    'h3': ('Segoe UI', 12, 'bold'),

    'body': ('Segoe UI', 11, 'normal'),
    'body_bold': ('Segoe UI', 11, 'bold'),
    'body_large': ('Segoe UI', 13, 'normal'),

    'small': ('Segoe UI', 9, 'normal'),
    'small_bold': ('Segoe UI', 9, 'bold'),
    'small_italic': ('Segoe UI', 9, 'italic'),
    'caption': ('Segoe UI', 8, 'normal'),

    'button': ('Segoe UI', 11, 'bold'),
    'button_large': ('Segoe UI', 12, 'bold'),
    'menu': ('Segoe UI', 11, 'bold'),
    'submenu': ('Segoe UI', 10, 'normal'),
}


# =============================================================================
# COMPONENT STYLES
# =============================================================================

BUTTON_STYLES = {
    'primary': {
        'bg': COLORS['primary'],
        'fg': 'white',
        'activebackground': COLORS['primary_hover'],
        'activeforeground': 'white',
        'relief': 'flat',
        'cursor': 'hand2',
        'padx': 20,
        'pady': 10,
        'font': FONTS['button'],
        'borderwidth': 0,
    },
    'secondary': {
        'bg': COLORS['surface'],
        'fg': COLORS['text_primary'],
        'activebackground': COLORS['border_light'],
        'activeforeground': COLORS['text_primary'],
        'relief': 'groove',
        'cursor': 'hand2',
        'padx': 20,
        'pady': 10,
        'font': FONTS['button'],
        'borderwidth': 1,
        'highlightthickness': 0,
    },
    'danger': {
        'bg': COLORS['error'],
        'fg': 'white',
        'activebackground': '#DC2626',
        'activeforeground': 'white',
        'relief': 'flat',
        'cursor': 'hand2',
        'padx': 28,
        'pady': 12,
        'font': FONTS['button'],
    },
    'small': {
        'bg': COLORS['border_light'],
        'fg': COLORS['text_primary'],
        'activebackground': COLORS['border'],
        'activeforeground': COLORS['text_primary'],
        'relief': 'flat',
        'cursor': 'hand2',
        'padx': 16,
        'pady': 8,
        'font': FONTS['small_bold'],
    },
}


INPUT_STYLES = {
    'entry': {
        'font': ('Segoe UI', 12, 'normal'),          # Slightly smaller font
        'relief': 'flat',
        'borderwidth': 1,
        'highlightthickness': 1,
        'highlightbackground': '#D0D7E2',            # Subtle gray border
        'highlightcolor': '#3A7BD5',                 # Blue focus border
        'background': '#FFFFFF',
        'foreground': '#1E293B',
        'insertbackground': '#1E293B',               # Cursor color
        'ipadx': 6,                                  # Horizontal padding inside
        'ipady': 4,                                  # Vertical padding (reduced)
    },
    'text': {
        'font': ('Segoe UI', 12, 'normal'),
        'relief': 'flat',
        'borderwidth': 1,
        'wrap': 'word',
        'background': '#FFFFFF',
        'highlightthickness': 1,
        'highlightbackground': '#D0D7E2',
        'highlightcolor': '#3A7BD5',
        'padx': 6,
        'pady': 4,
    },
}

CARD_STYLES = {
    'default': {
        'bg': COLORS['surface'],
        'relief': 'flat',
        'borderwidth': 1,
        'padx': SPACING['lg'],
        'pady': SPACING['lg'],
    },
    'elevated': {
        'bg': COLORS['surface'],
        'relief': 'solid',
        'borderwidth': 1,
        'padx': SPACING['lg'],
        'pady': SPACING['lg'],
    },
}


# =============================================================================
# LAYOUT
# =============================================================================

LAYOUT = {
    'login_width': 480,
    'login_height': 660,
    'dashboard_width': 1440,
    'dashboard_height': 920,

    'header_height': 72,
    'footer_height': 48,
    'sidebar_width': 260,
    'button_height': 44,
    'input_height': 44,
    'table_row_height': 56,
    'table_header_height': 52,

    'border_width': 1,
    'border_width_light': 0.5,
}


# =============================================================================
# ANIMATION (conceptual for Tkinter)
# =============================================================================

ANIMATION = {
    'duration_fast': 120,
    'duration_normal': 220,
    'duration_slow': 350,
}


# =============================================================================
# ACCESSIBILITY
# =============================================================================

ACCESSIBILITY = {
    'min_touch_target': 44,
    'focus_outline_width': 3,
    'focus_outline_color': COLORS['primary'],
    'contrast_ratio_min': 4.5,
}


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def apply_button_style(button, style='primary'):
    """Apply a button style to a tkinter Button widget."""
    if style in BUTTON_STYLES:
        button.config(**BUTTON_STYLES[style])


def get_hover_handlers(widget, normal_bg, hover_bg):
    """Return hover enter/leave event handlers for a widget."""
    def on_enter(e):
        widget.config(bg=hover_bg)
    def on_leave(e):
        widget.config(bg=normal_bg)
    return on_enter, on_leave


def configure_entry_style(entry_widget):
    """Placeholder for ttk.Entry custom theme configuration."""
    pass
