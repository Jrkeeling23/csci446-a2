"""
Authors: George Engel, Cory Johns, Justin Keeling
"""
class Tree:
    """
    The state tree for the problem, 
    
    - provides functions to move forward / backward in the tree
    """

    # Takes in coords of first color port and sets it up as the first state
    def __init__(self, node):
        # Initializes the parent as None for the root Node
        self.root = node
        self.current_node = self.root

    # Should never be reached if current_Node has no children
    def forward_node(self):
        self.current_node = self.current_node.children[0]

    def backtrack_node(self):
        if self.current_node != self.root:
            self.current_node = self.current_node.parent_Node
        else:
            print("Can't backtrack on root!")
