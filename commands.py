import argparse
import hashlib
import os
import zlib

from command import ZIT_DIR


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

def hash_object(args: argparse.Namespace):
    with open(args.file, 'rb') as f:
        data = f.read()

    header = f"blob {len(data)}\0".encode('utf-8')
    full_data = header + data
    sha1 = zlib.compress(full_data)

    # should be 40 chars for sha1
    object_name = int(hashlib.sha1(full_data).hexdigest(), 16)

    if args.w:
        dir_path = os.path.join(ZIT_DIR, "objects", f"{object_name:08x}"[:2])
        os.makedirs(dir_path, exist_ok=True)
        with open(os.path.join(dir_path, f"{object_name:08x}"[2:]), 'wb') as obj_file:
            obj_file.write(sha1)

    print(f"{object_name:08x}")
