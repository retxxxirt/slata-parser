from .parser import Parser

__all__ = [
    'get_categories'
]

parser = Parser()

get_categories = parser.get_categories
