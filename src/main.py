from textnode import *
from htmlnode import *
from test_textnode import *
from test_htmlnode import *

def main():

    test_textnode = TextNode("This is a text node", "bold", "https://www.boot.dev")
    print(test_textnode)

    test_htmlnode = HTMLNode("a", "https://www.google.com", None, {"href": "https://www.google.com", "target": "_blank",})
    print(test_htmlnode)

    test_parentnode = ParentNode("a", "https://www.google.com")
    print(test_htmlnode)

if __name__ == "__main__":
    main()