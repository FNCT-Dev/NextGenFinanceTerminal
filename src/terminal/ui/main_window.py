# ruff: noqa: E501

from PySide6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)
from qfluentwidgets import (
    FluentIcon,
    FluentWindow,
    NavigationItemPosition,
    PrimaryPushButton,
    SubtitleLabel,
    TitleLabel,
)

from terminal.onboarding.controller import OnboardingController, PersistedAppState
from terminal.security.credential_store import CredentialStore
from terminal.security.pin_service import PinService
from terminal.ui.credentials_page import CredentialSetupPage
from terminal.ui.dashboard import DashboardPage
from terminal.ui.onboarding_wizard import GettingStartedGuide
from terminal.ui.pin_entry import PinEntry
from terminal.ui.theme import ACCENT_COLOR


class PlaceholderPage(QWidget):
    def __init__(self, title: str) -> None:
        super().__init__()
        layout = QVBoxLayout(self)
        layout.addWidget(TitleLabel(title))
        layout.addWidget(
            SubtitleLabel(
                "\ub2e4\uc74c \uc2dc\uc7a5 \ub370\uc774\ud130 \ub2e8\uacc4\uc5d0\uc11c \uc81c\uacf5\ud560 \uc608\uc815\uc785\ub2c8\ub2e4."
            )
        )
        layout.addStretch()


class SecurityPage(QWidget):
    def __init__(
        self, pin_service: PinService, state: PersistedAppState, controller: OnboardingController
    ) -> None:
        super().__init__()
        self._pin_service, self._state, self._controller = pin_service, state, controller
        self._current, self._new, self._confirmation = PinEntry(), PinEntry(), PinEntry()
        self._status, self._error = QLabel(), False
        for entry in (self._current, self._new, self._confirmation):
            entry.changed.connect(self._clear_error)
        button = PrimaryPushButton("PIN \ubcc0\uacbd")
        button.clicked.connect(self._change)
        layout = QVBoxLayout(self)
        layout.addWidget(TitleLabel("\ubcf4\uc548"))
        layout.addWidget(
            SubtitleLabel(
                "\ub85c\uceec \uc571 \uc811\uadfc\uc6a9 6\uc790\ub9ac PIN\uc744 \ubcc0\uacbd\ud569\ub2c8\ub2e4."
            )
        )
        for label, entry in (
            ("\ud604\uc7ac PIN", self._current),
            ("\uc0c8 PIN", self._new),
            ("\uc0c8 PIN \ud655\uc778", self._confirmation),
        ):
            layout.addWidget(QLabel(label))
            layout.addWidget(entry)
        layout.addWidget(button)
        layout.addWidget(self._status)
        layout.addStretch()

    def _change(self) -> None:
        if not self._state.pin_hash or not self._pin_service.verify(
            self._state.pin_hash, self._current.value()
        ):
            self._status.setText(
                "\ud604\uc7ac PIN\uc774 \uc62c\ubc14\ub974\uc9c0 \uc54a\uc2b5\ub2c8\ub2e4."
            )
            return
        if self._new.value() != self._confirmation.value():
            self._current.clear()
            self._new.clear()
            self._confirmation.clear()
            self._confirmation.set_error(True)
            self._error = True
            self._status.setText(
                "PIN\uc774 \uc77c\uce58\ud558\uc9c0 \uc54a\uc2b5\ub2c8\ub2e4. \ub2e4\uc2dc \uc785\ub825\ud558\uc138\uc694."
            )
            return
        try:
            self._state.pin_hash = self._pin_service.create_hash(
                self._new.value(), self._confirmation.value()
            )
        except ValueError:
            self._status.setText(
                "\uc0c8 PIN\uc740 6\uc790\ub9ac \uc22b\uc790\uc5ec\uc57c \ud569\ub2c8\ub2e4."
            )
            return
        self._controller.save(self._state)
        self._current.clear()
        self._new.clear()
        self._confirmation.clear()
        self._status.setText("PIN\uc774 \ubcc0\uacbd\ub418\uc5c8\uc2b5\ub2c8\ub2e4.")

    def _clear_error(self) -> None:
        if self._error:
            self._confirmation.set_error(False)
            self._error = False
            self._status.clear()


