import unittest
import requests
import responses
from nhl import NHL
from espn import ESPN
from datetime import date, timedelta

class TestNHLAPI(unittest.TestCase):
    def test_get_today_date(self):
        actual = NHL()._get_today_date()
        expected = (date.today() - timedelta(days=1)).strftime(
            "%Y-%m-%d"
        )
        self.assertEqual(actual, expected)

    @responses.activate
    def test_api(self):
        responses.add(responses.GET, NHL().root_url, status=200)

        resp = requests.get(NHL().root_url)

        self.assertEqual(resp.status_code, 200)

class TestESPNAPI(unittest.TestCase):
    def test_get_today_date(self):
        actual = ESPN()._get_today_date()
        expected = (date.today() - timedelta()).strftime(
            "%Y%m%d"
        )
        self.assertEqual(actual, expected)

if __name__ == '__main__':
    unittest.main()