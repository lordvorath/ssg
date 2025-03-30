import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_ineq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_url(self):
        node = TextNode("This is a text node", TextType.BOLD, "https://test.com")
        self.assertEqual(node.url, "https://test.com")

    def test_repr(self):
        node = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev") 
        node_repr = node.__repr__()
        self.assertEqual(node_repr, "TextNode(This is some anchor text, link, https://www.boot.dev)")

if __name__ == "__main__":
    unittest.main()