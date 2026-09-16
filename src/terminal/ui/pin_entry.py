from PySide6.QtCore import QEvent, QObject, QRegularExpression, Qt, Signal
from PySide6.QtGui import QKeyEvent, QKeySequence, QRegularExpressionValidator
from PySide6.QtWidgets import QApplication, QHBoxLayout, QLineEdit, QWidget


class PinEntry(QWidget):
    """Six independent PIN cells with continuous keyboard entry."""

    submitted = Signal()
    changed = Signal()

    def __init__(self, length: int = 6) -> None:
        super().__init__()
        self._fields: list[QLineEdit] = []
        validator = QRegularExpressionValidator(QRegularExpression("[0-9]"), self)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)
        for index in range(length):
            field = QLineEdit()
            field.setFixedSize(42, 48)
            field.setAlignment(Qt.AlignmentFlag.AlignCenter)
            field.setEchoMode(QLineEdit.EchoMode.Password)
            field.setMaxLength(1)
            field.setValidator(validator)
            field.setProperty("pin_index", index)
            field.installEventFilter(self)
            field.textChanged.connect(lambda text, position=index: self._advance(text, position))
            layout.addWidget(field)
            self._fields.append(field)

    def value(self) -> str:
        return "".join(field.text() for field in self._fields)

    def clear(self) -> None:
        for field in self._fields:
            field.clear()
        self._fields[0].setFocus()
        self.changed.emit()

    def set_error(self, enabled: bool) -> None:
        border = "#ef4444" if enabled else "palette(mid)"
        for field in self._fields:
            field.setStyleSheet(
                f"QLineEdit {{ border: 2px solid {border}; border-radius: 6px; }}"
            )

    def eventFilter(self, watched: QObject, event: QEvent) -> bool:
        if not isinstance(watched, QLineEdit) or event.type() != QEvent.Type.KeyPress:
            return super().eventFilter(watched, event)
        if not isinstance(event, QKeyEvent):
            return super().eventFilter(watched, event)
        index = int(watched.property("pin_index"))
        if event.matches(QKeySequence.StandardKey.Paste):
            self._fill(QApplication.clipboard().text())
            return True
        if event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
            if len(self.value()) == len(self._fields):
                self.submitted.emit()
            return True
        if event.key() == Qt.Key.Key_Backspace and not watched.text() and index:
            self._fields[index - 1].clear()
            self._fields[index - 1].setFocus()
            return True
        return super().eventFilter(watched, event)

    def _advance(self, text: str, index: int) -> None:
        self.changed.emit()
        if not text:
            return
        if index < len(self._fields) - 1:
            self._fields[index + 1].setFocus()

    def _fill(self, value: str) -> None:
        digits = [character for character in value if character.isascii() and character.isdigit()]
        for field, digit in zip(self._fields, digits, strict=False):
            field.setText(digit)
