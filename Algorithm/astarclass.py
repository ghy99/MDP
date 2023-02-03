from queue import PriorityQueue
import numpy as np
import matplotlib.pyplot as plt
import pygame
from grid import Grid


'''
Astar class:
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
    def __init__(self, initpos, obstacles, grid, gridsize):
        self.path = {}
        self.pathcost = {}
        self.visited = {}
        self.edges = {}
        self.pq = PriorityQueue()
        self.currentpos = initpos
        self.obstacles = obstacles   # list of current obstacles still in play
        self.grid = grid
        self.gridsize = gridsize

    # returns all edges
    def allEdges(self):
        return self.edges

    # returns current node's edges
    def neighbours(self, node):
        return self.edges[node]

    # create possible paths (1 step) from each node to the next node
    def processNeighbours(self, gridsize):
        cheapCost = 1
        exCost = 6
        directions = ["N", "E", "S", "W"]
        for i in range(gridsize):
            for j in range(gridsize):
                for k in range(len(directions)):
                    # if self.grid.grid[i][j] >= 0:   # more than / equal to 0 cos starting position labeled as 1
                    neighbours = []
                    # Check border available paths
                    # cell above current cell: "N"
                    if (i > 0) and (self.grid.grid[i - 1][j] != -1 and self.grid.grid[i - 1][j] != -10):
                        neighbours.append(
                            ((i - 1, j, directions[k]), cheapCost))
                    # cell right of current cell: "E"
                    if (j < gridsize - 1) and (self.grid.grid[i][j+1] != -1 and self.grid.grid[i][j+1] != -10):
                        neighbours.append(
                            ((i, j + 1, directions[k]), cheapCost))
                    # cell below current cell: "S"
                    if (i < gridsize - 1) and (self.grid.grid[i + 1][j] != -1 and self.grid.grid[i + 1][j] != -10):
                        neighbours.append(
                            ((i + 1, j, directions[k]), cheapCost))
                    # cell left of current cell: "W"
                    if (j > 0) and (self.grid.grid[i][j - 1] != -1 and self.grid.grid[i][j - 1] != -10):
                        neighbours.append(
                            ((i, j - 1, directions[k]), cheapCost))
                    # cell NorthWest of current cell: "NW"
                    if (i > 0) and (j > 0) and (self.grid.grid[i - 1][j - 1] != -1 and self.grid.grid[i - 1][j - 1] != -10):
                        if directions[k] == "N" and (self.grid.grid[i - 1][j] != -1 and self.grid.grid[i - 1][j] != -10):
                            neighbours.append(((i - 1, j - 1, "W"), exCost))
                        elif directions[k] == "E" and (self.grid.grid[i][j - 1] != -1 and self.grid.grid[i][j - 1] != -10):
                            neighbours.append(((i - 1, j - 1, "S"), exCost))
                        elif directions[k] == "S" and (self.grid.grid[i - 1][j] != -1 and self.grid.grid[i - 1][j] != -10):
                            neighbours.append(((i - 1, j - 1, "E"), exCost))
                        elif directions[k] == "W" and (self.grid.grid[i][j - 1] != -1 and self.grid.grid[i][j - 1] != -10):
                            neighbours.append(((i - 1, j - 1, "N"), exCost))
                    # cell NorthEast of current cell: "NE"
                    if (i > 0) and (j < gridsize - 1) and (self.grid.grid[i - 1][j + 1] != -1 and self.grid.grid[i - 1][j + 1] != -10):
                        if directions[k] == "N" and (self.grid.grid[i - 1][j] != -1 and self.grid.grid[i - 1][j] != -10):
                            neighbours.append(((i - 1, j + 1, "E"), exCost))
                        elif directions[k] == "E" and (self.grid.grid[i][j + 1] != -1 and self.grid.grid[i][j + 1] != -10):
                            neighbours.append(((i - 1, j + 1, "N"), exCost))
                        elif directions[k] == "S" and (self.grid.grid[i - 1][j] != -1 and self.grid.grid[i - 1][j] != -10):
                            neighbours.append(((i - 1, j + 1, "W"), exCost))
                        elif directions[k] == "W" and (self.grid.grid[i][j + 1] != -1 and self.grid.grid[i][j + 1] != -10):
                            neighbours.append(((i - 1, j + 1, "S"), exCost))
                    # cell SouthEast of current cell: "SE"
                    if (i < gridsize - 1) and (j < gridsize - 1) and (self.grid.grid[i + 1][j + 1] != -1 and self.grid.grid[i + 1][j + 1] != -10):
                        if directions[k] == "N" and (self.grid.grid[i + 1][j] != -1 and self.grid.grid[i + 1][j] != -10):
                            neighbours.append(((i + 1, j + 1, "W"), exCost))
                        elif directions[k] == "E" and (self.grid.grid[i][j + 1] != -1 and self.grid.grid[i][j + 1] != -10):
                            neighbours.append(((i + 1, j + 1, "S"), exCost))
                        elif directions[k] == "S" and (self.grid.grid[i + 1][j] != -1 and self.grid.grid[i + 1][j] != -10):
                            neighbours.append(((i + 1, j + 1, "E"), exCost))
                        elif directions[k] == "W" and (self.grid.grid[i][j + 1] != -1 and self.grid.grid[i][j + 1] != -10):
                            neighbours.append(((i + 1, j + 1, "N"), exCost))
                        # cell SouthWest of current cell: "SW"
                    if (i < gridsize - 1) and (j > 0) and (self.grid.grid[i + 1][j - 1] != -1 and self.grid.grid[i + 1][j - 1] != -10):
                        if directions[k] == "N" and (self.grid.grid[i + 1][j] != -1 and self.grid.grid[i + 1][j] != -10):
                            neighbours.append(((i + 1, j - 1, "E"), exCost))
                        elif directions[k] == "E" and (self.grid.grid[i][j - 1] != -1 and self.grid.grid[i][j - 1] != -10):
                            neighbours.append(((i + 1, j - 1, "N"), exCost))
                        elif directions[k] == "S" and (self.grid.grid[i + 1][j] != -1 and self.grid.grid[i + 1][j] != -10):
                            neighbours.append(((i + 1, j - 1, "W"), exCost))
                        elif directions[k] == "W" and (self.grid.grid[i][j - 1] != -1 and self.grid.grid[i][j - 1] != -10):
                            neighbours.append(((i + 1, j - 1, "S"), exCost))
                    # insert edges into object grid
                    self.edges[(i, j, directions[k])] = neighbours
    
    
    def resetGrid(self, gridsize, obstacles):
        for i in range(gridsize):
            for j in range(gridsize):
                if self.currentpos[0] == i and self.currentpos[1] == j:
                    self.grid.grid[i][j] = 1
                if i < 4 and j < 4:
                    self.grid.grid[i][j] = -5
                self.grid.grid[i][j] = 0
        self.grid.setObstacles(obstacles, gridsize)

    
    def getReversePaths(self, currentNode, possibleSteps):
        cheapCost = 4
        exCost = 6
        if currentNode[2] == "N":
            # reverse SW
            if (currentNode[0] < self.gridsize - 1) and (currentNode[1] > 0) and self.grid.grid[currentNode[0] + 1][currentNode[1] - 1] != 1 and self.grid.grid[currentNode[0] + 1][currentNode[1] - 1] != -10:
                if self.grid.grid[currentNode[0] + 1][currentNode[1]] != 1 and self.grid.grid[currentNode[0] + 1][currentNode[1]] != -10:
                    possibleSteps.append(
                        ((currentNode[0]+1, currentNode[1]-1, "E"), exCost))
            # reverse S
            if (currentNode[0] < self.gridsize - 1) and self.grid.grid[currentNode[0]+1][currentNode[1]] != 1 and self.grid.grid[currentNode[0]+1][currentNode[1]] != -10:
                possibleSteps.append(
                    ((currentNode[0]+1, currentNode[1], "N"), cheapCost))
            # reverse SE
            if (currentNode[0] > self.gridsize - 1) and (currentNode[1] < self.gridsize - 1) and self.grid.grid[currentNode[0]+1][currentNode[1]+1] != 1 and self.grid.grid[currentNode[0]+1][currentNode[1]+1] != -10:
                if self.grid.grid[currentNode[0]+1][currentNode[1]] != 1 and self.grid.grid[currentNode[0]+1][currentNode[1]] != -10:
                    possibleSteps.append(
                        ((currentNode[0]+1, currentNode[1]+1, "W"), exCost))
        elif currentNode[2] == "E":
            # reverse NW
            if (currentNode[0] > 0) and (currentNode[1] > 0) and self.grid.grid[currentNode[0]-1][currentNode[1]-1] != 1 and self.grid.grid[currentNode[0]-1][currentNode[1]-1] != -10:
                if self.grid.grid[currentNode[0]][currentNode[1]-1] != 1 and self.grid.grid[currentNode[0]][currentNode[1]-1] != -10:
                    possibleSteps.append(
                        ((currentNode[0]-1, currentNode[1]-1, "S"), exCost))
            # reverse W
            if (currentNode[1] > 0) and self.grid.grid[currentNode[0]][currentNode[1]-1] != 1 and self.grid.grid[currentNode[0]][currentNode[1]-1] != -10:
                possibleSteps.append(
                    ((currentNode[0], currentNode[1]-1, "E"), cheapCost))
            # reverse SW
            if (currentNode[0] < self.gridsize - 1) and (currentNode[1] > 0) and self.grid.grid[currentNode[0]+1][currentNode[1]-1] != 1 and self.grid.grid[currentNode[0]+1][currentNode[1]-1] != -10:
                if self.grid.grid[currentNode[0]][currentNode[1]-1] != 1 and self.grid.grid[currentNode[0]][currentNode[1]-1] != -10:
                    possibleSteps.append(
                        ((currentNode[0]+1, currentNode[1]-1, "N"), exCost))
        elif currentNode[2] == "S":
            # reverse NW
            if (currentNode[0] > 0) and (currentNode[1] > 0) and self.grid.grid[currentNode[0]-1][currentNode[1]-1] != 1 and self.grid.grid[currentNode[0]-1][currentNode[1]-1] != -10:
                if self.grid.grid[currentNode[0]-1][currentNode[1]] != 1 and self.grid.grid[currentNode[0]-1][currentNode[1]] != -10:
                    possibleSteps.append(
                        ((currentNode[0]-1, currentNode[1]-1, "E"), exCost))
            # reverse N
            if (currentNode[0] > 0) and self.grid.grid[currentNode[0]-1][currentNode[1]] != 1 and self.grid.grid[currentNode[0]-1][currentNode[1]] != -10:
                possibleSteps.append(
                    ((currentNode[0]-1, currentNode[1], "S"), cheapCost))
            # reverse NE
            if (currentNode[0] > 0) and (currentNode[1] < self.gridsize - 1) and self.grid.grid[currentNode[0]-1][currentNode[1]+1] != 1 and self.grid.grid[currentNode[0]-1][currentNode[1]+1] != -10:
                if self.grid.grid[currentNode[0]-1][currentNode[1]] != 1 and self.grid.grid[currentNode[0]-1][currentNode[1]] != -10:
                    possibleSteps.append(
                        ((currentNode[0]-1, currentNode[1]+1, "W"), exCost))
        elif currentNode[2] == "W":
            # reverse NE
            if (currentNode[0] > 0) and (currentNode[1] < self.gridsize - 1) and self.grid.grid[currentNode[0]-1][currentNode[1]+1] != 1 and self.grid.grid[currentNode[0]-1][currentNode[1]+1] != -10:
                if self.grid.grid[currentNode[0]][currentNode[1]+1] != 1 and self.grid.grid[currentNode[0]][currentNode[1]+1] != -10:
                    possibleSteps.append(
                        ((currentNode[0]-1, currentNode[1]+1, "S"), exCost))
            # reverse E
            if (currentNode[1] < self.gridsize - 1) and self.grid.grid[currentNode[0]][currentNode[1]+1] != 1 and self.grid.grid[currentNode[0]][currentNode[1]+1] != -10:
                possibleSteps.append(
                    ((currentNode[0], currentNode[1]+1, "W"), cheapCost))
            # reverse SE
            if (currentNode[0] > self.gridsize - 1) and (currentNode[1] < self.gridsize - 1) and self.grid.grid[currentNode[0]+1][currentNode[1]+1] != 1 and self.grid.grid[currentNode[0]+1][currentNode[1]+1] != -10:
                if self.grid.grid[currentNode[0]][currentNode[1]+1] != 1 and self.grid.grid[currentNode[0]][currentNode[1]+1] != -10:
                    possibleSteps.append(
                        ((currentNode[0]+1, currentNode[1]+1, "N"), exCost))
        return possibleSteps

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

    ''' basically greedy find shortest distance but not accounting for 1 cell per move '''
    def heuristic(self, a, b):  # a = current position, b = destination position
        return np.abs(b[0] - a[0]) + np.abs(b[1] - a[1])

    ''' This function finds nearest obstacle to do a* (Can be changed to hamiltonian?) '''
    def findDest(self, obstacles):
        # dest = (9999, 9999, "N")
        if obstacles:
            dest = obstacles[0]

        print(f"Obstacles: {obstacles}")
        for i in obstacles:
            print(f"{self.currentpos}, {dest}")
            currentpos = (self.currentpos[0], self.currentpos[1])
            if self.heuristic(currentpos, i) <= self.heuristic(currentpos, dest):
                dest = i
        return dest

    ''' Finds the cell in front of obstacle's image to "flip direction" 
        so that robot faces obstacle instead of reversing into obstacle '''
    def chooseDest(self):
        self.dest = self.findDest(self.obstacles)
        # print(f"Obstacle list before: {self.obstacles}")
        self.obstacles.remove(self.dest)
        if self.dest[2] == "N":
            self.dest = (self.dest[0]-1, self.dest[1], "S")
        elif self.dest[2] == "E":
            self.dest = (self.dest[0], self.dest[1]+1, "W")
        elif self.dest[2] == "S":
            self.dest = (self.dest[0]+1, self.dest[1], "N")
        elif self.dest[2] == "W":
            self.dest = (self.dest[0], self.dest[1]-1, "E")
        # print(f"Obstacle list after: {self.obstacles}")

    ''' Update current location with location of last obstacle visited 
        (HAVE TO CHANGE THIS IN THE EVENT WHERE ROBOT RECOGNIZES IMAGE BEFORE STOPPING?
        Can be changed to path list's last cell visited? not sure about this)'''
    def updateNewDest(self):
        self.currentpos = self.dest

    ''' Filter out illegal / unnecessary moves '''
    def filterNeighbours(self, currentNode):
        nb = self.neighbours(currentNode)
        toBeRemoved = []
        for cell in nb:
            if cell[0] in self.visited:
                toBeRemoved.append(cell)
                continue
            if currentNode[2] == "N":
                if (currentNode[0] == cell[0][0]) and (currentNode[1] + 1 == cell[0][1]):
                    print("E TO BE DELETED")
                    toBeRemoved.append(cell)
                    continue
                elif (currentNode[0] + 1 == cell[0][0]) and (currentNode[1] + 1 == cell[0][1]):
                    print("SE TO BE DELETED")
                    toBeRemoved.append(cell)
                    continue
                elif (currentNode[0] + 1 == cell[0][0]) and (currentNode[1] == cell[0][1]):
                    print("S TO BE DELETED")
                    toBeRemoved.append(cell)
                    continue
                elif (currentNode[0] + 1 == cell[0][0]) and (currentNode[1] - 1 == cell[0][1]):
                    print("SW TO BE DELETED")
                    toBeRemoved.append(cell)
                    continue
                elif (currentNode[0] == cell[0][0]) and (currentNode[1] - 1 == cell[0][1]):
                    print("W TO BE DELETED")
                    toBeRemoved.append(cell)
                    continue
            elif currentNode[2] == "S":
                if (currentNode[0] - 1 == cell[0][0]) and (currentNode[1] - 1 == cell[0][1]):
                    print("NW TO BE DELETED")
                    toBeRemoved.append(cell)
                    continue
                elif (currentNode[0] - 1 == cell[0][0]) and (currentNode[1] == cell[0][1]):
                    print("N TO BE DELETED")
                    toBeRemoved.append(cell)
                    continue
                elif (currentNode[0] - 1 == cell[0][0]) and (currentNode[1] + 1 == cell[0][1]):
                    print("NE TO BE DELETED")
                    toBeRemoved.append(cell)
                    continue
                elif (currentNode[0] == cell[0][0]) and (currentNode[1] + 1 == cell[0][1]):
                    print("E TO BE DELETED")
                    toBeRemoved.append(cell)
                    continue
                elif (currentNode[0] == cell[0][0]) and (currentNode[1] - 1 == cell[0][1]):
                    print("W TO BE DELETED")
                    toBeRemoved.append(cell)
                    continue
            elif currentNode[2] == "E":
                if (currentNode[0] - 1 == cell[0][0]) and (currentNode[1] - 1 == cell[0][1]):
                    print("NW TO BE DELETED")
                    toBeRemoved.append(cell)
                    continue
                if (currentNode[0] - 1 == cell[0][0]) and (currentNode[1] == cell[0][1]):
                    print("N TO BE DELETED")
                    toBeRemoved.append(cell)
                    continue
                elif (currentNode[0] + 1 == cell[0][0]) and (currentNode[1] == cell[0][1]):
                    print("S TO BE DELETED")
                    toBeRemoved.append(cell)
                    continue
                elif (currentNode[0] + 1 == cell[0][0]) and (currentNode[1] - 1 == cell[0][1]):
                    print("SW TO BE DELETED")
                    toBeRemoved.append(cell)
                    continue
                elif (currentNode[0] == cell[0][0]) and (currentNode[1] - 1 == cell[0][1]):
                    print("W TO BE DELETED")
                    toBeRemoved.append(cell)
                    continue
            elif currentNode[2] == "W":
                if (currentNode[0] - 1 == cell[0][0]) and (currentNode[1] == cell[0][1]):
                    print("N TO BE DELETED")
                    toBeRemoved.append(cell)
                    continue
                elif (currentNode[0] - 1 == cell[0][0]) and (currentNode[1] + 1 == cell[0][1]):
                    print("NE TO BE DELETED")
                    toBeRemoved.append(cell)
                    continue
                elif (currentNode[0] == cell[0][0]) and (currentNode[1] + 1 == cell[0][1]):
                    print("E TO BE DELETED")
                    toBeRemoved.append(cell)
                    continue
                elif (currentNode[0] + 1 == cell[0][0]) and (currentNode[1] + 1 == cell[0][1]):
                    print("SE TO BE DELETED")
                    toBeRemoved.append(cell)
                    continue
                elif (currentNode[0] + 1 == cell[0][0]) and (currentNode[1] == cell[0][1]):
                    print("S TO BE DELETED")
                    toBeRemoved.append(cell)
                    continue
        for i in toBeRemoved:
            nb.remove(i)
        if len(nb) == 0:
            nb = self.getReversePaths(currentNode, nb)
        return nb

    # def changeCurrentNode(self, currentNode, nextNode):
    #     # print(f"Current: {currentNode}\tNext: {nextNode}")
    #     direction = None
    #     if (currentNode[0] - 1 == nextNode[0]) and (currentNode[1] == nextNode[1]):     # N
    #         if currentNode[2] == "N":
    #             direction = "N"
    #         elif currentNode[2] == "S":
    #             direction = "S"
    #     if (currentNode[0] == nextNode[0]) and (currentNode[1] + 1 == nextNode[1]):     # E
    #         if currentNode[2] == "E":
    #             direction = "E"
    #         elif currentNode[2] == "W":
    #             direction = "W"
    #     if (currentNode[0] + 1 == nextNode[0]) and (currentNode[1] == nextNode[1]):     # S
    #         if currentNode[2] == "N":
    #             direction = "N"
    #         elif currentNode[2] == "S":
    #             direction = "S"
    #     if (currentNode[0] == nextNode[0]) and (currentNode[1] - 1 == nextNode[1]):     # W
    #         if currentNode[2] == "E":
    #             direction = "E"
    #         elif currentNode[2] == "W":
    #             direction = "W"
    #     if (currentNode[0] - 1 == nextNode[0]) and (currentNode[1] - 1 == nextNode[1]):     # NW
    #         if currentNode[2] == "N":
    #             direction = "W"
    #         elif currentNode[2] == "W":
    #             direction = "N"
    #         elif currentNode[2] == "S":
    #             direction = "E"
    #         elif currentNode[2] == "E":
    #             direction = "S"
    #     if (currentNode[0] - 1 == nextNode[0]) and (currentNode[1] + 1 == nextNode[1]):     # NE
    #         if currentNode[2] == "N":
    #             direction = "E"
    #         elif currentNode[2] == "E":
    #             direction = "N"
    #         elif currentNode[2] == "S":
    #             direction = "W"
    #         elif currentNode[2] == "W":
    #             direction = "S"
    #     if (currentNode[0] + 1 == nextNode[0]) and (currentNode[1] + 1 == nextNode[1]):     # SE
    #         if currentNode[2] == "S":
    #             direction = "E"
    #         elif currentNode[2] == "E":
    #             direction = "S"
    #         elif currentNode[2] == "N":
    #             direction = "W"
    #         elif currentNode[2] == "W":
    #             direction = "N"
    #     if (currentNode[0] + 1 == nextNode[0]) and (currentNode[1] - 1 == nextNode[1]):     # SW
    #         if currentNode[2] == "S":
    #             direction = "W"
    #         elif currentNode[2] == "W":
    #             direction = "S"
    #         elif currentNode[2] == "N":
    #             direction = "E"
    #         elif currentNode[2] == "E":
    #             direction = "N"
    #     if direction == None:
    #         print(
    #             f"NONE ENCOUNTERED!!!!!!!\nCurrent Node: {currentNode}\tNext Node: {nextNode}\tdirection: {direction}\n")
    #     return (nextNode[0], nextNode[1], direction)

    def algorithm(self):
        self.pq.put((0, self.currentpos))
        semaphore = 0
        self.visited[self.currentpos] = None
        self.pathcost[self.currentpos] = 0
        while not self.pq.empty() or semaphore == 0:
            if self.pq.empty() and semaphore == 0:
                possibleSteps = self.getReversePaths(currentNode, [])
                possibleSteps = self.filterNeighbours(currentNode)
            else:
                currentNode = self.pq.get()[1]
                if currentNode == self.dest:
                    semaphore = 1
                    break
                possibleSteps = self.filterNeighbours(currentNode)

            for nextNode, weight in possibleSteps:
                if self.grid.grid[nextNode[0]][nextNode[1]] == 1 or self.grid.grid[nextNode[0]][nextNode[1]] == -10:
                    continue
                currentCost = weight + self.pathcost[currentNode]
                heuristic = self.heuristic(nextNode, self.dest)
                newCost = currentCost * heuristic
                if (nextNode not in self.visited) or (currentCost < self.pathcost[nextNode]):
                    priority = newCost
                    self.visited[nextNode] = self.currentpos
                    self.pq.put((priority, nextNode))
                    self.path[nextNode] = currentNode
                    self.pathcost[nextNode] = currentCost
        return

    def constructPath(self):
        currentNode = self.dest
        path = []
        while currentNode != self.currentpos:
            path.append(currentNode)
            currentNode = self.path[currentNode]
        path.append(self.currentpos)
        path.reverse()
        return path
