import unittest
from htmlnode import *

class TestHTMLNode(unittest.TestCase):
    def test_tag(self):
        node = HTMLNode("a", "https://www.google.com", None, {"href":"https://www.google.com"})
        valid_tags = ["a", "b", "i", "q", "code", "href", "p", "h1"]
        self.assertIn(node.tag, valid_tags, "[!] Missing tag")
    
    def test_value(self):
        node = HTMLNode("a", None, None, {"href":"https://www.google.com"})
        self.assertEqual(node.value, None)
        self.assertEqual(node.children, [])
    
    def test_prop(self):
        node = HTMLNode("a", "https://www.google.com", None, None)
        self.assertEqual(node.props, {}, "[!] missing props")

    def test_props_to_html(self):
        node = HTMLNode("a", "https://www.google.com", None, {"href": "https://www.google.com", "target": "_blank",})
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com" target="_blank"')

# LeafNode Tests
    def test_leaf_value(self):
        node = LeafNode("p", "This is a paragraph of text.")
        self.assertEqual(node.to_html(), '<p>This is a paragraph of text.</p>')

    def test_leaf_value_missing(self):
        node = LeafNode("h1", None)
        self.assertRaises(ValueError)

    def test_leaf_notag(self):
        node = LeafNode(None, "This is plain text.", None)
        self.assertEqual(node.to_html(), "This is plain text.")

# ParentNode Tests
    def test_parent_no_children(self):
        node = ParentNode("p", "This is a paragraph of text.")
        self.assertRaises(ValueError)  

    def test_to_html_with_children(self):
        child_node = LeafNode("span","child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span",[grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span><b>grandchild</b></span></div>")

    def test_to_html_multi_children(self):
        node = ParentNode(
            "p",
             [
                 LeafNode("b","Bold text"),
                 LeafNode(None,"Normal text"),
                 LeafNode("code","Code text"),
                 LeafNode("i","italic text"),
            ],
        )
        self.assertEqual(node.to_html(), "<p><b>Bold text</b>Normal text<code>Code text</code><i>italic text</i></p>")
         
if __name__ == "__main__":
    unittest.main()