class HelpPage(QWidget):
    def __init__(self, dark: bool) -> None:
        super().__init__()
        layout = QVBoxLayout(self)
        layout.addWidget(TitleLabel("\ub3c4\uc6c0\ub9d0"))
        layout.addWidget(
            SubtitleLabel(
                "\uc628\ubcf4\ub529 \uc548\ub0b4\ub97c \ub2e4\uc2dc \ubcf4\uc2e4 \uc218 \uc788\uc2b5\ub2c8\ub2e4."
            )
        )
        button = PrimaryPushButton("\uc2dc\uc791 \uc548\ub0b4 \ub2e4\uc2dc \ubcf4\uae30")
        button.clicked.connect(lambda: GettingStartedGuide(dark=dark).exec())
        layout.addWidget(button)
        layout.addStretch()


class SettingsPage(QWidget):
    def __init__(
        self,
        pin_service: PinService,
        state: PersistedAppState,
        controller: OnboardingController,
        credential_store: CredentialStore,
        *,
        dark: bool,
    ) -> None:
        super().__init__()
        self._categories, self._content = QListWidget(), QStackedWidget()
        self._categories.setFixedWidth(190)
        categories = (
            "\uc77c\ubc18",
            "\ubcf4\uc548",
            "\ub370\uc774\ud130 \uc81c\uacf5\uc790",
            "\ud654\uba74",
            "\ub370\uc774\ud130 \ubc0f \uac1c\uc778\uc815\ubcf4",
            "\ub3c4\uc6c0\ub9d0",
        )
        pages = (
            PlaceholderPage(categories[0]),
            SecurityPage(pin_service, state, controller),
            CredentialSetupPage(credential_store),
            PlaceholderPage(categories[3]),
            PlaceholderPage(categories[4]),
            HelpPage(dark),
        )
        for title, page in zip(categories, pages, strict=True):
            self._categories.addItem(QListWidgetItem(title))
            self._content.addWidget(page)
        self._categories.currentRowChanged.connect(self._content.setCurrentIndex)
        self._categories.setCurrentRow(0)
        layout = QVBoxLayout(self)
        layout.addWidget(TitleLabel("\uc124\uc815"))
        body = QHBoxLayout()
        body.addWidget(self._categories)
        body.addWidget(self._content, 1)
        layout.addLayout(body, 1)
        self.setStyleSheet(
            "QListWidget { border: 0; padding: 4px; } QListWidget::item { padding: 10px 8px; }"
            f"QListWidget::item:selected {{ border-left: 3px solid {ACCENT_COLOR}; }}"
        )


class TerminalWindow(FluentWindow):  # type: ignore[misc]
    def __init__(
        self,
        pin_service: PinService,
        state: PersistedAppState,
        controller: OnboardingController,
        credential_store: CredentialStore,
        *,
        dark: bool,
    ) -> None:
        super().__init__()
        self.setWindowTitle("NextGen Finance Terminal")
        self.setMinimumSize(960, 640)
        screen = QApplication.primaryScreen()
        if screen is None:
            self.resize(1200, 760)
        else:
            available = screen.availableGeometry()
            self.resize(
                min(1440, max(960, available.width() - 64)),
                min(900, max(640, available.height() - 64)),
            )
        self._add_page(DashboardPage(), FluentIcon.HOME, "\ub300\uc2dc\ubcf4\ub4dc")
        for title, icon in (
            ("\uc2dc\uc7a5", FluentIcon.MARKET),
            ("\ucc44\uad8c", FluentIcon.DATE_TIME),
            ("FX", FluentIcon.SYNC),
            ("\uc554\ud638\uc790\uc0b0", FluentIcon.GLOBE),
            ("\uac70\uc2dc\uacbd\uc81c", FluentIcon.PIE_SINGLE),
            ("\ub274\uc2a4", FluentIcon.MESSAGE),
        ):
            self._add_page(PlaceholderPage(title), icon, title)
        self._add_page(
            SettingsPage(pin_service, state, controller, credential_store, dark=dark),
            FluentIcon.SETTING,
            "\uc124\uc815",
            NavigationItemPosition.BOTTOM,
        )

    def _add_page(
        self,
        widget: QWidget,
        icon: FluentIcon,
        text: str,
        position: NavigationItemPosition = NavigationItemPosition.TOP,
    ) -> None:
        widget.setObjectName(text.replace(" ", ""))
        self.addSubInterface(widget, icon, text, position=position)
