class ExistsError(Exception):
    """That already exists"""
    pass


class NotExistsError(Exception):
    """That's just not there"""


class FullError(Exception):
    """This container is full"""
    pass
