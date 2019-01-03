import json
import time
import unittest
from unittest import mock

import pytest
import requests
from requests.exceptions import HTTPError

from src.social.reddit import Reddit

#TODO: Move _mock_response to a conf.py or something similiar, add more tests
time = time.time()
DATA = {
    "data": {
        "children": [{
            "foo": "bar",
            "bar": "foo",
            "data": {
                "created_utc": time,
            }
        }],
    }
}

def _mock_response(status=200, content="CONTENT", json_data=None, raise_for_status=None):
    ''' Helper that will build out a mock response for you

    Args:
        status (int): Http Status of Mock Request
        content (string): Content Type of Mock Request
        json_data (dict): JSON data sent back from Mock Request
        raise_for_status (): Exception to raise for status of Mock Requests

    Returns:
        mock.Mock request.Response object
    '''
    resp = mock.Mock()
    resp.raise_for_status = mock.Mock()
    if raise_for_status:
        resp.raise_for_status.side_effect = raise_for_status

    resp.status_code = status
    resp.content = content

    if json_data:
        resp.json = mock.Mock(
            return_value=json_data
        )

    return resp


@mock.patch('src.social.reddit.requests.get')
def test_reddit_scrape(mock_get):
    mock_resp = _mock_response(json_data=DATA)
    mock_get.return_value = mock_resp

    reddit = Reddit(user='FooBoi')
    got = reddit.scrape()

    assert got[0]['foo'] == 'bar'
    assert got[0]['bar'] == 'foo'


@mock.patch('src.social.reddit.requests.get')
def test_reddit_scrape_requests_error(mock_get):
    mock_resp = _mock_response(status=500, raise_for_status=HTTPError("reddit is down"))
    mock_get.return_value = mock_resp

    with pytest.raises(HTTPError):
        reddit = Reddit(user='FooBoi')
        got = reddit.scrape()
