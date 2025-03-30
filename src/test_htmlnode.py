import unittest

from htmlnode import HTMLNode, LeafNode

class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode("a", "hyperlink", [], {"href": "https://www.google.com"})
        node2 = HTMLNode("a", "hyperlink", [], {"href": "https://www.google.com"})
        self.assertEqual(node, node2)

    def test_children(self):
        children = [
            HTMLNode(),
            HTMLNode(),
            HTMLNode()
        ]
        node = HTMLNode("a", "hyperlink", children, {"href": "https://www.google.com"})
        self.assertEqual(len(node.children), 3)

    def test_props(self):
        node = HTMLNode("a", "hyperlink", [], {"href": "com", "test": "blah"})
        self.assertEqual("test" in node.props.keys(), True)

    def test_props_to_html(self):
        node = HTMLNode("a", "hyperlink", [], {"href": "https://www.google.com","target": "_blank"})
        out = node.props_to_html()
        self.assertEqual(out, ' href="https://www.google.com" target="_blank"')

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_leaf_no_tag(self):
        node = LeafNode(None, "this is raw text", {"not": "rendered"})
        self.assertEqual(node.to_html(), "this is raw text")

    def test_leaf_no_value(self):
        try:
            node = LeafNode("a", None, {"not": "rendered"})
        except ValueError:
            return True
        return False

if __name__ == "__main__":
    unittest.main()