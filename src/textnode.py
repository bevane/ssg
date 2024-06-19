import re
from typing import List, Tuple
from htmlnode import LeafNode


class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url


    def __eq__(self, other):
        if (
                self.text == other.text and
                self.text_type == other.text_type and
                self.url == other.url
            ):
            return True
        return False


    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"


def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    text_types_to_html_args = {
        "text": {"value": text_node.text},
        "bold": {"tag": "b", "value": text_node.text},
        "italic": {"tag": "i", "value": text_node.text},
        "code": {"tag": "code", "value": text_node.text},
        "link": {
            "tag": "a",
            "props": {"href": text_node.url}, "value": text_node.text
        },
        "image": {"tag": "img",
                  "props": {"src": text_node.url, "alt": text_node.text},
                  "value": ""
        },
    }

    if not text_node.text_type in text_types_to_html_args:
        raise ValueError(f"{text_node.text_type} is not a valid text type")
    html_node = LeafNode(**text_types_to_html_args[text_node.text_type])
    return html_node


def split_nodes_delimiter(old_nodes: List[TextNode | str],
                          delimiter: str, text_type: str) -> List[TextNode]:
    if text_type not in ["code", "bold", "italic"]:
        raise ValueError(
            'Unsupported text_type,'
            'only "code", "bold" and "italic" are supported'
        )
    new_nodes = []
    for node in old_nodes:
        if not isinstance(node, TextNode) or node.text_type != "text":
            new_nodes.append(node)
            continue
        new_texts = node.text.split(delimiter)
        if not len(new_texts) % 2 != 0:
            # if the number of delimiters is odd, then length of the split
            # will be odd too indicating unmatched delimters
            raise ValueError(
                f'Invalid markdown syntax: delimiter: "{delimiter}" '
                'is unclosed in: "{node.text}"'
            )
        for i in range(0, len(new_texts)):
            if new_texts[i] == "":
                continue
            if (i + 1) % 2 == 0:
                new_nodes.append(
                        TextNode(text=new_texts[i], text_type=text_type)
                )
                continue
            new_nodes.append(
                        TextNode(text=new_texts[i], text_type="text")
            )
    return new_nodes


def extract_markdown_images(text: str) -> List[Tuple[str, str]]:
    matches = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    return matches


def extract_markdown_links(text: str) -> List[Tuple[str, str]]:
    # (?<!!) is a negative lookbehind that will exclude any image markdown
    matches = re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)", text)
    return matches


def split_nodes_image(old_nodes: List[TextNode | str]) -> List[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if not isinstance(node, TextNode) or node.text_type != "text":
            new_nodes.append(node)
            continue
        extracted_md_images = extract_markdown_images(node.text)
        if not extracted_md_images:
            new_nodes.append(node)
        for i, image_tuple in enumerate(extracted_md_images):
            before_after_strs = node.text.split(    
                f"![{image_tuple[0]}]({image_tuple[1]})", maxsplit=1
            )
            if not before_after_strs[0] == "":
                new_nodes.append(
                    TextNode(text=before_after_strs[0], text_type="text")
                )
            new_nodes.append(
                TextNode(text=image_tuple[0], text_type="image",
                         url=image_tuple[1]))

            node.text = before_after_strs[1]
            # append any remaining text after the last image
            if i == len(extracted_md_images) - 1:
                if node.text == "":
                    continue
                new_nodes.append(
                    TextNode(text=node.text, text_type="text")
                )
    return new_nodes


def split_nodes_link(old_nodes: List[TextNode | str]) -> List[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if not isinstance(node, TextNode) or node.text_type != "text":
            new_nodes.append(node)
            continue
        extracted_md_links = extract_markdown_links(node.text)
        if not extracted_md_links:
            new_nodes.append(node)
        for i, link_tuple in enumerate(extracted_md_links):
            before_after_strs = node.text.split(
                f"[{link_tuple[0]}]({link_tuple[1]})", maxsplit=1
            )
            if not before_after_strs[0] == "":
                new_nodes.append(
                    TextNode(text=before_after_strs[0], text_type="text")
                )
            new_nodes.append(
                TextNode(text=link_tuple[0], text_type="link",
                         url=link_tuple[1]))

            node.text = before_after_strs[1]
            # append any remaining text after the last link
            if i == len(extracted_md_links) - 1:
                if node.text == "":
                    continue
                new_nodes.append(
                    TextNode(text=node.text, text_type="text")
                )
    return new_nodes

