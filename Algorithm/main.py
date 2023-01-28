import astarclass
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
'''



if __name__ == "__main__":
    gridsize = 20
    obstaclesNo = 5
    obstacles = []
    grid = astarclass.Grid(gridsize)                                    # init grid object
    obstacles = createObstacles(gridsize, obstaclesNo, grid)            # init obstacle location in grid object
    # copyObstacles = obstacles.copy()
    copyObstacles = copy.deepcopy(obstacles)
    grid.setObstacles(obstacles, gridsize)
    grid.printgrid(gridsize)
    

    astar = astarclass.Astar((gridsize - 1, 0, "N"), obstacles, grid)
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
        print(f"Path: {path}")
        for cell in range(len(path)):
            # print(f"cell: {cell}")
            try:
                path[cell + 1] = astar.changeCurrentNode(path[cell], path[cell + 1])
            except IndexError:
                print(f"LAST CELL? {cell} : {len(path)}")
            if path[cell][0] == astar.dest[0] and path[cell][1] == astar.dest[1]:
                astar.grid.grid[path[cell][0]][path[cell][1]] = -1
                continue
            astar.grid.grid[path[cell][0]][path[cell][1]] = 1
        astar.grid.printgrid(gridsize)
        astar.grid.plotgrid(gridsize, copyObstacles, astar.currentpos)
        
        astar.visited.clear()
        # print("\n\n")
        # gotta update currentpos with new destination after
        astar.updateNewDest()
        astar.pq.queue.clear()
        astar.visited.clear()
        # print(f"Original obstacles: {obstacles}")
        astar.resetGrid(gridsize, copyObstacles)
        # break