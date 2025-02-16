class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children if children is not None else []
        self.props = props if props is not None else {}

    def to_html(self):
        raise NotImplementedError("to_html method not implemented")

    def props_to_html(self):
        if self.props == None:
            return ""
        props_html = ""
        for prop in self.props:
            props_html += f' {prop}="{self.props[prop]}"'
        return props_html
    
    def __repr__(self):
        return f'HTMLNode(\ntag: {self.tag}\nvalue: {self.value}\nchildren: {self.children}, \nprops: {self.props})'


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value == None:
            raise ValueError("Invalid HTML as missing value")
        if self.tag == None:
            return f'{self.value}'  
        return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'
    
    def __repr__(self):
        return f'LeafNode(\ntag: {self.tag}\nvalue: {self.value}\nchildren: {self.children}, \nprops: {self.props})'


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("Invalid ParentNode as missing tag")
        if self.children is None:
            raise ValueError("Invalid ParentNode as missing children") 
        children_html = ""
        for child in self.children:
            children_html += child.to_html()
        return f'<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>' 
    
    def __repr__(self):
        return f'ParentNode(\ntag: {self.tag}\nchildren: {self.children}\nprops: {self.props}\n)'