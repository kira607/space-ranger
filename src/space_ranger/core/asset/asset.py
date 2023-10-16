import abc
import typing as t
from pathlib import Path

from space_ranger.core import ctx
from space_ranger.core.logging import LoggerMixin


T = t.TypeVar("T")


class Asset(abc.ABC, LoggerMixin, t.Generic[T]):
    """A base asset class.

    :param str name: A file name of asset.
    """

    sub_dir = ""

    def __init__(self, name: str, **kwargs: t.Any) -> None:
        self._path = Path(ctx.config.assets_dir, self.sub_dir, name)
        self._kwargs = kwargs
        self._asset = None

    @property
    def path(self) -> Path:
        """Full asset path.

        :return: Asset path
        :rtype: Path
        """
        return self._path

    def load(self, force: bool = False, **kwargs: t.Any) -> T:
        """Load asset.

        :param bool, optional force: Ignore if asset is already loaded, defaults to False

        :return: Loaded asset.
        :rtype: T
        """
        self._kwargs.update(kwargs)
        if not self._asset or force:
            self._asset = self._load_asset(**kwargs)
        return self._asset

    @abc.abstractmethod
    def _load_asset(self) -> T:
        """Load asset."""
        raise NotImplementedError()
