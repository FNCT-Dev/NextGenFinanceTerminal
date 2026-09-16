# ruff: noqa: E501

from collections.abc import Callable

from PySide6.QtWidgets import (
    QDialog,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)
from qfluentwidgets import BodyLabel, SubtitleLabel

from terminal.security.credential_store import CredentialStore
from terminal.security.pin_service import PinService
from terminal.ui.credentials_page import CredentialSetupPage
from terminal.ui.pin_entry import PinEntry
from terminal.ui.theme import colors_for


def _guide_pages() -> tuple[tuple[str, str], ...]:
    return (
        (
            "\ud658\uc601\ud569\ub2c8\ub2e4",
            "\uc8fc\uc2dd, \ucc44\uad8c, \uc678\ud658, \uc554\ud638\uc790\uc0b0, \uac70\uc2dc\uacbd\uc81c, \ub274\uc2a4\ub97c \uc704\ud55c \uc77d\uae30 \uc804\uc6a9 \ub370\uc2a4\ud06c\ud1b1 \ud130\ubbf8\ub110\uc785\ub2c8\ub2e4. \uac70\ub798 \uae30\ub2a5\uc740 \uc81c\uacf5\ud558\uc9c0 \uc54a\uc2b5\ub2c8\ub2e4.",
        ),
        (
            "\ubcf4\uc548",
            "6\uc790\ub9ac PIN\uc73c\ub85c \ub85c\uceec \uc571 \uc811\uadfc\uc744 \ubcf4\ud638\ud569\ub2c8\ub2e4. PIN\uc740 Argon2 \ud574\uc2dc\ub85c\ub9cc \uc800\uc7a5\ub429\ub2c8\ub2e4.",
        ),
        (
            "\uac1c\uc778 API \ud0a4 \uc0ac\uc6a9",
            "\uc790\uaca9 \uc99d\uba85\uc740 \uc120\ud0dd \uc0ac\ud56d\uc774\uba70, \uc77c\ubc18 \uc124\uc815 \ud30c\uc77c\uc774 \uc544\ub2cc \uc6b4\uc601\uccb4\uc81c \uc790\uaca9 \uc99d\uba85 \uc800\uc7a5\uc18c\uc5d0 \ubcf4\uad00\ub429\ub2c8\ub2e4.",
        ),
        (
            "\ub370\uc774\ud130 \ucd5c\uc2e0\uc131",
            "\uac00\uaca9\uc5d0\ub294 \uc2e4\uc2dc\uac04, \uc9c0\uc5f0, \uc7a5 \ub9c8\uac10, \uacfc\uac70 \ub370\uc774\ud130 \uc0c1\ud0dc\uac00 \uba85\ud655\ud788 \ud45c\uc2dc\ub429\ub2c8\ub2e4. \uc9c0\uc5f0 \ub370\uc774\ud130\ub294 \uc2e4\uc2dc\uac04\uc774 \uc544\ub2d9\ub2c8\ub2e4.",
        ),
        (
            "\ub370\uc774\ud130 \uc81c\uacf5\uc790",
            "\ub370\uc774\ud130 \uc81c\uacf5\uc790 \uc124\uc815\uc740 \uc120\ud0dd \uc0ac\ud56d\uc785\ub2c8\ub2e4. API \uc790\uaca9 \uc99d\uba85 \uc5c6\uc774\ub3c4 \uc124\uc815\uc744 \ub9c8\uce60 \uc218 \uc788\uc2b5\ub2c8\ub2e4.",
        ),
        (
            "\uc778\ud130\ud398\uc774\uc2a4 \uc548\ub0b4",
            "\uc0ac\uc774\ub4dc\ubc14\uc5d0\uc11c \uc2dc\uc7a5\uacfc \uc124\uc815\uc744 \uc774\uc6a9\ud558\uc138\uc694. \ub370\uc774\ud130\uc640 \ud568\uaed8 \uc81c\uacf5\uc790 \ubc0f \ucd5c\uc2e0\uc131 \ud45c\uc2dc\uac00 \uacc4\uc18d \ud45c\uc2dc\ub429\ub2c8\ub2e4.",
        ),
    )


def _apply_theme(widget: QWidget, dark: bool) -> None:
    c = colors_for(dark)
    widget.setStyleSheet(
        f"QDialog, QWidget {{ background: {c.background}; color: {c.text}; }} QLabel {{ color: {c.text}; }} QLineEdit {{ background: {c.surface}; color: {c.text}; border: 1px solid {c.border}; border-radius: 6px; }} QPushButton {{ background: {c.surface}; color: {c.text}; border: 1px solid {c.border}; border-radius: 4px; padding: 6px 18px; }}"
    )


class _InfoPage(QWidget):
    def __init__(self, title: str, text: str) -> None:
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 28, 28, 28)
        layout.addWidget(SubtitleLabel(title))
        label = BodyLabel(text)
        label.setWordWrap(True)
        layout.addWidget(label)
        layout.addStretch()


