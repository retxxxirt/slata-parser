class SlataParserException(Exception):
    pass


class TemporaryUnavailableException(SlataParserException):
    def __init__(self):
        super().__init__('Server temporary unavailable. Try again later.')


class CatalogNotFound(SlataParserException):
    def __init__(self, catalog_id: int):
        super().__init__(f'Catalog {catalog_id} not found.')


class ProductNotFound(SlataParserException):
    def __init__(self, category_id: int, product_id: int):
        super().__init__(f'Product {product_id} in category {category_id} not found.')
