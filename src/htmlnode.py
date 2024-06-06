class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props


    def to_html(self):
        raise NotImplementedError


    def props_to_html(self):
        html=""
        if self.props:
            for prop, value in self.props.items():
                html += f' {prop}="{value}"'
        return html


    def __repr__(self):
        return (
            f"tag: {self.tag}\n"
            f"value: {self.value}\n"
            f"children: {self.children}\n"
            f"props: {self.props}\n"
        )


class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props=None):
        super().__init__(tag=tag, value=value, props=props)


    def to_html(self):
        if not self.value:
            raise ValueError("LeafNode must have a value")
        if not self.tag:
            return self.value
        props_html = self.props_to_html()
        return f"<{self.tag}{props_html}>{self.value}</{self.tag}>"


class ParentNode(HTMLNode):
    def __init__(self, tag=None, children=None, props=None):
        super().__init__(tag=tag, children=children, props=props)


    def to_html(self):
        if not self.tag:
            raise ValueError("ParentNode must have a tag")
        if not self.children:
            return ValueError("ParentNode must have at least one child")
        props_html = self.props_to_html()
        children_html = ""
        for child in self.children:
            if isinstance(child, pare
            children_html += child.to_html()
        return f"<{self.tag}{props_html}>{children_html}</{self.tag}>"

