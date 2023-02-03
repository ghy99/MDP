import numpy as np
import matplotlib.pyplot as plt
import pygame
import settings

class Grid:
    def __init__(self, gridsize, obstacles):
        gridsize = settings.GRID_LENGTH // settings.GRID_CELL_LENGTH
        self.obstacles = obstacles
        self.grid = [[0 for i in range(gridsize)] for j in range(gridsize)]
        for i in range(4):
            for j in range(4):
                self.grid[gridsize - 1 - i][j] = -5
        self.grid[gridsize - 1][0] = 1

    ''' filling up the obstacle's grid cell in matrix'''
    def setObstacles(self, obstacles, gridsize):
        self.obstacles = obstacles
        for i in obstacles:
            self.grid[i[0]][i[1]] = -1
            if i[2] == "N":
                try:
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
                print(f"{self.grid[i][j]}", end=" ")
            print("\n")

    ''' Plotting path taken on grid using matplotlib '''
    def plotgrid(self, gridsize, obstacles, currentpos, path):
        ggrid = np.array(self.grid)
        fig, ax = plt.subplots(figsize=(11, 11))
        plt.gca().invert_yaxis()
        ax.imshow(ggrid)    # matrix gotta be numbers, not ^ < > v
        if currentpos[2] == "N":
            ax.scatter(currentpos[1], currentpos[0],
                       marker="^", color="blue", s=250)
        elif currentpos[2] == "E":
            ax.scatter(currentpos[1], currentpos[0],
                       marker=">", color="blue", s=250)
        elif currentpos[2] == "S":
            ax.scatter(currentpos[1], currentpos[0],
                       marker="v", color="blue", s=250)
        elif currentpos[2] == "W":
            ax.scatter(currentpos[1], currentpos[0],
                       marker="<", color="blue", s=250)
        # ax.scatter(0, gridsize - 1, marker = "o", color = "yellow", s = 250)
        for i in range(len(obstacles)):
            if obstacles[i][2] == "N":
                ax.scatter(obstacles[i][1], obstacles[i]
                           [0], marker="^", color="red", s=250)
            elif obstacles[i][2] == "E":
                ax.scatter(obstacles[i][1], obstacles[i]
                           [0], marker=">", color="red", s=250)
            elif obstacles[i][2] == "S":
                ax.scatter(obstacles[i][1], obstacles[i]
                           [0], marker="v", color="red", s=250)
            elif obstacles[i][2] == "W":
                ax.scatter(obstacles[i][1], obstacles[i]
                           [0], marker="<", color="red", s=250)
        for i in range(len(path)):
            if path[i][2] == "N":
                ax.scatter(path[i][1], path[i][0],
                           marker="^", color="blue", s=250)
            elif path[i][2] == "E":
                ax.scatter(path[i][1], path[i][0],
                           marker=">", color="blue", s=250)
            elif path[i][2] == "S":
                ax.scatter(path[i][1], path[i][0],
                           marker="v", color="blue", s=250)
            elif path[i][2] == "W":
                ax.scatter(path[i][1], path[i][0],
                           marker="<", color="blue", s=250)
        plt.show()