class _PinPage(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.pin, self.confirmation, self.status = PinEntry(), PinEntry(), QLabel()
        self._error = False
        self.pin.changed.connect(self._clear_error)
        self.confirmation.changed.connect(self._clear_error)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(28, 28, 28, 28)
        layout.addWidget(SubtitleLabel("\ub85c\uceec PIN \ub9cc\ub4e4\uae30"))
        for text, entry in (
            ("6\uc790\ub9ac PIN", self.pin),
            ("PIN \ud655\uc778", self.confirmation),
        ):
            layout.addWidget(QLabel(text))
            layout.addWidget(entry)
            layout.addSpacing(12)
        layout.addWidget(self.status)
        layout.addStretch()

    def valid(self) -> bool:
        if len(self.pin.value()) == 6 and self.pin.value() == self.confirmation.value():
            return True
        self.pin.clear()
        self.confirmation.clear()
        self.confirmation.set_error(True)
        self._error = True
        self.status.setText(
            "PIN\uc774 \uc77c\uce58\ud558\uc9c0 \uc54a\uc2b5\ub2c8\ub2e4. \ub2e4\uc2dc \uc785\ub825\ud558\uc138\uc694."
        )
        return False

    def complete(self) -> bool:
        return len(self.pin.value()) == 6 and len(self.confirmation.value()) == 6

    def _clear_error(self) -> None:
        if self._error:
            self.confirmation.set_error(False)
            self._error = False
            self.status.clear()


class GettingStartedGuide(QDialog):
    def __init__(self, *, dark: bool) -> None:
        super().__init__()
        self.setWindowTitle("\uc2dc\uc791 \uc548\ub0b4")
        self.setMinimumSize(620, 400)
        self._pages = QStackedWidget()
        for page in _guide_pages():
            self._pages.addWidget(_InfoPage(*page))
        self._back, self._next, close = (
            QPushButton("\uc774\uc804"),
            QPushButton("\ub2e4\uc74c"),
            QPushButton("\ub2eb\uae30"),
        )
        self._back.clicked.connect(lambda: self._move(-1))
        self._next.clicked.connect(lambda: self._move(1))
        close.clicked.connect(self.accept)
        buttons = QHBoxLayout()
        buttons.addStretch()
        buttons.addWidget(self._back)
        buttons.addWidget(self._next)
        buttons.addWidget(close)
        layout = QVBoxLayout(self)
        layout.addWidget(self._pages)
        layout.addLayout(buttons)
        _apply_theme(self, dark)
        self._update()

    def _move(self, delta: int) -> None:
        self._pages.setCurrentIndex(self._pages.currentIndex() + delta)
        self._update()

    def _update(self) -> None:
        self._back.setEnabled(self._pages.currentIndex() > 0)
        self._next.setEnabled(self._pages.currentIndex() < self._pages.count() - 1)


class OnboardingWizard(QDialog):
    def __init__(
        self,
        pin_service: PinService,
        credential_store: CredentialStore,
        on_complete: Callable[[str], None],
        *,
        dark: bool,
    ) -> None:
        super().__init__()
        self._pin_service, self._on_complete = pin_service, on_complete
        self._pin_page, self._credentials, self._pages = (
            _PinPage(),
            CredentialSetupPage(credential_store),
            QStackedWidget(),
        )
        self.setWindowTitle("\ud658\uc601\ud569\ub2c8\ub2e4 — NextGen Finance Terminal")
        self.setMinimumSize(720, 520)
        self.setModal(True)
        for page in (
            _InfoPage(*_guide_pages()[0]),
            _InfoPage(*_guide_pages()[1]),
            self._pin_page,
            _InfoPage(*_guide_pages()[2]),
            _InfoPage(*_guide_pages()[3]),
            _InfoPage(*_guide_pages()[4]),
            self._credentials,
            _InfoPage(*_guide_pages()[5]),
            _InfoPage(
                "\uc644\ub8cc",
                "\uc644\ub8cc\ub97c \uc120\ud0dd\ud558\uc5ec \ud130\ubbf8\ub110\uc744 \uc5fd\ub2c8\ub2e4.",
            ),
        ):
            self._pages.addWidget(page)
        self._back, self._next, self._finish = (
            QPushButton("\uc774\uc804"),
            QPushButton("\ub2e4\uc74c"),
            QPushButton("\uc644\ub8cc"),
        )
        for button in (self._back, self._next, self._finish):
            button.setMinimumSize(96, 38)
        self._back.clicked.connect(lambda: self._move(-1))
        self._next.clicked.connect(lambda: self._move(1))
        self._finish.clicked.connect(self._complete)
        self._pin_page.pin.changed.connect(self._update)
        self._pin_page.confirmation.changed.connect(self._update)
        buttons = QHBoxLayout()
        buttons.addStretch()
        buttons.addWidget(self._back)
        buttons.addWidget(self._next)
        buttons.addWidget(self._finish)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self._pages)
        layout.addLayout(buttons)
        _apply_theme(self, dark)
        self._update()

    def _move(self, delta: int) -> None:
        if (
            delta > 0
            and self._pages.currentWidget() is self._pin_page
            and not self._pin_page.valid()
        ):
            return
        self._pages.setCurrentIndex(self._pages.currentIndex() + delta)
        self._update()

    def _update(self) -> None:
        index = self._pages.currentIndex()
        self._back.setEnabled(index > 0)
        self._next.setVisible(index < self._pages.count() - 1)
        self._finish.setVisible(index == self._pages.count() - 1)
        self._next.setEnabled(index != 2 or self._pin_page.complete())

    def _complete(self) -> None:
        if not self._pin_page.valid():
            self._pages.setCurrentWidget(self._pin_page)
            self._update()
            return
        self._credentials.save()
        self._on_complete(
            self._pin_service.create_hash(
                self._pin_page.pin.value(), self._pin_page.confirmation.value()
            )
        )
        self.accept()
