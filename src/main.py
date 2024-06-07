from htmlnode import LeafNode
from textnode import TextNode


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

# t1 = TextNode(text="bold text", text_type="bold")
# t2 = TextNode(text="click me", text_type="link", url="www.boot.dev")
# t3 = TextNode(text="small cat", text_type="image", url="cat.png")
# print(text_node_to_html_node(t1).to_html())
# print(text_node_to_html_node(t2).to_html())
# print(text_node_to_html_node(t3).to_html())

