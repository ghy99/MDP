import astarclass
import grid
import copy
from queue import PriorityQueue


def createObstacles(gridsize, obstaclesNo, grid):
    obstacles = []
    grid.printgrid(gridsize)
    print("x = row number (1-20), y = column number (1-20), D = Direction (N S E W)")                          # this part is for selecting obstacles. change to passing in obstacles as a parameter
    print(f"Select {obstaclesNo} obstacle positions, separated by space(x y D):")
    for i in range(obstaclesNo):
        x, y, direction = input().split(" ")
        obstacles.append((gridsize - int(x), int(y) - 1, direction)) # start counting from bottom left corner
    print(obstacles)
    
    return obstacles

'''
Example obstacle input
5 5 N
7 9 E
15 5 S
4 17 W
20 20 S
1 20 N

7 3 S
12 4 W
10 10 E
2 12 N
19 19 W
8 15 W

10 1 N
17 3 N
13 15 E
4 18 S
20 20 W
10 10 W

6 1 N
1 6 E
8 8 W
14 2 E
10 20 W
18 13 S
'''



if __name__ == "__main__":
    gridsize = 20
    obstaclesNo = 6
    obstacles = []
    grid = astarclass.Grid(gridsize)                                    # init grid object
    obstacles = createObstacles(gridsize, obstaclesNo, grid)            # init obstacle location in grid object
    # copyObstacles = obstacles.copy()
    copyObstacles = copy.deepcopy(obstacles)
    grid.setObstacles(obstacles, gridsize)
    grid.printgrid(gridsize)
    

    astar = astarclass.Astar((gridsize - 1, 0, "N"), obstacles, grid, gridsize)
    # grid.plotgrid(gridsize, obstacles, astar.currentpos)
    astar.processNeighbours(gridsize)
    # for key, val in astar.edges.items():
    #     print(f"\t\t{key} : {val}\n")
    # astar.filterNeighbours(astar.currentpos)
    

    while(astar.obstacles):
        astar.chooseDest()
        # astar.printObject()
        # print(f"Obstacle {astar.dest}")
        astar.algorithm()
        path = astar.constructPath()
        # path.pop(-1) # remove destination
        # print(f"Path: {path}")
        for cell in range(len(path)):
            # if path[cell][0] == astar.dest[0] and path[cell][1] == astar.dest[1]:
            #     astar.grid.grid[path[cell][0]][path[cell][1]] = -1
            #     continue
            astar.grid.grid[path[cell][0]][path[cell][1]] = 1
        # astar.grid.printgrid(gridsize)
        # print(f"QUEUE: {astar.pq.queue}")
        astar.grid.plotgrid(gridsize, copyObstacles, astar.currentpos, path)
        
        astar.visited.clear()
        # print("\n\n")
        # gotta update currentpos with new destination after
        
        astar.updateNewDest()
        astar.pq.queue.clear()
        astar.path.clear()
        astar.pathcost.clear()
        # print(f"Original obstacles: {obstacles}")
        astar.resetGrid(gridsize, copyObstacles)
        # break
        # input("Enter to continue...")