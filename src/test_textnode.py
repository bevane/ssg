import unittest
from htmlnode import LeafNode
from textnode import TextNode, text_node_to_html_node
from textnode import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnode, markdown_to_blocks, block_to_block_type


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)


    def test_neq_url(self):
        node = TextNode("text example", "italic")
        node2 = TextNode("text example", "italic", "https://www.boot.dev")
        self.assertNotEqual(node, node2)


    def test_neq_type(self):
        node = TextNode("text example", "italic")
        node2 = TextNode("text example", "bold")
        self.assertNotEqual(node, node2)


class TestTextNodetoHTMLNode(unittest.TestCase):
    def test_bold(self):
        text_node = TextNode(text="bold text", text_type="bold")
        html = "<b>bold text</b>"
        self.assertEqual(text_node_to_html_node(text_node).to_html(), html)


    def test_url(self):
        text_node = TextNode(
            text="click me", text_type="link", url="www.boot.dev"
        )
        html = '<a href="www.boot.dev">click me</a>'
        self.assertEqual(text_node_to_html_node(text_node).to_html(), html)


    def test_image(self):
        text_node = TextNode(
            text="small cat", text_type="image", url="cat.png"
        )
        html = '<img src="cat.png" alt="small cat"></img>'
        self.assertEqual(text_node_to_html_node(text_node).to_html(), html)


