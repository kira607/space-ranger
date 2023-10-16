import pygame as pg

from ._ctx import ctx
from .logging import LoggerMixin
from .scene import Scene
from .utils import get_text_surface


class Application(LoggerMixin):
    """A main application class."""

    def __init__(self, title: str = "Game") -> None:
        self.logger.info(f"Initializing application {title}...")

        self._title = title
        self._scenes: dict[str, Scene] = {}
        self._running = False

        pg.init()

        self._screen = pg.display.set_mode(
            ctx.screen.size,
            pg.HWSURFACE | pg.DOUBLEBUF,
            vsync=ctx.screen.vsync,
        )

        ctx.screen.width = self._screen.get_width()
        ctx.screen.height = self._screen.get_height()
        pg.display.set_caption(self._title)

        self._clock = pg.time.Clock()
        self._debug_font = ctx.debug_text_font

        self._current_scene: Scene

    def register_scene(self, scene: Scene) -> None:
        """Add a scene to the application."""
        self._scenes[scene.id] = scene

    def run(self, start_scene_id: str) -> None:
        """Run application."""
        try:
            self._init(start_scene_id)
            self._main_loop()
        except BaseException as e:
            self.logger.exception(f"Unhandled exception {e}:")
            self.logger.critical("Application has stopped because of an unhandled exception")
        finally:
            self._cleanup()

    def _init(self, start_scene_id: str) -> None:
        """Initialize application."""
        if not self._scenes:
            raise ValueError("Cannot start application with zero scenes.")

        self._current_scene = self._scenes[start_scene_id]
        self._current_scene.start()
        self._running = True

    def _main_loop(self) -> None:
        """Run a main loop of the application."""
        self.logger.info("Running main loop of the application")
        while self._running:
            delta_time = self._clock.tick(ctx.screen.fps)
            self._process_events()
            self._update(delta_time)
            self._draw()

    def _process_events(self) -> None:
        """Process pygame events."""
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self._running = False
            if event.type == pg.KEYDOWN and event.key == pg.K_F3:
                on_off = "off" if ctx.config.debug else "on"
                self.logger.info(f"Switching debug mode to: {on_off}")
                ctx.config.debug = not ctx.config.debug
            self._current_scene.process_event(event)

    def _update(self, delta_time: int) -> None:
        """Run current scene update.

        :param int delta_time: Delta time (in milliseconds).
        """
        if self._current_scene.is_app_should_quit:
            self._running = False
        elif self._current_scene.is_done:
            self._current_scene = self._get_next_scene()
        self._current_scene.update(delta_time)

    def _draw(self) -> None:
        """Render current scene."""
        self._current_scene.draw(self._screen)
        if ctx.config.debug:
            self._draw_debug_info()
        pg.display.update()

    def _draw_debug_info(self) -> None:
        debug_surface = get_text_surface(
            f"FPS: {round(self._clock.get_fps(), 2)}",
            f"Scene: {self._current_scene.id}",
            f"Screen size: {ctx.screen.width}:{ctx.screen.height}",
            font=ctx.debug_text_font,
            color=ctx.debug_text_color,
            background=ctx.debug_text_background,
            antialias=True,
        )
        self._screen.blit(debug_surface, (0, 0))

        # screen grid
        pg.draw.line(self._screen, (30, 30, 30, 200), (0, ctx.screen.center.y), (ctx.screen.width, ctx.screen.center.y))
        pg.draw.line(
            self._screen, (30, 30, 30, 200), (ctx.screen.center.x, 0), (ctx.screen.center.x, ctx.screen.height)
        )

    def _cleanup(self) -> None:
        """Cleanup before quitting application."""
        self._current_scene.finish()
        pg.quit()

    def _get_next_scene(self) -> Scene:
        """Get a next scene.

        This will finish current scene and startup a next scene.

        :return: Next scene.
        :rtype: Scene
        """
        previous_scene_id = self._current_scene.id
        next_scene_id = self._current_scene.get_next_scene()
        self._current_scene.finish()
        next_scene = self._scenes[next_scene_id]
        next_scene.previous = previous_scene_id
        next_scene.start()
        return next_scene
