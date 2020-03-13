class SlataParserException(Exception):
    pass


class TemporaryUnavailableException(SlataParserException):
    def __init__(self):
        super().__init__('Server temporary unavailable. Try again later.')
