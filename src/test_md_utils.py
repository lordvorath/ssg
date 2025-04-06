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
        self.assertEqual(len(nodes), 4)
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

    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        new_nodes = text_to_textnodes(text)
        self.assertEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            new_nodes
        )

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
    """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_block_to_paragraph(self):
        md = """This is a paragraph
with two lines and **bold** text
"""
        block = markdown_to_blocks(md)[0]
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_block_to_heading_1(self):
        md = """
# This is a heading
"""
        block = markdown_to_blocks(md)[0]
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.HEADING)
    
    def test_block_to_heading_6(self):
        md = """
###### This is a heading
"""
        block = markdown_to_blocks(md)[0]
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.HEADING)

    def test_block_to_heading_7(self):
        md = """
####### This is not a valid heading
"""
        block = markdown_to_blocks(md)[0]
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_block_to_code(self):
        md = """
```python
var = 123
print(var)
# This is a python comment
```"""
        block = markdown_to_blocks(md)[0]
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.CODE)

    def test_block_to_quote(self):
        md = """
> The best laid plans
> of mice and men
is not a quote

is a > quote

> this is another
> proper quote
"""
        blocks = markdown_to_blocks(md)
        types = []
        for block in blocks:
            types.append(block_to_block_type(block))
        self.assertEqual(types, [
            BlockType.PARAGRAPH,
            BlockType.PARAGRAPH,
            BlockType.QUOTE
        ])

    def test_block_to_unordered_list(self):
        md = """
- The best laid plans
- of mice and men
is not a quote

is a - quote

- this is another
- proper quote
"""
        blocks = markdown_to_blocks(md)
        types = []
        for block in blocks:
            types.append(block_to_block_type(block))
        self.assertEqual(types, [
            BlockType.PARAGRAPH,
            BlockType.PARAGRAPH,
            BlockType.UNORDERED_LIST
        ])

    def test_block_to_ordered_list(self):
        md = """
2. this
1. is not
3. an OL

1. this
2. instead
3. is
"""
        blocks = markdown_to_blocks(md)
        types = []
        for block in blocks:
            types.append(block_to_block_type(block))
        self.assertEqual(types, [
            BlockType.PARAGRAPH,
            BlockType.ORDERED_LIST
        ])

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph 
text in a 
p tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph \ntext in a \np tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_headings(self):
        md = """
# Heading h1

### Heading h3
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html,
                         "<div><h1>Heading h1</h1><h3>Heading h3</h3></div>")

    def test_quote(self):
        md = """
> Markdown is a
> quote block

> and another
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html,
                         "<div><blockquote>Markdown is a\nquote block</blockquote><blockquote>and another</blockquote></div>")
                
    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
    )

    def test_unordered_list(self):
        md = """
- first item
- second **item**
- third _item_

- second list
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>first item</li><li>second <b>item</b></li><li>third <i>item</i></li></ul><ul><li>second list</li></ul></div>"

        )

    def test_ordered_list(self):
        md = """
1. Item 1
2. Item **2**
3. Item _3_
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>Item 1</li><li>Item <b>2</b></li><li>Item <i>3</i></li></ol></div>"
        )