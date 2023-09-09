from space_ranger.asset.font_asset import FontFactory
from space_ranger.core import Property


class Font(Property[FontFactory]):
    """A font game object property.

    Holds a FontFactory object that links
    to a system font or to a font file.

    :param FontFactory default: The default font,
      defaults to `FontFactory(None)` (which is `pg.font.Font(None, 16)`).
    """

    __animatable__ = False
    __default__ = FontFactory(None)
