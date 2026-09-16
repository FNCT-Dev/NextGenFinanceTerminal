# Onboarding

`OnboardingState` serializes `onboarding_completed`, `onboarding_version`, `pin_configured`, `app_schema_version`, and interrupted `current_step`. It avoids using one boolean for all state. Phase 2 will render welcome, security/PIN, BYOK, freshness, providers, optional API setup, interface guide, and finish; dashboard access will wait for completion. `requires_onboarding()` supports targeted future notice replay.

