# ruff: noqa: E501

"""Glacial design tokens shared by every QWidget-based surface."""

from dataclasses import dataclass

SPACING_SMALL = 8
SPACING_MEDIUM = 16
SPACING_LARGE = 28
RADIUS_SMALL = 8
RADIUS_MEDIUM = 14
RADIUS_LARGE = 20


@dataclass(frozen=True, slots=True)
class ThemeColors:
    background: str
    surface: str
    surface_elevated: str
    text: str
    muted_text: str
    border: str
    accent: str
    accent_soft: str
    positive: str
    negative: str


DARK_COLORS = ThemeColors(
    background="#07141f",
    surface="#0c1e2d",
    surface_elevated="#102a3d",
    text="#eaf7ff",
    muted_text="#9ab4c6",
    border="#23455d",
    accent="#55d9ff",
    accent_soft="#153e56",
    positive="#4ee0b1",
    negative="#ff7f9c",
)
LIGHT_COLORS = ThemeColors(
    background="#edf7fb",
    surface="#f8fcff",
    surface_elevated="#ffffff",
    text="#102638",
    muted_text="#567188",
    border="#c7e2ef",
    accent="#007fa8",
    accent_soft="#d9f3fc",
    positive="#008d6b",
    negative="#c93661",
)

# Backward-compatible token used by the existing Fluent navigation stylesheet.
ACCENT_COLOR = DARK_COLORS.accent


def colors_for(dark: bool) -> ThemeColors:
    return DARK_COLORS if dark else LIGHT_COLORS


def glacial_stylesheet(dark: bool) -> str:
    """A restrained glass-and-ice treatment for standard Qt controls."""
    c = colors_for(dark)
    return f"""
        QWidget {{ background: {c.background}; color: {c.text}; font-family: 'Segoe UI'; }}
        QMainWindow, QDialog {{ background: {c.background}; }}
        QLabel#muted {{ color: {c.muted_text}; }}
        QWidget#surface, QWidget#metricCard, QWidget#chartPanel {{
            background: {c.surface}; border: 1px solid {c.border}; border-radius: {RADIUS_MEDIUM}px;
        }}
        QWidget#metricCard:hover {{ background: {c.surface_elevated}; border-color: {c.accent}; }}
        QLineEdit, QComboBox, QListWidget {{
            background: {c.surface}; color: {c.text}; border: 1px solid {c.border};
            border-radius: {RADIUS_SMALL}px; padding: 7px 10px;
        }}
        QLineEdit:focus, QComboBox:focus {{ border: 2px solid {c.accent}; }}
        QComboBox::drop-down {{ border: 0; width: 26px; }}
        QListWidget::item {{ border-radius: {RADIUS_SMALL}px; margin: 2px 4px; padding: 8px; }}
        QListWidget::item:selected {{ background: {c.accent_soft}; color: {c.text}; }}
        QPushButton {{
            background: {c.surface_elevated}; color: {c.text}; border: 1px solid {c.border};
            border-radius: {RADIUS_SMALL}px; padding: 8px 14px;
        }}
        QPushButton:hover {{ border-color: {c.accent}; background: {c.accent_soft}; }}
        QPushButton:pressed {{ background: {c.accent}; color: {c.background}; }}
        QPushButton:disabled {{ color: {c.muted_text}; border-color: {c.border}; }}
        QToolTip {{ background: {c.surface_elevated}; color: {c.text}; border: 1px solid {c.border}; }}
        QScrollBar:vertical {{ background: transparent; width: 10px; margin: 4px; }}
        QScrollBar::handle:vertical {{ background: {c.border}; border-radius: 5px; min-height: 32px; }}
        QScrollBar::handle:vertical:hover {{ background: {c.accent}; }}
    """
