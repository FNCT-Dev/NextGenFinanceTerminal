from pydantic import BaseModel, Field


class OnboardingState(BaseModel):
    onboarding_completed: bool = False
    onboarding_version: int = Field(default=1, ge=1)
    pin_configured: bool = False
    app_schema_version: int = Field(default=1, ge=1)
    current_step: str = "welcome"

    def requires_onboarding(self, required_version: int) -> bool:
        return not self.onboarding_completed or self.onboarding_version < required_version
