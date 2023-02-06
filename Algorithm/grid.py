import numpy as np
import matplotlib.pyplot as plt
from obstacles import Obstacle
from robot import Robot
# import pygame
import settings

class Grid:
    def __init__(self):
        self.gridsize = settings.GRID_LENGTH // settings.GRID_CELL_LENGTH
        self.obstacles = []
        self.grid = [[0 for i in range(self.gridsize)] for j in range(self.gridsize)]
        # self.obstacles = obstacles
        # for i in range(4):
        #     for j in range(4):
        #         self.grid[gridsize - 1 - i][j] = -5
        # self.grid[gridsize - 1][0] = 1

    def getObstacles(self):
        return self.obstacles

    def setObstacles(self):
        # obstacles = []
        # grid.printgrid(gridsize)
        obstaclesNo = int(input("Enter number of obstacles: "))
        print("x = row number (1-20), y = column number (1-20), D = Direction (N S E W)")                          # this part is for selecting obstacles. change to passing in obstacles as a parameter
        print(f"Select {obstaclesNo} obstacle positions, separated by space (x y D):")
        for i in range(obstaclesNo):
            x, y, direction = input().split(" ")
            # obstacles.append((gridsize - int(x), int(y) - 1, direction)) # start counting from bottom left corner
            obstacle = Obstacle(self.gridsize - int(x), int(y) - 1, direction)
            self.obstacles.append(obstacle)
            # self.obstacles.append((self.gridsize - int(x), int(y) - 1, direction)) # start counting from bottom left corner
            print(self.obstacles[i].printObstacle())
        
        # return obstacles

    ''' filling up the obstacle's boundary in grid'''
    def setObstacleBoundary(self):
        # self.obstacles = obstacles
        for i in self.obstacles:
            coordinates = i.getCoord()
            print(f"coordinates: {coordinates}")
            self.grid[coordinates[0]][coordinates[1]] = -1
            if (coordinates[0] > 0):
                self.grid[coordinates[0] - 1][coordinates[1]] = -10     # N
                # self.grid[coordinates[0] - 2][coordinates[1]] = 10     # N
            if (coordinates[1] < self.gridsize - 1):
                self.grid[coordinates[0]][coordinates[1] + 1] = -10     # E
            if (coordinates[0] < self.gridsize - 1):
                self.grid[coordinates[0] + 1][coordinates[1]] = -10     # S
            if (coordinates[1] > 0):
                self.grid[coordinates[0]][coordinates[1] - 1] = -10     # W
            if (coordinates[0] > 0) and (coordinates[1] > 0):
                self.grid[coordinates[0] - 1][coordinates[1] - 1] = -10     # NW
                # self.grid[coordinates[0] - 2][coordinates[1] - 1] = 10
            if (coordinates[0] > 0) and (coordinates[1] < self.gridsize - 1):
                self.grid[coordinates[0] - 1][coordinates[1] + 1] = -10     # NE
                # self.grid[coordinates[0] - 2][coordinates[1] + 1] = 10
            if (coordinates[0] < self.gridsize - 1) and (coordinates[1] < self.gridsize - 1):
                self.grid[coordinates[0] + 1][coordinates[1] + 1] = -10     # SE
            if (coordinates[0] < self.gridsize - 1) and (coordinates[1] > 0):
                self.grid[coordinates[0] + 1][coordinates[1] - 1] = -10     # SW
            # self.grid[i[0]][i[1]] = -1
            if coordinates[2] == "N":
                try:
                    if (coordinates[0] > 1):
                        # self.grid[coordinates[0] - 1][coordinates[1]] = -10     # N
                        self.grid[coordinates[0] - 2][coordinates[1]] = 10     # N
                    # if (coordinates[1] < self.gridsize - 1):
                    #     self.grid[coordinates[0]][coordinates[1] + 1] = -10     # E
                    # if (coordinates[0] < self.gridsize - 1):
                    #     self.grid[coordinates[0] + 1][coordinates[1]] = -10     # S
                    # if (coordinates[1] > 0):
                    #     self.grid[coordinates[0]][coordinates[1] - 1] = -10     # W
                    if (coordinates[0] > 1) and (coordinates[1] > 0):
                        # self.grid[coordinates[0] - 1][coordinates[1] - 1] = -10     # NW
                        self.grid[coordinates[0] - 2][coordinates[1] - 1] = 10
                    if (coordinates[0] > 1) and (coordinates[1] < self.gridsize - 1):
                        # self.grid[coordinates[0] - 1][coordinates[1] + 1] = -10     # NE
                        self.grid[coordinates[0] - 2][coordinates[1] + 1] = 10
                    # if (coordinates[0] < self.gridsize - 1) and (coordinates[1] < self.gridsize - 1):
                    #     self.grid[coordinates[0] + 1][coordinates[1] + 1] = -10     # SE
                    # if (coordinates[0] < self.gridsize - 1) and (coordinates[1] > 0):
                    #     self.grid[coordinates[0] + 1][coordinates[1] - 1] = -10     # SW
                except IndexError:
                    print(f"{i} Out of range!")
            elif coordinates[2] == "E":
                try:
                    # if (coordinates[0] > 0):
                    #     self.grid[coordinates[0] - 1][coordinates[1]] = -10     # N
                    if (coordinates[1] < self.gridsize - 2):
                        self.grid[coordinates[0]][coordinates[1] + 2] = 10     # E
                    # if (coordinates[0] < self.gridsize - 1):
                    #     self.grid[coordinates[0] + 1][coordinates[1]] = -10     # S
                    # if (coordinates[1] > 0):
                    #     self.grid[coordinates[0]][coordinates[1] - 1] = -10     # W
                    # if (coordinates[0] > 0) and (coordinates[1] > 0):
                    #     self.grid[coordinates[0] - 1][coordinates[1] - 1] = -10     # NW
                    if (coordinates[0] > 0) and (coordinates[1] < self.gridsize - 2):
                        # self.grid[coordinates[0] - 1][coordinates[1] + 1] = -10     # NE
                        self.grid[coordinates[0] - 1][coordinates[1] + 2] = 10
                    if (coordinates[0] < self.gridsize - 1) and (coordinates[1] < self.gridsize - 2):
                        # self.grid[coordinates[0] + 1][coordinates[1] + 1] = -10     # SE
                        self.grid[coordinates[0] + 1][coordinates[1] + 2] = 10
                    # if (coordinates[0] < self.gridsize - 1) and (coordinates[1] > 0):
                    #     self.grid[coordinates[0] + 1][coordinates[1] - 1] = -10     # SW
                except IndexError:
                    print(f"{i} Out of range!")
            elif coordinates[2] == "S":
                try:
                    # if (coordinates[0] > 0):
                    #     self.grid[coordinates[0] - 1][coordinates[1]] = -10     # N
                    # if (coordinates[1] < self.gridsize - 1):
                    #     self.grid[coordinates[0]][coordinates[1] + 1] = -10     # E
                    if (coordinates[0] < self.gridsize - 2):
                        self.grid[coordinates[0] + 2][coordinates[1]] = 10     # S
                    # if (coordinates[1] > 0):
                    #     self.grid[coordinates[0]][coordinates[1] - 1] = -10     # W
                    # if (coordinates[0] > 0) and (coordinates[1] > 0):
                    #     self.grid[coordinates[0] - 1][coordinates[1] - 1] = -10     # NW
                    # if (coordinates[0] > 0) and (coordinates[1] < self.gridsize - 1):
                    #     self.grid[coordinates[0] - 1][coordinates[1] + 1] = -10     # NE
                    if (coordinates[0] < self.gridsize - 2) and (coordinates[1] < self.gridsize - 1):
                        # self.grid[coordinates[0] + 1][coordinates[1] + 1] = -10     # SE
                        self.grid[coordinates[0] + 2][coordinates[1] + 1] = 10     # SE
                    if (coordinates[0] < self.gridsize - 1) and (coordinates[1] > 0):
                        # self.grid[coordinates[0] + 1][coordinates[1] - 1] = -10     # SW
                        self.grid[coordinates[0] + 2][coordinates[1] - 1] = 10     # SW
                except IndexError:
                    print(f"{i} Out of range!")
            elif coordinates[2] == "W":
                try:
                    # if (coordinates[0] > 0):
                    #     self.grid[coordinates[0] - 1][coordinates[1]] = -10     # N
                    # if (coordinates[1] < self.gridsize - 1):
                    #     self.grid[coordinates[0]][coordinates[1] + 1] = -10     # E
                    # if (coordinates[0] < self.gridsize - 1):
                    #     self.grid[coordinates[0] + 1][coordinates[1]] = -10     # S
                    if (coordinates[1] > 1):
                        self.grid[coordinates[0]][coordinates[1] - 2] = 10     # W
                    if (coordinates[0] > 0) and (coordinates[1] > 1):
                        # self.grid[coordinates[0] - 1][coordinates[1] - 1] = -10     # NW
                        self.grid[coordinates[0] - 1][coordinates[1] - 2] = 10
                    # if (coordinates[0] > 0) and (coordinates[1] < self.gridsize - 1):
                    #     self.grid[coordinates[0] - 1][coordinates[1] + 1] = -10     # NE
                    # if (coordinates[0] < self.gridsize - 1) and (coordinates[1] < self.gridsize - 1):
                    #     self.grid[coordinates[0] + 1][coordinates[1] + 1] = -10     # SE
                    if (coordinates[0] < self.gridsize - 1) and (coordinates[1] > 1):
                        # self.grid[coordinates[0] + 1][coordinates[1] - 1] = -10     # SW
                        self.grid[coordinates[0] + 1][coordinates[1] - 2] = 10
                except IndexError:
                    print(f"{i} Out of range!")

    def reset(self):
        self.grid = [[0 for i in range(self.gridsize)] for j in range(self.gridsize)]
        if len(self.obstacles) != 0:
            self.setObstacleBoundary()

    def plotRobot(self, robot):
        '''
        Get robot current pos
        plot 3x3 grid for robot
        '''

    def checkValidMove(self, robot, direction):
        '''
        Get robot current pos, check if the direction the robot is turning has collision with obstacle / grid boundary
        '''

    def printgrid(self, gridsize):
        for i in range(gridsize):
            for j in range(gridsize):
                print(f"{self.grid[i][j]}", end=" ")
            print("\n")

    ''' Plotting path taken on grid using matplotlib '''
    # def plotgrid(self, currentpos, path):
    def plotgrid(self):
        ggrid = np.array(self.grid)
        fig, ax = plt.subplots(figsize=(11, 11))
        plt.gca().invert_yaxis()
        ax.imshow(ggrid)    # matrix gotta be numbers, not ^ < > v
        for i in range(len(self.obstacles)):
            self.obstacles[i].getCoord()
            if self.obstacles[i].getCoord()[2] == "N":
                ax.scatter(self.obstacles[i].getCoord()[1], self.obstacles[i].getCoord()
                           [0], marker="^", color="red", s=250)
            elif self.obstacles[i].getCoord()[2] == "E":
                ax.scatter(self.obstacles[i].getCoord()[1], self.obstacles[i].getCoord()
                           [0], marker=">", color="red", s=250)
            elif self.obstacles[i].getCoord()[2] == "S":
                ax.scatter(self.obstacles[i].getCoord()[1], self.obstacles[i].getCoord()
                           [0], marker="v", color="red", s=250)
            elif self.obstacles[i].getCoord()[2] == "W":
                ax.scatter(self.obstacles[i].getCoord()[1], self.obstacles[i].getCoord()
                           [0], marker="<", color="red", s=250)
        # if currentpos[2] == "N":
        #     ax.scatter(currentpos[1], currentpos[0],
        #                marker="^", color="blue", s=250)
        # elif currentpos[2] == "E":
        #     ax.scatter(currentpos[1], currentpos[0],
        #                marker=">", color="blue", s=250)
        # elif currentpos[2] == "S":
        #     ax.scatter(currentpos[1], currentpos[0],
        #                marker="v", color="blue", s=250)
        # elif currentpos[2] == "W":
        #     ax.scatter(currentpos[1], currentpos[0],
        #                marker="<", color="blue", s=250)
        # ax.scatter(0, gridsize - 1, marker = "o", color = "yellow", s = 250)

        # for i in range(len(path)):
        #     if path[i][2] == "N":
        #         ax.scatter(path[i][1], path[i][0],
        #                    marker="^", color="blue", s=250)
        #     elif path[i][2] == "E":
        #         ax.scatter(path[i][1], path[i][0],
        #                    marker=">", color="blue", s=250)
        #     elif path[i][2] == "S":
        #         ax.scatter(path[i][1], path[i][0],
        #                    marker="v", color="blue", s=250)
        #     elif path[i][2] == "W":
        #         ax.scatter(path[i][1], path[i][0],
        #                    marker="<", color="blue", s=250)
        plt.show()
