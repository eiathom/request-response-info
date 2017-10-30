"""
testing the url_checker component
"""
from urllib2 import URLError
from urllib2 import HTTPError
from mock import patch
from src.component.code.url_checker import (
    get_http_request_response_data,
    get_error_data,
    get_checked_url
)


@patch('src.component.code.url_checker.urllib2.urlopen')
def test_get_handled_exception_response_data(mock_urlopen):
    """
    test get_handled_exception_response_data
    """
    url_to_use = 'http://www.some.url.com'

    # assert data when URLError
    expected_data = get_error_data(url_to_use, 'Invalid URL', True)
    do_assert_error_response_data(
        mock_urlopen, url_to_use, expected_data, URLError(
            reason='something'))

    # assert data when HTTPError
    expected_data = get_error_data(url_to_use, 404)
    do_assert_error_response_data(
        mock_urlopen, url_to_use, expected_data, HTTPError(
            url=None, code=404, msg=None, hdrs=None, fp=None))


def test_get_checked_url():
    """
    test test_get_checked_url
    """
    invalid_urls = [r"www.bbc.co.uk", r"bad://address"]
    for url in invalid_urls:
        actual_data = get_checked_url(url)
        assert actual_data == get_error_data(url, "Invalid URL", True)

    valid_urls = [r"https://www.bbc.co.uk/", r"http://google.com"]
    for url in valid_urls:
        actual_data = get_checked_url(url)
        assert actual_data is None


def do_assert_error_response_data(
        mock_urlopen, url_to_use, expected_data, exception_object):
    mock_urlopen.side_effect = exception_object
    actual_data = get_http_request_response_data(url_to_use)
    assert expected_data == actual_data

