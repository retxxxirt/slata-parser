import json
import os
from typing import List
from unittest import TestCase

from requests import HTTPError

from slata_parser.parser import Parser


class ParserTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.parser = Parser()

    @staticmethod
    def load_fixture(filename: str) -> List[dict]:
        with open(os.path.join(os.path.dirname(__file__), filename), 'r+') as file:
            return json.loads(file.read())

    def test__make_request(self):
        self.assertEqual(self.parser._make_request('/').status_code, 200)
        self.assertRaises(HTTPError, self.parser._make_request, '/catalog/0/0/')

    def test_get_catalogues(self):
        self.assertEqual(self.load_fixture('catalogues.json'), self.parser.get_catalogues())

    def test_get_catalog(self):
        for catalog_sample in self.load_fixture('catalog-samples.json'):
            catalog = self.parser.get_catalog(catalog_sample['id'])

            for key in catalog.keys() - {'products'}:
                self.assertEqual(catalog[key], catalog_sample[key])

            self.assertGreater(len(catalog['products']), 0)
