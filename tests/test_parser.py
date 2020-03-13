import json
import os
from typing import List
from unittest import TestCase

from requests import HTTPError

from slata_parser.exceptions import CatalogNotFound
from slata_parser.parser import Parser


class ParserTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.parser = Parser()

    @staticmethod
    def load_fixture(filename: str) -> List[dict]:
        with open(os.path.join(os.path.dirname(__file__), filename), 'r+') as file:
            return json.loads(file.read())

    @staticmethod
    def save_fixture(filename: str, fixture: List[dict]):
        with open(os.path.join(os.path.dirname(__file__), filename), 'w+') as file:
            file.write(json.dumps(fixture))

    def test__make_request(self):
        self.assertEqual(self.parser._make_request('/').status_code, 200)
        self.assertRaises(HTTPError, self.parser._make_request, '/catalog/0/0/')

    def test_get_catalogs(self):
        self.assertEqual(self.load_fixture('catalogs-sample.json'), self.parser.get_catalogs())

    def test_get_catalog(self):
        for catalog_sample in self.load_fixture('catalog-samples.json'):
            catalog = self.parser.get_catalog(catalog_sample['id'])

            for key in catalog.keys() - {'products'}:
                self.assertEqual(catalog[key], catalog_sample[key])

            self.assertGreater(len(catalog['products']), 0)

        self.assertRaises(CatalogNotFound, self.parser.get_catalog, 4469)

    def test_get_product(self):
        for product_sample in self.load_fixture('product-samples.json'):
            product = self.parser.get_product(product_sample['catalog_id'], product_sample['id'])

            for key in product.keys() - {'common_price', 'discount_price', 'is_available'}:
                self.assertEqual(product[key], product_sample[key])
