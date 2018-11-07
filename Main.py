"""
Authors: George Engel, Cory Johns, Justin Keeling 
"""
import SolveMaze as SM


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


# "Global" variables
running = True
auto_run = False
smart = False
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
        solve = SM.SolveMaze(read_in_maze(st), smart, gif_gen, manhattan)
output_file.close()
