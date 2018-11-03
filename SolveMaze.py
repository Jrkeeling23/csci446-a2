import Tree as T
import State as S
import Node as N
import time
import GifMaker


class SolveMaze:

    def __init__(self, maze):
        if len(maze) > 0:
            self.vars_assigned = 0
            self.smart = True
            self.finished = False
            self.initMaze = maze
            self.make_gif = True
            self.compare = [[0, -1], [-1, 0], [0, 1], [1, 0]]

            # Make list of unique colors
            # use index of a 'COLOR' in domain to find it's numerical value
            self.domain = self.find_unique_colors()

            # make empty color lists for each unique color in domain
            self.color_lists = [[] for i in range(len(self.domain))]

            # initializes 2D boolean array for keeping track of whether a state has been colored already or not
            temp = len(maze[0])
            self.has_been_colored = [[False] * temp for i in range(temp)]
            # set up answer array
            self.answer = [[" "] * temp for i in range(temp)]

            # get list of each starting state
            self.start_states, self.end_states = self.select_start_states()

            # update has been colored for all port states
            for state in self.start_states + self.end_states:
                x, y = state.pos
                self.has_been_colored[x][y] = True

            # set the root node to the first start state w/ no parent
            init_node = N.Node(self.start_states[0], None)

            # initializes the Tree
            self.tree = T.Tree(init_node)
            # initialize trackers
            self.add_to_trackers(self.tree.current_node)

            # clear vars we are done with, so they are not in the debugger for the following while loop
            x = None
            del x
            y = None
            del y
            state = None
            del state
            init_node = None
            del init_node
            temp = None
            del temp

            # build the global color rgb reference
            self.index_ref = ['B', 'A', 'W', 'R', 'P', 'D', 'O', 'G', 'Y', 'K', 'Q']
            self.rgb_ref = [[0, 0, 255], [125, 255, 210], [255, 255, 255], [255, 0, 0], [140, 0, 255],
                            [190, 150, 100], [255, 100, 0], [0, 255, 0], [255, 255, 0], [230, 160, 200], [140, 60, 90]]

            # lists the domain
            print("\nDomain: " + str(self.domain))
            print("Maze Solver Initialized")

            run_time = 0
            while not self.finished:
                start_time = time.process_time()
                self.evaluate()
                if self.make_gif:
                    self.export_png("maze" + str(len(self.initMaze)) + "_" + str(self.vars_assigned))
                end_time = time.process_time()
                run_time += end_time - start_time
                if not self.make_gif and run_time >= 120:
                    print("Process aborted after 2 minutes")
                    break

            # export solution png
            self.export_png("sol" + str(len(self.initMaze)))
            # build the gif
            if self.make_gif:
                size = len(self.initMaze)
                GifMaker.GifMaker.make_gif("maze_animation_s_" + str(size) + "X" + str(size), size)

            # build and print the answer
            for color in self.color_lists:
                for pos in color:
                    self.answer[pos[0]][pos[1]] = self.domain[self.color_lists.index(color)]
            for row in self.answer:
                for col in row:
                    print(col, end=" ")
                print()
            print("Number of attempted variable assignments:", self.vars_assigned)
            print("Run time: %.5f seconds\n" % run_time)
        else:
            # no maze, can't do anything
            pass

    def export_png(self, name):
        """
        Builds and exports a png from the current state of the maze
        :param name: of the png image
        :return: Nothing
        """
        # make a copy of the initial maze
        png_maze = [row.copy() for row in self.initMaze]
        # build the current array
        for color in self.color_lists:
            for pos in color:
                png_maze[pos[0]][pos[1]] = self.domain[self.color_lists.index(color)]

        # build and export png
        GifMaker.GifMaker.make_png_from_maze(png_maze, self.index_ref, self.rgb_ref, name)

    def select_start_states(self):
        """
        Makes a list of start states, one for each color in the order of the domain
        :return: list of start states
        """
        start_node_list = []
        end_node_list = []

        for color in self.domain:
            coords = []
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

        if self.smart:
            smart_start_list, smart_end_list = self.smart_start(start_node_list, end_node_list)
            return smart_start_list, smart_end_list
        else:
            # return list of start states
            return start_node_list, end_node_list

    def smart_start(self, start_list, end_list):
        """
        Makes two lists for smarter start domain
        :param start_list:
        :param end_list:
        :return: start and end list sorted by available paths
        """
        start_path_number = []
        end_path_number = []
        smart_start_list = []
        new_start_list = []
        new_end_list = []
        # check surrounding
        for i in range(len(start_list)):
            # obtain possible moves for each color
            start_path_number.append(self.find_available_paths(start_list[i], size=len(start_list)))
            end_path_number.append(self.find_available_paths(end_list[i], size=len(end_list)))
        # add path values to find most constrained value
        for i in range(len(start_list)):
            # variable that holds summed available paths of start and end nodes, as well as color index
            lowest = [[start_path_number[i] + end_path_number[i], i]]
            smart_start_list.append(lowest)
        # creates a list from least to greatest of available paths
        smart_start_list.sort(key=lambda x: x[0])
        for i in range(len(start_list)):
            # iterates through smart_start to obtain domain
            index_color = smart_start_list[i][1]
            # orders start_list according to least available paths
            new_start_list.append(start_list[index_color])
            # orders start_list according to least available paths
            new_end_list.append(end_list[index_color])
        return new_start_list, new_end_list

    def find_available_paths(self, node, size):
        """
        Finds available paths for a node
        :param node:
        :param size:
        :return: returns available paths for a node
        """
        coords = node.pos
        # first value in coordinate
        coord1 = node.pos[0]
        # second value in coordinate
        coord2 = node.pos[1]
        # counts number of available paths
        path = 0
        # temp value to check
        temp = None

        # at top edge
        if coords[0] != 0:
            # check up
            temp = coord1 - 1
            # checks if it is not assigned a color
            if not self.has_been_colored[temp][coord2]:
                path += 1
        # at left edge
        elif coords[1] != 0:
            # check left
            temp = coord2 - 1
            if not self.has_been_colored[0][temp]:
                path += 1
        # at bottom edge
        elif coords[0] != size / 2 - 1:
            # check down
            temp = coord1 + 1
            if not self.has_been_colored[temp][0]:
                path += 1
        # at right edge
        elif coords[1] != size / 2 - 1:
            # check right
            temp = coord2 + 1
            if not self.has_been_colored[0][temp]:
                path += 1
        # return total number of available paths
        return path

    def next_start_state(self):
        """
        Gets the next starting state
        :return: starting state for the next color, or None if there are no more
        """
        return self.__gen_next_state(self.start_states, 1)

    def current_end_state(self):
        """
        Gets the next ending state
        :return: ending state for the next color, or None if there are no more
        """
        return self.__gen_next_state(self.end_states, 0)

    def __gen_next_state(self, main_list, delta):
        """
        Helper function for next state getting
        :param main_list: list to get from
        :return: next state, or None if there were none
        """
        index = self.domain.index(self.tree.current_node.state.color) + delta
        if index < len(main_list):
            return main_list[index]
        else:
            return None

    def find_unique_colors(self):
        list_c = []
        for x in self.initMaze:
            for y in x:
                if (not list_c.__contains__(y)) and (y != '_'):
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
        if len(self.color_lists[i]) >= 4:
            # find pos of adjacent states
            x, y = self.tree.current_node.state.pos
            adj_nodes = [[x + dx, y + dy] for dx, dy in self.compare]

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
        side_check = [[0, -1], [-1, 0], [0, 1], [1, 0]]

        if self.tree.current_node.state.equals(self.current_end_state()):

            if self.check_end():
                self.finished = True
                # still need to append the last color though

            else:
                # Add the next color's start node here, this also appends as a child of the current node
                self.make_node2(self.next_start_state())
        else:

            # Gets the Value of the current node's state color for selecting the color_list
            current_color = self.tree.current_node.state.color
            color_index = self.domain.index(current_color)

            # stores the cords of the current node
            current_node_cords = self.color_lists[color_index][-1]

            # for a start port don't remove previous node's pos from the check,
            # since it is ether None or a different color
            is_start_port = False
            for state in self.start_states:
                if self.tree.current_node.state.equals(state):
                    is_start_port = True
                    break

            if not is_start_port:
                # stores the cords of the previous node
                prev_node_cords = self.color_lists[color_index][-2]

                # Computes the difference of the two positions
                x = prev_node_cords[0] - current_node_cords[0]
                y = prev_node_cords[1] - current_node_cords[1]
                pos_diff = [x, y]

                side_check.remove(pos_diff)

            endport_is_adj = False
            # use visited bool array to see if the node we're trying to create is already made
            for pos in side_check:
                v_x = current_node_cords[0] + pos[0]
                v_y = current_node_cords[1] + pos[1]
                # self.has_been_colored will return false if the pos hasn't been visited
                try:
                    if v_x < 0 or v_y < 0:
                        raise IndexError
                    # allow the end state for this color to be added anyway
                    if not self.has_been_colored[v_x][v_y] or self.current_end_state().pos == [v_x, v_y]:
                        # end ports are the only valid adjacent node
                        if self.current_end_state().pos == [v_x, v_y]:
                            endport_is_adj = True
                            break
                        # Add node
                        temp = [v_x, v_y]
                        # this also appends as a child of the current node
                        self.make_node(current_color, temp)
                except IndexError:
                    pass
            # clear all children and re-add the end port
            if endport_is_adj:
                self.tree.current_node.children = []
                self.make_node2(self.current_end_state())

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
        if self.smart:
            # TODO add extra smart checks here

            pass

        # No zig zags
        if not self.check_zigzag():
            # zigzag constraint failed
            return False

        # all tests passed
        return True

    def evaluate(self):
        """
        Evaluates the position and either moves forward or backtracks in the tree
        :return: Nothing
        """

        def backtrack():
            # Move Tree backward
            self.remove_from_trackers(self.tree.current_node)
            # remove the current node from its parent's valid options
            self.tree.current_node.parent_Node.remove_current_child()
            self.tree.backtrack_node()

        def forward():
            # Move Tree forward
            self.tree.forward_node()
            self.add_to_trackers(self.tree.current_node)

        if not self.tree.current_node.state.expanded:
            # Check constraints for Tree's current_Node
            result = self.constraint_check()

            # According to constraint results, either backtrack, or forward Tree's current_Node
            if result:
                # set this node to expanded before moving to the next
                self.tree.current_node.state.expanded = True
                # Expand current node by adding on children nodes
                self.check_adj()
                if len(self.tree.current_node.children) > 0:
                    forward()
                else:
                    # no options after check_adj, so we need to backtrack unless we are finished
                    if not self.finished:
                        backtrack()
            else:
                backtrack()
        else:
            if len(self.tree.current_node.children) > 0:
                forward()
            else:
                backtrack()

    # Trackers are the 2D boolean array & color list
    def add_to_trackers(self, node):
        # pos should be a list of x and y ints, i.e. [x, y]
        x, y = node.state.pos
        # set the boolean array at this node's location to True
        self.has_been_colored[x][y] = True
        # increment number of attempted variable assignments count
        self.vars_assigned += 1

        color = node.state.color
        color_val = self.domain.index(color)
        # add this node's location set to the end of its color's list
        self.color_lists[color_val].append(node.state.pos)

    # Should always remove the last node from color list, and sets the has_been_colored pos to False
    def remove_from_trackers(self, node):
        is_port = False
        for port in self.start_states + self.end_states:
            if node.state.equals(port):
                is_port = True
                break

        color = node.state.color
        # don't set a port's has_been_colored to False
        if not is_port:
            x, y = node.state.pos
            # set the boolean array at this node's location to False
            self.has_been_colored[x][y] = False
        else:
            # not important for non-port nodes since they are regenerated
            self.tree.current_node.state.expanded = False

        # removes last item from the color list
        color_val = self.domain.index(color)
        self.color_lists[color_val].pop()
