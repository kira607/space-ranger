import argparse
import cProfile
import os
import pstats
import sys
from pathlib import Path

from space_ranger import __version__
from space_ranger.core import Application, ctx
from space_ranger.core.logging import init_logging
from space_ranger.scenes import Playground


def get_title() -> str:
    """Get application title."""
    return f"Space ranger {__version__}"


def get_parser() -> argparse.ArgumentParser:
    """Get a cli args parser."""
    parser = argparse.ArgumentParser(description=get_title())
    parser.add_argument("-v", "--version", action="store_true", help="show version and exit")
    parser.add_argument(
        "-l",
        "--logging-level",
        choices=["debug", "info", "warning", "critical"],
        default="debug",
        help="logs level",
    )
    parser.add_argument(
        "-d",
        "--debug",
        action="store_true",
        help="run application in debug mode",
    )
    return parser


def main() -> None:
    """Create and run application."""
    parser = get_parser()
    args = parser.parse_args()

    if args.version:
        sys.stdout.write(get_title() + "\n")
        exit(0)

    ctx.config.logging_level = args.logging_level.upper()
    init_logging(level=ctx.config.logging_level)
    ctx.config.debug = args.debug
    ctx.config.assets_dir = Path(os.path.dirname(__file__), "assets")
    ctx.screen.width = 1920
    ctx.screen.height = 1080

    app = Application(get_title())
    # app.register_scene(Playground("playground"))

    with cProfile.Profile() as pr:
        app.run()

    stats = pstats.Stats(pr)
    stats.sort_stats(pstats.SortKey.TIME)
    # stats.print_stats()
    # uid = datetime.now().strftime("%S-%M-%H-%d-%m-%Y")
    # profiling_resutls_path = f"logs/profile-{uid}.prof"
    # stats.dump_stats(filename=profiling_resutls_path)
    # ctx.logger.info(f"session profiling and logs are written to: {profiling_resutls_path}")


if __name__ == "__main__":
    main()
