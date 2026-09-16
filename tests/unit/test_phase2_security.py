from terminal.core.app_state import AppState
from terminal.onboarding.controller import OnboardingController, PersistedAppState
from terminal.security.argon2_hasher import Argon2PinHasher
from terminal.security.lockout import PinLockout
from terminal.security.pin_service import PinService
from terminal.ui.credentials_page import CredentialSetupPage


class MemoryCredentialStore:
    def __init__(self) -> None:
        self.values: dict[tuple[str, str], str] = {}

    def get(self, provider: str, account: str = "default") -> str | None:
        return self.values.get((provider, account))

    def set(self, provider: str, secret: str, account: str = "default") -> None:
        self.values[(provider, account)] = secret

    def delete(self, provider: str, account: str = "default") -> None:
        self.values.pop((provider, account), None)


def test_argon2_pin_hash_is_not_plaintext() -> None:
    service = PinService(Argon2PinHasher())
    stored_hash = service.create_hash("123456", "123456")

    assert stored_hash != "123456"
    assert service.verify(stored_hash, "123456")
    assert not service.verify(stored_hash, "654321")


def test_lockout_progressively_delays_attempts() -> None:
    lockout = PinLockout()

    assert lockout.record_failure() == 0
    assert lockout.record_failure() == 0
    assert lockout.record_failure() == 30
    assert not lockout.can_attempt()
    lockout.reset()
    assert lockout.can_attempt()


def test_lockout_escalates_at_five_and_seven_failures() -> None:
    lockout = PinLockout()
    assert [lockout.record_failure() for _ in range(4)] == [0, 0, 30, 30]
    lockout.locked_until = 0
    assert lockout.record_failure() == 60
    lockout.locked_until = 0
    assert lockout.record_failure() == 60
    lockout.locked_until = 0
    assert lockout.record_failure() == 300
    lockout.locked_until = 0
    assert lockout.record_failure() == 600


def test_persisted_state_round_trip_does_not_store_plaintext_pin(tmp_path) -> None:
    controller = OnboardingController(tmp_path / "state.json")
    state = PersistedAppState(
        app_state=AppState(onboarding_completed=True, pin_configured=True),
        pin_hash="$argon2id$synthetic-hash",
    )

    controller.save(state)
    restored = controller.load()
    content = (tmp_path / "state.json").read_text(encoding="utf-8")

    assert restored == state
    assert "123456" not in content
    assert "pin_hash" in content


def test_credential_page_clears_fields_after_keyring_save() -> None:
    from PySide6.QtWidgets import QApplication

    app = QApplication.instance() or QApplication([])
    store = MemoryCredentialStore()
    page = CredentialSetupPage(store)
    page._alpaca_key.setText("key-value")  # type: ignore[attr-defined]
    page._alpaca_secret.setText("secret-value")  # type: ignore[attr-defined]
    page.save()

    assert app is not None
    assert store.get("alpaca", "api_key") == "key-value"
    assert store.get("alpaca", "api_secret") == "secret-value"
    assert not page._alpaca_key.text()  # type: ignore[attr-defined]
    assert not page._alpaca_secret.text()  # type: ignore[attr-defined]
