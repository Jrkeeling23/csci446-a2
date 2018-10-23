import Tree as T
import State as S
import Node as N


class SolveMaze:

    colorLists = []

    def __init__(self, maze):
        self.initMaze = maze
        # Make list of unique colors
        self.domain = self.find_unique_colors()
        # lists the domain
        print("\nDomain: " + str(self.domain))
        # use index of a 'COLOR' in domain to find it's numerical value

        # make empty color lists for each unique color in domain
        for l in self.domain:
            self.colorLists.append([])

        # initializes 2D boolean array for keeping track of whether a state has been colored already or not
        temp = len(maze[0])
        self.hasBeenColored = [[False]*temp for j in range(temp)]
        # TODO: add logic for keeping track of these True/False values according to color List's coords
        # (Update when backtracking and moving forward)

        # get list of each starting state
        # TODO once color #n is done we need to get color #n+1 from the following list
        self.start_states = self.select_start_states()
        # set the root node to the first start state w/ no parent
        init_node = N.Node(self.start_states[0], None)

        # initializes the Tree
        self.tree = T.Tree(init_node)

        print("Maze Sovler Initialized")

    def select_start_states(self):
        """
        Makes a list of start states, one for each color in the order of the domain
        :return: list of start states
        """
        init_node_list = []
        coords = None
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

    def find_unique_colors(self):
        list_c = []
        for x in self.initMaze:
            for y in x:
                if(not list_c.__contains__(y))and (y != '_'):
                    list_c.append(y)
        return list_c

    def check_zigzag(self):
        # TODO: Add logic for checking zigzag using the list of Color's positions
        pass

    # TODO: Add method for checking if a node is adjacent to others in the list not including the last 2 coords
    # entered in the list
    def check_adj(self):

        compare = [[1,0],[0,-1],[-1,0],[0,1]]

        # Use last x/y coords in the ColorList as the State being checked
        # the 2nd to last x/y coord set in the Color list would need to be subtracted from the State being checked,
        # and have the result x/y be removed from the list of x,y differences used to compare for
        # each other node, to see if that one would evaluate to 3 adjacent nodes
        pass

    def make_node(self, color, pos):
        node = N.Node(S.State(color, pos), self.tree.current_Node)
        return node

    # TODO: Make constraints evaluations
    def constraint_check(self):
        # TODO evaluate constraints, return end result
        # evaluates on Tree's current_Node
        return False

    def evaluate(self):
        # Check constraints for Tree's current_Node
        result = self.constraint_check()
        # According to constraint results, either backtrack, or forward Tree's current_Node
        if result:
            # Move Tree forward
            self.tree.forward_node()
            self.add_to_trackers(self.tree.current_Node)
        else:
            self.remove_from_trackers(self.tree.current_Node)
            self.tree.backtrack_node()

    # Trackers are the 2D boolean array & color list
    def add_to_trackers(self, node):
        # pos should be a list of x and y ints, i.e. [x, y]
        x, y = node.state.pos
        # set the boolean array at this node's location to True
        self.hasBeenColored[x][y] = True

        color = node.state.color
        color_val = self.domain.index(color)
        # add this node's location set to the end of its color's list
        self.colorLists[color_val].append(node.state.pos)

    # Should always remove the last node from color list, and sets the hasBeenColored pos to False
    def remove_from_trackers(self, node):
        x, y = node.state.pos
        # set the boolean array at this node's location to False
        self.hasBeenColored[x][y] = False

        # removes last item from the color list
        color = node.state.color
        color_val = self.domain.index(color)
        # remove last set from this color's list
        self.colorLists[color_val].pop()
