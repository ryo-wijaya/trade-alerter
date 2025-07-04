import logging


class AlerterError(Exception):
    """
    Generic exception class for the alerter.
    """

    def __init__(self, message):
        super().__init__(message)
        logging.error(message)


class AuthenticationError(AlerterError):
    """
    Exception raised for authentication errors.
    """

    def __init__(self, message):
        super().__init__(message)
        logging.error(message)
