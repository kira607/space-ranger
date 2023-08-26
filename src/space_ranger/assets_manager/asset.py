import os
import typing
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Generic, TypeVar

from space_ranger.logging import LoggerMixin

if typing.TYPE_CHECKING:
    from space_ranger.assets_manager.assets_manager import AssetsManager


ASSETS_DIR = Path(os.path.dirname(__file__), "..", "assets")


T = TypeVar("T")


class Asset(ABC, LoggerMixin, Generic[T]):
    """A base asset class.

    This is a descriptor abstracting loading assets.
    Asset properties are readonly.

    :param str name: A file name of asset.
    :param str description: Asset description
    """

    sub_dir = ""
    asset_type = None

    def __init__(
        self,
        name: str,
        description: str | None = None,
        **kwargs: Any,
    ) -> None:
        self.owner: AssetsManager
        self.private_name: str
        self.asset_name: str
        self.kwargs: dict[str, Any]
        if description is None:
            description = f"{self.__class__.__name__} '{self.asset_name}' at '{self.path}'"
        self.__doc__ = description

    @property
    def path(self) -> Path:
        """Full asset path.

        :return: Asset path
        :rtype: Path
        """
        return Path(ASSETS_DIR, self.sub_dir, self.asset_name)

    @property
    def asset(self) -> T | None:
        """Get asset object."""
        return getattr(self.owner, self.private_name, None)

    @asset.setter
    def asset(self, value: T) -> None:
        """Set asset value."""
        setattr(self.owner, self.private_name, value)

    def __get__(self, instance: object, owner: type) -> "Asset[T]" | T | None:
        """Get asset value."""
        if instance is None:
            return self
        if self.asset is None:
            self.load_asset()
        return self.asset

    def __set__(self, instance: object, value: Any) -> None:  # noqa: ANN401
        """Set value.

        :raises AttributeError: Asset assignment is forbidden
        """
        raise AttributeError(f"{self.__class__.__name__} attribute is read only.")

    def __set_name__(self, owner: "AssetsManager", name: str) -> None:
        """Initialize asset propery.

        :param type owner: Owner class. Always should be :class:`space_ranger.assets_manager.AssetsManager`
        :param str name: Name of asset property.
        """
        self.logger.info(f"Creating a new asset: {self.__doc__}")
        self.owner = owner
        self.private_name = f"_{name}"

    @abstractmethod
    def load_asset(self) -> None:
        """Load asset."""
        raise NotImplementedError()
