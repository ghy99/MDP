from grid import Grid
from astarclass import Astar
# import settings
# import copy

class Robot:
    '''
    x, y = Center coordinate of robot, initialise starting position to (1, 1)
    direction = Current direction robot is facing
    Robot will be a 3x3 grid cell
    1 1 1
    1 1 1
    1 1 1
    '''
    def __init__(self):
        self.setCurrentPos(18, 1, 'N')
        self.initGrid()


    def initGrid(self):
        self.grid = Grid()
        self.grid.setObstacles(2)
        self.grid.setObstacleBoundary()
        self.grid.plotRobot(self.getCurrentPos())
        self.grid.printgrid()
        # self.grid.plotgrid(self.getCurrentPos(), [])
        

    def setCurrentPos(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction
    
    def getCurrentPos(self):
        return (self.x, self.y, self.direction)

    def checkDestination(self):
        ''' if current position + 2 cells in direction it is facing == destination, return true? '''
        pass

    ''' Run A* Algo'''
    # def runAlgo(self, obstacles):
    def callAlgo(self):
        self.algo.runAlgo(self.grid.getObstacles())

    def checkForwardRightTurn(self):
        if self.direction == 'N':
            
            pass
        elif self.direction == 'E':
            pass
        elif self.direction == 'S':
            pass
        elif self.direction == 'W':
            pass
        pass

    def plotGrid(self):
        self.grid.plotRobot(self.getCurrentPos())

    def forwardRightTurn(self):
        pass

    def checkForwardLeftTurn(self):
        pass

    def forwardLeftTurn(self):
        pass

    def checkReverseRightTurn(self):
        pass

    def reverseRightTurn(self):
        pass

    def checkReverseLeftTurn(self):
        pass

    def reverseLeftTurn(self):
        pass