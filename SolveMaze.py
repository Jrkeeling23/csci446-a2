from enum import Enum

class SolveMaze:

    #Lists of color positions (in sync with the STATE TREE
    colorLists = []

    def __init__(self, maze):
        self.initMaze = maze
        #Make list of unique colors
        self.domain = self.findUniqueColors()
        #lists the domain
        print("\nDomain: "+str(self.domain))
        #use index of a 'COLOR' in domain to find it's numerical value

        #make empty color lists for each unique color in domain
        for l in self.domain:
            self.colorLists.append([])

        print("Maze Sovler Initialized")

    def validate(self):
        pass

    def findUniqueColors(self):
        listC = []
        for x in self.initMaze:
            for y in x:
                if(not listC.__contains__(y))and (y!='_'):
                    listC.append(y)
        return listC
