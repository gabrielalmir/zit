import argparse
import sys
from typing import Callable

from rich import print

ZIT_DIR = ".zit"

class CommandHandler:
    args: argparse.Namespace
    commands: dict[str, Callable]

    def __init__(self, args: argparse.Namespace):
        self.args = args
        self.commands = {}

    @staticmethod
    def parse() -> argparse.Namespace:
        parser = argparse.ArgumentParser(description="Zit Version Control System")

        subparsers = parser.add_subparsers(dest="command")
        subparsers.add_parser("init", help="Initialize a new zit repository")

        catfile_parsers = subparsers.add_parser("cat-file", help="Provide content of a file object")
        catfile_parsers.add_argument("-p", help="Pretty-print the contents of <object>", action="store_true")
        catfile_parsers.add_argument("object", help="The object to display")

        hash_objects_parser = subparsers.add_parser("hash-object", help="Compute object ID and optionally create a blob from a file")
        hash_objects_parser.add_argument("-w", help="Write the object into the database", action="store_true")
        hash_objects_parser.add_argument("file", help="The file to hash")

        return parser.parse_args()

    def add_command(self, command_name: str, handler):
        self.commands[command_name] = handler

    def execute(self):
        if self.args.command in self.commands:
            self.commands[self.args.command](self.args)
            return

        print("[red]Usage: zit <command> [<args>][/red]", file=sys.stderr)
        sys.exit(1)

