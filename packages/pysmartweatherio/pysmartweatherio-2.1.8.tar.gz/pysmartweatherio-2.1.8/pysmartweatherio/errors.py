"""Define package errors."""


class SmartWeatherError(Exception):
    """Define a base error."""


class InvalidApiKey(SmartWeatherError):
    """Define an error related to invalid or missing API Key."""


class RequestError(SmartWeatherError):
    """Define an error related to invalid requests."""


class ResultError(SmartWeatherError):
    """Define an error related to the result returned from a request."""
