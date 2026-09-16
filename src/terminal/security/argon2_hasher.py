from argon2 import PasswordHasher
from argon2.exceptions import InvalidHashError, VerifyMismatchError


class Argon2PinHasher:
    """Argon2 adapter that stores only irreversible PIN hashes."""

    def __init__(self) -> None:
        self._hasher = PasswordHasher()

    def hash(self, secret: str) -> str:
        return self._hasher.hash(secret)

    def verify(self, stored_hash: str, secret: str) -> bool:
        try:
            return self._hasher.verify(stored_hash, secret)
        except (InvalidHashError, VerifyMismatchError):
            return False