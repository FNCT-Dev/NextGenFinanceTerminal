import os
import sys
from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QPalette
from PySide6.QtWidgets import QApplication
from qfluentwidgets import Theme, setTheme

from terminal.onboarding.controller import OnboardingController
from terminal.security.argon2_hasher import Argon2PinHasher
from terminal.security.keyring_store import KeyringCredentialStore
from terminal.security.pin_service import PinService
from terminal.ui.lock_screen import LockScreen
from terminal.ui.main_window import TerminalWindow
from terminal.ui.onboarding_wizard import OnboardingWizard
from terminal.ui.theme import DARK_COLORS


def state_file() -> Path:
    root = Path(os.environ.get("LOCALAPPDATA", Path.home())) / "NextGenFinanceTerminal"
    return root / "state.json"


def _system_theme(app: QApplication) -> Theme:
    """Read Windows' app theme, with Qt's color scheme as a fallback."""
    if sys.platform == "win32":
        try:
            import winreg

            with winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize",
            ) as key:
                apps_use_light_theme, _ = winreg.QueryValueEx(key, "AppsUseLightTheme")
                return Theme.LIGHT if apps_use_light_theme else Theme.DARK
        except OSError:
            return (
                Theme.DARK
                if app.styleHints().colorScheme() is Qt.ColorScheme.Dark
                else Theme.LIGHT
            )
    return Theme.DARK if app.styleHints().colorScheme() is Qt.ColorScheme.Dark else Theme.LIGHT


def _apply_palette(app: QApplication, theme: Theme) -> None:
    """Give regular Qt widgets the same colors as the Fluent theme."""
    palette = QPalette()
    if theme is Theme.DARK:
        palette.setColor(QPalette.ColorRole.Window, QColor(DARK_COLORS.background))
        palette.setColor(QPalette.ColorRole.WindowText, QColor(DARK_COLORS.text))
        palette.setColor(QPalette.ColorRole.Base, QColor(DARK_COLORS.surface))
        palette.setColor(QPalette.ColorRole.AlternateBase, QColor("#2a2a2a"))
        palette.setColor(QPalette.ColorRole.Text, QColor(DARK_COLORS.text))
        palette.setColor(QPalette.ColorRole.Button, QColor("#2d2d2d"))
        palette.setColor(QPalette.ColorRole.ButtonText, QColor(DARK_COLORS.text))
        palette.setColor(QPalette.ColorRole.Highlight, QColor("#0078d4"))
        palette.setColor(QPalette.ColorRole.HighlightedText, QColor("#ffffff"))
    app.setPalette(palette)


def main() -> int:
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    theme = _system_theme(app)
    setTheme(theme)
    _apply_palette(app, theme)
    controller = OnboardingController(state_file())
    stored = controller.load()
    pin_service = PinService(Argon2PinHasher())
    credential_store = KeyringCredentialStore()

    def open_terminal() -> None:
        window = TerminalWindow(
            pin_service, stored, controller, credential_store, dark=theme is Theme.DARK
        )
        window.show()
        app.main_window = window  # type: ignore[attr-defined]

    if not stored.app_state.onboarding_completed or not stored.pin_hash:

        def complete(pin_hash: str) -> None:
            stored.app_state.onboarding_completed = True
            stored.app_state.pin_configured = True
            stored.pin_hash = pin_hash
            controller.save(stored)
            open_terminal()

        wizard = OnboardingWizard(
            pin_service, credential_store, complete, dark=theme is Theme.DARK
        )
        wizard.show()
        app.wizard = wizard  # type: ignore[attr-defined]
    else:
        lock_screen = LockScreen(pin_service, stored.pin_hash)

        def unlock_to_terminal() -> None:
            lock_screen.close()
            open_terminal()

        lock_screen.unlocked.connect(unlock_to_terminal)
        lock_screen.show()
        app.lock_screen = lock_screen  # type: ignore[attr-defined]
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
