from textnode import *
from os import path, listdir, mkdir
from shutil import copy, rmtree

def cleanup_public(public):
    if path.exists(public):
        print(f"Demolishing {public} directory")
        try:
            rmtree(public)
        except Exception as e:
            print(f"Failed to remove {public}: {e}")
    try:
        mkdir(public)
    except Exception as e:
        print(f"Failed to create {public}: {e}")

def copy_static_to_public():
    if path.exists("./static"):
        static = "./static"
    elif path.exists("../static"):
        static = "../static"
    else:
        raise Exception("static directory not found")
    if path.exists("./public"):
        public = "./public"
    elif path.exists("../public"):
        public = "../public"
    else:
        raise Exception("public directory not found")
    cleanup_public(public)
    copy_dir_to(static, public)

def copy_dir_to(dir, to):
    if not path.exists(dir):
        raise Exception(f"Source Path {dir} does not exist")
    if not path.exists(to):
        print(f"Destination Path {to} does not exist, creating now...")
        try:
            mkdir(to)
        except Exception as e:
            raise Exception(f"Failed to create destination {to}: {e}")
    for file in listdir(dir):
        p = path.join(dir, file)
        if not path.isfile(p):
            if path.isdir(p):
                copy_dir_to(p, path.join(to, file))
                continue
            raise Exception(f"{p} is neither file nor directory")
        try:
            copy(p, to)
        except Exception as e:
            print(f"Failed to copy {p} to {to}: {e}")

def main():
    copy_static_to_public()

main()