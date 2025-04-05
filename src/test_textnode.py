import unittest

from md_utils import *
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

class TestTextNodeToHTML(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is a bold node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold node")

    def test_italic(self):
        node = TextNode("This is a italic node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is a italic node")

    def test_code(self):
        node = TextNode("This is a code node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a code node")

    def test_link(self):
        node = TextNode("This is a link node", TextType.LINK, "http://testurl.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link node")
        self.assertEqual(html_node.props["href"], "http://testurl.com")

    def test_image(self):
        node = TextNode("This is a img node", TextType.IMAGE, "http://testurl.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props["src"], "http://testurl.com")
        self.assertEqual(html_node.props["alt"], "This is a img node")

    def test_value_error(self):
        node = TextNode("This is a img node", "something", "http://testurl.com")
        self.assertRaises(ValueError, text_node_to_html_node, node)

if __name__ == "__main__":
    unittest.main()