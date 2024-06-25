import os
import shutil

def main():
    copy_to_public("static")


def copy_to_public(dir, first_iter=True):
    if first_iter:
        if os.path.exists("public"):
            shutil.rmtree("public")
            print(f"old public dir cleared")
        os.mkdir("public")
    dir_items = os.listdir(path=dir)
    # for path in directories:
    for item in dir_items:
        full_path = os.path.join(dir, item)
        new_path = full_path.split("/", maxsplit=1)
        new_path[0] = "public"
        new_path = "/".join(new_path)
        if os.path.isfile(full_path):
            shutil.copy(full_path, new_path)
            print(f"file copied from '{full_path}' to '{new_path}'")
        # if path is directory recurse
        else:
            if not os.path.exists(new_path):
                os.mkdir(new_path)
                print(f"new dir created: {new_path}")
            copy_to_public(full_path, first_iter=False)
    return

