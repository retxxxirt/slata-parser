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

    def get_catalogues(self) -> List[dict]:
        catalogues, soup = [], BeautifulSoup(self._make_request('/').content, 'html.parser')

        for catalog_element in soup.select('nav li.dropmenu__list--item.hasDrop'):
            catalog_link_element = catalog_element.select_one('.item__link')

            catalogues.append({
                'id': int(catalog_link_element['href'].split('/')[2]),
                'name': catalog_link_element.text.replace('\t', '').strip(),
                'catalogues': []
            })

            for child_catalog_link_element in catalog_element.select('.list__item--link'):
                catalogues[-1]['catalogues'].append({
                    'id': int(child_catalog_link_element['href'].split('/')[2]),
                    'name': child_catalog_link_element.text.replace('\t', '').strip()
                })

        return catalogues
