import hashlib
import secrets


def generate_api_key() -> tuple[str, str, str]:
    # Public lookup id
    key_id = secrets.token_hex(4)
    # High entropy secret
    secret = secrets.token_urlsafe(32)
    full_key = f"rtt_{key_id}_{secret}"

    secret_hash = hash_secret(secret)
    return full_key, key_id, secret_hash


def hash_secret(secret: str) -> str:
    return hashlib.sha256(secret.encode("utf-8")).hexdigest()
