class State:

    def __init__(self, color, pos):
        # Sets the color
        self.color = color
        # Keeps track of the adjacent States with the same color.
        # If it becomes greater than 2, it counts as a Zig-Zag
        self.pos = pos