from .parser import Parser

__all__ = [
    'get_catalogues', 'get_catalog'
]

parser = Parser()

get_catalogues = parser.get_catalogues
get_catalog = parser.get_catalog
