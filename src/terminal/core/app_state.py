from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class AppState:
    onboarding_completed: bool = False
    onboarding_version: int = 1
    pin_configured: bool = False
    app_schema_version: int = 1
    enabled_providers: set[str] = field(default_factory=set)

    def to_dict(self) -> dict[str, Any]:
        return {
        "onboarding_completed": self.onboarding_completed,
        "onboarding_version": self.onboarding_version,
        "pin_configured": self.pin_configured,
        "app_schema_version": self.app_schema_version,
        "enabled_providers": sorted(self.enabled_providers),
    }

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "AppState":
        providers = payload.get("enabled_providers", [])

        if not isinstance(providers, list) or not all(
            isinstance(provider, str) for provider in providers
        ):
            raise TypeError("enabled_providers must be a list of strings")

        return cls(
            onboarding_completed=bool(payload.get("onboarding_completed", False)),
            onboarding_version=int(payload.get("onboarding_version", 1)),
            pin_configured=bool(payload.get("pin_configured", False)),
            app_schema_version=int(payload.get("app_schema_version", 1)),
            enabled_providers=set(providers),
        )