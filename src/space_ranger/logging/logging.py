import logging
from typing import Literal

DEFAULT_LOGGING_LEVEL = "DEBUG"
DEFAULT_LOGGING_FORMAT = "{asctime} ({filename}) [{levelname}]: {message}"
DEFAULT_LOGGING_STYLE = "{"


def init_logging(
    level: str = "DEBUG",
    fmt: str = "{asctime} ({filename}) [{levelname}]: {message}",
    style: Literal["{", "%", "$"] = "{",
) -> None:
    """Initialize logging.

    :param str, optional level: Logging level, defaults to "DEBUG"
    :param str, optional fmt: Logging format, defaults to "{asctime} ({filename}) [{levelname}]: {message}"
    :param str, optional style: Logging format style, defaults to "{"
    """
    logging.basicConfig(level=level, format=fmt, style=style)
