from dataclasses import dataclass
from time import monotonic


@dataclass(slots=True)
class PinLockout:
    """Session-local progressive delay after failed PIN attempts."""

    failed_attempts: int = 0
    locked_until: float = 0.0

    def remaining_seconds(self) -> int:
        return max(0, int(self.locked_until - monotonic() + 0.999))

    def can_attempt(self) -> bool:
        return self.remaining_seconds() == 0

    def record_failure(self) -> int:
        self.failed_attempts += 1
        delay = self._delay_for(self.failed_attempts)
        if delay:
            self.locked_until = monotonic() + delay
        return delay

    def reset(self) -> None:
        self.failed_attempts = 0
        self.locked_until = 0.0

    @staticmethod
    def _delay_for(failures: int) -> int:
        if failures < 3:
            return 0
        if failures <= 4:
            return 30
        if failures <= 6:
            return 60
        return 300 * (failures - 6)
