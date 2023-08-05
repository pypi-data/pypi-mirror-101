""" Communicates with a Smart Weather weatherstation from WeatherFlow using REST. """

from pysmartweatherio.client import SmartWeather  # noqa # pylint: disable=unused-import
from pysmartweatherio.const import (  # noqa # pylint: disable=unused-import
    FORECAST_TYPE_DAILY,
    FORECAST_TYPE_HOURLY,
    FORECAST_TYPES,
    UNIT_SYSTEM_IMPERIAL,
    UNIT_SYSTEM_METRIC,
    UNIT_TYPE_DISTANCE,
    UNIT_TYPE_PRESSURE,
    UNIT_TYPE_RAIN,
    UNIT_TYPE_TEMP,
    UNIT_TYPE_WIND,
    UNIT_WIND_KMH,
    UNIT_WIND_MPH,
    UNIT_WIND_MS,
)
from pysmartweatherio.errors import (  # noqa # pylint: disable=unused-import
    InvalidApiKey,
    RequestError,
    ResultError,
    SmartWeatherError,
)
