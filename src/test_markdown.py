import unittest
from translate_markdown import *
from block_markdown import *


class TestMdNode(unittest.TestCase):
    def extract_md_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        self.assertEqual(text, [
            ("rick roll", "https://i.imgur.com/aKaOqIh.gif"), 
            ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")
            ])

class TestMdNode(unittest.TestCase):
    def extract_md_images_no_alt(self):
        text = "This is text with a (https://i.imgur.com/aKaOqIh.gif) and ![](https://i.imgur.com/fJRm4Vk.jpeg)"
        self.assertEqual(text, [
            (None, "https://i.imgur.com/aKaOqIh.gif"), 
            ("", "https://i.imgur.com/fJRm4Vk.jpeg")
            ])

class TestMdNode(unittest.TestCase):
    def extract_md_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        self.assertEqual(text, [
            ("to boot dev", "https://www.boot.dev"), 
            ("to youtube", "https://www.youtube.com/@bootdotdev")
            ])

class TestMdNode(unittest.TestCase):
    def extract_md_links_no_anchor(self):
        text = "This is text with a link [](https://www.boot.dev) and (https://www.youtube.com/@bootdotdev)"
        self.assertEqual(text, [
            ("", "https://www.boot.dev"), 
            (None, "https://www.youtube.com/@bootdotdev")
            ])

class TestInlineMarkdown(unittest.TestCase):        
    def test_split_image(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_image_single(self):
        node = TextNode(
            "![image](https://www.example.COM/IMAGE.PNG)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://www.example.COM/IMAGE.PNG"),
            ],
            new_nodes,
        )

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
            "This is text with a [link](https://boot.dev) and [another link](https://blog.boot.dev) with text that follows",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("another link", TextType.LINK, "https://blog.boot.dev"),
                TextNode(" with text that follows", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_text_to_textnodes(self):
        nodes = text_to_textnodes(
            "This is **text** with an *italic* word and a `code block` and an ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://boot.dev)"
        )
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            nodes,
        )

# Test block_markdown
class TestMarkdownToHTML(unittest.TestCase):
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

    def test_markdown_to_blocks_newlines(self):
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

# Test block identification

class TestBlockIdentification(unittest.TestCase):
    def test_block_to_block_type_paragraph(self):
        block = "This is **bolded** paragraph"
        id = block_to_block_type(block)
        self.assertEqual(id, BlockType.PARAGRAPH)

    def test_block_to_block_type_unordered_list(self):
        block = "- This is a list\n- with items"
        id = block_to_block_type(block)
        self.assertEqual(id, BlockType.UNORDERED_LIST)

    def test_block_to_block_heading(self):
        block = "### Heading"
        id = block_to_block_type(block)
        self.assertEqual(id, BlockType.HEADING)

    def test_block_to_block_ordered_list(self):
        block = "1. First item\n2. Second item\n3. Third item"
        id = block_to_block_type(block)
        self.assertEqual(id, BlockType.ORDERED_LIST)

    def test_block_to_block_code(self):
        block = "```\ncode\n```"
        id = block_to_block_type(block)
        self.assertEqual(id, BlockType.CODE)

    def test_block_to_block_quote(self):
        block = "> First line of quote\n> Second line of quote\n> leading to third line of quote"
        id = block_to_block_type(block)
        self.assertEqual(id, BlockType.QUOTE)