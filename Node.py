class Node:
    """
    Node is a wrapper class for State that handles tree connectivity
    """
    def __init__(self, state, parent):
        self.parent_Node = parent
        self.state = state
        self.children = []
        # When creating a node, add it as a child to its parent
        if parent is not None:
            parent.append_child(self)

    def append_child(self, node):
        self.children.append(node)

    def remove_child(self, node):
        self.remove_child(node)