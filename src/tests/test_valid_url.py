from utils import is_valid_url

def test_is_valid_url_valid():
    assert is_valid_url("http://example.com") == True
    assert is_valid_url("https://example.com/page") == True

def test_is_valid_url_invalid():
    assert is_valid_url("invalid_url") == False
    assert is_valid_url("ftp://example.com") == False
