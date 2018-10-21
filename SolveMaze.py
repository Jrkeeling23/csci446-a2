import Tree as T
import State as S
import Node as N

class SolveMaze:

    # TODO:
    # Lists of color positions (in sync with the STATE TREE)
    # Make 2D boolean array to check that a state has been colored already (Check by position)

    colorLists = []

    def __init__(self, maze):
        self.initMaze = maze
        # Make list of unique colors
        self.domain = self.findUniqueColors()
        # lists the domain
        print("\nDomain: " + str(self.domain))
        # use index of a 'COLOR' in domain to find it's numerical value

        # make empty color lists for each unique color in domain
        for l in self.domain:
            self.colorLists.append([])

        # initializes 2D boolean array for keeping track of whether a state has been colored already or not
        temp = len(maze[0])
        self.hasBeenColored = [[False for i in range(temp)] for j in range(temp)]
        # TODO: add logic for keeping track of these True/False values according to color List's coords
        # (Update when backtracking and moving forward)

        # TODO: Make method for choosing start
        init_Node = N.Node(S.State(color, coords, None))

        #initializes the Tree
        self.tree = T.Tree(init_Node)

        # TODO: Make method for making a node from color & pos

        print("Maze Sovler Initialized")

    def select_start_states(self):
        """
        Makes a list of start states, one for each color in the order of the domain
        :return: list of start states
        """
        init_node_list = []
        for color in self.domain:
            # get list of port indexes, organized by domain order
            for row in self.initMaze:
                try:
                    # get coordinates of the first port of this color
                    coords = [self.initMaze.index(row), row.index(color)]
                    break
                except ValueError:
                    # wasn't in the list
                    pass

            # make state for port
            init_node_list.append(S.State(color, coords))

        # return list of start states
        return init_node_list

    def validate(self):
        pass

    def findUniqueColors(self):
        listC = []
        for x in self.initMaze:
            for y in x:
                if(not listC.__contains__(y))and (y!='_'):
                    listC.append(y)
        return listC

    def checkZigZag(self):
        # TODO: Add logic for checking zigzag using the list of Color's positions
        pass

    # TODO: Add method for checking if a node is adjecent to others in the list not including the last 2 coords entered in the list
    def check_adj(self):

        compare = [[1,0],[0,-1]]

        # Use last x/y coords in the ColorList as the State being checked
        # the 2nd to last x/y coord set in the Color list would need to be subtracted from the State being checked,
        # and have the result x/y be removed from the list of x,y differences used to compare for
        # each other node, to see if that one would evaluate to 3 adjacent nodes
        pass

    def make_node(self, color, pos):
        node = N.Node(S.State(color, pos, self.tree.current_Node))
        return node

    # TODO: Make constraints evaluations
    def constraint_check(self):
        pass

    # TODO: Add 2D boolean array manipulation here, as well as color list adding
    def evaluate(self):
        # Check constraints for Tree's current_Node
        result = self.constraint_check()
        # According to constraint results, either backtrack, or forward Tree's current_Node
        if result:
            # Move Tree forward
            self.tree.forward_node()
            pass
        else:
            pass
        # Manipulate 2D boolean array accordingly, and add/remove from colorList
        pass
