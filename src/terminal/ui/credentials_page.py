# ruff: noqa: E501

from PySide6.QtWidgets import QFormLayout, QLabel, QLineEdit, QPushButton, QWidget

from terminal.security.credential_store import CredentialStore


class CredentialSetupPage(QWidget):
    """Optional credentials that cross only the OS-keyring boundary."""

    def __init__(self, credential_store: CredentialStore) -> None:
        super().__init__()
        self._credential_store = credential_store
        self._alpaca_key = QLineEdit()
        self._alpaca_secret = QLineEdit()
        self._tiingo_key = QLineEdit()
        self._status = QLabel()
        for field in (self._alpaca_key, self._alpaca_secret, self._tiingo_key):
            field.setEchoMode(QLineEdit.EchoMode.Password)
        button = QPushButton("\uc790\uaca9 \uc99d\uba85 \uc800\uc7a5")
        button.clicked.connect(self.save)
        layout = QFormLayout(self)
        layout.addRow("Alpaca API Key", self._alpaca_key)
        layout.addRow("Alpaca API Secret", self._alpaca_secret)
        layout.addRow("Tiingo API Key", self._tiingo_key)
        layout.addRow(button)
        layout.addRow(self._status)

    def save(self) -> None:
        credentials = (
            ("alpaca", "api_key", self._alpaca_key.text()),
            ("alpaca", "api_secret", self._alpaca_secret.text()),
            ("tiingo", "api_key", self._tiingo_key.text()),
        )
        saved = False
        for provider, account, value in credentials:
            if value:
                self._credential_store.set(provider, value, account)
                saved = True
        self._alpaca_key.clear()
        self._alpaca_secret.clear()
        self._tiingo_key.clear()
        self._status.setText(
            "\uc790\uaca9 \uc99d\uba85\uc774 \uc6b4\uc601\uccb4\uc81c \uc790\uaca9 \uc99d\uba85 \uc800\uc7a5\uc18c\uc5d0 \uc800\uc7a5\ub418\uc5c8\uc2b5\ub2c8\ub2e4."
            if saved
            else "\uc800\uc7a5\ud560 \uc790\uaca9 \uc99d\uba85\uc774 \uc5c6\uc2b5\ub2c8\ub2e4. \uc774 \ub2e8\uacc4\ub294 \uac74\ub108\ub6f8 \uc218 \uc788\uc2b5\ub2c8\ub2e4."
        )
