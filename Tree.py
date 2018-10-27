class Tree:
    """
    The state tree for the problem, 
    
    - provides functions to move forward / backward in the tree
    """

    # Takes in coords of first color port and sets it up as the first state
    def __init__(self, node):
        # Initializes the parent as None for the root Node
        self.root = node
        self.current_Node = self.root

        # Add +1 to depth when setting current_Node forward, and -1 when setting current_Node to a parent
        self.depth = 1

    # Should never be reached if current_Node has no children
    def forward_node(self):
        # TODO this only check the fist child node, so the first node must always be the next state
        self.current_Node = self.current_Node.children[0]
        self.depth += 1

    def backtrack_node(self):
        if self.current_Node != self.root:
            self.current_Node = self.current_Node.parent_Node
            self.depth -= 1
        else:
            print("Can't backtrack on root!")
