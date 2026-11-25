import hashlib
import hmac

import pytest
from fastapi.security import HTTPAuthorizationCredentials
from httpx import ASGITransport, AsyncClient

from edge.database.db import MOCK_DB
from edge.dependencies.auth import (
    get_current_provider,
    verify_api_key,
)
from edge.exceptions import UnauthorizedException
from edge.main import app

API_KEY = "rtt_a948c11c_AFEKCZj0RmjvllWO4GuZbvlhyMwxrArrA03wjAOTH8M"
SECRET = "AFEKCZj0RmjvllWO4GuZbvlhyMwxrArrA03wjAOTH8M"


def credentials(value: str) -> HTTPAuthorizationCredentials:
    return HTTPAuthorizationCredentials(scheme="Bearer", credentials=value)


def test_known_api_key_returns_provider_id():
    assert verify_api_key(MOCK_DB, credentials(API_KEY)) == "SeaRates"


def test_stored_hash_matches_the_key_secret():
    digest = hashlib.sha256(SECRET.encode()).hexdigest()
    assert hmac.compare_digest(digest, MOCK_DB["a948c11c"]["secret_hash"])


def test_wrong_secret_is_rejected():
    assert verify_api_key(MOCK_DB, credentials("rtt_a948c11c_wrong")) is None


def test_unknown_key_id_is_rejected():
    assert verify_api_key(MOCK_DB, credentials("rtt_missing1_secret")) is None


def test_malformed_key_is_rejected():
    assert verify_api_key(MOCK_DB, credentials("not-a-key")) is None


def test_missing_provider_is_unauthorized():
    with pytest.raises(UnauthorizedException):
        get_current_provider(None)


def test_provider_id_is_returned():
    assert get_current_provider("SeaRates") == "SeaRates"


async def test_missing_bearer_is_rejected():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post("/event", content=b"{}")
    assert response.status_code == 401


async def test_invalid_bearer_is_unauthorized():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post(
            "/event",
            content=b"{}",
            headers={"Authorization": "Bearer rtt_missing1_secret"},
        )
    assert response.status_code == 401
