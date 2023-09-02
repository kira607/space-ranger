from enum import Enum, auto

import pygame

from space_ranger.common import Color
from space_ranger.globals import ASSETS, SETTINGS
from space_ranger.states import State, StateId
from space_ranger.ui import Button


class MenuState(Enum):
    """Main menu state."""

    MAIN = auto()
    CONTROLS = auto()
    OPTIONS = auto()


class MainMenu(State):
    """A main menu state."""

    def __init__(self, state_id: StateId) -> None:
        super().__init__(state_id)

        self.click_sound: pygame.mixer.Sound
        self.font: pygame.font.Font
        self.button_color: Color
        self.text_color: Color

        self.button_play_hover_color: Color
        self.button_controls_hover_color: Color
        self.button_options_hover_color: Color
        self.button_exit_hover_color: Color

        self.button_play: Button
        self.button_controls: Button
        self.button_options: Button
        self.button_exit: Button

        self.front_flash: pygame.Surface

        self.state: MenuState

        self.updating: bool
        self.update_time: float
        self.update_time_max: int

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

        self.front_flash = pygame.Surface(SETTINGS.screen_size)

        self.state = MenuState.MAIN

        self.updating = False
        self.update_time = 0
        self.update_time_max = 600

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
            self._handle_click()

        if event.type == pygame.KEYDOWN and event.key == pygame.K_u:
            self.button_play.position = (100, 100)

        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self._quit = True
            return

    def update(self, delta_time: int) -> None:
        """Update main menu state.

        :param int delta_time: Delta time (in milliseconds).
        """
        self.update_time += delta_time
        self._update_buttons_colors()

        if self.update_progress >= 1:
            self.updating = False

        if self.updating:
            self.logger.debug(f"Updating... t={self.update_time} ({self.update_progress})")
            self._move_button(self.button_play)
            self._move_button(self.button_controls)
            self._move_button(self.button_options)
            self._move_button(self.button_exit)

    def draw(self, screen: pygame.Surface) -> None:
        """Draw main menu on a given screen.

        :param pygame.Surface screen: Target screen.
        """
        screen.fill(Color(230, 230, 230, 200))

        self.button_play.draw(screen)
        self.button_controls.draw(screen)
        self.button_options.draw(screen)
        self.button_exit.draw(screen)

        if self.updating:
            t = self.update_progress
            alpha = max(0, int((-7 * t * t + 4 * t) * 255))
            self.front_flash.set_alpha(alpha)
            self.front_flash.fill(Color(255, 255, 255, alpha))
            screen.blit(self.front_flash, (0, 0))

    @property
    def update_progress(self) -> float:
        """Get a normalized state update progress."""
        return self.update_time / self.update_time_max

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

    def _handle_click(self) -> None:
        """Handle mouse button click."""
        self.click_sound.play()
        clicked_button = self._get_hovered_button()

        if not clicked_button:
            return

        self.logger.info(f"Clicked: {clicked_button.text}")

        if clicked_button == self.button_play:
            pass

        if clicked_button == self.button_controls:
            if self.state == MenuState.CONTROLS:
                self.state = MenuState.MAIN
            else:
                self.state = MenuState.CONTROLS

            self.update_time = 0
            self.updating = True

        if clicked_button == self.button_options:
            if self.state == MenuState.OPTIONS:
                self.state = MenuState.MAIN
            else:
                self.state = MenuState.OPTIONS

            self.update_time = 0
            self.updating = True

        if clicked_button == self.button_exit:
            self._quit = True
            return

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

    def _move_button(self, button: Button) -> None:
        current_pos = pygame.math.Vector2(button.position.x, button.position.y)
        dest_pos = self._get_button_dest(button)
        path_vector = current_pos + (dest_pos - current_pos) * self.update_progress
        button.position = (path_vector.x, path_vector.y)

    def _get_button_dest(self, button: Button) -> pygame.math.Vector2:
        if self.state == MenuState.MAIN:
            x = (SETTINGS.screen_width - button.width) / 2

        if self.state == MenuState.CONTROLS:
            x = SETTINGS.screen_width - self.space_between_buttons - button.width

        if self.state == MenuState.OPTIONS:
            x = self.space_between_buttons

        return pygame.math.Vector2(x, button.position.y)

    def _get_hovered_button(self) -> Button | None:
        """Get a button on which mouse is hovered on.

        :return: A currently hovered button if available, None otherwise.
        :rtype: Button | None
        """
        mouse_point = pygame.mouse.get_pos()
        for button in (
            self.button_play,
            self.button_controls,
            self.button_options,
            self.button_exit,
        ):
            if button._rect.collidepoint(mouse_point):
                return button
        return None
