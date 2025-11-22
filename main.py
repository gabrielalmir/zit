import sys

from rich import print

import command


def main():
    args = command.parse_commands()

    if args.command == "init":
        command.initialize_repository()
        return

    print("[red]Usage: zit <command> [<args>][/red]", file=sys.stderr)
    sys.exit(1)

if __name__ == "__main__":
    main()
