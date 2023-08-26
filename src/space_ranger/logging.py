import logging
from typing import Literal

DEFAULT_LOGGING_LEVEL = "DEBUG"
DEFAULT_LOGGING_FORMAT = "{asctime} ({filename}) [{levelname}]: {message}"
DEFAULT_LOGGING_STYLE = "{"


def init_logging(
    level: str = DEFAULT_LOGGING_LEVEL,
    fmt: str = DEFAULT_LOGGING_FORMAT,
    style: Literal["{", "%", "$"] = "{",
) -> None:
    """Initialize logging.

    :param str, optional level: Logging level, defaults to DEFAULT_LOGGING_LEVEL
    :param str, optional fmt: Logging format, defaults to DEFAULT_LOGGING_FORMAT
    :param str, optional style: Logging format style, defaults to DEFAULT_LOGGING_STYLE
    """
    logging.basicConfig(level=level, format=fmt, style=style)


class LoggerMixin:
    """A mixin adding logger member to a class."""

    _logger = None

    @property
    def logger(self) -> logging.Logger:
        """Get a local logger."""
        if self._logger is None:
            self._logger = logging.getLogger(self.__class__.__name__)
        return self._logger
