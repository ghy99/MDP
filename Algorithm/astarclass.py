from queue import PriorityQueue
import numpy as np
# import matplotlib.pyplot as plt
# import settings
# from grid import Grid
import copy


'''
self class:
uses:
Priority queue
dictionary of path {current node : parent node}
dictionary of pathcost {next node : total cost to travel to that node}
dictionary of visited nodes (only visit nv travel) {current node : parent node}
dictionary of edges {node : [surrounding nodes]}
stores:
current position before moving to destination
list of obstacles
a grid displaying all obstacles, path taken to reach destination (obstacle), current position
'''

# will require 2 queues, 1 for next path to take, 1 for which obstacle to go to first


class Astar:
    # def __init__(self, initpos, obstacles, grid, gridsize):
    def __init__(self, bot):
        # self.path = {}
        self.pathcost = {}
        self.visited = {}
        self.edges = {}
        self.pq = PriorityQueue()
        self.bot = bot
        self.currentpos = bot.getCurrentPos()
        
        # self.obstacles = obstacles   # list of current obstacles still in play
        self.grid = bot.grid
        self.obstacles = copy.deepcopy(bot.grid.getObstacles())
        # self.gridsize = gridsize
        self.gridsize = bot.grid.getGridSize()

    def getBot(self):
        return self.bot

    # returns all edges
    def allEdges(self):
        return self.edges

    # returns current node's edges
    def neighbours(self, node):
        return self.edges[node]

    ''' Finds the cell in front of obstacle's image to "flip direction" 
        so that robot faces obstacle instead of reversing into obstacle '''
    def chooseDest(self):
        self.dest = self.findDest(self.obstacles)
        # print(f"Obstacle list before: {self.obstacles}")
        self.obstacles.remove(self.dest)
        if self.dest.getCoord()[2] == "N":
            self.dest = (self.dest.getCoord()[0]-2, self.dest.getCoord()[1], "S")
        elif self.dest.getCoord()[2] == "E":
            self.dest = (self.dest.getCoord()[0], self.dest.getCoord()[1]+2, "W")
        elif self.dest.getCoord()[2] == "S":
            self.dest = (self.dest.getCoord()[0]+2, self.dest.getCoord()[1], "N")
        elif self.dest.getCoord()[2] == "W":
            self.dest = (self.dest.getCoord()[0], self.dest.getCoord()[1]-2, "E")
        # print(f"Obstacle list after: {self.obstacles}")
        print(f"self.dest: {self.dest}\tself.dest value: {self.grid.grid[self.dest[0]][self.dest[1]]}")

    ''' Update current location with location of last obstacle visited 
        (HAVE TO CHANGE THIS IN THE EVENT WHERE ROBOT RECOGNIZES IMAGE BEFORE STOPPING?
        Can be changed to path list's last cell visited? not sure about this)'''
    def updateNewDest(self):
        self.currentpos = self.dest
        self.bot.setCurrentPos(self.dest[0], self.dest[1], self.dest[2])
    
    def resetGrid(self, gridsize, obstacles):
        self.grid.reset(obstacles)
    
    def printObject(self):
        print(f"\nTaken path:")
        for key, val in self.path.items():
            print(f"\t\t{key}: {val}\n")
        print(f"Visited:")
        for key, val in self.visited.items():
            print(f"\t\t{key} : {val}\n")
        print(f"Priority Queue: \t{self.pq}")
        print(f"Current Position: \t{self.currentpos}")
        print(f"Next Destination: \t{self.dest}")
        print(f"Leftover Obstacles: \t{self.obstacles}\n")

    def checkforward(self, x, y, direction):
        pass
    
    def getReversePaths(self, currentNode, possibleSteps):
        pass

    ''' basically greedy find shortest distance but not accounting for 1 cell per move '''
    def heuristic(self, a, b):  # a = current position, b = destination position
        # print(f"a: {a}\tb: {b}")
        return np.abs(b[0] - a[0]) + np.abs(b[1] - a[1])

    ''' This function finds nearest obstacle to do a* (Can be changed to hamiltonian?) '''
    def findDest(self, obstacles):
        if obstacles:
            dest = obstacles[0]

        for i in obstacles:
            print(f"Current Position: {self.currentpos}\ti: {i.getCoord()}\tdestination: {dest.getCoord()}")
            if self.heuristic(self.currentpos, i.getCoord()) <= self.heuristic(self.currentpos, dest.getCoord()):
                dest = i
        return dest

    '''
    Add moving forward node, 
    right / left turns will be + 3 for each coordinate, 
    e.g.
    (1, 1) right turn to (4, 4)
    if (1, 1) left turn, (-2, 4) which will be illegal, pls check in filter Neighbours
    (19, 19) right turn, (22, 22) which is outside self.gridsize - 1 limit, pls check
    '''
    def processForwardSteps(self, currentNode):
        possibleSteps = []
        cheapCost = 1
        exCost = 6
        if currentNode[2] == 'N':
            # Move forward
            possibleSteps.append(((currentNode[0] - 1, currentNode[1], currentNode[2]), cheapCost))
            # Turn right
            possibleSteps.append(((currentNode[0] - 3, currentNode[1] + 3, 'E'), exCost))
            # Turn left
            possibleSteps.append(((currentNode[0] - 3, currentNode[1] - 3, 'W'), exCost))
        elif currentNode[2] == 'E':
            # Move forward
            possibleSteps.append(((currentNode[0], currentNode[1] + 1, currentNode[2]), cheapCost))
            # Turn right
            possibleSteps.append(((currentNode[0] + 3, currentNode[1] + 3, 'S'), exCost))
            # Turn left
            possibleSteps.append(((currentNode[0] - 3, currentNode[1] + 3, 'N'), exCost))
        elif currentNode[2] == 'S':
            # Move forward
            possibleSteps.append(((currentNode[0] + 1, currentNode[1], currentNode[2]), cheapCost))
            # Turn right
            possibleSteps.append(((currentNode[0] + 3, currentNode[1] - 3, 'W'), exCost))
            # Turn left
            possibleSteps.append(((currentNode[0] + 3, currentNode[1] + 3, 'E'), exCost))
        elif currentNode[2] == 'W':
            # Move forward
            possibleSteps.append(((currentNode[0], currentNode[1] - 1, currentNode[2]), cheapCost))
            # Turn right
            possibleSteps.append(((currentNode[0] - 3, currentNode[1] - 3, 'N'), exCost))
            # Turn left
            possibleSteps.append(((currentNode[0] + 3, currentNode[1] - 3, 'S'), exCost))
        return possibleSteps
        
    def checkForwardStep(self, currentNode, nextNode):
        if currentNode[2] == 'N':
            if (nextNode[1] > 0) and (nextNode[1] < self.gridsize - 1):
                for i in range(nextNode[1] - 1, nextNode[1] + 2):
                    if self.grid.grid[nextNode[0] - 1][i] == -10:
                        return False
                    else:
                        continue
        elif currentNode[2] == 'E':
            if (nextNode[0] > 0) and (nextNode[0] < self.gridsize - 1):
                for i in range(nextNode[0] - 1, nextNode[0] + 2):
                    if self.grid.grid[i][nextNode[1] + 1] == -10:
                        return False
                    else:
                        continue
        elif currentNode[2] == 'S':
            if (nextNode[1] > 0) and (nextNode[1] < self.gridsize - 1):
                for i in range(nextNode[1] - 1, nextNode[1] + 2):
                    if self.grid.grid[nextNode[0] + 1][i] == -10:
                        return False
                    else:
                        continue
        elif currentNode[2] == 'W':
            if (nextNode[0] > 0) and (nextNode[0] < self.gridsize - 1):
                for i in range(nextNode[0] - 1, nextNode[0] + 2):
                    if self.grid.grid[i][nextNode[1] - 1] == -10:
                        return False
                    else:
                        continue
        return True

    def checkRightTurn(self, currentNode, nextNode):
        return False

    def checkLeftTurn(self, currentNode, nextNode):
        return False

    
    ''' Filter out illegal / unnecessary moves '''
    def filterNeighbours(self, currentNode, possibleSteps):
        temp = []
        for eachStep in possibleSteps:
            if currentNode[2] == eachStep[0][2]:
                if self.checkForwardStep(currentNode, eachStep) == False:
                    temp.append(eachStep)
            else:
                if currentNode[2] == 'N':
                    if eachStep[0][2] == 'E':
                        if self.checkRightTurn(currentNode, eachStep) == False:
                            temp.append(eachStep)
                    elif eachStep[0][2] == 'W':
                        if self.checkLeftTurn(currentNode, eachStep) == False:
                            temp.append(eachStep)
                elif currentNode[2] == 'E':
                    if eachStep[0][2] == 'S':
                        if self.checkRightTurn(currentNode, eachStep) == False:
                            temp.append(eachStep)
                    elif eachStep[0][2] == 'N':
                        if self.checkLeftTurn(currentNode, eachStep) == False:
                            temp.append(eachStep)
                elif currentNode[2] == 'S':
                    if eachStep[0][2] == 'W':
                        if self.checkRightTurn(currentNode, eachStep) == False:
                            temp.append(eachStep)
                    elif eachStep[0][2] == 'E':
                        if self.checkLeftTurn(currentNode, eachStep) == False:
                            temp.append(eachStep)
                elif currentNode[2] == 'W':
                    if eachStep[0][2] == 'N':
                        if self.checkRightTurn(currentNode, eachStep) == False:
                            temp.append(eachStep)
                    elif eachStep[0][2] == 'S':
                        if self.checkLeftTurn(currentNode, eachStep) == False:
                            temp.append(eachStep)
        for step in temp:
            possibleSteps.remove(step)
        return possibleSteps

    def checkDest(self, currentNode, destination):
        pass

    def algorithm(self):
        self.pq.put((0, self.currentpos))
        self.visited[self.getBot().getCurrentPos()] = None
        self.pathcost[self.getBot().getCurrentPos()] = None
        while not self.pq.empty():
            currentNode = self.pq.get()[1]
            possibleSteps = self.processForwardSteps(currentNode)
            possibleSteps = self.filterNeighbours(currentNode, possibleSteps)
        return

    def constructPath(self):
        currentNode = self.dest
        path = []
        # while currentNode != self.currentpos:
        while currentNode != self.bot.getCurrentPos():
            path.append(currentNode)
            currentNode = self.path[currentNode]
        # path.append(self.currentpos)
        path.append(self.bot.getCurrentPos())
        path.reverse()
        return path

    ''' Run A* Algo'''
    def runAlgo(self):
        pass