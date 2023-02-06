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
        pass

    def setCurrentPos(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction
    
    def getCurrentPos(self):
        return (self.x, self.y, self.direction)

    def checkDestination(self):
        ''' if current position + 2 cells in direction it is facing == destination, return true? '''
        pass

    def checkForwardRightTurn(self):
        pass

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