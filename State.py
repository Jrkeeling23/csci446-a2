class State:
    """
    A class that represents a possible or actual state of a variable. Defined as a variable with a value from the domain.
    In the case of this assignment, that is a square with a set color.
    
    State contains no functions since it is never changed after initialization and only contains set values
    """

    def __init__(self, color, pos):
        # Sets the color
        self.color = color
        # position of this state
        self.pos = pos
