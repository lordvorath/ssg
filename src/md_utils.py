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
    matches = re.findall(r"[^!]\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
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
