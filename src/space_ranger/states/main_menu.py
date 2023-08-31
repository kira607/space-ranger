import pygame

from space_ranger.common import Color
from space_ranger.globals import ASSETS, SETTINGS
from space_ranger.states import State, StateId
from space_ranger.ui import Button


class MainMenu(State):
    """A main menu state."""

    def __init__(self, state_id: StateId) -> None:
        super().__init__(state_id)

        self.click_sound: pygame.mixer.Sound
        self.font: pygame.font.Font
        self.button_color: Color
        self.text_color: Color

        self.button_play: Button
        self.button_controls: Button
        self.button_options: Button
        self.button_exit: Button

        self.button_play_hover_color: Color
        self.button_controls_hover_color: Color
        self.button_options_hover_color: Color
        self.button_exit_hover_color: Color

        self.space_between_buttons: int

    def startup(self) -> None:
        """Startup."""
        super().startup()

        self.click_sound = ASSETS.click_sound
        self.font = ASSETS.menu_font(int(SETTINGS.screen_height * 0.027))
        self.button_color = Color(100, 100, 100, 255)
        self.text_color = Color(170, 170, 170, 255)

        self.button_play_hover_color = Color(150, 250, 150, 255)
        self.button_controls_hover_color = Color(250, 250, 150, 255)
        self.button_options_hover_color = Color(150, 250, 250, 255)
        self.button_exit_hover_color = Color(250, 150, 150, 255)

        self.button_play = self._make_button("PLAY")
        self.button_controls = self._make_button("CONTROLS")
        self.button_options = self._make_button("OPTIONS")
        self.button_exit = self._make_button("EXIT")

        button_height = self.button_play.height
        self.space_between_buttons = int(SETTINGS.screen_height * 0.009)

        self.button_play.position = (
            (SETTINGS.screen_width - self.button_play.width) / 2,
            SETTINGS.screen_height / 2 - button_height * 2 - self.space_between_buttons * 1.5,
        )
        self.button_controls.position = (
            (SETTINGS.screen_width - self.button_controls.width) / 2,
            SETTINGS.screen_height / 2 - button_height - self.space_between_buttons * 0.5,
        )
        self.button_options.position = (
            (SETTINGS.screen_width - self.button_options.width) / 2,
            SETTINGS.screen_height / 2 + self.space_between_buttons * 0.5,
        )
        self.button_exit.position = (
            (SETTINGS.screen_width - self.button_exit.width) / 2,
            SETTINGS.screen_height / 2 + button_height + self.space_between_buttons * 1.5,
        )

    def cleanup(self) -> None:
        """Cleanup."""
        super().cleanup()

    def process_event(self, event: pygame.event.Event) -> None:
        """Process pygame event.

        :param pygame.event.Event event: A pygame event to process.
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.click_sound.play()

        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self._quit = True
            return

    def update(self, delta_time: float) -> None:
        """Update main menu state.

        :param float delta_time: Delta time.
        """
        self._update_buttons_colors()

    def draw(self, screen: pygame.Surface) -> None:
        """Draw main menu on a given screen.

        :param pygame.Surface screen: Target screen.
        """
        screen.fill(Color(230, 230, 230, 200))
        self.button_play.draw(screen)
        self.button_controls.draw(screen)
        self.button_options.draw(screen)
        self.button_exit.draw(screen)

    def _make_button(self, text: str) -> Button:
        """Make a menu button.

        :param str text: Button text.

        :return: A new menu button
        :rtype: Button
        """
        return Button(
            text=text,
            color=self.button_color,
            text_color=self.text_color,
            text_font=self.font,
        )

    def _update_buttons_colors(self) -> None:
        """Highlight hovered button."""
        mouse_point = pygame.mouse.get_pos()

        if self.button_play._rect.collidepoint(mouse_point):
            self.button_play.text_color = self.button_play_hover_color
        else:
            self.button_play.text_color = self.text_color

        if self.button_controls._rect.collidepoint(mouse_point):
            self.button_controls.text_color = self.button_controls_hover_color
        else:
            self.button_controls.text_color = self.text_color

        if self.button_options._rect.collidepoint(mouse_point):
            self.button_options.text_color = self.button_options_hover_color
        else:
            self.button_options.text_color = self.text_color

        if self.button_exit._rect.collidepoint(mouse_point):
            self.button_exit.text_color = self.button_exit_hover_color
        else:
            self.button_exit.text_color = self.text_color

    def _get_hovered_button(self) -> Button | None:
        """Get a button on which mouse is hovered on.

        :return: A currently hovered button if available, None otherwise.
        :rtype: Button | None
        """
        mouse_point = pygame.mouse.get_pos()
        if self.button_play._rect.collidepoint(mouse_point):
            return self.button_play
        return None
