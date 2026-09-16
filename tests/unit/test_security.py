from terminal.security.pin_service import PinService, validate_pin


class FakeHasher:
    def hash(self, secret: str) -> str:
        return f"hash::{secret[::-1]}"

    def verify(self, hash: str, secret: str) -> bool:
        return hash == self.hash(secret)


def test_pin_validation() -> None:
    assert validate_pin("123456")
    assert not validate_pin("12345")
    assert not validate_pin("1234567")
    assert not validate_pin("12ab56")


def test_pin_hash_does_not_contain_plaintext() -> None:
    stored = PinService(FakeHasher()).create_hash("123456", "123456")
    assert stored != "123456"
    assert PinService(FakeHasher()).verify(stored, "123456")
