from .parser import Parser

__all__ = [
    'get_catalogues'
]

parser = Parser()

get_catalogues = parser.get_catalogues
