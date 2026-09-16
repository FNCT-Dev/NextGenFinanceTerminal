from typing import Protocol


class PinHasher(Protocol):
    def hash(self, secret: str) -> str: ...
    def verify(self, stored_hash: str, secret: str) -> bool: ...


def validate_pin(pin: str) -> bool:
    return len(pin) == 6 and pin.isascii() and pin.isdecimal()


class PinService:
    def __init__(self, hasher: PinHasher) -> None:
        self._hasher = hasher

    def create_hash(self, pin: str, confirmation: str) -> str:
        if not validate_pin(pin):
            raise ValueError("PIN must contain exactly six ASCII digits")
        if pin != confirmation:
            raise ValueError("PIN confirmation does not match")
        return self._hasher.hash(pin)

    def verify(self, stored_hash: str, pin: str) -> bool:
        return validate_pin(pin) and self._hasher.verify(stored_hash, pin)
