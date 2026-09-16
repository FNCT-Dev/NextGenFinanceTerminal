from enum import StrEnum


class DataFreshness(StrEnum):
    """How current a data point is, as asserted by its provider."""

    LIVE = "live"
    DELAYED = "delayed"
    EOD = "eod"
    HISTORICAL = "historical"

    def label(self, delay_seconds: int | None = None) -> str:
        if self is not DataFreshness.DELAYED or not delay_seconds:
            return self.value.upper()
        if delay_seconds % 604800 == 0:
            return f"DELAYED {delay_seconds // 604800}W"
        if delay_seconds % 60 == 0:
            return f"DELAYED {delay_seconds // 60}M"
        return f"DELAYED {delay_seconds}S"
