import Tree as T
import State as S
import Node as N


class SolveMaze:

    def __init__(self, maze):
        if len(maze) > 0:
            self.smart = False
            self.finished = False
            self.initMaze = maze
            # Make list of unique colors
            # use index of a 'COLOR' in domain to find it's numerical value
            self.domain = self.find_unique_colors()

            # make empty color lists for each unique color in domain
            self.color_lists = [[] for i in range(len(self.domain))]

            # initializes 2D boolean array for keeping track of whether a state has been colored already or not
            temp = len(maze[0])
            self.has_been_colored = [[False] * temp for i in range(temp)]

            # get list of each starting state
            self.start_states, self.end_states = self.select_start_states()
            # set the root node to the first start state w/ no parent
            init_node = N.Node(self.start_states[0], None)

            # initializes the Tree
            self.tree = T.Tree(init_node)
            # initialize trackers
            self.add_to_trackers(self.tree.current_node)

            # lists the domain
            print("\nDomain: " + str(self.domain))
            print("Maze Sovler Initialized")
            while not self.finished:
                self.evaluate()
                print("Oh no!")
            print("We done!")
        else:
            # no maze can't do anything
            pass

    def select_start_states(self):
        """
        Makes a list of start states, one for each color in the order of the domain
        :return: list of start states
        """
        start_node_list = []
        end_node_list = []
        coords = []
        for color in self.domain:
            # get list of port indexes, organized by domain order
            for row in self.initMaze:
                # get coordinates of the all the ports of this color in this row
                # coords = [self.initMaze.index(row), row.index(color)]
                col_index = [i for i, x in enumerate(row) if x == color]
                row_index = self.initMaze.index(row)

                # add coords only if color is in the row
                if len(col_index) > 1:
                    # same row
                    coords.append([row_index, col_index[0]])
                    coords.append([row_index, col_index[1]])
                elif len(col_index) == 1:
                    # different rows, will run twice
                    coords.append([row_index, col_index[0]])

            # make states for port
            start_node_list.append(S.State(color, coords[0]))
            end_node_list.append(S.State(color, coords[1]))

        # return list of start states
        return start_node_list, end_node_list

    def next_start_state(self):
        """
        Gets the next starting state
        :return: starting state for the next color, or None if there are no more
        """
        return self.__gen_next_state(self.start_states)

    def next_end_state(self):
        """
        Gets the next ending state
        :return: ending state for the next color, or None if there are no more
        """
        return self.__gen_next_state(self.end_states)

    def __gen_next_state(self, main_list):
        """
        Helper function for next state getting
        :param main_list: list to get from
        :return: next state, or None if there were none
        """
        index = self.domain.index(self.tree.current_node.state.color) + 1
        if index < len(main_list):
            return main_list[index]
        else:
            return None

    def find_unique_colors(self):
        list_c = []
        for x in self.initMaze:
            for y in x:
                if(not list_c.__contains__(y))and (y != '_'):
                    list_c.append(y)
        return list_c

    def check_zigzag(self):
        """
        Checks if the current state has no zig-zags
        :return: True if this constraint passes, False otherwise
        """
        # get index of the current color
        i = self.domain.index(self.tree.current_node.state.color)

        # if length of the current color list is less then 4, there can't be a zig zag
        if len(self.color_lists[i]) > 4:
            # find pos of adjacent states
            compare = [[1, 0], [0, -1], [-1, 0], [0, 1]]
            x, y = self.tree.current_node.state.pos
            adj_nodes = [[x + dx, y + dy] for dx, dy in compare]

            # remove pos of the prev state
            prev = self.color_lists[i][-2]
            for pos in adj_nodes:
                if pos == prev:
                    # remove pos from adj_nodes
                    adj_nodes.remove(pos)
                    break

            for pos in adj_nodes:
                for test_pos in self.color_lists[i][:-3]:
                    if pos == test_pos:
                        # found one, so we have a zig zag
                        return False

            # none were found, so there were no zig-zags
            return True
        else:
            return True

    def check_end(self):
        for row in self.has_been_colored:
            for col in row:
                if not col:
                    return False
        return True

    # checks for the adjacent nodes that aren't the previously visited node
    def check_adj(self):
        """
        Adds valid child nodes to the current nodes
        Valid being defined as not the previous node, and not having been visited already.
        :return:
        """
        compare = [[1, 0], [0, -1], [-1, 0], [0, 1]]

        if self.tree.current_node.state.equals(self.next_end_state()):

            if self.check_end():
                self.finished = True
            else:
                # Add the next color's start node here
                next_node = self.make_node2(self.next_end_state())
                self.tree.current_node.append_child(next_node)
        else:

            # Gets the Value of the current node's state color for selecting the color_list
            current_color = self.tree.current_node.state.color
            color_index = self.domain.index(current_color)

            # stores the cords of the current node
            current_node_cords = self.color_lists[color_index][-1]

            if not self.tree.current_node.state.equals(self.tree.root.state):
                # stores the cords of the previous node
                prev_node_cords = self.color_lists[color_index][-2]

                # Computes the difference of the two positions
                x = current_node_cords[0] - prev_node_cords[0]
                y = current_node_cords[1] - prev_node_cords[1]
                pos_diff = [x, y]

                compare.remove(pos_diff)

            # use visited bool array to see if the node we're trying to create is already made
            for pos in compare:
                v_x = current_node_cords[0]+pos[0]
                v_y = current_node_cords[1]+pos[1]
                # self.has_been_colored will return false if the pos hasn't been visited
                try:
                    if not self.has_been_colored[v_x][v_y]:
                        # Add node
                        temp = [v_x, v_y]
                        self.tree.current_node.append_child(self.make_node(current_color, temp))
                except IndexError:
                    pass

    def make_node(self, color, pos):
        node = N.Node(S.State(color, pos), self.tree.current_node)
        return node

    def make_node2(self, state):
        node = N.Node(state, self.tree.current_node)
        return node

    # TODO: Make constraints evaluations
    def constraint_check(self):
        """
        evaluates constraints and returns the result
        evaluates on Tree's current_Node
        :return: True if all test passed, False otherwise
        """
        # No zig zags
        if not self.check_zigzag():
            # zigzag constraint failed
            return False

        if self.smart:
            # TODO add extra smart checks here
            pass

        # all tests passed
        return True

    def evaluate(self):
        """
        Evaluates the position and ether moves forward or backtracks in the tree
        :return: Nothing
        """
        # Check constraints for Tree's current_Node
        result = self.constraint_check()
        # According to constraint results, either backtrack, or forward Tree's current_Node
        if result:
            # Expand current node by adding on children nodes
            self.check_adj()
            # Move Tree forward
            self.tree.forward_node()
            self.add_to_trackers(self.tree.current_node)
        else:
            self.remove_from_trackers(self.tree.current_node)
            self.tree.backtrack_node()

    # Trackers are the 2D boolean array & color list
    def add_to_trackers(self, node):
        # pos should be a list of x and y ints, i.e. [x, y]
        x, y = node.state.pos
        # set the boolean array at this node's location to True
        self.has_been_colored[x][y] = True

        color = node.state.color
        color_val = self.domain.index(color)
        # add this node's location set to the end of its color's list
        self.color_lists[color_val].append(node.state.pos)

    # Should always remove the last node from color list, and sets the has_been_colored pos to False
    def remove_from_trackers(self, node):
        x, y = node.state.pos
        # set the boolean array at this node's location to False
        self.has_been_colored[x][y] = False

        # removes last item from the color list
        color = node.state.color
        color_val = self.domain.index(color)
        # remove last set from this color's list
        self.color_lists[color_val].pop()
