

class HTMLNode():
    def __init__(self, tag=None, value=None, children:list=None, props:dict=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        out = ""
        if self.props is None:
            return ""
        for key, val in self.props.items():
            out += f' {key}="{val}"'
        return out

    def __repr__(self):
        return f"tag=\t{self.tag}\nvalue=\t{self.value}\nchildren=\t{self.children}\nprops=\t{self.props}"

    def __eq__(self, other):
        return (self.tag == other.tag and
        self.value == other.value and
        self.children == other.children and
        self.props == other.props)
    

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props = None):
        super().__init__(tag, value, [], props)

    def to_html(self):
        if self.value is None:
            raise ValueError("LeafNode must have a value")
        if self.tag is None:
            return self.value
        return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props = None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("ParentNode must have a tag")
        if self.children is None or len(self.children) == 0:
            raise ValueError("ParentNode must have at least one child")
        out = ""
        for child in self.children:
            out += child.to_html()
        return f"<{self.tag}{self.props_to_html()}>{out}</{self.tag}>"