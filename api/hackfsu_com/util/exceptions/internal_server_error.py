"""
    For logging internal server errors
"""

from hackfsu_com.util.exceptions import BaseError


class InternalServerError(BaseError):
    def __init__(self, source_exception: Exception):
        super().__init__(source_exception)
