class State:
    """
    A class that represents a possible or actual state of a variable. Defined as a variable with a value from the domain.
    In the case of this assignment, that is a square with a set color.
    """

    def __init__(self, color, pos):
        # Sets the color
        self.color = color
        # position of this state
        self.pos = pos

    def equals(self, state):
        """
        Checks if this state is equal to another state
        :param state: Should be a State that is being compared to
        :return: Boolean variable
        """
        if(state.color == self.color)and(state.pos == self.pos):
            return True
        return False