class SplitNodes(unittest.TestCase):
    def test_bold(self):
        old_nodes = [
            TextNode(
                text="This is text with a **bolded** word", text_type="text"
            ),
        ]
        new_nodes = [
            TextNode("This is text with a ", "text"),
            TextNode("bolded", "bold"),
            TextNode(" word", "text")
        ]
        self.assertEqual(
            split_nodes_delimiter(old_nodes, "**", "bold"), new_nodes
        )


    def test_italic(self):
        old_nodes = [
            TextNode(
                text="This is text with an *italic* word", text_type="text"
            ),
        ]
        new_nodes = [
            TextNode("This is text with an ", "text"),
            TextNode("italic", "italic"),
            TextNode(" word", "text")
        ]
        self.assertEqual(
            split_nodes_delimiter(old_nodes, "*", "italic"), new_nodes
        )


    def test_code(self):
        old_nodes = [
            TextNode(
                text="This is text with a `code block` word", text_type="text"
            ),
        ]
        new_nodes = [
            TextNode("This is text with a ", "text"),
            TextNode("code block", "code"),
            TextNode(" word", "text")
        ]
        self.assertEqual(
            split_nodes_delimiter(old_nodes, "`", "code"), new_nodes
        )


    def test_bold_different_words(self):
        old_nodes = [
            TextNode(
                text="This is text with a **bolded** word and **another**",
                text_type="text"
            ),
        ]
        new_nodes = [
            TextNode("This is text with a ", "text"),
            TextNode("bolded", "bold"),
            TextNode(" word and ", "text"),
            TextNode("another", "bold")
        ]
        self.assertEqual(
            split_nodes_delimiter(old_nodes, "**", "bold"), new_nodes
        )


    def test_bold_multi_words(self):
        old_nodes = [
            TextNode(
                text="This is text with **bolded words**.",
                text_type="text"
            ),
        ]
        new_nodes = [
            TextNode("This is text with ", "text"),
            TextNode("bolded words", "bold"),
            TextNode(".", "text"),
        ]
        self.assertEqual(
            split_nodes_delimiter(old_nodes, "**", "bold"), new_nodes
        )


    def test_bold_with_other_types(self):
        old_nodes = [
            TextNode(text="This is a text with ", text_type="text"),
            TextNode(text="italic word", text_type="italic"),
            TextNode(text="and a **bold** word.", text_type="text"),
        ]
        new_nodes = [
            TextNode(text="This is a text with ", text_type="text"),
            TextNode(text="italic word", text_type="italic"),
            TextNode(text="and a ", text_type="text"),
            TextNode(text="bold", text_type="bold"),
            TextNode(text=" word.", text_type="text"),
        ]
        self.assertEqual(
            split_nodes_delimiter(old_nodes, "**", "bold"), new_nodes
        )


    def test_unmatched_delimter_error(self):
        old_node = TextNode(text="This is a **bold text", text_type="text")
        with self.assertRaises(ValueError):
            split_nodes_delimiter([old_node], "**", "bold")


    def test_images(self):
        old_nodes = [
            TextNode("This is a text with an ![image](www.example.com/cat.png)", "text")
        ]
        result = [
            TextNode("This is a text with an ", "text"),
            TextNode("image", "image", "www.example.com/cat.png")
        ]
        self.assertEqual(split_nodes_image(old_nodes), result)


    def test_images_with_trailing_text(self):
        old_nodes = [
            TextNode("This is a text with an ![image](www.example.com/cat.png) and trailing text.", "text")
        ]
        result = [
            TextNode("This is a text with an ", "text"),
            TextNode("image", "image", "www.example.com/cat.png"),
            TextNode(" and trailing text.", "text"),
        ]
        self.assertEqual(split_nodes_image(old_nodes), result)


    def test_images_two_in_one(self):
        old_nodes = [
            TextNode("This is a text with an ![image1](www.example.com/cat.png) and another ![image2](www.example.com/kitten.png)", "text")
        ]
        result = [
            TextNode("This is a text with an ", "text"),
            TextNode("image1", "image", "www.example.com/cat.png"),
            TextNode(" and another ", "text"),
            TextNode("image2", "image", "www.example.com/kitten.png"),
        ]
        self.assertEqual(split_nodes_image(old_nodes), result)


    def test_images_two_together(self):
        old_nodes = [
            TextNode("This is a text with two ![image1](www.example.com/cat.png)![image2](www.example.com/kitten.png)", "text")
        ]
        result = [
            TextNode("This is a text with two ", "text"),
            TextNode("image1", "image", "www.example.com/cat.png"),
            TextNode("image2", "image", "www.example.com/kitten.png"),
        ]
        self.assertEqual(split_nodes_image(old_nodes), result)


    def test_images_with_links(self):
        old_nodes = [
            TextNode("This is a text with an ![image](www.example.com/cat.png) and a link [click me](www.example.com)", "text")
        ]
        result = [
            TextNode("This is a text with an ", "text"),
            TextNode("image", "image", "www.example.com/cat.png"),
            TextNode(" and a link [click me](www.example.com)", "text"),
        ]
        self.assertEqual(split_nodes_image(old_nodes), result)


    def test_images_with_other_types(self):
        old_nodes = [
            TextNode("This is a text with ", "text"),
            TextNode("bold words", "bold"),
            TextNode(" and an ![image](www.example.com/cat.png)", "text")
        ]
        result = [
            TextNode("This is a text with ", "text"),
            TextNode("bold words", "bold"),
            TextNode(" and an ", "text"),
            TextNode("image", "image", "www.example.com/cat.png"),
        ]
        self.assertEqual(split_nodes_image(old_nodes), result)


    def test_links(self):
        old_nodes = [
            TextNode("This is a text with a [hyperlink](www.example.com)", "text")
        ]
        result = [
            TextNode("This is a text with a ", "text"),
            TextNode("hyperlink", "link", "www.example.com")
        ]
        self.assertEqual(split_nodes_link(old_nodes), result)


    def test_links_with_trailing_text(self):
        old_nodes = [
            TextNode("This is a text with a [link](www.example.com) and trailing text.", "text")
        ]
        result = [
            TextNode("This is a text with a ", "text"),
            TextNode("link", "link", "www.example.com"),
            TextNode(" and trailing text.", "text"),
        ]
        self.assertEqual(split_nodes_link(old_nodes), result)


    def test_links_two_in_one(self):
        old_nodes = [
            TextNode("This is a text with a [link1](www.example.com/1/) and another [link2](www.example.com/2/)", "text")
        ]
        result = [
            TextNode("This is a text with a ", "text"),
            TextNode("link1", "link", "www.example.com/1/"),
            TextNode(" and another ", "text"),
            TextNode("link2", "link", "www.example.com/2/"),
        ]
        self.assertEqual(split_nodes_link(old_nodes), result)


    def test_links_two_together(self):
        old_nodes = [
            TextNode("This is a text with two [link1](www.example.com/1/a)[link2](www.example.com/2/a)", "text")
        ]
        result = [
            TextNode("This is a text with two ", "text"),
            TextNode("link1", "link", "www.example.com/1/a"),
            TextNode("link2", "link", "www.example.com/2/a"),
        ]
        self.assertEqual(split_nodes_link(old_nodes), result)


    def test_links_with_images(self):
        old_nodes = [
            TextNode("This is a text with a [link](www.example.com) and an ![image](www.example.com/cat.png)", "text")
        ]
        result = [
            TextNode("This is a text with a ", "text"),
            TextNode("link", "link", "www.example.com"),
            TextNode(" and an ![image](www.example.com/cat.png)", "text"),
        ]
        self.assertEqual(split_nodes_link(old_nodes), result)


    def test_links_with_other_types(self):
        old_nodes = [
            TextNode("This is a text with ", "text"),
            TextNode("bold words", "bold"),
            TextNode(" and a [hyperlink](www.example.com)", "text")
        ]
        result = [
            TextNode("This is a text with ", "text"),
            TextNode("bold words", "bold"),
            TextNode(" and a ", "text"),
            TextNode("hyperlink", "link", "www.example.com"),
        ]
        self.assertEqual(split_nodes_link(old_nodes), result)


    def test_split_all(self):
        text = "All: This is **text** with an *italic* word and a `code block` and an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and a [link](https://boot.dev)"
        results = [
            TextNode("All: This is ", "text"),
            TextNode("text", "bold"),
            TextNode(" with an ", "text"),
            TextNode("italic", "italic"),
            TextNode(" word and a ", "text"),
            TextNode("code block", "code"),
            TextNode(" and an ", "text"),
            TextNode("image", "image", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
            TextNode(" and a ", "text"),
            TextNode("link", "link", "https://boot.dev"),
        ]
        self.assertEqual(text_to_textnode(text), results)


class ExtractMarkdown(unittest.TestCase):
    def test_extract_images(self):
        text = (
            "This is text with an ![image](https://storage.googleapis.com/"
                "qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and "
                "![another](https://storage.googleapis.com/"
                "qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png)"
        )
        result =[
            ("image", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"), ("another", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png")
        ]
        self.assertEqual(extract_markdown_images(text), result)


    def test_extract_links(self):
        text = "This is text with a [link](https://www.example.com) and [another](https://www.example.com/another)"
        result = [("link", "https://www.example.com"), ("another", "https://www.example.com/another")]
        self.assertEqual(extract_markdown_links(text), result)


    def test_extract_links_with_images(self):
        text = "This is text with a [link](https://www.example.com) and an ![image](https://www.example.com/img.png)"
        result = [("link", "https://www.example.com")]
        self.assertEqual(extract_markdown_links(text), result)


class MarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is a list item
* This is another list item
"""
        result = [
            '# This is a heading',
            'This is a paragraph of text. It has some **bold** and *italic* words inside of it.',
            '* This is a list item\n* This is another list item'
        ]
        self.assertEqual(markdown_to_blocks(md), result)


    def test_markdown_to_blocks_trailing_spaces(self):
        md = """
# This is a heading  

   This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is a list item
* This is another list item   
"""
        result = [
            '# This is a heading',
            'This is a paragraph of text. It has some **bold** and *italic* words inside of it.',
            '* This is a list item\n* This is another list item'
        ]
        self.assertEqual(markdown_to_blocks(md), result)


    def test_markdown_to_extra_newlines(self):
        md = """
# This is a heading





This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is a list item
* This is another list item
"""
        result = [
            '# This is a heading',
            'This is a paragraph of text. It has some **bold** and *italic* words inside of it.',
            '* This is a list item\n* This is another list item'
        ]
        self.assertEqual(markdown_to_blocks(md), result)


    def test_block_type_heading(self):
        block = "## heading"
        result = "heading"
        self.assertEqual(block_to_block_type(block), result)


    def test_block_type_code(self):
        block = "```this is a code block````"
        result = "code"
        self.assertEqual(block_to_block_type(block), result)


    def test_block_type_quote(self):
        block = """>this is a quote
>block"""
        result = "quote"
        self.assertEqual(block_to_block_type(block), result)


    def test_block_type_ul(self):
        block = """* this is a list item
- this is a another list item"""
        result = "unordered_list"
        self.assertEqual(block_to_block_type(block), result)


    def test_block_type_ol(self):
        block = """1. this is a list item
2. this is a another list item
3. this is another list item"""
        result = "ordered_list"
        self.assertEqual(block_to_block_type(block), result)


    def test_block_type_para(self):
        block = """this is a
a normal paragraph"""
        result = "paragraph"
        self.assertEqual(block_to_block_type(block), result)


    def test_block_type_para_not_heading(self):
        block = "#this is not a heading"
        result = "paragraph"
        self.assertEqual(block_to_block_type(block), result)


    def test_block_type_para_not_code(self):
        block = """```this is
not a code block"""
        result = "paragraph"
        self.assertEqual(block_to_block_type(block), result)


    def test_block_type_para_not_quote(self):
        block = """>This is 
not a quote 
>block"""
        result = "paragraph"
        self.assertEqual(block_to_block_type(block), result)


    def test_block_type_para_not_ul(self):
        block = """* this is a list item
but this is not
* this is another list item"""
        result = "paragraph"
        self.assertEqual(block_to_block_type(block), result)


    def test_block_type_para_not_ol(self):
        block = """1. this is a list item
3. this is a another list item
4. this is another list item"""
        result = "paragraph"
        self.assertEqual(block_to_block_type(block), result)


if __name__ == "__main__":
    unittest.main()

