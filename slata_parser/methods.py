from .parser import Parser

__all__ = [
    'get_catalogs', 'get_catalog'
]

parser = Parser()

get_catalogs = parser.get_catalogs
get_catalog = parser.get_catalog
