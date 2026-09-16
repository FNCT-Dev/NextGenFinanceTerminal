import keyring


class KeyringCredentialStore:
    """Credential storage backed by the operating system keyring."""

    def __init__(self, service_name: str = "NextGenFinanceTerminal") -> None:
        self._service_name = service_name

    def get(self, provider: str, account: str = "default") -> str | None:
        return keyring.get_password(f"{self._service_name}:{provider}", account)

    def set(self, provider: str, secret: str, account: str = "default") -> None:
        keyring.set_password(f"{self._service_name}:{provider}", account, secret)

    def delete(self, provider: str, account: str = "default") -> None:
        try:
            keyring.delete_password(f"{self._service_name}:{provider}", account)
        except keyring.errors.PasswordDeleteError:
            return
