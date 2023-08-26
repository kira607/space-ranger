import pygame

from space_ranger.assets_manager import ASSETS
from space_ranger.states import State as State
from space_ranger.states import StateId as StateId


class Text:
    """A text object."""

    def __init__(self, text: str, color: pygame.Color, font: pygame.font.Font) -> None:
        self._text = text
        self._color = color
        self._font = font
        self._img: pygame.Surface
        self._update()

    @property
    def text(self) -> str:
        """Text."""
        return self.text

    @text.setter
    def text(self, new_text: str) -> None:
        """Set a new text."""
        self._text = new_text
        self._update

    @property
    def color(self) -> pygame.Color:
        """Text color."""
        return self._color

    @color.setter
    def color(self, new_color: pygame.Color) -> None:
        """Set a new text color."""
        self._color = new_color
        self._update()

    @property
    def font(self) -> pygame.font.Font:
        """Text font."""
        return self._font

    @font.setter
    def font(self, new_font: pygame.font.Font) -> None:
        """Set a new text font."""
        self._font = new_font
        self._update()

    def _update(self) -> None:
        """Update an uderlying pygame.Surface object for text."""
        self._img = self._font.render(self._text, False, self._color)

    def draw(self, screen: pygame.Surface) -> None:
        """Draw text on screen.

        :param pygame.Surface screen: Target screen.
        """
        screen.blit(self._img, (100, 100))


class Button:
    """A menu button.

    :param str text: Button text.
    """

    def __init__(self, text: str = "Button") -> None:
        self._rect = pygame.Rect(30, 30, 60, 60)
        self._text = Text(text, pygame.Color(255, 255, 255), ASSETS.menu_font)  # type: ignore

    def draw(self, screen: pygame.Surface) -> None:
        """Draw a buttion on a screen.

        :param pygame.Surface screen: A screen to draw on.
        """
        pygame.draw.rect(screen, pygame.Color(255, 0, 0), self._rect, border_radius=0)
        self._text.draw(screen)


class MainMenu(State):
    """A main menu state."""

    def __init__(self, state_id: StateId) -> None:
        super().__init__(state_id)
        self.play_button = None
        self.asteroid = None
        self.sound = None

    def startup(self) -> None:
        """Startup."""
        self.button = Button()
        self.asteroid = ASSETS.big_asteroid
        self.sound = ASSETS.click_sound
        ASSETS.main_menu_music.play()

    def cleanup(self) -> None:
        """Cleanup."""
        self.play_button = None
        self.asteroid = None
        self.sound = None

    def process_event(self, event: pygame.event.Event) -> None:
        """Process event."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.sound.play()

    def update(self, screen: pygame.Surface, delta_time: float) -> None:
        """Update state.

        :param pygame.Surface screen: A current screen.
        :param float delta_time: Delta time.
        :return: None
        """
        self.button.draw(screen)
        screen.blit(self.asteroid, (40, 20))
