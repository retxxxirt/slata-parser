from typing import List

import requests
from bs4 import BeautifulSoup
from requests import Response

from .exceptions import TemporaryUnavailableException


class Parser:
    DEFAULT_URL = 'https://shop.slata.ru'
    ERROR_STRINGS = ['DB query error', 'Mysql connect error']

    def _make_request(self, uri: str, params: dict = None) -> Response:
        response = requests.get((self.DEFAULT_URL + uri), params)
        response.raise_for_status()

        if True in [e in response.text for e in self.ERROR_STRINGS]:
            raise TemporaryUnavailableException()
        return response

    def get_catalogs(self) -> List[dict]:
        catalogs, soup = [], BeautifulSoup(self._make_request('/').content, 'html.parser')

        for catalog_element in soup.select('nav li.dropmenu__list--item.hasDrop'):
            catalog_link_element = catalog_element.select_one('.item__link')

            catalogs.append({
                'id': int(catalog_link_element['href'].split('/')[2]),
                'name': catalog_link_element.text.replace('\t', '').strip(),
                'catalogs': []
            })

            for child_catalog_link_element in catalog_element.select('.list__item--link'):
                catalogs[-1]['catalogs'].append({
                    'id': int(child_catalog_link_element['href'].split('/')[2]),
                    'name': child_catalog_link_element.text.replace('\t', '').strip()
                })

        return catalogs

    def get_catalog(self, catalog_id: int) -> dict:
        response = self._make_request(f'/catalog/{catalog_id}/', params={'SHOWALL_1': 1})
        soup = BeautifulSoup(response.content, 'html.parser')

        catalog = {
            'id': catalog_id, 'products': [], 'catalogs': [],
            'name': soup.select_one('.page-header').text.replace('\n', '')
        }

        for product_element in soup.select('.js-product'):
            product = {
                'id': int(product_element.select_one('.item__link')['href'].split('/')[-2]),
                'url': self.DEFAULT_URL + product_element.select_one('.item__link')['href'],
                'image_url': self.DEFAULT_URL + product_element.select_one('.item__pic--in img')['src'],
                'name': product_element.select_one('.item__title--wrap').text.strip()
            }

            product_outer_price_element = product_element.select_one('.item__price')
            product_common_price_element = product_outer_price_element.select_one('s')

            if product_common_price_element:
                product['common_price'] = float(product_common_price_element.text.strip().split()[0])
                product['discount_price'] = float(product_outer_price_element.text.strip().split()[0])
            else:
                product['common_price'] = float(product_outer_price_element.text.strip().split()[0])
                product['discount_price'] = None

            catalog['products'].append(product)

        for catalog_link_element in soup.select('.as-categories a'):
            catalog['catalogs'].append({
                'id': int(catalog_link_element['href'].split('/')[-2]),
                'url': self.DEFAULT_URL + catalog_link_element['href'],
                'name': catalog_link_element.text.strip()
            })

        return catalog
