import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_to_props(self):
        prop = {
            "href": "https://www.google.com",
            "target": "_blank",
        }
        prop2 = {
            "class": "nav",
        }
        node = HTMLNode("p", "Lorem Ipsum", "div", prop)
        node2 = HTMLNode("p", "Example Text", None, prop2)
        
        props=' href="https://www.google.com" target="_blank"'
        props2=' class="nav"'
        self.assertEqual(node.props_to_html(), props)
        self.assertEqual(node2.props_to_html(), props2)


class TestLeafNode(unittest.TestCase):
    def test_to_html(self):
        node = LeafNode("p", "This is a paragraph of text.")
        node2 = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        node_html = '<p>This is a paragraph of text.</p>'
        node2_html = '<a href="https://www.google.com">Click me!</a>'
        self.assertEqual(node.to_html(), node_html)
        self.assertEqual(node2.to_html(), node2_html)


class TestParentNode(unittest.TestCase):
    def test_to_html(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        node2 = ParentNode(
                "div",
                [node,]
        )
        node3 = ParentNode(
                "div",
                [
                    LeafNode("h1", "Title"),
                    node,
                    node2,
                ]
        )
        node_html = '<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>'
        node2_html = (
            '<div>'
                '<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>'
            '</div>'
        )
        node3_html = (
            '<div>'
                '<h1>Title</h1>'
                '<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>'
                '<div>'
                    '<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>'
                '</div>'
            '</div>'
        )
        self.assertEqual(node.to_html(), node_html)
        # test for nesting ParentNode inside a ParentNode
        self.assertEqual(node2.to_html(), node2_html)
        # test for varying and multiple levels of nesting
        self.assertEqual(node3.to_html(), node3_html)


if __name__ == "__main__":
    unittest.main()
 
