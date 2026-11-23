import hashlib
import hmac

from fastapi import Request

from edge.exceptions import UnauthorizedException
from edge.settings import settings


async def verify_signature(request: Request):
    """
    Verifies the payload's signature with header's value.
    """
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
