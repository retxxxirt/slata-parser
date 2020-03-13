import json
from unittest import TestCase

from requests import HTTPError

from slata_parser.parser import Parser


class ParserTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.parser = Parser()

    def test__make_request(self):
        self.assertEqual(self.parser._make_request('/').status_code, 200)
        self.assertRaises(HTTPError, self.parser._make_request, '/catalog/0/0/')

    def test_get_categories(self):
        with open('categories.js', 'r+') as file:
            categories_sample = json.loads(file.read())

        self.assertEqual(categories_sample, self.parser.get_categories())
