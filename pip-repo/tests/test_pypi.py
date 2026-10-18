import httpx
import pytest
import respx

from pip_repro.pypi import PyPIClient

FAKE = {
    "info": {"name": "django", "version": "4.2.1"},
    "releases": {},
}


@pytest.mark.asyncio
@respx.mock
async def test_get_project():
    respx.get("https://pypi.org/pypi/django/json").mock(
        return_value=httpx.Response(200, json=FAKE)
    )
    async with PyPIClient() as client:
        data = await client.get_project("django")
    assert data["info"]["name"] == "django"


@pytest.mark.asyncio
@respx.mock
async def test_get_many_handles_http_errors_and_invalid_json():
    respx.get("https://pypi.org/pypi/django/json").mock(side_effect=httpx.HTTPError("boom"))
    respx.get("https://pypi.org/pypi/requests/json").mock(
        return_value=httpx.Response(200, text="not json")
    )

    async with PyPIClient() as client:
        data = await client.get_many(["django", "requests"])

    assert data["django"] == {}
    assert data["requests"] == {}
