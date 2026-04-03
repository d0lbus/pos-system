import base64
import hashlib
import hmac
import secrets
import json
import time
from typing import Any

from app.core.constants import PIN_LENGTH
from app.core.config import settings

def _b64url_encode(value: bytes) -> str:
    return base64.urlsafe_b64encode(value).rstrip(b"=").decode("utf-8")


def _b64url_decode(value: str) -> bytes:
    padding = "=" * (-len(value) % 4)
    return base64.urlsafe_b64decode((value + padding).encode("utf-8"))


def create_access_token(
    subject: str,
    extra_claims: dict[str, Any] | None = None,
    expires_in_minutes: int | None = None,
) -> str:
    now = int(time.time())
    expiry_minutes = expires_in_minutes or settings.auth_access_token_expire_minutes

    header = {
        "alg": "HS256",
        "typ": "JWT",
    }

    payload: dict[str, Any] = {
        "sub": subject,
        "iat": now,
        "exp": now + (expiry_minutes * 60),
        "iss": settings.auth_issuer,
    }

    if extra_claims:
        payload.update(extra_claims)

    encoded_header = _b64url_encode(
        json.dumps(header, separators=(",", ":"), sort_keys=True).encode("utf-8")
    )
    encoded_payload = _b64url_encode(
        json.dumps(payload, separators=(",", ":"), sort_keys=True).encode("utf-8")
    )

    signing_input = f"{encoded_header}.{encoded_payload}".encode("utf-8")
    signature = hmac.new(
        settings.auth_secret_key.encode("utf-8"),
        signing_input,
        hashlib.sha256,
    ).digest()

    encoded_signature = _b64url_encode(signature)
    return f"{encoded_header}.{encoded_payload}.{encoded_signature}"


def decode_access_token(token: str) -> dict[str, Any]:
    try:
        encoded_header, encoded_payload, encoded_signature = token.split(".")
    except ValueError as exc:
        raise ValueError("Invalid token structure.") from exc

    signing_input = f"{encoded_header}.{encoded_payload}".encode("utf-8")
    expected_signature = hmac.new(
        settings.auth_secret_key.encode("utf-8"),
        signing_input,
        hashlib.sha256,
    ).digest()

    provided_signature = _b64url_decode(encoded_signature)

    if not hmac.compare_digest(expected_signature, provided_signature):
        raise ValueError("Invalid token signature.")

    payload = json.loads(_b64url_decode(encoded_payload).decode("utf-8"))

    if payload.get("iss") != settings.auth_issuer:
        raise ValueError("Invalid token issuer.")

    exp = payload.get("exp")
    if not isinstance(exp, int) or exp < int(time.time()):
        raise ValueError("Token has expired.")

    return payload


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