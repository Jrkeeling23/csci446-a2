"""
Authors: George Engel, Cory Johns, Justin Keeling 
"""
import SolveMaze as SM
from scipy.optimize import fmin
import numpy as np
import time


def read_in_maze(string):
    global running, auto_run, smart, gif_gen, manhattan

    def __build_maze(file):
        """
        Builds a 2D array from the input file
        :param file: containing the board in text form
        """
        nonlocal maze_xy
        # open file, make a 2d list of each letter
        # with covers try-catch business, '__' prefix is 'private' sort of
        with open(file) as __f:
            for __line in __f:
                # build up a row, then add it to the maze
                __x_tmp = []
                for __char in __line:
                    # don't add newline chars
                    if __char != '\n':
                        __x_tmp.append(__char)
                maze_xy.append(__x_tmp)

    # the maze will go here, overwrites for each run
    maze_xy = []

    try:
        # maze txt files must be in the same directory with the given names
        if string == "Q" or string == "q":
            running = False
        elif string == "A" or string == "a":
            auto_run = True
        elif string == "S" or string == "s":
            smart = not smart
            print("Now using %s implementation\n" % ("Smart" if smart else "Dumb"))
        elif string == "G" or string == "g":
            gif_gen = not gif_gen
            print("Now generating GIFs while solving,"
                  "\nWarning!! run time / memory space can become excessive"
                  " - Not recommended with variable assignments in excess of 25000\n"
                  if gif_gen else "GIF generation disabled\n")
        elif string == "M" or string == "m":
            manhattan = not manhattan
            print("Now%s using manhattan distance\n" % ("" if manhattan else " not"))
        elif string == '5':
            __build_maze("assignment-resources/5x5maze.txt")
        elif string == '7':
            __build_maze("assignment-resources/7x7maze.txt")
        elif string == '8':
            __build_maze("assignment-resources/8x8maze.txt")
        elif string == '9':
            __build_maze("assignment-resources/9x9maze.txt")
        elif string == '10':
            __build_maze("assignment-resources/10x10maze.txt")
        elif string == '12':
            __build_maze("assignment-resources/12x12maze.txt")
        elif string == '14':
            __build_maze("assignment-resources/14x14maze.txt")
        else:
            __build_maze(string)
    except FileNotFoundError:
        print("No such file %s" % string)

    return maze_xy


def objective_function(x, mazes):
    # initial guess x = [5, 6, 10, 3] = [proximity_range, proximity_bonus, edge_bonus, wall_bonus]
    val = [0, 0, 0, 0]

    i = 0
    # get answers
    for maze in mazes:
        solve = SM.SolveMaze(maze, True, False, True)
        solve.proximity_range = x[0]
        solve.proximity_bonus = x[1]
        solve.proximity_scale = x[2]
        solve.edge_bonus = x[3]
        solve.wall_bonus = x[4]
        solve.start_solving(True)
        val[i] = solve.vars_assigned
        i += 1

    return val


# "Global" variables
running = True
auto_run = False
smart = True
gif_gen = False
manhattan = True
# the output file
output_file = open('output.txt', 'w+')
# input for auto run
auto_input = "5, 7, 8, 9, 10, 12, 14"
# index for auto run
index = 0

# main program loop
while running:
    # auto run emulates sequential keyboard input, to save the user hassle
    if auto_run:
        print("Automatic running enabled ...")
        inp = auto_input
    # normal input
    else:
        inp = "" + input("Enter the maze file you want to run, or enter an option(s) separated by \',\':\n"
                         "Options: 5, 7, 8, 9, 10, 12, or 14 to run the corresponding maze, "
                         "\nA to start automatic running,\nS to toggle smart/dumb implementation,"
                         "\nG to generate GIF animations of the solving process, "
                         "\nor Q to quit:\n")
    # always do this stuff
    # for loop to allow multiple inputs in sequence
    for st in inp.split(","):
        # remove the space after a comma if the user added one
        if st[0] == " ":
            st = st[1:]
        # init new SolveMaze here and input 2D list returned by read_in_maze
        maze = read_in_maze(st)
        if len(maze) > 0:
            solve = SM.SolveMaze(maze, smart, gif_gen, manhattan)
            smart_str = "smart" if smart else "dumb"
            manhat_str = "_manhattan" if smart and manhattan else ""
            solve.png_name = "maze" + str(len(maze)) + "_" + smart_str + manhat_str
            solve.animation_name += "_" + smart_str + manhat_str
            solve.start_solving()
output_file.close()

# # optimize values, with grid testing
# mazes = (read_in_maze("5"), read_in_maze("7"), read_in_maze("8"), read_in_maze("9"))
# # [proximity_range, proximity_bonus, proximity_scale, edge_bonus, wall_bonus]
# grid1 = [6]
# grid2 = [85]
# grid2b = [12]
# grid3 = [20]
# grid4 = [4]
# best = [0, -1]
# start_time = time.process_time()
# for p_range in grid1:
#     for p_scale in grid2b:
#         for p_bonus in grid2:
#             for e_bonus in grid3:
#                 for w_bonus in grid4:
#                     x0 = [p_range, p_bonus, p_scale, e_bonus, w_bonus]
#                     vars_assigned = objective_function(x0, mazes)
#                     s = sum(vars_assigned)
#                     if s < best[-1] or best[-1] == -1:
#                         best = vars_assigned + [s]
#                     print("for", x0, "vars =", vars_assigned)
# end_time = time.process_time()
# print(best)
# print("process took:", end_time - start_time)
