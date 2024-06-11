import unittest

from textnode import TextNode, text_node_to_html_node


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


if __name__ == "__main__":
    unittest.main()

