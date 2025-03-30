import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

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

class TestLeafNode(unittest.TestCase):

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
        node = LeafNode("a", None, {"not": "rendered"})
        self.assertRaises(ValueError, node.to_html)

class TestParentNode(unittest.TestCase):

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_parent_no_tag(self):
        node = ParentNode(None, [])
        self.assertRaises(ValueError, node.to_html)
    
    def test_parent_no_children(self):
        node = ParentNode("a", [])
        self.assertRaises(ValueError, node.to_html)
 
    def test_to_html_with_more_grandchildren(self):
            grandchild_node = LeafNode("b", "grandchild")
            other_grandchild = LeafNode(None, "some raw text")
            child_node = ParentNode("span", [grandchild_node, other_grandchild])
            parent_node = ParentNode("div", [child_node])
            parent_node2 = ParentNode("a", [parent_node], {"href": "https://www.google.com"})
            self.assertEqual(
                parent_node2.to_html(),
                "<a href=\"https://www.google.com\"><div><span><b>grandchild</b>some raw text</span></div></a>",
            )
 


if __name__ == "__main__":
    unittest.main()