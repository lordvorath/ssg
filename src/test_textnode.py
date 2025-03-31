import unittest

from main import text_node_to_html_node, split_nodes_delimiter
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

class TestMarkdownToHTML(unittest.TestCase):
    def test_bold(self):
        node = TextNode("This text has **a bold section** inside it", TextType.TEXT) 
        nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(nodes), 3)
        self.assertEqual(nodes[1].text_type, TextType.BOLD)

    def test_italic(self):
        node = TextNode("This text has _italic section_ inside it", TextType.TEXT) 
        nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(len(nodes), 3)
        self.assertEqual(nodes[1].text_type, TextType.ITALIC)

    def test_code(self):
        node = TextNode("This text has `code section` inside it", TextType.TEXT) 
        nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(nodes), 3)
        self.assertEqual(nodes[1].text_type, TextType.CODE)

    def test_more_code(self):
        node = TextNode("This text has `code section` inside it `and another one`", TextType.TEXT) 
        nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(nodes), 5)
        self.assertEqual(nodes[1].text_type, TextType.CODE)

    def test_invalid_bold(self):
        node = TextNode("This text has **a bold section** inside it **but broken", TextType.TEXT) 
        self.assertRaises(ValueError, split_nodes_delimiter, [node], "**", TextType.BOLD)

    def test_not_text_node(self):
        node = TextNode("This node is **not** of Type TEXT", TextType.BOLD)
        nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(nodes[0].text_type, TextType.BOLD)

    def test_more_nodes(self):
        n1 = TextNode('one', TextType.TEXT)
        n2 = TextNode('two', TextType.TEXT)
        n3 = TextNode('three', TextType.TEXT)
        nodes = split_nodes_delimiter([n1, n2, n3], "**", TextType.BOLD)
        self.assertEqual(len(nodes), 3)

if __name__ == "__main__":
    unittest.main()