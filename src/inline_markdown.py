import re
from textnode import *

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_list = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_list.append(old_node)
            continue
        if old_node.text.count(delimiter) % 2 != 0:
            raise Exception("Delimiter not closed")
        split_nodes = []
        sections = old_node.text.split(delimiter)
        for i in range(len(sections)):
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_list.extend(split_nodes)
    return new_list