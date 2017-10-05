"""
    For logging external user errors
"""

from hackfsu_com.util.exceptions import BaseError


class ExternalUserError(BaseError):
    response_status = 400

    def __init__(self, source_exception: Exception):
        super().__init__(source_exception)
