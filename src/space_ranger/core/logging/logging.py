import logging
from typing import Literal


def init_logging(
    level: str = "DEBUG",
    fmt: str = "{asctime} ({filename}:{lineno}) [{levelname}]: {message}",
    style: Literal["{", "%", "$"] = "{",
) -> None:
    """Initialize logging.

    :param str, optional level: Logging level, defaults to "DEBUG"
    :param str, optional fmt: Logging format, defaults to "{asctime} ({filename}:{lineno}) [{levelname}]: {message}"
    :param str, optional style: Logging format style, defaults to "{"
    """
    logging.basicConfig(level=level, format=fmt, style=style)
