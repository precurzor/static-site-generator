import re
from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_block_type(block):
    lines = block.split('\n')
    if block.startswith('#'):
        if re.match(r'^#{1,6} ', block): 
            return BlockType.HEADING
    if block.startswith('```') and lines[-1] == '```':
        return BlockType.CODE
    if all(line.startswith('>') for line in lines):
        return BlockType.QUOTE
    if all(line.startswith('- ') for line in lines):
        return BlockType.UNORDERED_LIST
    if lines:  # Making sure there's at least one line
        is_ordered_list = True
        pattern = re.compile(r'^(\d+)\.\s')
        for index, line in enumerate(lines, start=1):
            match = pattern.match(line)
            if not match or int(match.group(1)) != index:
                is_ordered_list = False
                break      
        if is_ordered_list:
            return BlockType.ORDERED_LIST
    
    return BlockType.PARAGRAPH


def markdown_to_blocks(markdown):
    blocks = re.split(r'\n{2,}', markdown)
    block_list = []
    for block in blocks:
        # Split the block into lines, strip each line, and rejoin
        lines = [line.strip() for line in block.split('\n')]
        cleaned_block = '\n'.join(lines).strip()
        if cleaned_block != "":
            block_list.append(cleaned_block)
    return block_list


def markdown_to_html_node(markdown):
    