import argparse
import sys

from space_ranger import __version__, ctx
from space_ranger.application import Application
from space_ranger.logging import init_logging
from space_ranger.scenes import Playground


def get_title() -> str:
    """Get title."""
    return f"Space ranger {__version__}"


def get_parser() -> argparse.ArgumentParser:
    """Get a cli args parser."""
    parser = argparse.ArgumentParser(description=get_title())
    parser.add_argument("-v", "--version", action="store_true", help="show version and exit")
    parser.add_argument("-l", "--logging-level", choices=["debug", "info", "warning", "critical"], help="logs level")
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

    states = {
        state.id: state
        for state in (
            # MainMenu("main_menu"),
            Playground("playground"),
        )
    }
    app = Application(states, "playground")
    app.run()


if __name__ == "__main__":
    main()
