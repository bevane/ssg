import os
import shutil
import markdown

def main():
    copy_to_public("static")
    generate_pages_recursive("content", "template.html", "public")


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


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, 'r') as f:
        md_contents = f.read()

    with open(template_path, 'r') as f:
        template_contents = f.read()

    title = markdown.extract_title(md_contents)
    html_content = markdown.markdown_to_html_node(md_contents).to_html()

    html_file_content = (template_contents.replace("{{ Title }}", title)
                                          .replace("{{ Content }}", html_content)
    )

    dest_dir = os.path.dirname(dest_path)
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    with open(dest_path, 'w') as f:
        f.write(html_file_content)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    dir_items = os.listdir(path=dir_path_content)
    # for path in directories:
    for item in dir_items:
        full_path = os.path.join(dir_path_content, item)
        new_path = os.path.join(dest_dir_path, item.replace("md", "html"))
        if full_path.endswith(".md"):
            generate_page(full_path, template_path, new_path)
        # if path is directory recurse
        else:
            if not os.path.exists(new_path):
                os.mkdir(new_path)
                print(f"new dir created: {new_path}")
            generate_pages_recursive(full_path, template_path, new_path)
    return


main()
