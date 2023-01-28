from queue import PriorityQueue
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure

'''
[
    [  0 ,  0 ,  0 ,  0 ,  0 , -4 ],
    [  0 ,  0 ,  0 ,  0 ,  0 ,  0 ],
    [  0 ,  0 ,  0 , -2 ,  0 ,  0 ],
    [  0 , -3 ,  0 ,  0 ,  0 ,  0 ],
    [  0 ,  0 ,  0 ,  0 , -1 ,  0 ],
    [  1 ,  0 ,  0 ,  0 ,  0 ,  0 ],
]
^ = starting position, direction it is facing
path that robot can take will only be:
\ (forward diagonal left) 
| (forward), 
/ ( forward diagonal right)

Might not be implemented, still deciding
if direction == '\'
path on matrix will be written as ^ @ (x + 1, y),
followed by < @ (x + 1, y - 1)

else if direction == '|',
path on matrix will be written as ^ @ (x + 1, y)

else if direction =='/',
path on matrix will be written as ^ @ (x + 1, y), 
followed by > @ (x + 1, y + 1)

 1 = Current location in matrix, will be updated with ^ < > v when robot moves

current direction robot is pointing at
^ = 1
> = 2
v = 3
< = 4

-ve numbers = obstacles
-1 = image on North
-2 = image on East
-3 = image on South
-4 = image on West
'''

