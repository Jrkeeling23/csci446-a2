"""
Authors: George Engel, Cory Johns, Justin Keeling 
"""

import SolveMaze as SM

def read_in_maze(string):
    global running, auto_run

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

    def print_maze(maze):
        for row in maze:
            print(row)

    # the maze will go here, overwrites for each run
    maze_xy = []

    # maze txt files must be in the same directory with the given names
    if string == "Q" or string == "q":
        running = False
    elif string == "A" or string == "a":
        auto_run = True
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

    #print_maze(maze_xy)
    return maze_xy

# "Global" variables
running = True
auto_run = False
# the output file
output_file = open('output.txt', 'w+')
# input for auto run
input_list = ["5", "7", "8", "9", "10", "12", "14", "Q"]
# index for auto run
index = 0

# main program loop
while running:
    # auto run emulates sequential keyboard input, to save the user hassle
    if auto_run:
        print("Automatic running enabled: ", input_list[index])
        inp = input_list[index]
        index += 1
    # normal input
    else:
        inp = "" + input("Enter the maze file you want to run, or enter an option to run a pre-configured maze:\n"
                         "Enter N where N is the 5, 7, 8, 9, 10, 12, or 14, "
                         "Enter A to start automatic running, "
                         "or Enter Q to quit:\n")
    # always do this stuff
    #init new solvemaze here and input 2D list returned by readinmaze
    solve = SM.SolveMaze(read_in_maze(inp))
output_file.close()