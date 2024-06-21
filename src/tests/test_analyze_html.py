import pytest
from analyzer import analyze_html

@pytest.mark.asyncio
async def test_analyze_html():
    url = "https://www.linkedin.com/"
    results = await analyze_html(url)
    
    assert 'html_version' in results
    assert 'title' in results
    assert 'headings' in results
    assert 'internal_links' in results
    assert 'external_links' in results
    assert 'login_form' in results
    assert 'link_validation' in results
