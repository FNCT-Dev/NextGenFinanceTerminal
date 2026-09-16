from PySide6.QtCore import QTimer, Signal
from PySide6.QtWidgets import QVBoxLayout, QWidget
from qfluentwidgets import (
    BodyLabel,
    PrimaryPushButton,
    SubtitleLabel,
    TitleLabel,
)

from terminal.security.lockout import PinLockout
from terminal.security.pin_service import PinService
from terminal.ui.pin_entry import PinEntry


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

        button = PrimaryPushButton("잠금 해제")
        button.clicked.connect(self._verify)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(48, 48, 48, 48)
        layout.addStretch()
        layout.addWidget(TitleLabel("NextGen Finance Terminal"))
        layout.addWidget(SubtitleLabel("PIN 입력"))
        layout.addWidget(self._pin)
        layout.addSpacing(18)
        layout.addWidget(button)
        layout.addWidget(self._status)
        layout.addStretch()

        self._timer = QTimer(self)
        self._timer.setInterval(250)
        self._timer.timeout.connect(self._update_lockout_label)

        self.setStyleSheet(
            "QLineEdit { border: 1px solid palette(mid); "
            "border-radius: 8px; font-size: 20px; }"
            "QLineEdit:focus { border: 2px solid palette(highlight); }"
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
            "PIN이 올바르지 않습니다." if not delay else f"{delay}초 후에 다시 시도하세요."
        )
        if delay:
            self._timer.start()

    def _update_lockout_label(self) -> None:
        remaining = self._lockout.remaining_seconds()
        if remaining:
            self._status.setText(f"{remaining}초 후에 다시 시도하세요.")
        else:
            self._timer.stop()
            self._status.setText("")
