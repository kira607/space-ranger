import pygame as pg

from space_ranger.assets_manager.font_asset import FontFactory

from ._game_object_property import GameObjectProperty


class Font(GameObjectProperty[pg.font.Font]):
    """An font game object property.

    Holds a pygame.font.Font object that links
    to a system font or to a font file.

    This property itself is linking to a font
    asset.

    :param pygame.font.Font default: The default font,
      defaults to `pg.font.SysFont("Arial", 16)`.
    """

    __animatable__ = False
    __default__ = FontFactory(None)

    def __init__(self, default: FontFactory | None = None, *, always_rebuild: bool = True) -> None:
        super().__init__(default, always_rebuild=always_rebuild)
        self._size = 16
        self._font_factory = default or self.__default__

    @property
    def size(self) -> int:
        """Get the font size in pixels."""
        return self._size

    @size.setter
    def size(self, new_size: int) -> None:
        """Resize the font.

        :param int new_size: A new font size (in pixels).
        """
        self._value = self._font_factory(new_size)

    def set_value(self, value: FontFactory) -> None:
        """Set font value.

        :param FontFactory value: A FontFactory which is used
          to create a text surface.
        """
        if not isinstance(value, FontFactory):
            raise ValueError(f"value must be a FontFactory instance, got {type(value).__name__}")
        self._font_factory = value
        self.resize(self.size)
