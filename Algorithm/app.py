import astarclass
from grid import Grid

import settings
import copy
import pygame
import sys

''' Call simulation.py to init pygame simulation HAVENT DO YET '''
def simAlgo():
    pygame.init()
    clock = pygame.time.Clock()
    # screen = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
    screen = pygame.display.set_mode((600, 600), pygame.HWSURFACE | pygame.DOUBLEBUF)
    bg = pygame.image.load(os.path.join("./images/", "white.png"))
    pygame.mouse.set_visible(0)
    pygame.display.set_caption("Vroom Vroom Simulation")
    while True:
        clock.tick(60)
        screen.blit(bg, (0, 0)) # copy background image onto canvas in display
        x, y = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        pygame.display.update()

''' Get Obstacle coordinate & direction through input '''
def createObstacles(gridsize):
    obstacles = []
    # grid.printgrid(gridsize)
    obstaclesNo = int(input("Enter number of obstacles: "))
    print("x = row number (1-20), y = column number (1-20), D = Direction (N S E W)")                          # this part is for selecting obstacles. change to passing in obstacles as a parameter
    print(f"Select {obstaclesNo} obstacle positions, separated by space (x y D):")
    for i in range(obstaclesNo):
        x, y, direction = input().split(" ")
        obstacles.append((gridsize - int(x), int(y) - 1, direction)) # start counting from bottom left corner
    print(obstacles)
    return obstacles

''' create grid object and list of obstacles '''
def initGrid():
    gridsize = settings.GRID_LENGTH // settings.GRID_CELL_LENGTH
    obstacles = createObstacles(gridsize)           # init obstacle location in grid object
    grid = Grid(gridsize, obstacles)                           # init grid object
    
    grid.printgrid(gridsize)                         
    
    grid.setObstacles(obstacles, gridsize)
    grid.printgrid(gridsize)
    return grid, obstacles


