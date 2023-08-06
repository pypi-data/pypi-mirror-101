"""
datass submodule for handling module exceptions
"""

import traceback


class DataSSBaseException(Exception):
    """
    Modules base exception

    Returns
    -------
    str
        Error message
    """
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
