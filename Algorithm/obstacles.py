class Obstacle:
    def __init__(self):
        self.gridValue = -1

    def __init__(self, x, y, direction):
        self.gridValue = -1
        self.x = x
        self.y = y
        self.direction = direction
    
    def getCoord(self):
        return (self.x, self.y, self.direction)

    def setCoord(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction

    def printObstacle(self):
        return (self.x, self.y, self.direction)
