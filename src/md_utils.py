from textnode import *
from htmlnode import *
import re

def split_nodes_delimiter(old_nodes:list[TextNode], delimiter, text_type:TextType):
    out = []
    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            out.append(node)
            continue
        lines = node.text.split(delimiter)
        if len(lines) % 2 == 0:
            raise ValueError("Invalid text: Uneven number of delimiters")
        for i in range(len(lines)):
            if lines[i] == "":
                continue
            new_type = TextType.TEXT if i % 2 == 0 else text_type
            out.append(TextNode(lines[i], new_type))
    return out       

def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT: return LeafNode(None, text_node.text)
        case TextType.BOLD: return LeafNode("b", text_node.text)
        case TextType.ITALIC: return LeafNode("i", text_node.text)
        case TextType.CODE: return LeafNode("code", text_node.text)
        case TextType.LINK: return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE: return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        case _: raise ValueError("Invalid TextNode text_type")

def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def split_nodes_image(old_nodes:list[TextNode]):
    out = []
    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            out.append(node)
            continue
        matches = extract_markdown_images(node.text)
        if not matches:
            out.append(node)
            continue
        text = node.text
        for match in matches:
            lines = text.split(f"![{match[0]}]({match[1]})", 1)
            out.append(TextNode(lines[0], TextType.TEXT))
            out.append(TextNode(match[0], TextType.IMAGE, match[1]))
            text = lines[1]
        if text:
            out.append(TextNode(text, TextType.TEXT))
    return out

def split_nodes_link(old_nodes:list[TextNode]):
    out = []
    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            out.append(node)
            continue
        matches = extract_markdown_links(node.text)
        if not matches:
            out.append(node)
            continue
        text = node.text
        for match in matches:
            lines = text.split(f"[{match[0]}]({match[1]})", 1)
            out.append(TextNode(lines[0], TextType.TEXT))
            out.append(TextNode(match[0], TextType.LINK, match[1]))
            text = lines[1]
        if text:
            out.append(TextNode(text, TextType.TEXT))
    return out

def text_to_textnodes(text):
    nodes = TextNode(text, TextType.TEXT)
    nodes = split_nodes_delimiter([nodes], "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    out = []
    for block in blocks:
        if not block:
            continue
        out.append(block.strip())
    return out

def block_to_block_type(block):
    if re.findall(r"^#{1,6}\s", block):
        return BlockType.HEADING
    if re.findall(r"^```[\s\S]*```$", block):
        return BlockType.CODE
    if re.findall(r"^>", block):
        for line in block.split("\n"):
            if not re.findall(r"^>", line):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    if len(re.findall(r"^-\s", block)):
        for line in block.split("\n"):
            if not re.findall(r"^-\s", line):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST
    if len(re.findall(r"^1\.\s", block)):
        i = 1
        for line in block.split("\n"):
            if not re.findall(f"{i}. ", block):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for node in text_nodes:
        children.append(text_node_to_html_node(node))
    return children

def markdown_to_html_node(markdown):
    html_root = ParentNode("div", [])
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        bt = block_to_block_type(block)
        match bt:
            case BlockType.PARAGRAPH:
                children = text_to_children(block)
                child = ParentNode("p", children)
            case BlockType.CODE:
                text = block.strip("```").lstrip()
                node = TextNode(text,TextType.CODE)
                children = text_node_to_html_node(node)
                child = ParentNode("pre", [children])
            case BlockType.QUOTE:
                lines = block.replace(">", "").split("\n")
                lines = map(lambda x: x.lstrip(), lines)
                text = "\n".join(lines)
                children = text_to_children(text)
                child = ParentNode("blockquote", children)
            case BlockType.HEADING:
                n = 0
                text = block
                while text.startswith("#"):
                    text = text.removeprefix("#")
                    n += 1
                text = text.lstrip()
                children = text_to_children(text)
                child = ParentNode(f"h{n}", children)
            case BlockType.UNORDERED_LIST:
                lines = block.split("\n")
                children = []
                for line in lines:
                    line = line.removeprefix("- ")
                    inner_children = text_to_children(line)
                    children.append(ParentNode("li", inner_children))
                child = ParentNode("ul", children)
            case BlockType.ORDERED_LIST:
                lines = block.split("\n")
                children = []
                for line in lines:
                    line = line[line.find(".") + 2 : ]
                    inner_children = text_to_children(line)
                    children.append(ParentNode("li", inner_children))
                child = ParentNode("ol", children)
            case _:
                raise Exception("Unrecognized BlockType")
        html_root.children.append(child)
    return html_root
        