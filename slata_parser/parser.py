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

    def get_categories(self):
        categories, soup = [], BeautifulSoup(self._make_request('/').content, 'html.parser')

        for category_element in soup.select('nav li.dropmenu__list--item.hasDrop'):
            category_link_element = category_element.select_one('.item__link')

            categories.append({
                'id': int(category_link_element['href'].split('/')[2]),
                'name': category_link_element.text.replace('\t', '').strip(),
                'subcategories': []
            })

            for subcategory_link_element in category_element.select('.list__item--link'):
                categories[-1]['subcategories'].append({
                    'id': int(subcategory_link_element['href'].split('/')[2]),
                    'name': subcategory_link_element.text.replace('\t', '').strip()
                })

        return categories
