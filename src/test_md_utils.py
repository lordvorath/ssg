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

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with an [link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_mixed_images_links(self):
        node = TextNode(
            "This is text with an [mix1link](https://i.imgur.com/zjjcJKZ.png) and an ![mix1image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an [mix1link](https://i.imgur.com/zjjcJKZ.png) and an ", TextType.TEXT),
                TextNode(
                    "mix1image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_mixed_images_links2(self):
        node = TextNode(
            "This is text with an [mix2link](https://i.imgur.com/zjjcJKZ.png) and an ![mix2image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("mix2link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and an ![mix2image](https://i.imgur.com/3elNhQu.png)", TextType.TEXT),
            ],
            new_nodes,
        )

