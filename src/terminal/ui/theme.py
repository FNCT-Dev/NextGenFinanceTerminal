from dataclasses import dataclass

ACCENT_COLOR = "#22d3ee"
SPACING_SMALL = 8
SPACING_MEDIUM = 16
SPACING_LARGE = 28


@dataclass(frozen=True, slots=True)
class ThemeColors:
    background: str
    surface: str
    text: str
    border: str


DARK_COLORS = ThemeColors(
    background="#202020",
    surface="#1e1e1e",
    text="#f5f5f5",
    border="#4a4a4a",
)
LIGHT_COLORS = ThemeColors(
    background="#f5f5f5",
    surface="#ffffff",
    text="#202020",
    border="#b8b8b8",
)


def colors_for(dark: bool) -> ThemeColors:
    return DARK_COLORS if dark else LIGHT_COLORS
