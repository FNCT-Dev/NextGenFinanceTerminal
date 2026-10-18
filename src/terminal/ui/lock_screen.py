from PySide6.QtCore import QTimer, Signal
from PySide6.QtWidgets import QVBoxLayout, QWidget
from qfluentwidgets import BodyLabel, PrimaryPushButton, SubtitleLabel, TitleLabel

from terminal.security.lockout import PinLockout
from terminal.security.pin_service import PinService
from terminal.ui.pin_entry import PinEntry
from terminal.ui.theme import SPACING_LARGE


class LockScreen(QWidget):
    unlocked = Signal()

    def __init__(self, pin_service: PinService, pin_hash: str) -> None:
        super().__init__()
        self._pin_service = pin_service
        self._pin_hash = pin_hash
        self._lockout = PinLockout()
        self._pin = PinEntry()
        self._pin.submitted.connect(self._verify)
        self._status = BodyLabel()
        button = PrimaryPushButton("\uc7a0\uae08 \ud574\uc81c")
        button.clicked.connect(self._verify)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(64, 64, 64, 64)
        layout.setSpacing(SPACING_LARGE)
        layout.addStretch(2)
        layout.addWidget(TitleLabel("NextGen Finance Terminal"))
        subtitle = SubtitleLabel("\ub85c\uceec \uc811\uadfc \ubcf4\ud638")
        subtitle.setObjectName("muted")
        layout.addWidget(subtitle)
        layout.addSpacing(SPACING_LARGE)
        layout.addWidget(SubtitleLabel("PIN \uc785\ub825"))
        layout.addWidget(self._pin)
        layout.addWidget(button)
        layout.addWidget(self._status)
        layout.addStretch(3)
        self._timer = QTimer(self)
        self._timer.setInterval(250)
        self._timer.timeout.connect(self._update_lockout_label)
        self.setStyleSheet(
            "QWidget { background: #07141f; }"
            "QLineEdit { background: #0c1e2d; border: 1px solid #23455d; "
            "border-radius: 10px; font-size: 20px; }"
            "QLineEdit:focus { border: 2px solid #55d9ff; }"
        )

    def _verify(self) -> None:
        if not self._lockout.can_attempt():
            return
        pin = self._pin.value()
        self._pin.clear()
        if self._pin_service.verify(self._pin_hash, pin):
            self._lockout.reset()
            self.unlocked.emit()
            return
        delay = self._lockout.record_failure()
        self._status.setText(
            "PIN\uc774 \uc62c\ubc14\ub974\uc9c0 \uc54a\uc2b5\ub2c8\ub2e4."
            if not delay
            else f"{delay}\ucd08 \ud6c4\uc5d0 \ub2e4\uc2dc \uc2dc\ub3c4\ud558\uc138\uc694."
        )
        if delay:
            self._timer.start()

    def _update_lockout_label(self) -> None:
        remaining = self._lockout.remaining_seconds()
        if remaining:
            self._status.setText(
                f"{remaining}\ucd08 \ud6c4\uc5d0 \ub2e4\uc2dc \uc2dc\ub3c4\ud558\uc138\uc694."
            )
        else:
            self._timer.stop()
            self._status.clear()
