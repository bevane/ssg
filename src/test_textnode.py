import unittest
from htmlnode import LeafNode
from textnode import TextNode, text_node_to_html_node, split_nodes_delimiter, extract_markdown_images, extract_markdown_links


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


    def test_unmatched_delimter_error(self):
        old_node = TextNode(text="This is a **bold text", text_type="text")
        with self.assertRaises(ValueError):
            split_nodes_delimiter([old_node], "**", "bold")


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


if __name__ == "__main__":
    unittest.main()