class Grid:
    def __init__(self, gridsize):
        self.grid = [[0 for i in range(gridsize)] for j in range(gridsize)]
        for i in range(4):
            for j in range(4):
                self.grid[gridsize - 1 - i][j] = -5
        self.grid[gridsize - 1][0] = 1
        

        

    def setObstacles(self, obstacles, gridsize):
        for i in obstacles:
            self.grid[i[0]][i[1]] = -1
            if i[2] == "N":
                try:
                    # if (i[0] > 0):
                    #     self.grid[i[0] - 1][i[1]] = -10     # N
                    if (i[1] < gridsize - 1):
                        self.grid[i[0]][i[1] + 1] = -10     # E
                    if (i[0] < gridsize - 1):
                        self.grid[i[0] + 1][i[1]] = -10     # S
                    if (i[1] > 0):
                        self.grid[i[0]][i[1] - 1] = -10     # W
                    if (i[0] > 0) and (i[1] > 0):                        
                        self.grid[i[0] - 1][i[1] - 1] = -10     # NW
                        self.grid[i[0] - 2][i[1] - 1] = -10
                    if (i[0] > 0) and (i[1] < gridsize - 1):
                        self.grid[i[0] - 1][i[1] + 1] = -10     # NE
                        self.grid[i[0] - 2][i[1] + 1] = -10
                    if (i[0] < gridsize - 1) and (i[1] < gridsize - 1):
                        self.grid[i[0] + 1][i[1] + 1] = -10     # SE
                    if (i[0] < gridsize - 1) and (i[1] > 0):
                        self.grid[i[0] + 1][i[1] - 1] = -10     # SW
                except IndexError:
                    print(f"{i} Out of range!")
            elif i[2] == "E":
                try:
                    if (i[0] > 0):
                        self.grid[i[0] - 1][i[1]] = -10     # N
                    # if (i[1] < gridsize - 1):
                    #     self.grid[i[0]][i[1] + 1] = -10     # E
                    if (i[0] < gridsize - 1):
                        self.grid[i[0] + 1][i[1]] = -10     # S
                    if (i[1] > 0):
                        self.grid[i[0]][i[1] - 1] = -10     # W
                    if (i[0] > 0) and (i[1] > 0):                        
                        self.grid[i[0] - 1][i[1] - 1] = -10     # NW
                    if (i[0] > 0) and (i[1] < gridsize - 1):
                        self.grid[i[0] - 1][i[1] + 1] = -10     # NE
                        self.grid[i[0] - 1][i[1] + 2] = -10
                    if (i[0] < gridsize - 1) and (i[1] < gridsize - 1):
                        self.grid[i[0] + 1][i[1] + 1] = -10     # SE
                        self.grid[i[0] + 1][i[1] + 2] = -10
                    if (i[0] < gridsize - 1) and (i[1] > 0):
                        self.grid[i[0] + 1][i[1] - 1] = -10     # SW
                except IndexError:
                    print(f"{i} Out of range!")
            elif i[2] == "S":
                try:
                    if (i[0] > 0):
                        self.grid[i[0] - 1][i[1]] = -10     # N
                    if (i[1] < gridsize - 1):
                        self.grid[i[0]][i[1] + 1] = -10     # E
                    # if (i[0] < gridsize - 1):
                    #     self.grid[i[0] + 1][i[1]] = -10     # S
                    if (i[1] > 0):
                        self.grid[i[0]][i[1] - 1] = -10     # W
                    if (i[0] > 0) and (i[1] > 0):                        
                        self.grid[i[0] - 1][i[1] - 1] = -10     # NW
                    if (i[0] > 0) and (i[1] < gridsize - 1):
                        self.grid[i[0] - 1][i[1] + 1] = -10     # NE
                    if (i[0] < gridsize - 1) and (i[1] < gridsize - 1):
                        self.grid[i[0] + 1][i[1] + 1] = -10     # SE
                        self.grid[i[0] + 2][i[1] + 1] = -10     # SE
                    if (i[0] < gridsize - 1) and (i[1] > 0):
                        self.grid[i[0] + 1][i[1] - 1] = -10     # SW
                        self.grid[i[0] + 2][i[1] - 1] = -10     # SW
                except IndexError:
                    print(f"{i} Out of range!")
            elif i[2] == "W":
                try:
                    if (i[0] > 0):
                        self.grid[i[0] - 1][i[1]] = -10     # N
                    if (i[1] < gridsize - 1):
                        self.grid[i[0]][i[1] + 1] = -10     # E
                    if (i[0] < gridsize - 1):
                        self.grid[i[0] + 1][i[1]] = -10     # S
                    # if (i[1] > 0):
                    #     self.grid[i[0]][i[1] - 1] = -10     # W
                    if (i[0] > 0) and (i[1] > 0):                        
                        self.grid[i[0] - 1][i[1] - 1] = -10     # NW
                        self.grid[i[0] - 1][i[1] - 2] = -10
                    if (i[0] > 0) and (i[1] < gridsize - 1):
                        self.grid[i[0] - 1][i[1] + 1] = -10     # NE
                    if (i[0] < gridsize - 1) and (i[1] < gridsize - 1):
                        self.grid[i[0] + 1][i[1] + 1] = -10     # SE
                    if (i[0] < gridsize - 1) and (i[1] > 0):
                        self.grid[i[0] + 1][i[1] - 1] = -10     # SW
                        self.grid[i[0] + 1][i[1] - 2] = -10
                except IndexError:
                    print(f"{i} Out of range!")


    def printgrid(self, gridsize):
        for i in range(gridsize):
            for j in range(gridsize):
                print(f"{self.grid[i][j]}", end= " ")
            print("\n")

    

    def plotgrid(self, gridsize, obstacles, currentpos):
        ggrid = np.array(self.grid)
        fig, ax = plt.subplots(figsize=(12, 12))
        plt.gca().invert_yaxis()
        ax.imshow(ggrid)    # matrix gotta be numbers, not ^ < > v
        if currentpos[2] == "N":
            ax.scatter(currentpos[1], currentpos[0], marker="^", color="blue", s=250)
        elif currentpos[2] == "E":
            ax.scatter(currentpos[1], currentpos[0], marker=">", color="blue", s=250)
        elif currentpos[2] == "S":
            ax.scatter(currentpos[1], currentpos[0], marker="v", color="blue", s=250)
        elif currentpos[2] == "W":
            ax.scatter(currentpos[1], currentpos[0], marker="<", color="blue", s=250)
        # ax.scatter(0, gridsize - 1, marker = "o", color = "yellow", s = 250)
        for i in range(len(obstacles)):
            if obstacles[i][2] == "N":
                ax.scatter(obstacles[i][1], obstacles[i][0], marker = "^", color = "red", s = 250)
            elif obstacles[i][2] == "E":
                ax.scatter(obstacles[i][1], obstacles[i][0], marker = ">", color = "red", s = 250)
            elif obstacles[i][2] == "S":
                ax.scatter(obstacles[i][1], obstacles[i][0], marker = "v", color = "red", s = 250)
            elif obstacles[i][2] == "W":
                ax.scatter(obstacles[i][1], obstacles[i][0], marker = "<", color = "red", s = 250)
        plt.show()
            



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
    def __init__(self, initpos, obstacles, grid):
        self.path = {}
        self.pathcost = {}
        self.visited = {}
        self.edges = {}
        self.pq = PriorityQueue()
        self.currentpos = initpos
        self.obstacles = obstacles   # dest is currently a list of tuples of obstacle location
        self.grid = grid

    # returns all edges 
    def allEdges(self):
        return self.edges
    
    # returns current node's edges
    def neighbours(self, node):
        return self.edges[node]

    # create possible paths (1 step) from each node to the next node
    def processNeighbours(self, gridsize):
        for i in range(gridsize):
            for j in range(gridsize):
                # if self.grid.grid[i][j] >= 0:   # more than / equal to 0 cos starting position labeled as 1
                    neighbours = []
                    # Check border available paths
                    # cell above current cell: "N"
                    if (i > 0): #and self.grid.grid[i - 1][j] == 0:
                        neighbours.append(((i - 1, j), 1))
                    # cell right of current cell: "E"
                    if (j < gridsize - 1): #and self.grid.grid[i][j + 1] == 0:
                        neighbours.append(((i, j + 1), 1))
                    # cell below current cell: "S"
                    if (i < gridsize - 1): # and self.grid.grid[i + 1][j] == 0:
                        neighbours.append(((i + 1, j), 1))
                    # cell left of current cell: "W"
                    if (j > 0): # and self.grid.grid[i][j - 1] == 0:
                        neighbours.append(((i, j - 1), 1))
                    # cell NorthWest of current cell: "NW"
                    if (i > 0) and (j > 0): # and self.grid.grid[i - 1][j - 1] == 0:
                        neighbours.append(((i - 1, j - 1), 2))
                    # cell NorthEast of current cell: "NE"
                    if (i > 0) and (j < gridsize - 1): # and self.grid.grid[i - 1][j + 1] == 0:
                        neighbours.append(((i - 1, j + 1), 2))
                    # cell SouthEast of current cell: "SE"
                    if (i < gridsize - 1) and (j < gridsize - 1): # and self.grid.grid[i + 1][j + 1] == 0:
                        neighbours.append(((i + 1, j + 1), 2))
                        # cell SouthWest of current cell: "SW"
                    if (i < gridsize - 1) and (j > 0): # and self.grid.grid[i + 1][j - 1] == 0:
                        neighbours.append(((i + 1, j - 1), 2))
                    # insert edges into object grid
                    self.edges[(i, j)] = neighbours
                    

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

    '''
    11 12 13
    14  1 16
    17 18 19
    '''
    
    
    '''
    Append next cell movement in self.visited to say this cell is explored
    Tuple represents (X-Coordinate +- 1, Y-Coordinate +- 1, Direction it is facing)
    Data Structure is a dictionary, in the form of 
    {
          Possible Path ((x, y, Direction), cost) : Parent Node (x, y, Direction),
    }
    '''

    # basically greedy find shortest distance but not accounting for 1 cell per move
    def heuristic(self, a, b): # a = current position, b = destination position
        # return np.sqrt((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2)
        # print(f"b[0] - a[0]: {b[0] - a[0]}\tb[1] - a[1]: {b[1] - a[1]}")
        return np.abs(b[0] - a[0]) + np.abs(b[1] - a[1])

    # This function finds nearest obstacle and do a* to find shortest path
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


    def chooseDest(self):
        self.dest = self.findDest(self.obstacles)
        # print(f"Obstacle list before: {self.obstacles}")
        self.obstacles.remove(self.dest)
        # print(f"Obstacle list after: {self.obstacles}")


    def updateNewDest(self):
        self.currentpos = self.dest
        # self.chooseDest()


    def filterNeighbours(self, currentNode):
        nb = self.neighbours((currentNode[0], currentNode[1]))
        toBeRemoved = []
        print(f"PRE FILTER possible steps: {nb}")
        for cell in nb:
            # print(f"Current Node: {currentNode}\tCell: {cell}")
            if currentNode[2] == "N" or currentNode[2] == "S":
                # if (currentNode[0] - 1 == cell[0][0]) and (currentNode[1] - 1 == cell[0][1]):
                #     print("NW")
                # elif (currentNode[0] - 1 == cell[0][0]) and (currentNode[1] == cell[0][1]):
                #     print("N")
                # elif (currentNode[0] - 1 == cell[0][0]) and (currentNode[1] + 1 == cell[0][1]):
                #     print("NE")
                if (currentNode[0] == cell[0][0]) and (currentNode[1] + 1 == cell[0][1]):
                    print("E TO BE DELETED")
                    toBeRemoved.append(cell)
                    continue
                # elif (currentNode[0] + 1 == cell[0][0]) and (currentNode[1] + 1 == cell[0][1]):
                #     print("SE")
                # elif (currentNode[0] + 1 == cell[0][0]) and (currentNode[1] == cell[0][1]):
                #     print("S")
                # elif (currentNode[0] + 1 == cell[0][0]) and (currentNode[1] - 1 == cell[0][1]):
                #     print("SW")
                elif (currentNode[0] == cell[0][0]) and (currentNode[1] - 1 == cell[0][1]):
                    print("W TO BE DELETED")
                    toBeRemoved.append(cell)
                    continue
            else:
                # if (currentNode[0] - 1 == cell[0][0]) and (currentNode[1] - 1 == cell[0][1]):
                #     print("NW")
                if (currentNode[0] - 1 == cell[0][0]) and (currentNode[1] == cell[0][1]):
                    print("N TO BE DELETED")
                    toBeRemoved.append(cell)
                    continue
                # elif (currentNode[0] - 1 == cell[0][0]) and (currentNode[1] + 1 == cell[0][1]):
                #     print("NE")
                # elif (currentNode[0] == cell[0][0]) and (currentNode[1] + 1 == cell[0][1]):
                #     print("E")
                # elif (currentNode[0] + 1 == cell[0][0]) and (currentNode[1] + 1 == cell[0][1]):
                #     print("SE")
                elif (currentNode[0] + 1 == cell[0][0]) and (currentNode[1] == cell[0][1]):
                    print("S TO BE DELETED")
                    toBeRemoved.append(cell)
                    continue
                # elif (currentNode[0] + 1 == cell[0][0]) and (currentNode[1] - 1 == cell[0][1]):
                #     print("SW")
                # elif (currentNode[0] == cell[0][0]) and (currentNode[1] - 1 == cell[0][1]):
                #     print("W")
        for i in toBeRemoved:
            nb.remove(i)
        return nb

    def changeCurrentNode(self, currentNode, nextNode):
        print(f"Current: {currentNode}\tNext: {nextNode}")
        direction = None
        if (currentNode[0] - 1 == nextNode[0]) and (currentNode[1] == nextNode[1]):     # N
            if currentNode[2] == "N":
                direction = "N"
            elif currentNode[2] == "S":
                direction = "S"
        if (currentNode[0] == nextNode[0]) and (currentNode[1] + 1 == nextNode[1]):     # E
            if currentNode[2] == "E":
                direction = "E"
            elif currentNode[2] == "W":
                direction = "W"
        if (currentNode[0] + 1 == nextNode[0]) and (currentNode[1] == nextNode[1]):     # S
            if currentNode[2] == "N":
                direction = "N"
            elif currentNode[2] == "S":
                direction = "S"
        if (currentNode[0] == nextNode[0]) and (currentNode[1] - 1 == nextNode[1]):     # W
            if currentNode[2] == "E":
                direction = "E"
            elif currentNode[2] == "W":
                direction = "W"
        if (currentNode[0] - 1 == nextNode[0]) and (currentNode[1] - 1 == nextNode[1]):     # NW
            if currentNode[2] == "N":
                direction = "W"
            elif currentNode[2] == "W":
                direction = "N"
            elif currentNode[2] == "S":
                direction = "E"
            elif currentNode[2] == "E":
                direction = "S"
        if (currentNode[0] - 1 == nextNode[0]) and (currentNode[1] + 1 == nextNode[1]):     # NE
            if currentNode[2] == "N":
                direction = "E"
            elif currentNode[2] == "E":
                direction = "N"
            elif currentNode[2] == "S":
                direction = "W"
            elif currentNode[2] == "W":
                direction = "S"
        if (currentNode[0] + 1 == nextNode[0]) and (currentNode[1] + 1 == nextNode[1]):     # SE
            if currentNode[2] == "S":
                direction = "E"
            elif currentNode[2] == "E":
                direction = "S"
            elif currentNode[2] == "N":
                direction = "W"
            elif currentNode[2] == "W":
                direction = "N"
        if (currentNode[0] + 1 == nextNode[0]) and (currentNode[1] - 1 == nextNode[1]):     # SW
            if currentNode[2] == "S":
                direction = "W"
            elif currentNode[2] == "W":
                direction = "S"
            elif currentNode[2] == "N":
                direction = "E"
            elif currentNode[2] == "E":
                direction = "N"
        if direction == None:
            print(f"NONE ENCOUNTERED!!!!!!!\nCurrent Node: {currentNode}\tNext Node: {nextNode}\tdirection: {direction}\n")
        return (nextNode[0], nextNode[1], direction)

    def resetGrid(self, gridsize, obstacles):
        for i in range(gridsize):
            for j in range(gridsize):
                if self.currentpos[0] == i and self.currentpos[1] == j:
                    self.grid.grid[i][j] = 1
                if i < 4 and j < 4:
                    self.grid.grid[i][j] = -5
                self.grid.grid[i][j] = 0
        self.grid.setObstacles(obstacles, gridsize)


    def algorithm(self):
        self.pq.put((0, self.currentpos))
        
        self.visited[self.currentpos] = None
        self.pathcost[self.currentpos] = 0
        # i am hitting infinite loop here?
        while not self.pq.empty():
            currentNode = self.pq.get()[1]
            # self.grid.grid[currentNode[0]][currentNode[1]] = 1
            if currentNode[0] == self.dest[0] and currentNode[1] == self.dest[1]:
                # self.path[currentNode]
                break
            # print(f"Current Node: {currentNode}")
            # possibleSteps = self.filterNeighbours(currentNode)
            # print(f"POST FILTER possible steps: {possibleSteps}\n")
            print(f"neighbours: {self.neighbours((currentNode[0], currentNode[1]))}")
            for nextNode, weight in self.neighbours((currentNode[0], currentNode[1])):
            # for nextNode, weight in possibleSteps:
                if self.grid.grid[nextNode[0]][nextNode[1]] == 1 or self.grid.grid[nextNode[0]][nextNode[1]] == -10:
                    # print(f"Skipping this node: {nextNode}")
                    # self.grid.printgrid(20)
                    continue
                # print(f"\nPQ: {self.pq.queue}\n")
                print(f"Current Node: {currentNode}\tNext Node: {nextNode}")
                currentCost = weight + self.pathcost[currentNode]
                heuristic = self.heuristic(nextNode, self.dest)
                # print(f"Current node: {currentNode}\tNext node: {nextNode}\tdestination:{self.dest}\theuristics: {heuristic}\n")
                newCost = currentCost + heuristic
                
                if (nextNode not in self.visited) or (currentCost < self.pathcost[nextNode]):
                    priority = newCost
                    # print(f"nextnode: {nextNode}\tweight: {weight}\n")
                    # this part got problem?
                    # print(f"current: {currentNode}\tOld next node: {nextNode}")

                    # nextNode = self.changeCurrentNode(currentNode, nextNode)

                    # node = self.changeCurrentNode(currentNode, nextNode)
                    # print(f"current: {currentNode}\tNew next node: {nextNode}")
                    self.visited[nextNode] = self.currentpos
                    self.pq.put((priority, nextNode))
                    self.path[nextNode] = currentNode
                    self.pathcost[nextNode] = currentCost
            
            # print(f"PRIORITY QUEUE: {self.pq.queue}")
            # print(f"VISITED: {self.visited}\n")
        return

    def constructPath(self):
        currentNode = self.dest
        path = []
        while currentNode != self.currentpos:
            path.append(currentNode)
            currentNode = self.path[(currentNode[0], currentNode[1])]
        path.append(self.currentpos)
        path.reverse()

        # avail = self.availableMoves()
        # print(f"Available path: {avail}")
        # self.expandPossiblePath(avail)
        # print(f"Visited:")
        # for key, val in self.visited.items():
        #     print(f"\t\t{key} : {val}\n")
        return path
