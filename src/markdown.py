import re
from typing import List, Tuple
from htmlnode import HTMLNode, ParentNode
from textnode import TextNode, text_node_to_html_node


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


def text_to_textnode(text):
    raw_text_nodes = [TextNode(text, "text")]
    bold_nodes = split_nodes_delimiter(raw_text_nodes, "**", "bold")
    italic_bold_nodes = split_nodes_delimiter(bold_nodes, "*", "italic")
    code_italic_bold_nodes = split_nodes_delimiter(italic_bold_nodes, "`", "code")
    image_code_italic_bold_nodes = split_nodes_image(code_italic_bold_nodes)
    link_image_code_italic_bold_nodes = split_nodes_link(image_code_italic_bold_nodes)

    return link_image_code_italic_bold_nodes


def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    new_blocks = []
    for block in blocks:
        block = block.strip().strip("\n")
        if block:
            new_blocks.append(block)

    return new_blocks


def block_to_block_type(block):
    if (block.startswith("# ")
        or block.startswith("## ")
        or block.startswith("### ")
        or block.startswith("#### ")
        or block.startswith("##### ")
        or block.startswith("###### ")
    ):
        return "heading"

    if block.startswith("```") and block.endswith("```"):
        return "code"

    is_quote=False
    for line in block.split("\n"):
        if line.startswith(">"):
            is_quote = True
        else:
            is_quote = False
            break
    if is_quote:
        return "quote"

    is_ul = False
    for line in block.split("\n"):
        if line.startswith("* ") or line.startswith("- "):
            is_ul = True
        else:
            is_ul = False
            break
    if is_ul:
        return "unordered_list"

    is_ol = False
    n = 1
    for line in block.split("\n"):
        if line.startswith(f"{n}. "):
            is_ol = True
            n += 1
        else:
            is_ol = False
            break
    if is_ol:
        return "ordered_list"

    return "paragraph"


def heading_block_to_html_node(heading_block):
    level = 0
    content_start_index = 0
    for i in range(len(heading_block)):
        if heading_block[i] != "#":
            content_start_index = i + 1
            break
        level += 1
    content = heading_block[content_start_index:]
    text_nodes = text_to_textnode(content)
    html_children = [text_node_to_html_node(node) for node in text_nodes]
    return ParentNode(tag=f"h{level}", children=html_children)


def code_block_to_html_node(code_block):
    content = code_block.strip("```")
    text_nodes = text_to_textnode(content)
    html_children = [text_node_to_html_node(node) for node in text_nodes]
    return ParentNode(
        tag="pre", children=[ParentNode(
                      tag="code", children=html_children
        )]
    )


def quote_block_to_html_node(quote_block):
    content = "\n".join([line[1:] for line in quote_block.split("\n")])
    text_nodes = text_to_textnode(content)
    html_children = [text_node_to_html_node(node) for node in text_nodes]
    return ParentNode(tag="quoteblock", children=html_children)


def ul_block_to_html_node(ul_block):
    items = [item[2:] for item in ul_block.split("\n")]
    items_text_nodes = [text_to_textnode(item) for item in items]
    html_items = [
        ParentNode(tag="li", children=[
            text_node_to_html_node(item_inline) for item_inline in list_item
        ]) for list_item in items_text_nodes
    ]
    return ParentNode(tag="ul", children=html_items)


def ol_block_to_html_node(ol_block):
    items = [item[3:] for item in ol_block.split("\n")]
    items_text_nodes = [text_to_textnode(item) for item in items]
    html_items = [
        ParentNode(tag="li", children=[
            text_node_to_html_node(item_inline) for item_inline in list_item
        ]) for list_item in items_text_nodes
    ]
    return ParentNode(tag="ol", children=html_items)


def paragraph_block_to_html_node(paragraph_block):
    content = paragraph_block
    text_nodes = text_to_textnode(content)
    html_children = [text_node_to_html_node(node) for node in text_nodes]
    return ParentNode(tag="p", children=html_children)


def markdown_to_html_node(markdown) -> HTMLNode:
    block_types_to_functions = {
        "heading": heading_block_to_html_node,
        "code": code_block_to_html_node,
        "quote": quote_block_to_html_node,
        "unordered_list": ul_block_to_html_node,
        "ordered_list": ol_block_to_html_node,
        "paragraph": paragraph_block_to_html_node

    }
    blocks = markdown_to_blocks(markdown)
    blocks_with_types = []
    for block in blocks:
        block_type = block_to_block_type(block)
        blocks_with_types.append((block, block_type))
    html_nodes = []
    for block in blocks_with_types:
        html_nodes.append(block_types_to_functions[block[1]](block[0]))

    return ParentNode(tag="div", children=html_nodes)

def extract_title(markdown):
    first_block = markdown_to_blocks(markdown)[0].split("\n")[0]
    if not first_block.startswith("# "):
        raise ValueError(
        "Markdown file does not have a header (line starting with # in the beginning"
    )
    title = first_block[2:]
    return title

