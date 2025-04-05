import unittest

from md_utils import *

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

    def test_extract_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        out = extract_markdown_images(text)
        self.assertEqual(out, [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")])
    
    def test_extract_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        out = extract_markdown_links(text)
        self.assertEqual(out, [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")])
