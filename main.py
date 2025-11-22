

import commands
from command import CommandHandler


def main():
    args = CommandHandler(CommandHandler.parse())
    args.add_command("init", lambda args: commands.initialize_repository())
    args.add_command("cat-file", commands.cat_file)
    args.add_command("hash-object", commands.hash_object)
    args.execute()

if __name__ == "__main__":
    main()
