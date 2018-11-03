"""
Authors: George Engel, Cory Johns, Justin Keeling 
"""
import SolveMaze as SM


def read_in_maze(string):
    global running, auto_run, smart, gif_gen

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
    elif string == "S" or string == "s":
        smart = not smart
        print("Now using %s implementation\n" % ("Smart" if smart else "Dumb"))
    elif string == "G" or string == "g":
        gif_gen = not gif_gen
        print("Now generating GIFs while solving,"
              "\nWarning!! run time / memory space can become excessive"
              " - Not recommended with variable assignments in excess of 25000\n"
              if gif_gen else "GIF generation disabled\n")
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

    return maze_xy


# "Global" variables
running = True
auto_run = False
smart = False
gif_gen = False
# the output file
output_file = open('output.txt', 'w+')
# input for auto run
input_list = ["5", "7", "8", "9", "10", "12", "14",
              "s", "5", "7", "8", "9", "10", "12", "14", "Q"]
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
        inp = "" + input("Enter the maze file you want to run, or enter an option:\n"
                         "Options: 5, 7, 8, 9, 10, 12, or 14 to run the corresponding maze, "
                         "\nA to start automatic running,\nS to toggle smart/dumb implementation,"
                         "\nG to generate GIF animations of the solving process, "
                         "\nor Q to quit:\n")
    # always do this stuff
    # init new SolveMaze here and input 2D list returned by read_in_maze
    solve = SM.SolveMaze(read_in_maze(inp), smart, gif_gen)
output_file.close()