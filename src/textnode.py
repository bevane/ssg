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

