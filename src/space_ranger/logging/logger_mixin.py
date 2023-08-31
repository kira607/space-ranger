import logging


class LoggerMixin:
    """A mixin adding logger member to a class."""

    _logger = None

    @property
    def logger(self) -> logging.Logger:
        """Get a local logger."""
        if self._logger is None:
            self._logger = logging.getLogger(self.__class__.__name__)
        return self._logger
