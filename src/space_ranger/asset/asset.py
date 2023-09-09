import abc
import typing as t
from pathlib import Path

from space_ranger import ctx
from space_ranger.logging import LoggerMixin

T = t.TypeVar("T")


class Asset(abc.ABC, LoggerMixin, t.Generic[T]):
    """A base asset class.

    This is a descriptor abstracting loading assets.
    Asset properties are readonly.

    :param str name: A file name of asset.
    :param str description: Asset description
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
        return Path(ctx.config.assets_dir, self.sub_dir, self.asset_name)

    def load(self, force: bool = False, **kwargs) -> T:
        """Load asset.

        :param bool, optional force: Ignore if asset is already loaded, defaults to False

        :return: Loaded asset.
        :rtype: T
        """
        self._kwargs.update(kwargs)
        if not self.asset or force:
            self.asset = self._load_asset(**kwargs)
        return self.asset

    @abc.abstractmethod
    def _load_asset(self) -> T:
        """Load asset."""
        raise NotImplementedError()
