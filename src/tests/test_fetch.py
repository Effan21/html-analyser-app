import pytest
import aiohttp
from analyzer import fetch

@pytest.mark.asyncio
async def test_fetch():
    url = "https://www.linkedin.com/"
    async with aiohttp.ClientSession() as session:
        status, reason = await fetch(session, url)
        assert status == 200