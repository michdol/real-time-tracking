import hashlib
import hmac

from fastapi import Request, Depends, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from typing import Annotated

from edge.exceptions import UnauthorizedException
from edge.settings import settings
from edge.auth.api_key import hash_secret
from edge.database.db import Database
from edge.dependencies.database import get_db


async def verify_signature(request: Request):
    """
    Verifies the payload's signature with header's value.
    """
    if settings.app.skip_auth:
        return
    signature: str = request.headers.get("Content-Digest", "")

    if not signature:
        raise UnauthorizedException()
    try:
        signature = signature[8:]
    except IndexError:
        raise UnauthorizedException(detail="Invalid signature format")
    digest = hmac.new(
        settings.signing_secret.get_secret_value().encode(),
        await request.body(),
        hashlib.sha256,
    ).hexdigest()
    if digest != signature:
        raise UnauthorizedException(detail="Invalid signature")


def verify_api_key(
    database: Annotated[Database, Depends(get_db)],
    credentials: HTTPAuthorizationCredentials = Security(HTTPBearer()),
) -> str | None:
    """
    Validates api key.
    returns:
    - provider id on successful key validation
    - None otherwise
    """
    try:
        _, key_id, provided_secret = credentials.credentials.split("_")
    except ValueError:
        return None

    try:
        record = database[key_id]
    except KeyError:
        return None

    expected_hash = record["secret_hash"]
    provided_hash = hash_secret(provided_secret)

    if hmac.compare_digest(expected_hash, provided_hash):
        return record["id"]
    return None


def get_current_provider(
    provider_id: Annotated[str | None, Depends(verify_api_key)],
):
    if not provider_id:
        raise UnauthorizedException()
    return provider_id


"""
(
    # full key
    "rtt_a948c11c_AFEKCZj0RmjvllWO4GuZbvlhyMwxrArrA03wjAOTH8M",
    # key_id
    "a948c11c",
    # secret_hash
    "42f7a6fb91587868b2cccc46b3af63a03f9878ecde1064cbe3cd37d049443643",
)
"""
