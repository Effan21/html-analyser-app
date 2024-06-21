import pytest
import aiohttp
from analyzer import validate_link

@pytest.mark.asyncio
async def test_validate_link():
    base_url = "https://www.linkedin.com/"
    link = "/?trk=guest_homepage-basic_nav-header-logo"
    link_type = "Internal"
    async with aiohttp.ClientSession() as session:
        result = await validate_link(session, base_url, link, link_type)
        assert result[0] == link
        assert result[1] == link_type
        assert result[2] == True 