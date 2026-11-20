import hashlib
import secrets


def hash_password(password: str) -> str:
    salt = secrets.token_bytes(16)
    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        600_000,
    )
    return f"pbkdf2_sha256${salt.hex()}${password_hash.hex()}"


def verify_password(password: str, stored_password: str) -> bool:
    try:
        algorithm, salt_hex, password_hash_hex = stored_password.split("$")
        if algorithm != "pbkdf2_sha256":
            return False
        salt = bytes.fromhex(salt_hex)
        expected_hash = bytes.fromhex(password_hash_hex)
    except ValueError:
        return False

    actual_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        600_000,
    )
    return secrets.compare_digest(actual_hash, expected_hash)
