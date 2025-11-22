import argparse
import os
import zlib

ZIT_DIR = ".zit"

def parse_commands():
    parser = argparse.ArgumentParser(description="Zit Version Control System")

    subparsers = parser.add_subparsers(dest="command")
    subparsers.add_parser("init", help="Initialize a new zit repository")

    catfile_parsers = subparsers.add_parser("cat-file", help="Provide content of a file object")
    catfile_parsers.add_argument("-p", help="Pretty-print the contents of <object>", action="store_true")
    catfile_parsers.add_argument("object", help="The object to display")

    return parser.parse_args()

def initialize_repository():
    os.makedirs(ZIT_DIR, exist_ok=True)
    os.makedirs(os.path.join(ZIT_DIR, "objects"), exist_ok=True)
    os.makedirs(os.path.join(ZIT_DIR, "refs"), exist_ok=True)

    with open(os.path.join(ZIT_DIR, "HEAD"), 'w') as head_file:
        head_file.write("ref: refs/heads/main\n")

    print("Initialized empty zit repository in {}".format(os.path.abspath(ZIT_DIR)))

def cat_file(args: argparse.Namespace):
    object_name = args.object
    path = os.path.join(ZIT_DIR, "objects", object_name[:2], object_name[2:])

    try:
        with open(path, 'rb') as f:
            raw = zlib.decompress(f.read())
            header, content = raw.split(b"\0", 1)

            if args.p:
                print(content.decode('utf-8'), end='')
    except FileNotFoundError:
        print(f"Error: Not a valid object name {object_name}")
    except Exception as e:
        print(f"Error reading object: {e}")
