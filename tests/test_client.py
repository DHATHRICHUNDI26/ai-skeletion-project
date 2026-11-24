import httpx
import pytest
import respx
from ai_client.client import AIClient
from ai_client.config import settings
from ai_client.config import settings
from ai_client.client import AIClient
@pytest.mark.asyncio
@respx.mock
async def test_successful_get_request():
    route = respx.get(
        "https://api.example.com/users"
    ).mock(
        return_value=httpx.Response(
            200,
            json={"name": "Dhathri"}
        )
    )
    client = AIClient()
    result = await client.get("/users")
    assert result == {"name": "Dhathri"}
    assert route.called

@pytest.mark.asyncio
@respx.mock
async def test_authentication_header():
    route = respx.get(
        "https://api.example.com/users"
    ).mock(
        return_value=httpx.Response(200, json={"status": "ok"})
    )

    client = AIClient()
    await client.get("/users")

    request = route.calls[0].request
    assert request.headers["Authorization"] == f"Bearer {settings.api_key}"


@pytest.mark.asyncio
@respx.mock
async def test_request_timeout():
    route = respx.get(
        "https://api.example.com/users"
    ).mock(
        return_value=httpx.Response(200, json={"status": "ok"})
    )

    client = AIClient()
    await client.get("/users")

    timeout = route.calls[0].request.extensions["timeout"]
    assert timeout["read"] == settings.request_timeout


@pytest.mark.asyncio
@respx.mock
async def test_retry_after_connection_error(monkeypatch):
    monkeypatch.setattr(settings, "max_retries", 1)

    route = respx.get(
        "https://api.example.com/users"
    ).mock(
        side_effect=[
            httpx.ConnectError("Connection failed"),
            httpx.Response(200, json={"status": "recovered"})
        ]
    )

    client = AIClient()
    result = await client.get("/users")

    assert result == {"status": "recovered"}
    assert route.call_count == 2


@pytest.mark.asyncio
@respx.mock
async def test_retry_after_timeout(monkeypatch):
    monkeypatch.setattr(settings, "max_retries", 1)

    route = respx.get(
        "https://api.example.com/users"
    ).mock(
        side_effect=[
            httpx.ReadTimeout("Request timed out"),
            httpx.Response(200, json={"status": "recovered"})
        ]
    )

    client = AIClient()
    result = await client.get("/users")

    assert result == {"status": "recovered"}
    assert route.call_count == 2


@pytest.mark.asyncio
@respx.mock
async def test_retry_exhaustion(monkeypatch):
    monkeypatch.setattr(settings, "max_retries", 2)

    route = respx.get(
        "https://api.example.com/users"
    ).mock(
        side_effect=httpx.ConnectError("Connection failed")
    )

    client = AIClient()

    with pytest.raises(httpx.ConnectError):
        await client.get("/users")

    assert route.call_count == 3


@pytest.mark.asyncio
@respx.mock
async def test_http_error_is_not_retried(monkeypatch):
    monkeypatch.setattr(settings, "max_retries", 2)

    route = respx.get(
        "https://api.example.com/users"
    ).mock(
        return_value=httpx.Response(404, json={"error": "Not found"})
    )

    client = AIClient()

    with pytest.raises(httpx.HTTPStatusError):
        await client.get("/users")

    assert route.call_count == 1


@pytest.mark.asyncio
@respx.mock
async def test_get_request_uses_correct_endpoint():
    route = respx.get(
        "https://api.example.com/products"
    ).mock(
        return_value=httpx.Response(200, json={"items": []})
    )

    client = AIClient()
    result = await client.get("/products")

    assert result == {"items": []}
    assert route.called
