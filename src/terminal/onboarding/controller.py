import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from terminal.core.app_state import AppState


@dataclass(slots=True)
class PersistedAppState:
    """Non-secret local state. PIN is retained only as an Argon2 hash."""

    app_state: AppState
    pin_hash: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {"app_state": self.app_state.to_dict(), "pin_hash": self.pin_hash}

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "PersistedAppState":
        app_payload = payload.get("app_state", {})
        if not isinstance(app_payload, dict):
            raise TypeError("app_state must be an object")
        pin_hash = payload.get("pin_hash")
        if pin_hash is not None and not isinstance(pin_hash, str):
            raise TypeError("pin_hash must be a string or null")
        return cls(app_state=AppState.from_dict(app_payload), pin_hash=pin_hash)


class OnboardingController:
    """Durable onboarding/PIN state without credential persistence."""

    def __init__(self, state_path: Path) -> None:
        self._state_path = state_path

    def load(self) -> PersistedAppState:
        if not self._state_path.exists():
            return PersistedAppState(AppState())
        return PersistedAppState.from_dict(json.loads(self._state_path.read_text(encoding="utf-8")))

    def save(self, state: PersistedAppState) -> None:
        self._state_path.parent.mkdir(parents=True, exist_ok=True)
        self._state_path.write_text(
            json.dumps(state.to_dict(), indent=2, sort_keys=True), encoding="utf-8"
        )
