import json
import os
from unittest import TestCase

from requests import HTTPError

from slata_parser.parser import Parser


class ParserTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.parser = Parser()

    @staticmethod
    def load_fixture(filename: str) -> dict:
        with open(os.path.join(os.path.dirname(__file__), filename), 'r+') as file:
            return json.loads(file.read())

    def test__make_request(self):
        self.assertEqual(self.parser._make_request('/').status_code, 200)
        self.assertRaises(HTTPError, self.parser._make_request, '/catalog/0/0/')

    def test_get_categories(self):
        self.assertEqual(self.load_fixture('categories.json'), self.parser.get_categories())
