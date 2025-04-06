from textnode import *
from md_utils import *
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

def extract_title(md):
    for line in md.split("\n"):
        if line.startswith("# "):
            return line.replace("# ", "")
    raise Exception("No h1 header found")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    if not path.exists(from_path) or not path.isfile(from_path):
        raise Exception(f"{from_path} doesn't exist or is not a file")
    if not path.exists(template_path) or not path.isfile(template_path):
        raise Exception(f"{template_path} doesn't exist or is not a file")
    if not path.exists(dest_path) or not path.isfile(dest_path):
        try:
            print(f"{dest_path} not found, attempting to create it")
            out = open(dest_path, "x")
        except Exception as e:
            raise Exception(f"{dest_path} doesn't exist or is not a file: {e}")
    else:
        try:
            out = open(dest_path, "w")
        except Exception as e:
            raise Exception(f"Failed to opend {dest_path} to write")
    try:
        md = open(from_path).read()
    except Exception as e:
        print(f"Could not open {from_path}: {e}")
    try:
        template = open(template_path).read()
    except Exception as e:
        print(f"Could not open {template_path}: {e}")
    html = markdown_to_html_node(md).to_html()
    h1 = extract_title(md)
    result = template.replace(r"{{ Title }}", h1).replace(r"{{ Content }}", html)
    out.write(result)
    out.close()


    

    


def main():
    copy_static_to_public()
    generate_page("content/index.md", "template.html", "public/index.html")

main()