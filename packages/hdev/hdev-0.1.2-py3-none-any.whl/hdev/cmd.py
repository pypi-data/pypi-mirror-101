"""Entry point for the hdev tool."""
import argparse
import pathlib
import sys

from hdev.configuration import load_configuration
from hdev.requirements import PythonRequirements


class HParser(argparse.ArgumentParser):
    """Overwrites ArgumentParser to control the `error` behaviour."""

    def error(self, message):
        """Implement callback for error while parsing user input."""
        sys.stderr.write("error: %s\n" % message)
        self.print_help()
        sys.exit(2)

    @staticmethod
    def create_parser():
        """Create a argparse parser for hdev parameters."""
        parser = HParser()
        parser.add_argument(
            "-f",
            type=pathlib.Path,
            dest="pyproject_path",
            required=False,
            help="Path of the project's pyproject.toml Defaults to `./pyproject.toml`",
        )
        subparsers = parser.add_subparsers()

        parser_requirements = subparsers.add_parser(
            "requirements",
            help="Compiles .txt requirements file based on the existing .in files using pip-tools",
        )
        parser_requirements.set_defaults(class_=PythonRequirements)

        return parser


def hdev():  # pragma: no cover
    """Create an argsparse cmdline tools to expose hdev functionality.

    Main entry point of hdev
    """
    parser = HParser.create_parser()
    args = parser.parse_args()
    if not hasattr(args, "class_"):
        parser.print_help()
        sys.exit(2)

    config = load_configuration(args.pyproject_path)

    cmd_args = vars(args)
    # Remove common arguments
    CommandClass = cmd_args.pop("class_")  # pylint: disable=invalid-name
    cmd_args.pop("pyproject_path", None)

    # All classes that implement commands will take the config on __init__
    # and the command specific argparse arguments on .run
    message, exit_code = CommandClass(config).run(**cmd_args)
    if message:
        print(message)

    sys.exit(exit_code)
