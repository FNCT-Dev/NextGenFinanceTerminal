import logging
import re

_SENSITIVE = re.compile(
    r"(?i)(pin|password|secret|token|authorization|api[_-]?key)\s*[:=]\s*[^\s,}]+"
)


class SecretRedactionFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        record.msg = _SENSITIVE.sub(lambda match: f"{match.group(1)}=[REDACTED]", str(record.msg))
        record.args = ()
        return True


def configure_logging(level: str) -> None:
    handler = logging.StreamHandler()
    handler.addFilter(SecretRedactionFilter())
    logging.basicConfig(level=level, handlers=[handler], force=True)
