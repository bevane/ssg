import unittest

from textnode import TextNode


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


if __name__ == "__main__":
    unittest.main()
