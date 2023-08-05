import base64
import struct

DEFAULT_SALT = ""


class Fvn64StringHasher:
    """Python fnv string hash implementation."""

    @staticmethod
    def works_ok() -> bool:
        """Check if Hasher class works as expected."""
        expected = "nrcBhky9Y68"
        string = "A"
        salt = ""
        return Fvn64StringHasher.from_string(string, salt=salt) == expected

    @staticmethod
    def as_int(string: str, salt: str = None) -> int:
        """Compute FNV64 hash."""
        salt = DEFAULT_SALT if not salt else salt
        data = salt.encode("utf8") + string.encode("utf8")
        hash_ = 0xCBF29CE484222325
        for b in data:
            hash_ *= 0x100000001B3
            hash_ &= 0xFFFFFFFFFFFFFFFF
            hash_ ^= b
        return hash_

    @staticmethod
    def as_bytes(string: str, salt: str = None) -> bytes:
        """Return hash as bytes object."""
        return struct.pack("<Q", Fvn64StringHasher.as_int(string, salt=salt))

    @staticmethod
    def as_base64(string: str, salt: str = None) -> str:
        """Return hash as base64 string."""
        return base64.urlsafe_b64encode(Fvn64StringHasher.as_bytes(string, salt=salt))[
            :-1
        ].decode("ascii")

    @staticmethod
    def from_string(string: str, salt: str = None) -> str:
        """Return hash as base64 string."""
        return Fvn64StringHasher.as_base64(string, salt=salt)
