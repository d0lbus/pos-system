import base64
import hashlib
import hmac
import secrets

from app.core.constants import PIN_LENGTH


PBKDF2_ALGORITHM = "sha256"
PBKDF2_ITERATIONS = 390_000
SALT_LENGTH = 16


def is_valid_pin_format(pin: str) -> bool:
    return pin.isdigit() and len(pin) == PIN_LENGTH


def validate_pin_format(pin: str) -> None:
    if not is_valid_pin_format(pin):
        raise ValueError(f"PIN must be exactly {PIN_LENGTH} numeric digits.")


def _b64_encode(value: bytes) -> str:
    return base64.b64encode(value).decode("utf-8")


def _b64_decode(value: str) -> bytes:
    return base64.b64decode(value.encode("utf-8"))


def hash_pin(pin: str) -> str:
    validate_pin_format(pin)

    salt = secrets.token_bytes(SALT_LENGTH)
    pin_hash = hashlib.pbkdf2_hmac(
        PBKDF2_ALGORITHM,
        pin.encode("utf-8"),
        salt,
        PBKDF2_ITERATIONS,
    )

    return (
        f"pbkdf2_{PBKDF2_ALGORITHM}"
        f"${PBKDF2_ITERATIONS}"
        f"${_b64_encode(salt)}"
        f"${_b64_encode(pin_hash)}"
    )


def verify_pin(pin: str, stored_hash: str) -> bool:
    if not stored_hash or not is_valid_pin_format(pin):
        return False

    try:
        scheme, iterations_str, salt_b64, hash_b64 = stored_hash.split("$", 3)
        algorithm = scheme.removeprefix("pbkdf2_")
        iterations = int(iterations_str)

        salt = _b64_decode(salt_b64)
        expected_hash = _b64_decode(hash_b64)

        candidate_hash = hashlib.pbkdf2_hmac(
            algorithm,
            pin.encode("utf-8"),
            salt,
            iterations,
        )

        return hmac.compare_digest(candidate_hash, expected_hash)
    except Exception:
        return False