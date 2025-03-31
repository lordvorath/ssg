from textnode import *
from htmlnode import *

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
    

def main():
    node = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev") 
    print(node)

main()