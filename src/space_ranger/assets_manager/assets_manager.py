from .font_asset import FontAsset
from .image_asset import ImageAsset
from .music_asset import MusicAsset
from .sound_asset import SoundAsset


class AssetsManager:
    """Assets manager."""

    main_menu_music = MusicAsset("Sayer_Remembrance_Park.mp3")
    game_music = MusicAsset("Sayer_Andromeda.mp3")

    click_sound = SoundAsset("click2.wav")
    shoot_sound = SoundAsset("shoot.wav")

    big_asteroid = ImageAsset("asteroid_big.png")

    menu_font = FontAsset("MK-90.ttf")
