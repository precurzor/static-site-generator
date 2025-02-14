from textnode import *

text_type_text = "text"
text_type_bold = "bold"
text_type_italic = "italic"
text_type_code = "code"
text_type_link = "link"
text_type_image = "image"

def main():

    test_textnode = TextNode("This is a text node", "bold", "https://www.boot.dev")
    print(test_textnode)


if __name__ == "__main__":
    main()