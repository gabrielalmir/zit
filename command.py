import argparse
import os

ZIT_DIR = ".zit"

def parse_commands():
    parser = argparse.ArgumentParser(description="Zit Version Control System")

    subparsers = parser.add_subparsers(dest="command")
    subparsers.add_parser("init", help="Initialize a new zit repository")

    return parser.parse_args()

def initialize_repository():
    os.makedirs(ZIT_DIR, exist_ok=True)
    os.makedirs(os.path.join(ZIT_DIR, "objects"), exist_ok=True)
    os.makedirs(os.path.join(ZIT_DIR, "refs"), exist_ok=True)

    with open(os.path.join(ZIT_DIR, "HEAD"), 'w') as head_file:
        head_file.write("ref: refs/heads/main\n")

    print("Initialized empty zit repository in {}".format(os.path.abspath(ZIT_DIR)))

