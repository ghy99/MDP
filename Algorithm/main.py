import astarclass
from grid import Grid
from simulation import Simulation

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
    print(f"Select {obstaclesNo} obstacle positions, separated by space(x y D):")
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


''' Run A* Algo'''
def runAlgo(grid, obstacles):
    gridsize = settings.GRID_LENGTH // settings.GRID_CELL_LENGTH
    copyObstacles = copy.deepcopy(obstacles)
    astar = astarclass.Astar(settings.INITPOS, obstacles, grid, gridsize)
    astar.processNeighbours(gridsize)
    while(astar.obstacles):
        astar.chooseDest()
        astar.algorithm()
        path = astar.constructPath()
        for cell in range(len(path)):
            astar.grid.grid[path[cell][0]][path[cell][1]] = 1
        astar.grid.plotgrid(gridsize, copyObstacles, astar.currentpos, path)
        
        astar.visited.clear()
        astar.updateNewDest()
        astar.pq.queue.clear()
        astar.path.clear()
        astar.pathcost.clear()
        astar.resetGrid(gridsize, copyObstacles)
'''
Example obstacle input
6
5 5 N
7 9 E
15 5 S
4 17 W
20 20 S
1 20 N

6
7 3 S
12 4 W
10 10 E
2 12 N
19 19 W
8 15 W

6
10 1 N
17 3 N
13 15 E
4 18 S
20 20 W
10 10 W

6
6 1 N
1 6 E
8 8 W
14 2 E
10 20 W
18 13 S
'''


if __name__ == "__main__":
    # grid, obstacles = initGrid()
    # runAlgo(grid, obstacles)
    sim = Simulation()
    # sim.drawGrid()
    sim.runSimulation()
    ''' idk why the simulation not running LOL '''
    