"""
Authors: George Engel, Cory Johns, Justin Keeling
"""
import Tree as T
import State as S
import Node as N
import time
import GifMaker
import PriorityQueue


class SolveMaze:

    def __init__(self, maze, smart=True, make_gif=False, manhattan=True):
        self.vars_assigned = 0
        self.smart = smart

        # manhattan variables, through grid testing the values given here are the best rounded for mazes 5x5 - 9x9
        self.manhattan = manhattan
        self.proximity_range = 6
        self.proximity_bonus = 85  # actual bonus is proximity_bonus - proximity_scale * distance
        self.proximity_scale = 12
        self.edge_bonus = 20
        self.wall_bonus = 4
        self.png_name = "maze_bk" + str(len(maze))
        self.animation_name = "maze_animation_holechecking"

        self.finished = False
        self.initMaze = maze
        self.make_gif = make_gif
        self.compare = [[0, -1], [-1, 0], [0, 1], [1, 0]]
        self.color_list_index = 0
        # build the global color rgb reference
        self.index_ref = ['B', 'A', 'W', 'R', 'P', 'D', 'O', 'G', 'Y', 'K', 'Q']
        self.rgb_ref = [[0, 0, 255], [125, 255, 210], [255, 255, 255], [255, 0, 0], [140, 0, 255],
                        [190, 150, 100], [255, 100, 0], [0, 255, 0], [255, 255, 0], [230, 160, 200], [140, 60, 90]]

        # Make list of unique colors
        # use index of a 'COLOR' in domain to find it's numerical value
        self.domain = self.find_unique_colors()

        # make empty color lists for each unique color in domain
        self.color_lists = [[] for i in range(len(self.domain))]

        # initializes 2D boolean array for keeping track of whether a state has been colored already or not
        temp = len(maze[0])
        self.has_been_colored = [[False] * temp for i in range(temp)]

        # set up empty square matrix for detecting holes / trapped colors
        self.hole_matrix = [[-1] * temp for i in range(temp)]
        # index for holes
        self.hole_index = 0

        # set up answer array
        self.answer = [["_"] * temp for i in range(temp)]

        # initialed in start_solving
        self.start_states, self.end_states = None, None
        self.tree = None

    def start_solving(self, suppress_output=False):
        self.vars_assigned = 0
        if not suppress_output:
            smart_str = "smart" if self.smart else "dumb"
            manhattan_str = ", manhattan" if self.manhattan and self.smart else ""
            smart_str = "Using:" + smart_str + manhattan_str

        if self.smart:
            self.detect_adjacent_edges()

        # get list of each starting state
        self.start_states, self.end_states = self.select_start_states()

        # update has been colored for all port states
        for state in self.start_states + self.end_states:
            x, y = state.pos
            self.has_been_colored[x][y] = True

        # set the root node to the first start state w/ no parent
        init_node = N.Node(self.start_states[self.color_list_index], None)

        # initializes the Tree
        self.tree = T.Tree(init_node)
        # initialize trackers
        self.add_to_trackers(self.tree.current_node)

        if not suppress_output:
            # lists the domain
            print("\nDomain: " + str(self.domain))
            print("Maze Solver Initialized, %s %sx%s:" % (smart_str, str(len(self.initMaze)), str(len(self.initMaze))))

        run_time = 0
        # export initial state
        if self.make_gif:
            self.export_png(self.png_name + "_" + str(self.vars_assigned))
        while not self.finished:
            if suppress_output:
                self.evaluate()
            else:
                start_time = time.process_time()
                self.evaluate()
                if self.make_gif:
                    self.export_png(self.png_name + "_" + str(self.vars_assigned))
                end_time = time.process_time()
                run_time += end_time - start_time
                if not self.make_gif and run_time >= 120:
                    print("Process aborted after 2 minutes")
                    break
        if not suppress_output:
            # export solution png
            self.export_png("sol_" + self.png_name + str(len(self.initMaze)))
            # build the gif
            if self.make_gif:
                size = len(self.initMaze)
                GifMaker.GifMaker.make_gif(self.animation_name + str(size) + "x" + str(size), self.png_name)

            # build and print the answer
            for color in self.color_lists:
                for pos in color:
                    self.answer[pos[0]][pos[1]] = self.domain[self.color_lists.index(color)]
            # add ports to answer
            for state in self.start_states + self.end_states:
                row, col = state.pos
                self.answer[row][col] = state.color
            # print answer
            for row in self.answer:
                for col in row:
                    print(col, end=" ")
                print()
            print("Number of attempted variable assignments:", self.vars_assigned)
            print("Run time: %.5f seconds\n" % run_time)

    def find_edge_colors(self):
        """
        Builds a list of color start/end nodes on the edge of the maze
        :return: list of states of the edge nodes
        """
        # use initMaze to find edges

        # initialize list to be returned
        edge_list = []
        # stores the size of the initial maze
        size = len(self.initMaze)-1

        # top left to top right
        for x in range(0, size+1):
            if self.initMaze[0][x] != '_':
                # should add any initial color nodes in the top row
                edge_list.append(S.State(self.initMaze[0][x], [0, x]))

        # top right to bottom right
        for x in range(1, size+1):
            if self.initMaze[x][size] != '_':
                # should add any initial color nodes in the right side of the maze
                edge_list.append(S.State(self.initMaze[x][size], [x, size]))

        # bottom right to bottom left
        for x in range(size-1, -1, -1):
            if self.initMaze[size][x] != '_':
                # should add any initial color nodes in the bottom part of the maze
                edge_list.append(S.State(self.initMaze[size][x], [size, x]))

        # bottom left to the top left
        for x in range(size-1, 0, -1):
            if self.initMaze[x][0] != '_':
                # should add any initial color nodes in the left side of the maze
                edge_list.append(S.State(self.initMaze[x][0], [x, 0]))

        return edge_list

    def detect_adjacent_edges(self):
        """
        checks to see if there are any start/end nodes in edge_list,
        and if there are, it marks them as visted in the boolean 2D array,
        as well as reordering the colors from the domain & color_list
        so they aren't re-attempted when the program is running.

        TL;DR: It solves the edge cases first, and then lets the rest of the program run.
        :return:
        """
        edge_list = self.find_edge_colors()

        if len(edge_list) >= 2:
            prev_color = edge_list[-1]

            # iterates through the list to check for adjacent colors
            for x in range(0, len(edge_list)):
                if edge_list[x].color == prev_color.color:
                    # print("Match! Color is: " + list[x].color + ","+str(list[x].pos)+"
                    # and :" + prev_color.color + "," + str(prev_color.pos))
                    # Mimics adding a node to the tree and map without actually doing it
                    self.add_edges_to_trackers(prev_color, edge_list[x])
                    self.reorder(edge_list[x].color)
                    # print(self.has_been_colored)
                prev_color = edge_list[x]
        else:
            pass

    def add_edges_to_trackers(self, s1, s2):
        """
        Adds all the nodes in between adjacent nodes on an edge to trackers
        :param s1:
        :param s2:
        :return:
        """
        directions = [[0, 1], [1, 0], [0, -1], [-1, 0]]  # N, E, S, W

        current_pos = [s1.pos[0], s1.pos[1]]
        # Adds initial node
        self.add_to_trackers(N.Node(s1, None))

        # Then use a loop to have it go in that direction until it either hits an edge,or finds S2
        while current_pos != s2.pos:
            # Left side
            if (current_pos[1] == 0) and not (current_pos[0] == 0):
                direction = directions[3]  # North
            # Right Side
            elif (current_pos[1] == len(self.initMaze) - 1) and not (current_pos[0] == len(self.initMaze) - 1):
                direction = directions[1]  # South
            # Bottom Side
            elif (current_pos[0] == len(self.initMaze) - 1) and not (current_pos[1] == 0):
                direction = directions[2]  # West
            # Top Side
            elif (current_pos[0] == 0) and not (current_pos[0] == len(self.initMaze) - 1):
                direction = directions[0]  # East
            else:
                print("No direction?")

            current_pos = [current_pos[0] + direction[0], current_pos[1] + direction[1]]
            self.add_to_trackers(N.Node(S.State(s1.color, current_pos), None))
            # update animation
            if self.make_gif:
                self.export_png(self.png_name + "_" + str(self.vars_assigned))

    def reorder(self, color):
        """
        Reorders the domain and color_list to have this color first
        Also adds 1 to the variable telling SolveMaze where to start
        :param color:
        :return:
        """
        # Store the color_list I'll be moving temporarily
        temp_color_list = self.color_lists.pop(self.domain.index(color))
        self.domain.remove(color)

        #  moves the color_list to pos 0
        self.color_lists.insert(0, temp_color_list)
        self.domain.insert(0, color)

        self.color_list_index += 1

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

        # trim lists to start of unfinished colors
        local_domain = self.domain[self.color_list_index:]
        local_start_ls = start_list[self.color_list_index:]
        local_end_ls = end_list[self.color_list_index:]
        # remainder of the trim
        remd_domain = self.domain[:self.color_list_index]
        remd_start_ls = start_list[:self.color_list_index]
        remd_end_ls = end_list[:self.color_list_index]
        lowest = []

        # check surrounding
        for i in range(len(local_start_ls)):
            # obtain possible moves for each color
            start_path_number.append(self.find_available_paths(local_start_ls[i]))
            end_path_number.append(self.find_available_paths(local_end_ls[i]))
        # add path values to find most constrained value
        for i in range(len(local_start_ls)):
            # variable that holds summed available paths of start and end nodes, as well as color index
            lowest.append([start_path_number[i] + end_path_number[i], i])

        lowest.sort(key=lambda x: x[0])
        new_start_list = []
        new_end_list = []
        new_domain = []
        # build reordered lists
        for i in range(len(lowest)):
            node_index = lowest[i][1]
            new_start_list.append(local_start_ls[node_index])
            new_end_list.append(local_end_ls[node_index])
            new_domain.append(local_domain[node_index])
        # insert finished lists
        new_start_list = remd_start_ls + new_start_list
        new_end_list = remd_end_ls + new_end_list
        self.domain = remd_domain + new_domain

        return new_start_list, new_end_list

    def find_available_paths(self, node):
        """
        Finds available paths for a node and returns the number
        :param node: The node to find the number of available paths for
        :return: returns available paths for a node
        """
        # counts number of available paths
        path = 0
        # find pos of adjacent states
        x, y = node.pos
        # list of adjacent node positions
        adj_nodes = [[x + dx, y + dy] for dx, dy in self.compare]
        for x, y in adj_nodes:
            try:
                if x < 0 or y < 0:
                    raise IndexError
                elif not self.has_been_colored[x][y]:
                    path += 1
            except IndexError:
                pass

        # return total number of available paths
        return path

    def next_start_state(self):
        """
        Gets the next starting state
        :return: starting state for the next color, or None if there are no more
        """
        return self.__gen_next_state(self.start_states, self.tree.current_node.state, 1)

    def current_end_state(self):
        """
        Gets the next ending state
        :return: ending state for the current color
        """
        return self.__gen_next_state(self.end_states, self.tree.current_node.state, 0)

    def __gen_next_state(self, main_list, state, delta):
        """
        Helper function for next state getting
        :param main_list: list to get from
        :return: next state, or None if there were none
        """
        index = self.domain.index(state.color) + delta
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

    def check_for_islands(self, color):
        """
        Checks for islands in all subsequent colors, returns True if none-where found.
        An island is formed when an unevaluated port is surrounded by other colors, dooming that color to failure.
        :param color: the current color being evaluated, only ports for subsequent colors can be surrounded
        during this color's evaluation.
        :return: True if no islands have been formed
        """
        # start testing on the next color
        i = self.domain.index(color) + 1
        # disable this constraint for the last color
        if i >= len(self.domain):
            return True
        # test each remaining port
        for port in self.start_states[i:] + self.end_states[i:]:
            if self.find_available_paths(port) == 0:
                return False
        # no islands found
        return True

    def manhattan_ordering(self, wall_follow):
        """
        Sorts the child nodes of the current node according to min manhattan distance to the end port
        :param wall_follow: if True a bonus will be applied to the manhattan distance of a node if it is on a wall
        :return: Nothing, but the current node's children will be sorted
        """
        target_pos = self.current_end_state().pos
        order_queue = PriorityQueue.PriorityQueue()
        for child in self.tree.current_node.children:
            position = child.state.pos
            # add wall following bonus, if enabled
            bonus = 0
            if wall_follow:
                # on a wall bonus
                if (child.state.pos[0] == 0 or child.state.pos[0] == len(self.initMaze) - 1 or
                        child.state.pos[1] == 0 or child.state.pos[1] == len(self.initMaze) - 1):
                    bonus -= self.edge_bonus  # manhattan distance of children can only differ by at most 2

                # on a color wall bonus
                local_pos = [[position[0] + dx, position[1] + dy] for dx, dy in self.compare]
                color_wall_bonus = 1  # will always find the previous node
                for row, col in local_pos:
                    if row < 0 or row >= len(self.initMaze) or col < 0 or col >= len(self.initMaze):
                        pass  # not a valid coordinate
                    elif self.has_been_colored[row][col]:
                        color_wall_bonus -= self.wall_bonus
                # total bonus
                bonus += color_wall_bonus

            # sort the children
            manhat_dis = abs(target_pos[0] - position[0]) + abs(target_pos[1] - position[1])
            if manhat_dis < self.proximity_range:
                bonus -= self.proximity_bonus - self.proximity_scale * manhat_dis

            order_queue.put(child, manhat_dis + bonus)

        # clear current children, then add them back in queue order
        self.tree.current_node.children = []
        while not order_queue.empty:
            self.tree.current_node.append_child(order_queue.get())

    def __update_hole_matrix(self):
        reevaluate = PriorityQueue.PriorityQueue()
        reevaluate.priority = False
        self.hole_index = 0

        for row in range(len(self.initMaze)):
            for col in range(len(self.initMaze)):
                # only check empty squares
                self.hole_matrix[row][col] = -1
                if not self.has_been_colored[row][col]:
                    reevaluate.put([row, col])

        while not reevaluate.empty:
            row, col = reevaluate.get()
            adj_queue = PriorityQueue.PriorityQueue()
            for dx, dy in self.compare:
                i, j = row + dx, col + dy
                # check for out of bounds
                if not (i < 0 or j < 0 or i >= len(self.initMaze) or j >= len(self.initMaze)):
                    # check for empty square
                    if not self.hole_matrix[i][j] == -1:
                        adj_queue.put([self.hole_matrix[i][j], [i, j]], self.hole_matrix[i][j])

            # adj squares exist, update them
            if not adj_queue.empty:
                # set this hole to the lowest available value
                min_val = adj_queue.get()[0]
                # set this square to the min
                self.hole_matrix[row][col] = min_val
                # update higher adj values
                while not adj_queue.empty:
                    next_val = adj_queue.get()
                    # don't reevaluate squares in the same hole
                    if not next_val[0] == min_val:
                        reevaluate.put(next_val[1])
            # no adj squares
            else:
                self.hole_matrix[row][col] = self.hole_index
                self.hole_index += 1

    def check_for_holes(self):
        hole_list = []
        # find all holes in the maze
        for row in self.hole_matrix:
            for hole_num in row:
                if hole_num >= 0 and not hole_list.__contains__(hole_num):
                    hole_list.append(hole_num)

        # for remaining port pairs, check
        current_index = self.domain.index(self.tree.current_node.state.color)
        for n in range(len(self.start_states[current_index:])):
            skip = False
            # use the current node instead of the start node for the current color
            if n == 0:
                pos = [self.tree.current_node.state.pos, self.current_end_state().pos]
                # disable current color for check if the current state is adj to the end state
                if abs(pos[0][0] - pos[1][0]) + abs(pos[0][1] - pos[1][1]) <= 1:
                    skip = True
            # use the starting port for unexpanded colors
            else:
                pos = [self.start_states[current_index + n].pos, self.end_states[current_index + n].pos]
            adj_list = [[], []]

            if not skip:
                # get adj square coordinates for the pair
                for dx, dy in self.compare:
                    for i in range(len(pos)):
                        delta_x, delta_y = [pos[i][0] + dx, pos[i][1] + dy]
                        # check for out of bounds
                        if not (delta_x < 0 or delta_y < 0 or
                                delta_x >= len(self.initMaze) or delta_y >= len(self.initMaze)):
                            # check for empty square
                            if not self.has_been_colored[delta_x][delta_y]:
                                # add square to current list
                                adj_list[i].append(self.hole_matrix[delta_x][delta_y])
                # check if pair share a hole
                valid = False
                for hole1 in adj_list[0]:
                    for hole2 in adj_list[1]:
                        if hole1 == hole2:
                            try:
                                # keep checking on a valid pair to remove all adj holes from the list
                                valid = True
                                # remove
                                hole_list.remove(hole1)
                            except ValueError:
                                pass

                # a pair of remaining ports cannot reach each other
                if not valid:
                    return False

        # also check all available holes are used
        if len(hole_list) > 0:
            return False

        # all tests passed
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

            # order the children according to distance from the goal, no use on children list less then 2
            if self.smart and self.manhattan and len(self.tree.current_node.children) > 1:
                self.manhattan_ordering(True)

    def make_node(self, color, pos):
        node = N.Node(S.State(color, pos), self.tree.current_node)
        return node

    def make_node2(self, state):
        node = N.Node(state, self.tree.current_node)
        return node

    def constraint_check(self):
        """
        evaluates constraints and returns the result
        evaluates on Tree's current_Node
        :return: True if all test passed, False otherwise
        """
        if self.smart:
            if not self.check_for_islands(self.tree.current_node.state.color):
                return False
            if not self.check_for_holes():
                return False

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
        # update hole tracking
        self.__update_hole_matrix()
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
            # update hole tracking
            self.__update_hole_matrix()
        else:
            # not important for non-port nodes since they are regenerated
            self.tree.current_node.state.expanded = False

        # removes last item from the color list
        color_val = self.domain.index(color)
        self.color_lists[color_val].pop()
