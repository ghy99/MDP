import pygame
import sys
from copy import deepcopy
import constants
# import app
from Misc.direction import Direction


class Simulation():
    def __init__(self):
        pygame.init()
        self.running = True
        # window size = 800, 650
        self.obstacles = []
        self.font = pygame.font.SysFont('Arial', 25)
        self.screen = pygame.display.set_mode(
            (800, 650), pygame.HWSURFACE | pygame.DOUBLEBUF)
        self.clock = None
        pygame.mouse.set_visible(1)
        pygame.display.set_caption("Vroom Vroom Simulation")
        self.screen.fill(constants.BLACK)

    def reset(cls, bot):
        cls.screen.fill(constants.BLACK)
        currentPosX = bot.get_current_pos().x
        currentPosY = bot.get_current_pos().y
        direction = bot.get_current_pos().direction
        currentPos = ((constants.GRID_LENGTH - constants.GRID_CELL_LENGTH -
                      currentPosX) // 10, currentPosY // 10, direction)
        cls.bot.setCurrentPos(currentPos[0], currentPos[1], currentPos[2])
        cls.obstacles.clear()

    ''' Get Obstacle coordinate & direction through input '''
    def createObstacles(gridsize):
        obstacles = []
        # grid.printgrid(gridsize)
        obstaclesNo = int(input("Enter number of obstacles: "))
        # this part is for selecting obstacles. change to passing in obstacles as a parameter
        print("x = row number (1-20), y = column number (1-20), D = Direction (N S E W)")
        print(
            f"Select {obstaclesNo} obstacle positions, separated by space (x y D):")
        for i in range(obstaclesNo):
            x, y, direction = input().split(" ")
            # start counting from bottom left corner
            obstacles.append((gridsize - int(x), int(y) - 1, direction))
        print(obstacles)
        return obstacles

    def selectObstacles(cls, y, x, cellSize, color):
        newRect = pygame.Rect(y * cellSize, x * cellSize, cellSize, cellSize)
        cls.screen.fill(color, newRect)
        pygame.draw.rect(cls.screen, color, newRect, 2)

    def drawRobot(cls, robotPos, cellSize, directionColor, botColor, botAreaColor):
        # print(robotPos)
        for x in range(robotPos[0] - 1, robotPos[0] + 2):
            for y in range(robotPos[1] - 1, robotPos[1] + 2):
                if (0 <= x * cellSize < constants.GRID_LENGTH * constants.SCALING_FACTOR) and (0 <= y * cellSize < constants.GRID_LENGTH * constants.SCALING_FACTOR):
                    if robotPos[0] == x and robotPos[1] == y:
                        cls.selectObstacles(
                            robotPos[1], robotPos[0], cellSize, botColor)
                        if robotPos[2] == Direction.TOP:
                            imageSide = pygame.Rect(
                                robotPos[1] * cellSize, robotPos[0] * cellSize, cellSize, 5)
                            cls.screen.fill(directionColor, imageSide)
                            pygame.draw.rect(
                                cls.screen, directionColor, imageSide, 5)
                        elif robotPos[2] == Direction.RIGHT:
                            imageSide = pygame.Rect(
                                (robotPos[1] * cellSize) + cellSize - 5, (robotPos[0] * cellSize), 5, cellSize)
                            cls.screen.fill(directionColor, imageSide)
                            pygame.draw.rect(
                                cls.screen, directionColor, imageSide, 5)
                        elif robotPos[2] == Direction.BOTTOM:
                            imageSide = pygame.Rect(
                                robotPos[1] * cellSize, (robotPos[0] * cellSize) + cellSize - 5, cellSize, 5)
                            cls.screen.fill(directionColor, imageSide)
                            pygame.draw.rect(
                                cls.screen, directionColor, imageSide, 5)
                        elif robotPos[2] == Direction.LEFT:
                            imageSide = pygame.Rect(
                                robotPos[1] * cellSize, robotPos[0] * cellSize, 5, cellSize)
                            cls.screen.fill(directionColor, imageSide)
                            pygame.draw.rect(
                                cls.screen, directionColor, imageSide, 5)
                    else:
                        rect = pygame.Rect(
                            y * cellSize, x * cellSize, cellSize, cellSize)
                        cls.screen.fill(botAreaColor, rect)
                        pygame.draw.rect(cls.screen, botAreaColor, rect, 1)

    def drawGrid(cls):
        for x in range(0, constants.GRID_LENGTH * constants.SCALING_FACTOR, constants.GRID_CELL_LENGTH * constants.SCALING_FACTOR):
            for y in range(0, constants.GRID_LENGTH * constants.SCALING_FACTOR, constants.GRID_CELL_LENGTH * constants.SCALING_FACTOR):
                rect = pygame.Rect(y, x, constants.GRID_CELL_LENGTH * constants.SCALING_FACTOR,
                                   constants.GRID_CELL_LENGTH * constants.SCALING_FACTOR)
                pygame.draw.rect(cls.screen, constants.WHITE, rect, 2)

    ''' How to add texts?? '''
    def drawButtons(cls, xpos, ypos, bgcolor, text, textColor, length, width):
        startButton = pygame.Rect(xpos, ypos, length, width)
        pygame.draw.rect(cls.screen, bgcolor, startButton)
        text = cls.font.render(text, True, textColor)
        cls.screen.blit(text, text.get_rect(
            center=(startButton.x + (length//2), startButton.y + (width//2))))

    def drawImage(cls, image, xpos, ypos, bgcolor, length, width):
        rect = image.get_rect()
        rect.center = (xpos + (length // 2), ypos + (width // 2))
        cls.screen.blit(image, rect)

    def drawObstaclesButton(cls, obstacles, color):
        size = constants.GRID_CELL_LENGTH * constants.SCALING_FACTOR
        turningSize = ((constants.GRID_CELL_LENGTH *
                       constants.SCALING_FACTOR * 3) + 10) // 4
        # self.selectObstacles(x // (10 * 3), y // ( 10 * 3),
        # constants.GRID_CELL_LENGTH * constants.SCALING_FACTOR,
        # constants.GREY)
        for i in obstacles:
            x = (constants.GRID_LENGTH - constants.GRID_CELL_LENGTH -
                 i.position.x) // constants.GRID_CELL_LENGTH
            y = (i.position.y - constants.GRID_CELL_LENGTH) // constants.GRID_CELL_LENGTH
            direction = i.position.direction
            # print(f"obstacle coordinates: {i.position.x, i.position.y, i.position.direction}")
            cls.selectObstacles(
                y, x, constants.GRID_CELL_LENGTH * constants.SCALING_FACTOR, constants.YELLOW)
            # cls.selectObstacles(i[1], i[0], constants.GRID_CELL_LENGTH * constants.SCALING_FACTOR, constants.YELLOW)
            # if i[2] == 'N':
            if direction == Direction.TOP:
                # imageSide = pygame.Rect(i[1] * size, i[0] * size, size, 5)
                imageSide = pygame.Rect(y * size, x * size, size, 5)
                cls.screen.fill(color, imageSide)
                pygame.draw.rect(cls.screen, color, imageSide, 5)
            # elif i[2] == 'E':
            elif direction == Direction.RIGHT:
                # imageSide = pygame.Rect((i[1] * size) + size - 5, (i[0] * size), 5, size)
                imageSide = pygame.Rect(
                    (y * size) + size - 5, (x * size), 5, size)
                cls.screen.fill(color, imageSide)
                pygame.draw.rect(cls.screen, color, imageSide, 5)
            # elif i[2] == 'S':
            elif direction == Direction.BOTTOM:
                # imageSide = pygame.Rect(i[1] * size, (i[0] * size) + size - 5, size, 5)
                imageSide = pygame.Rect(
                    y * size, (x * size) + size - 5, size, 5)
                cls.screen.fill(color, imageSide)
                pygame.draw.rect(cls.screen, color, imageSide, 5)
            # elif i[2] == 'W':
            elif direction == Direction.LEFT:
                # imageSide = pygame.Rect(i[1] * size, i[0] * size, 5, size)
                imageSide = pygame.Rect(y * size, x * size, 5, size)
                cls.screen.fill(color, imageSide)
                pygame.draw.rect(cls.screen, color, imageSide, 5)

        img = pygame.image.load("images/MoveForward.png").convert()
        cls.drawImage(img, 685, 110, constants.GREY,
                      size, size)       # Forward N
        img = pygame.image.load("images/MoveBackward.png").convert()
        cls.drawImage(img, 685, 180, constants.GREY,
                      size, size)       # Backward S

        img = pygame.image.load("images/TurnForwardRight.png").convert()
        cls.drawImage(img, 720, 132.5, constants.GREY,
                      size, size)       # Forward E
        img = pygame.image.load("images/TurnForwardLeft.png").convert()
        cls.drawImage(img, 650, 132.5, constants.GREY,
                      size, size)       # Forward W
        img = pygame.image.load("images/TurnReverseRight.png").convert()
        cls.drawImage(img, 720, 160, constants.GREY,
                      size, size)       # Backward E
        img = pygame.image.load("images/TurnReverseLeft.png").convert()
        cls.drawImage(img, 650, 160, constants.GREY,
                      size, size)       # Backward W

        img = pygame.image.load("images/slantForwardRight.png").convert()
        cls.drawImage(img, 720, 107.5, constants.GREY,
                      size, size)       # Slant Forward E
        img = pygame.image.load("images/slantForwardLeft.png").convert()
        cls.drawImage(img, 650, 107.5, constants.GREY,
                      size, size)       # Slant Forward W
        img = pygame.image.load("images/slantBackwardsRight.png").convert()
        cls.drawImage(img, 720, 182.5, constants.GREY,
                      size, size)       # Slant Backward E
        img = pygame.image.load("images/slantBackwardsLeft.png").convert()
        cls.drawImage(img, 650, 182.5, constants.GREY,
                      size, size)       # Slant Backward W

    def moveForward(self, currentPos, gridSize, cellSize):
        steps = 1
        if currentPos[2] == Direction.TOP:
            for y in range(currentPos[1] - 1, currentPos[1] + 2):
                for obstacle in self.obstacles:
                    i = (constants.GRID_LENGTH - constants.GRID_CELL_LENGTH -
                         obstacle.position.x) // constants.GRID_CELL_LENGTH
                    j = (obstacle.position.y -
                         constants.GRID_CELL_LENGTH) // constants.GRID_CELL_LENGTH
                    if (currentPos[0] - 2 == i) and (y == j):
                        print(f"COLLISION!")
                        return
            if (0 <= (currentPos[0] - steps) * cellSize < gridSize) and (0 <= currentPos[1] * cellSize < gridSize):
                self.drawRobot(currentPos, cellSize, constants.GREEN,
                               constants.GREEN, constants.GREEN)
                self.bot.setCurrentPos(
                    currentPos[0] - steps, currentPos[1], currentPos[2])
        elif currentPos[2] == Direction.RIGHT:
            for x in range(currentPos[0] - 1, currentPos[0] + 2):
                for obstacle in self.obstacles:
                    i = (constants.GRID_LENGTH - constants.GRID_CELL_LENGTH -
                         obstacle.position.x) // constants.GRID_CELL_LENGTH
                    j = (obstacle.position.y -
                         constants.GRID_CELL_LENGTH) // constants.GRID_CELL_LENGTH
                    if (x == i) and (currentPos[1] + 2 == j):
                        print(f"COLLISION!")
                        return
            if (0 <= currentPos[0] * cellSize < gridSize) and (0 <= (currentPos[1] + steps) * cellSize < gridSize):
                self.drawRobot(currentPos, cellSize,
                               constants.GREEN, constants.GREEN, constants.GREEN)
                self.bot.setCurrentPos(
                    currentPos[0], currentPos[1] + steps, currentPos[2])
        elif currentPos[2] == Direction.BOTTOM:
            for y in range(currentPos[1] - 1, currentPos[1] + 2):
                for obstacle in self.obstacles:
                    i = (constants.GRID_LENGTH - constants.GRID_CELL_LENGTH -
                         obstacle.position.x) // constants.GRID_CELL_LENGTH
                    j = (obstacle.position.y -
                         constants.GRID_CELL_LENGTH) // constants.GRID_CELL_LENGTH
                    if (currentPos[0] + 2 == i) and (y == j):
                        print(f"COLLISION!")
                        return
            if (0 <= (currentPos[0] + steps) * cellSize < gridSize) and (0 <= currentPos[1] * cellSize < gridSize):
                self.drawRobot(currentPos, cellSize, constants.GREEN,
                               constants.GREEN, constants.GREEN)
                self.bot.setCurrentPos(
                    currentPos[0] + steps, currentPos[1], currentPos[2])
        elif currentPos[2] == Direction.LEFT:
            for x in range(currentPos[0] - 1, currentPos[0] + 2):
                for obstacle in self.obstacles:
                    i = (constants.GRID_LENGTH - constants.GRID_CELL_LENGTH -
                         obstacle.position.x) // constants.GRID_CELL_LENGTH
                    j = (obstacle.position.y -
                         constants.GRID_CELL_LENGTH) // constants.GRID_CELL_LENGTH
                    if (x == i) and (currentPos[1] - 2 == j):
                        print(f"COLLISION!")
                        return
            if (0 <= currentPos[0] * cellSize < gridSize) and (0 <= (currentPos[1] - steps) * cellSize < gridSize):
                self.drawRobot(currentPos, cellSize, constants.GREEN,
                               constants.GREEN, constants.GREEN)
                self.bot.setCurrentPos(
                    currentPos[0], currentPos[1] - steps, currentPos[2])

    def moveBackward(self, currentPos, gridSize, cellSize):
        steps = 1
        if currentPos[2] == Direction.TOP:
            for y in range(currentPos[1] - 1, currentPos[1] + 2):
                for obstacle in self.obstacles:
                    i = (constants.GRID_LENGTH - constants.GRID_CELL_LENGTH -
                         obstacle.position.x) // constants.GRID_CELL_LENGTH
                    j = (obstacle.position.y -
                         constants.GRID_CELL_LENGTH) // constants.GRID_CELL_LENGTH
                    if (currentPos[0] + 2 == i) and (y == j):
                        print(f"COLLISION!")
                        return
            if (0 <= (currentPos[0] + steps) * cellSize < gridSize) and (0 <= currentPos[1] * cellSize < gridSize):
                self.drawRobot(currentPos, cellSize, constants.GREEN,
                               constants.GREEN, constants.GREEN)
                self.bot.setCurrentPos(
                    currentPos[0] + steps, currentPos[1], currentPos[2])
        elif currentPos[2] == Direction.RIGHT:
            for x in range(currentPos[0] - 1, currentPos[0] + 2):
                for obstacle in self.obstacles:
                    i = (constants.GRID_LENGTH - constants.GRID_CELL_LENGTH -
                         obstacle.position.x) // constants.GRID_CELL_LENGTH
                    j = (obstacle.position.y -
                         constants.GRID_CELL_LENGTH) // constants.GRID_CELL_LENGTH
                    if (x == i) and (currentPos[1] - 2 == j):
                        print(f"COLLISION!")
                        return
            if (0 <= currentPos[0] * cellSize < gridSize) and (0 <= (currentPos[1] - steps) * cellSize < gridSize):
                self.drawRobot(currentPos, cellSize, constants.GREEN,
                               constants.GREEN, constants.GREEN)
                self.bot.setCurrentPos(
                    currentPos[0], currentPos[1] - steps, currentPos[2])
        elif currentPos[2] == Direction.BOTTOM:
            for y in range(currentPos[1] - 1, currentPos[1] + 2):
                for obstacle in self.obstacles:
                    i = (constants.GRID_LENGTH - constants.GRID_CELL_LENGTH -
                         obstacle.position.x) // constants.GRID_CELL_LENGTH
                    j = (obstacle.position.y -
                         constants.GRID_CELL_LENGTH) // constants.GRID_CELL_LENGTH
                    if (currentPos[0] - 2 == i) and (y == j):
                        print(f"COLLISION!")
                        return
            if (0 <= (currentPos[0] - steps) * cellSize < gridSize) and (0 <= currentPos[1] * cellSize < gridSize):
                self.drawRobot(currentPos, cellSize, constants.GREEN,
                               constants.GREEN, constants.GREEN)
                self.bot.setCurrentPos(
                    currentPos[0] - steps, currentPos[1], currentPos[2])
        elif currentPos[2] == Direction.LEFT:
            for x in range(currentPos[0] - 1, currentPos[0] + 2):
                for obstacle in self.obstacles:
                    i = (constants.GRID_LENGTH - constants.GRID_CELL_LENGTH -
                         obstacle.position.x) // constants.GRID_CELL_LENGTH
                    j = (obstacle.position.y -
                         constants.GRID_CELL_LENGTH) // constants.GRID_CELL_LENGTH
                    if (x == i) and (currentPos[1] + 2 == j):
                        print(f"COLLISION!")
                        return
            if (0 <= currentPos[0] * cellSize < gridSize) and (0 <= (currentPos[1] + steps) * cellSize < gridSize):
                self.drawRobot(currentPos, cellSize, constants.GREEN,
                               constants.GREEN, constants.GREEN)
                self.bot.setCurrentPos(
                    currentPos[0], currentPos[1] + steps, currentPos[2])

    def turnRight(self, currentPos, gridSize, cellSize):
        xSteps = 4
        ySteps = 3
        if currentPos[2] == Direction.TOP:
            if (0 <= (currentPos[0] - xSteps) * cellSize < gridSize) and (0 <= (currentPos[1] + ySteps) * cellSize < gridSize):
                for x in range(currentPos[0] - 5, currentPos[0] + 2):
                    for y in range(currentPos[1] - 1, currentPos[1] + 5):
                        if (x > currentPos[0] - 3) and (y > currentPos[1] + 1):
                            continue
                        else:
                            for obstacle in self.obstacles:
                                i = (constants.GRID_LENGTH - constants.GRID_CELL_LENGTH -
                                     obstacle.position.x) // constants.GRID_CELL_LENGTH
                                j = (
                                    obstacle.position.y - constants.GRID_CELL_LENGTH) // constants.GRID_CELL_LENGTH
                                if (x == i) and (y == j):
                                    print(f"COLLISION!")
                                    return
                        if (0 <= x * cellSize < gridSize) and (0 <= y * cellSize < gridSize):
                            newRect = pygame.Rect(
                                y * cellSize, x * cellSize, cellSize, cellSize)
                            self.screen.fill(constants.GREEN, newRect)
                            pygame.draw.rect(
                                self.screen, constants.GREEN, newRect, 2)
                # if (0 <= (currentPos[0] - 4) * cellSize < gridSize) and (0 <= (currentPos[1] + 3) * cellSize < gridSize):
                print(f"TURNING RIGHT\t{currentPos}")
                self.drawRobot(currentPos, cellSize, constants.GREEN,
                               constants.GREEN, constants.GREEN)
                self.bot.setCurrentPos(
                    currentPos[0] - xSteps, currentPos[1] + ySteps, Direction.RIGHT)
        elif currentPos[2] == Direction.RIGHT:
            if (0 <= (currentPos[0] + ySteps) * cellSize < gridSize) and (0 <= (currentPos[1] + xSteps) * cellSize < gridSize):
                for x in range(currentPos[0] - 1, currentPos[0] + 5):
                    for y in range(currentPos[1] - 1, currentPos[1] + 6):
                        if (x > currentPos[0] + 1) and (y < currentPos[1] + 3):
                            continue
                        else:
                            for obstacle in self.obstacles:
                                i = (constants.GRID_LENGTH - constants.GRID_CELL_LENGTH -
                                     obstacle.position.x) // constants.GRID_CELL_LENGTH
                                j = (
                                    obstacle.position.y - constants.GRID_CELL_LENGTH) // constants.GRID_CELL_LENGTH
                                if (x == i) and (y == j):
                                    print(f"COLLISION!")
                                    return
                            if (0 <= x * cellSize < gridSize) and (0 <= y * cellSize < gridSize):
                                newRect = pygame.Rect(
                                    y * cellSize, x * cellSize, cellSize, cellSize)
                                self.screen.fill(constants.GREEN, newRect)
                                pygame.draw.rect(
                                    self.screen, constants.GREEN, newRect, 2)
                # if (0 <= (currentPos[0] + 3) * cellSize < gridSize) and (0 <= (currentPos[1] + 4) * cellSize < gridSize):
                print(f"TURNING RIGHT\t{currentPos}")
                self.drawRobot(currentPos, cellSize, constants.GREEN,
                               constants.GREEN, constants.GREEN)
                self.bot.setCurrentPos(
                    currentPos[0] + ySteps, currentPos[1] + xSteps, Direction.BOTTOM)
        elif currentPos[2] == Direction.BOTTOM:
            if (0 <= (currentPos[0] + xSteps) * cellSize < gridSize) and (0 <= (currentPos[1] - ySteps) * cellSize < gridSize):
                for x in range(currentPos[0] - 1, currentPos[0] + 6):
                    for y in range(currentPos[1] - 4, currentPos[1] + 2):
                        if (x < currentPos[0] + 3) and (y < currentPos[1] - 1):
                            continue
                        else:
                            for obstacle in self.obstacles:
                                i = (constants.GRID_LENGTH - constants.GRID_CELL_LENGTH -
                                     obstacle.position.x) // constants.GRID_CELL_LENGTH
                                j = (
                                    obstacle.position.y - constants.GRID_CELL_LENGTH) // constants.GRID_CELL_LENGTH
                                if (x == i) and (y == j):
                                    print(f"COLLISION!")
                                    return
                            if (0 <= x * cellSize < gridSize) and (0 <= y * cellSize < gridSize):
                                newRect = pygame.Rect(
                                    y * cellSize, x * cellSize, cellSize, cellSize)
                                self.screen.fill(constants.GREEN, newRect)
                                pygame.draw.rect(
                                    self.screen, constants.GREEN, newRect, 2)
                # if (0 <= (currentPos[0] + 4) * cellSize < gridSize) and (0 <= (currentPos[1] - 3) * cellSize < gridSize):
                print(f"TURNING RIGHT\t{currentPos}")
                self.drawRobot(currentPos, cellSize, constants.GREEN,
                               constants.GREEN, constants.GREEN)
                self.bot.setCurrentPos(
                    currentPos[0] + xSteps, currentPos[1] - ySteps, Direction.LEFT)
        elif currentPos[2] == Direction.LEFT:
            if (0 <= (currentPos[0] - ySteps) * cellSize < gridSize) and (0 <= (currentPos[1] - xSteps) * cellSize < gridSize):
                for x in range(currentPos[0] - 4, currentPos[0] + 2):
                    for y in range(currentPos[1] - 5, currentPos[1] + 2):
                        if (x < currentPos[0] - 1) and (y > currentPos[1] - 3):
                            continue
                        else:
                            for obstacle in self.obstacles:
                                i = (constants.GRID_LENGTH - constants.GRID_CELL_LENGTH -
                                     obstacle.position.x) // constants.GRID_CELL_LENGTH
                                j = (
                                    obstacle.position.y - constants.GRID_CELL_LENGTH) // constants.GRID_CELL_LENGTH
                                if (x == i) and (y == j):
                                    print(f"COLLISION!")
                                    return
                            if (0 <= x * cellSize < gridSize) and (0 <= y * cellSize < gridSize):
                                newRect = pygame.Rect(
                                    y * cellSize, x * cellSize, cellSize, cellSize)
                                self.screen.fill(constants.GREEN, newRect)
                                pygame.draw.rect(
                                    self.screen, constants.GREEN, newRect, 2)
                # if (0 <= (currentPos[0] - 4) * cellSize < gridSize) and (0 <= (currentPos[1] - 3) * cellSize < gridSize):
                print(f"TURNING RIGHT\t{currentPos}")
                self.drawRobot(currentPos, cellSize, constants.GREEN,
                               constants.GREEN, constants.GREEN)
                self.bot.setCurrentPos(
                    currentPos[0] - ySteps, currentPos[1] - xSteps, Direction.TOP)

    def turnLeft(self, currentPos, gridSize, cellSize):
        xStep = 4
        yStep = 3
        if currentPos[2] == Direction.TOP:
            if (0 <= (currentPos[0] - xStep) * cellSize < gridSize) and (0 <= (currentPos[1] - yStep) * cellSize < gridSize):
                for x in range(currentPos[0] - 5, currentPos[0] + 2):
                    for y in range(currentPos[1] - 4, currentPos[1] + 2):
                        if (x > currentPos[0] - 3) and (y < currentPos[1] - 1):
                            continue
                        else:
                            for obstacle in self.obstacles:
                                i = (constants.GRID_LENGTH - constants.GRID_CELL_LENGTH -
                                     obstacle.position.x) // constants.GRID_CELL_LENGTH
                                j = (
                                    obstacle.position.y - constants.GRID_CELL_LENGTH) // constants.GRID_CELL_LENGTH
                                if (x == i) and (y == j):
                                    print(f"COLLISION!")
                                    return
                            if (0 <= x * cellSize < gridSize) and (0 <= y * cellSize < gridSize):
                                newRect = pygame.Rect(
                                    y * cellSize, x * cellSize, cellSize, cellSize)
                                self.screen.fill(constants.GREEN, newRect)
                                pygame.draw.rect(
                                    self.screen, constants.GREEN, newRect, 2)
                # if (0 <= (currentPos[0] - 4) * cellSize < gridSize) and (0 <= (currentPos[1] - 3) * cellSize < gridSize):
                print(f"TURNING LEFT\t{currentPos}")
                self.drawRobot(currentPos, cellSize, constants.GREEN,
                               constants.GREEN, constants.GREEN)
                self.bot.setCurrentPos(
                    currentPos[0] - xStep, currentPos[1] - yStep, Direction.LEFT)
        elif currentPos[2] == Direction.RIGHT:
            if (0 <= (currentPos[0] - yStep) * cellSize < gridSize) and (0 <= (currentPos[1] + xStep) * cellSize < gridSize):
                for x in range(currentPos[0] - 4, currentPos[0] + 2):
                    for y in range(currentPos[1] - 1, currentPos[1] + 6):
                        if (x < currentPos[0] - 1) and (y < currentPos[1] + 3):
                            continue
                        else:
                            for obstacle in self.obstacles:
                                i = (constants.GRID_LENGTH - constants.GRID_CELL_LENGTH -
                                     obstacle.position.x) // constants.GRID_CELL_LENGTH
                                j = (
                                    obstacle.position.y - constants.GRID_CELL_LENGTH) // constants.GRID_CELL_LENGTH
                                if (x == i) and (y == j):
                                    print(f"COLLISION!")
                                    return
                            if (0 <= x * cellSize < gridSize) and (0 <= y * cellSize < gridSize):
                                newRect = pygame.Rect(
                                    y * cellSize, x * cellSize, cellSize, cellSize)
                                self.screen.fill(constants.GREEN, newRect)
                                pygame.draw.rect(
                                    self.screen, constants.GREEN, newRect, 2)
                # if (0 <= (currentPos[0] - 3) * cellSize < gridSize) and (0 <= (currentPos[1] + 4) * cellSize < gridSize):
                print(f"TURNING LEFT\t{currentPos}")
                self.drawRobot(currentPos, cellSize, constants.GREEN,
                               constants.GREEN, constants.GREEN)
                self.bot.setCurrentPos(
                    currentPos[0] - yStep, currentPos[1] + xStep, Direction.TOP)
        elif currentPos[2] == Direction.BOTTOM:
            if (0 <= (currentPos[0] + xStep) * cellSize < gridSize) and (0 <= (currentPos[1] + yStep) * cellSize < gridSize):
                for x in range(currentPos[0] - 1, currentPos[0] + 6):
                    for y in range(currentPos[1] - 1, currentPos[1] + 5):
                        if (x < currentPos[0] + 3) and (y > currentPos[1] + 1):
                            continue
                        else:
                            for obstacle in self.obstacles:
                                i = (constants.GRID_LENGTH - constants.GRID_CELL_LENGTH -
                                     obstacle.position.x) // constants.GRID_CELL_LENGTH
                                j = (
                                    obstacle.position.y - constants.GRID_CELL_LENGTH) // constants.GRID_CELL_LENGTH
                                if (x == i) and (y == j):
                                    print(f"COLLISION!")
                                    return
                            if (0 <= x * cellSize < gridSize) and (0 <= y * cellSize < gridSize):
                                newRect = pygame.Rect(
                                    y * cellSize, x * cellSize, cellSize, cellSize)
                                self.screen.fill(constants.GREEN, newRect)
                                pygame.draw.rect(
                                    self.screen, constants.GREEN, newRect, 2)
                # if (0 <= (currentPos[0] + 4) * cellSize < gridSize) and (0 <= (currentPos[1] + 3) * cellSize < gridSize):
                print(f"TURNING LEFT\t{currentPos}")
                self.drawRobot(currentPos, cellSize, constants.GREEN,
                               constants.GREEN, constants.GREEN)
                self.bot.setCurrentPos(
                    currentPos[0] + xStep, currentPos[1] + yStep, Direction.RIGHT)
        elif currentPos[2] == Direction.LEFT:
            if (0 <= (currentPos[0] + yStep) * cellSize < gridSize) and (0 <= (currentPos[1] - xStep) * cellSize < gridSize):
                for x in range(currentPos[0] - 1, currentPos[0] + 5):
                    for y in range(currentPos[1] - 5, currentPos[1] + 2):
                        if (x > currentPos[0] + 1) and (y > currentPos[1] - 3):
                            continue
                        else:
                            for obstacle in self.obstacles:
                                i = (constants.GRID_LENGTH - constants.GRID_CELL_LENGTH -
                                     obstacle.position.x) // constants.GRID_CELL_LENGTH
                                j = (
                                    obstacle.position.y - constants.GRID_CELL_LENGTH) // constants.GRID_CELL_LENGTH
                                if (x == i) and (y == j):
                                    print(f"COLLISION!")
                                    return
                            if (0 <= x * cellSize < gridSize) and (0 <= y * cellSize < gridSize):
                                newRect = pygame.Rect(
                                    y * cellSize, x * cellSize, cellSize, cellSize)
                                self.screen.fill(constants.GREEN, newRect)
                                pygame.draw.rect(
                                    self.screen, constants.GREEN, newRect, 2)
                # if (0 <= (currentPos[0] + 3) * cellSize < gridSize) and (0 <= (currentPos[1] - 4) * cellSize < gridSize):
                print(f"TURNING LEFT\t{currentPos}")
                self.drawRobot(currentPos, cellSize, constants.GREEN,
                               constants.GREEN, constants.GREEN)
                self.bot.setCurrentPos(
                    currentPos[0] + yStep, currentPos[1] - xStep, Direction.BOTTOM)

    def reverseTurnRight(self, currentPos, gridSize, cellSize):
        xStep = 3
        yStep = 4
        if currentPos[2] == Direction.TOP:
            if (0 <= (currentPos[0] + xStep) * cellSize < gridSize) and (0 <= (currentPos[1] + yStep) * cellSize < gridSize):
                for x in range(currentPos[0] - 1, currentPos[0] + 5):
                    for y in range(currentPos[1] - 1, currentPos[1] + 6):
                        if (x < currentPos[0] + 2) and (y > currentPos[1] + 1):
                            continue
                        else:
                            for obstacle in self.obstacles:
                                i = (constants.GRID_LENGTH - constants.GRID_CELL_LENGTH -
                                     obstacle.position.x) // constants.GRID_CELL_LENGTH
                                j = (
                                    obstacle.position.y - constants.GRID_CELL_LENGTH) // constants.GRID_CELL_LENGTH
                                if (x == i) and (y == j):
                                    print(f"COLLISION!")
                                    return
                            if (0 <= x * cellSize < gridSize) and (0 <= y * cellSize < gridSize):
                                newRect = pygame.Rect(
                                    y * cellSize, x * cellSize, cellSize, cellSize)
                                self.screen.fill(constants.GREEN, newRect)
                                pygame.draw.rect(
                                    self.screen, constants.GREEN, newRect, 2)
                # if (0 <= (currentPos[0] - 4) * cellSize < gridSize) and (0 <= (currentPos[1] + 3) * cellSize < gridSize):
                print(f"REVERSE RIGHT\t{currentPos}")
                self.drawRobot(currentPos, cellSize, constants.GREEN,
                               constants.GREEN, constants.GREEN)
                self.bot.setCurrentPos(
                    currentPos[0] + xStep, currentPos[1] + yStep, Direction.LEFT)
        elif currentPos[2] == Direction.RIGHT:
            if (0 <= (currentPos[0] + yStep) * cellSize < gridSize) and (0 <= (currentPos[1] - xStep) * cellSize < gridSize):
                for x in range(currentPos[0] - 1, currentPos[0] + 6):
                    for y in range(currentPos[1] - 4, currentPos[1] + 2):
                        if (x > currentPos[0] + 1) and (y > currentPos[1] - 2):
                            continue
                        else:
                            for obstacle in self.obstacles:
                                i = (constants.GRID_LENGTH - constants.GRID_CELL_LENGTH -
                                     obstacle.position.x) // constants.GRID_CELL_LENGTH
                                j = (
                                    obstacle.position.y - constants.GRID_CELL_LENGTH) // constants.GRID_CELL_LENGTH
                                if (x == i) and (y == j):
                                    print(f"COLLISION!")
                                    return
                        if (0 <= x * cellSize < gridSize) and (0 <= y * cellSize < gridSize):
                            newRect = pygame.Rect(
                                y * cellSize, x * cellSize, cellSize, cellSize)
                            self.screen.fill(constants.GREEN, newRect)
                            pygame.draw.rect(
                                self.screen, constants.GREEN, newRect, 2)
                # if (0 <= (currentPos[0] + 3) * cellSize < gridSize) and (0 <= (currentPos[1] + 4) * cellSize < gridSize):
                print(f"REVERSE RIGHT\t{currentPos}")
                self.drawRobot(currentPos, cellSize, constants.GREEN,
                               constants.GREEN, constants.GREEN)
                self.bot.setCurrentPos(
                    currentPos[0] + yStep, currentPos[1] - xStep, Direction.TOP)
        elif currentPos[2] == Direction.BOTTOM:
            if (0 <= (currentPos[0] - xStep) * cellSize < gridSize) and (0 <= (currentPos[1] - yStep) * cellSize < gridSize):
                for x in range(currentPos[0] - 4, currentPos[0] + 2):
                    for y in range(currentPos[1] - 5, currentPos[1] + 2):
                        if (x > currentPos[0] - 2) and (y < currentPos[1] - 1):
                            continue
                        else:
                            for obstacle in self.obstacles:
                                i = (constants.GRID_LENGTH - constants.GRID_CELL_LENGTH -
                                     obstacle.position.x) // constants.GRID_CELL_LENGTH
                                j = (
                                    obstacle.position.y - constants.GRID_CELL_LENGTH) // constants.GRID_CELL_LENGTH
                                if (x == i) and (y == j):
                                    print(f"COLLISION!")
                                    return
                            if (0 <= x * cellSize < gridSize) and (0 <= y * cellSize < gridSize):
                                newRect = pygame.Rect(
                                    y * cellSize, x * cellSize, cellSize, cellSize)
                                self.screen.fill(constants.GREEN, newRect)
                                pygame.draw.rect(
                                    self.screen, constants.GREEN, newRect, 2)
                # if (0 <= (currentPos[0] + 4) * cellSize < gridSize) and (0 <= (currentPos[1] - 3) * cellSize < gridSize):
                print(f"REVERSE RIGHT\t{currentPos}")
                self.drawRobot(currentPos, cellSize, constants.GREEN,
                               constants.GREEN, constants.GREEN)
                self.bot.setCurrentPos(
                    currentPos[0] - xStep, currentPos[1] - yStep, Direction.RIGHT)
        elif currentPos[2] == Direction.LEFT:
            if (0 <= (currentPos[0] - yStep) * cellSize < gridSize) and (0 <= (currentPos[1] + xStep) * cellSize < gridSize):
                for x in range(currentPos[0] - 5, currentPos[0] + 2):
                    for y in range(currentPos[1] - 1, currentPos[1] + 5):
                        if (x < currentPos[0] - 1) and (y < currentPos[1] + 2):
                            continue
                        else:
                            for obstacle in self.obstacles:
                                i = (constants.GRID_LENGTH - constants.GRID_CELL_LENGTH -
                                     obstacle.position.x) // constants.GRID_CELL_LENGTH
                                j = (
                                    obstacle.position.y - constants.GRID_CELL_LENGTH) // constants.GRID_CELL_LENGTH
                                if (x == i) and (y == j):
                                    print(f"COLLISION!")
                                    return
                            if (0 <= x * cellSize < gridSize) and (0 <= y * cellSize < gridSize):
                                newRect = pygame.Rect(
                                    y * cellSize, x * cellSize, cellSize, cellSize)
                                self.screen.fill(constants.GREEN, newRect)
                                pygame.draw.rect(
                                    self.screen, constants.GREEN, newRect, 2)
                # if (0 <= (currentPos[0] - 4) * cellSize < gridSize) and (0 <= (currentPos[1] - 3) * cellSize < gridSize):
                print(f"REVERSE RIGHT\t{currentPos}")
                self.drawRobot(currentPos, cellSize, constants.GREEN,
                               constants.GREEN, constants.GREEN)
                self.bot.setCurrentPos(
                    currentPos[0] - yStep, currentPos[1] + xStep, Direction.BOTTOM)

    def reverseTurnLeft(self, currentPos, gridSize, cellSize):
        xStep = 3
        yStep = 4
        if currentPos[2] == Direction.TOP:
            if (0 <= (currentPos[0] + xStep) * cellSize < gridSize) and (0 <= (currentPos[1] - yStep) * cellSize < gridSize):
                for x in range(currentPos[0] - 1, currentPos[0] + 5):
                    for y in range(currentPos[1] - 5, currentPos[1] + 2):
                        if (x < currentPos[0] + 2) and (y < currentPos[1] - 1):
                            continue
                        else:
                            for obstacle in self.obstacles:
                                i = (constants.GRID_LENGTH - constants.GRID_CELL_LENGTH -
                                     obstacle.position.x) // constants.GRID_CELL_LENGTH
                                j = (
                                    obstacle.position.y - constants.GRID_CELL_LENGTH) // constants.GRID_CELL_LENGTH
                                if (x == i) and (y == j):
                                    print(f"COLLISION!")
                                    return
                            if (0 <= x * cellSize < gridSize) and (0 <= y * cellSize < gridSize):
                                newRect = pygame.Rect(
                                    y * cellSize, x * cellSize, cellSize, cellSize)
                                self.screen.fill(constants.GREEN, newRect)
                                pygame.draw.rect(
                                    self.screen, constants.GREEN, newRect, 2)
                # if (0 <= (currentPos[0] - 4) * cellSize < gridSize) and (0 <= (currentPos[1] - 3) * cellSize < gridSize):
                print(f"REVERSE LEFT\t{currentPos}")
                self.drawRobot(currentPos, cellSize, constants.GREEN,
                               constants.GREEN, constants.GREEN)
                self.bot.setCurrentPos(
                    currentPos[0] + xStep, currentPos[1] - 4, Direction.RIGHT)
        elif currentPos[2] == Direction.RIGHT:
            if (0 <= (currentPos[0] - yStep) * cellSize < gridSize) and (0 <= (currentPos[1] - xStep) * cellSize < gridSize):
                for x in range(currentPos[0] - 5, currentPos[0] + 2):
                    for y in range(currentPos[1] - 4, currentPos[1] + 2):
                        if (x < currentPos[0] - 1) and (y > currentPos[1] - 2):
                            continue
                        else:
                            for obstacle in self.obstacles:
                                i = (constants.GRID_LENGTH - constants.GRID_CELL_LENGTH -
                                     obstacle.position.x) // constants.GRID_CELL_LENGTH
                                j = (
                                    obstacle.position.y - constants.GRID_CELL_LENGTH) // constants.GRID_CELL_LENGTH
                                if (x == i) and (y == j):
                                    print(f"COLLISION!")
                                    return
                            if (0 <= x * cellSize < gridSize) and (0 <= y * cellSize < gridSize):
                                newRect = pygame.Rect(
                                    y * cellSize, x * cellSize, cellSize, cellSize)
                                self.screen.fill(constants.GREEN, newRect)
                                pygame.draw.rect(
                                    self.screen, constants.GREEN, newRect, 2)
                # if (0 <= (currentPos[0] - 3) * cellSize < gridSize) and (0 <= (currentPos[1] + 4) * cellSize < gridSize):
                print(f"REVERSE LEFT\t{currentPos}")
                self.drawRobot(currentPos, cellSize, constants.GREEN,
                               constants.GREEN, constants.GREEN)
                self.bot.setCurrentPos(
                    currentPos[0] - yStep, currentPos[1] - xStep, Direction.BOTTOM)
        elif currentPos[2] == Direction.BOTTOM:
            if (0 <= (currentPos[0] - xStep) * cellSize < gridSize) and (0 <= (currentPos[1] + yStep) * cellSize < gridSize):
                for x in range(currentPos[0] - 4, currentPos[0] + 2):
                    for y in range(currentPos[1] - 1, currentPos[1] + 6):
                        if (x > currentPos[0] - 2) and (y > currentPos[1] + 1):
                            continue
                        else:
                            for obstacle in self.obstacles:
                                i = (constants.GRID_LENGTH - constants.GRID_CELL_LENGTH -
                                     obstacle.position.x) // constants.GRID_CELL_LENGTH
                                j = (
                                    obstacle.position.y - constants.GRID_CELL_LENGTH) // constants.GRID_CELL_LENGTH
                                if (x == i) and (y == j):
                                    print(f"COLLISION!")
                                    return
                            if (0 <= x * cellSize < gridSize) and (0 <= y * cellSize < gridSize):
                                newRect = pygame.Rect(
                                    y * cellSize, x * cellSize, cellSize, cellSize)
                                self.screen.fill(constants.GREEN, newRect)
                                pygame.draw.rect(
                                    self.screen, constants.GREEN, newRect, 2)
                # if (0 <= (currentPos[0] + 4) * cellSize < gridSize) and (0 <= (currentPos[1] + 3) * cellSize < gridSize):
                print(f"REVERSE LEFT\t{currentPos}")
                self.drawRobot(currentPos, cellSize, constants.GREEN,
                               constants.GREEN, constants.GREEN)
                self.bot.setCurrentPos(
                    currentPos[0] - xStep, currentPos[1] + yStep, Direction.LEFT)
        elif currentPos[2] == Direction.LEFT:
            if (0 <= (currentPos[0] + yStep) * cellSize < gridSize) and (0 <= (currentPos[1] + xStep) * cellSize < gridSize):
                for x in range(currentPos[0] - 1, currentPos[0] + 6):
                    for y in range(currentPos[1] - 1, currentPos[1] + 5):
                        if (x > currentPos[0] + 1) and (y < currentPos[1] + 2):
                            continue
                        else:
                            for obstacle in self.obstacles:
                                i = (constants.GRID_LENGTH - constants.GRID_CELL_LENGTH -
                                     obstacle.position.x) // constants.GRID_CELL_LENGTH
                                j = (
                                    obstacle.position.y - constants.GRID_CELL_LENGTH) // constants.GRID_CELL_LENGTH
                                if (x == i) and (y == j):
                                    print(f"COLLISION!")
                                    return
                            if (0 <= x * cellSize < gridSize) and (0 <= y * cellSize < gridSize):
                                newRect = pygame.Rect(
                                    y * cellSize, x * cellSize, cellSize, cellSize)
                                self.screen.fill(constants.GREEN, newRect)
                                pygame.draw.rect(
                                    self.screen, constants.GREEN, newRect, 2)
                # if (0 <= (currentPos[0] + 3) * cellSize < gridSize) and (0 <= (currentPos[1] - 4) * cellSize < gridSize):
                print(f"REVERSE LEFT\t{currentPos}")
                self.drawRobot(currentPos, cellSize, constants.GREEN,
                               constants.GREEN, constants.GREEN)
                self.bot.setCurrentPos(
                    currentPos[0] + yStep, currentPos[1] + xStep, Direction.TOP)

    def moveNorthEast(self, currentPos, gridSize, cellSize):
        xStep = 4
        yStep = 1
        if currentPos[2] == Direction.TOP:
            # for y in range(currentPos[1] - 1, currentPos[1] + 2):
            #     for obstacle in self.obstacles:
            #         i = (constants.GRID_LENGTH - constants.GRID_CELL_LENGTH - obstacle.position.x) // constants.GRID_CELL_LENGTH
            #         j = (obstacle.position.y - constants.GRID_CELL_LENGTH) // constants.GRID_CELL_LENGTH
            #         if (currentPos[0] - 2 == i) and (y == j):
            #             print(f"COLLISION!")
            #             return
            if (0 <= (currentPos[0] - xStep) * cellSize < gridSize) and (0 <= (currentPos[1] + yStep) * cellSize < gridSize):
                self.drawRobot(currentPos, cellSize, constants.GREEN,
                               constants.GREEN, constants.GREEN)
                self.bot.setCurrentPos(
                    currentPos[0] - xStep, currentPos[1] + yStep, currentPos[2])
        elif currentPos[2] == Direction.RIGHT:
            # for y in range(currentPos[1] - 1, currentPos[1] + 2):
            #     for obstacle in self.obstacles:
            #         i = (constants.GRID_LENGTH - constants.GRID_CELL_LENGTH - obstacle.position.x) // constants.GRID_CELL_LENGTH
            #         j = (obstacle.position.y - constants.GRID_CELL_LENGTH) // constants.GRID_CELL_LENGTH
            #         if (currentPos[0] - 2 == i) and (y == j):
            #             print(f"COLLISION!")
            #             return
            if (0 <= (currentPos[0] + yStep) * cellSize < gridSize) and (0 <= (currentPos[1] + xStep) * cellSize < gridSize):
                self.drawRobot(currentPos, cellSize, constants.GREEN,
                               constants.GREEN, constants.GREEN)
                self.bot.setCurrentPos(
                    currentPos[0] + yStep, currentPos[1] + xStep, currentPos[2])
        elif currentPos[2] == Direction.BOTTOM:
            # for y in range(currentPos[1] - 1, currentPos[1] + 2):
            #     for obstacle in self.obstacles:
            #         i = (constants.GRID_LENGTH - constants.GRID_CELL_LENGTH - obstacle.position.x) // constants.GRID_CELL_LENGTH
            #         j = (obstacle.position.y - constants.GRID_CELL_LENGTH) // constants.GRID_CELL_LENGTH
            #         if (currentPos[0] - 2 == i) and (y == j):
            #             print(f"COLLISION!")
            #             return
            if (0 <= (currentPos[0] + xStep) * cellSize < gridSize) and (0 <= (currentPos[1] - yStep) * cellSize < gridSize):
                self.drawRobot(currentPos, cellSize, constants.GREEN,
                               constants.GREEN, constants.GREEN)
                self.bot.setCurrentPos(
                    currentPos[0] + xStep, currentPos[1] - yStep, currentPos[2])
        elif currentPos[2] == Direction.LEFT:
            # for y in range(currentPos[1] - 1, currentPos[1] + 2):
            #     for obstacle in self.obstacles:
            #         i = (constants.GRID_LENGTH - constants.GRID_CELL_LENGTH - obstacle.position.x) // constants.GRID_CELL_LENGTH
            #         j = (obstacle.position.y - constants.GRID_CELL_LENGTH) // constants.GRID_CELL_LENGTH
            #         if (currentPos[0] - 2 == i) and (y == j):
            #             print(f"COLLISION!")
            #             return
            if (0 <= (currentPos[0] - yStep) * cellSize < gridSize) and (0 <= (currentPos[1] - xStep) * cellSize < gridSize):
                self.drawRobot(currentPos, cellSize, constants.GREEN,
                               constants.GREEN, constants.GREEN)
                self.bot.setCurrentPos(
                    currentPos[0] - yStep, currentPos[1] - xStep, currentPos[2])

    def moveNorthWest(self, currentPos, gridSize, cellSize):
        xStep = 4
        yStep = 1
        if currentPos[2] == Direction.TOP:
            # for y in range(currentPos[1] - 1, currentPos[1] + 2):
            #     for obstacle in self.obstacles:
            #         i = (constants.GRID_LENGTH - constants.GRID_CELL_LENGTH - obstacle.position.x) // constants.GRID_CELL_LENGTH
            #         j = (obstacle.position.y - constants.GRID_CELL_LENGTH) // constants.GRID_CELL_LENGTH
            #         if (currentPos[0] - 2 == i) and (y == j):
            #             print(f"COLLISION!")
            #             return
            if (0 <= (currentPos[0] - xStep) * cellSize < gridSize) and (0 <= (currentPos[1] - yStep) * cellSize < gridSize):
                self.drawRobot(currentPos, cellSize, constants.GREEN,
                               constants.GREEN, constants.GREEN)
                self.bot.setCurrentPos(
                    currentPos[0] - xStep, currentPos[1] - yStep, currentPos[2])
        elif currentPos[2] == Direction.RIGHT:
            # for y in range(currentPos[1] - 1, currentPos[1] + 2):
            #     for obstacle in self.obstacles:
            #         i = (constants.GRID_LENGTH - constants.GRID_CELL_LENGTH - obstacle.position.x) // constants.GRID_CELL_LENGTH
            #         j = (obstacle.position.y - constants.GRID_CELL_LENGTH) // constants.GRID_CELL_LENGTH
            #         if (currentPos[0] - 2 == i) and (y == j):
            #             print(f"COLLISION!")
            #             return
            if (0 <= (currentPos[0] - yStep) * cellSize < gridSize) and (0 <= (currentPos[1] + xStep) * cellSize < gridSize):
                self.drawRobot(currentPos, cellSize, constants.GREEN,
                               constants.GREEN, constants.GREEN)
                self.bot.setCurrentPos(
                    currentPos[0] - yStep, currentPos[1] + xStep, currentPos[2])
        elif currentPos[2] == Direction.BOTTOM:
            # for y in range(currentPos[1] - 1, currentPos[1] + 2):
            #     for obstacle in self.obstacles:
            #         i = (constants.GRID_LENGTH - constants.GRID_CELL_LENGTH - obstacle.position.x) // constants.GRID_CELL_LENGTH
            #         j = (obstacle.position.y - constants.GRID_CELL_LENGTH) // constants.GRID_CELL_LENGTH
            #         if (currentPos[0] - 2 == i) and (y == j):
            #             print(f"COLLISION!")
            #             return
            if (0 <= (currentPos[0] + xStep) * cellSize < gridSize) and (0 <= (currentPos[1] + yStep) * cellSize < gridSize):
                self.drawRobot(currentPos, cellSize, constants.GREEN,
                               constants.GREEN, constants.GREEN)
                self.bot.setCurrentPos(
                    currentPos[0] + xStep, currentPos[1] + yStep, currentPos[2])
        elif currentPos[2] == Direction.LEFT:
            # for y in range(currentPos[1] - 1, currentPos[1] + 2):
            #     for obstacle in self.obstacles:
            #         i = (constants.GRID_LENGTH - constants.GRID_CELL_LENGTH - obstacle.position.x) // constants.GRID_CELL_LENGTH
            #         j = (obstacle.position.y - constants.GRID_CELL_LENGTH) // constants.GRID_CELL_LENGTH
            #         if (currentPos[0] - 2 == i) and (y == j):
            #             print(f"COLLISION!")
            #             return
            if (0 <= (currentPos[0] + yStep) * cellSize < gridSize) and (0 <= (currentPos[1] - xStep) * cellSize < gridSize):
                self.drawRobot(currentPos, cellSize, constants.GREEN,
                               constants.GREEN, constants.GREEN)
                self.bot.setCurrentPos(
                    currentPos[0] + yStep, currentPos[1] - xStep, currentPos[2])

    def moveSouthEast(self, currentPos, gridSize, cellSize):
        xStep = 4
        yStep = 1
        if currentPos[2] == Direction.TOP:
            # for y in range(currentPos[1] - 1, currentPos[1] + 2):
            #     for obstacle in self.obstacles:
            #         i = (constants.GRID_LENGTH - constants.GRID_CELL_LENGTH - obstacle.position.x) // constants.GRID_CELL_LENGTH
            #         j = (obstacle.position.y - constants.GRID_CELL_LENGTH) // constants.GRID_CELL_LENGTH
            #         if (currentPos[0] - 2 == i) and (y == j):
            #             print(f"COLLISION!")
            #             return
            if (0 <= (currentPos[0] + xStep) * cellSize < gridSize) and (0 <= (currentPos[1] + yStep) * cellSize < gridSize):
                self.drawRobot(currentPos, cellSize, constants.GREEN,
                               constants.GREEN, constants.GREEN)
                self.bot.setCurrentPos(
                    currentPos[0] + xStep, currentPos[1] + yStep, currentPos[2])
        elif currentPos[2] == Direction.RIGHT:
            # for y in range(currentPos[1] - 1, currentPos[1] + 2):
            #     for obstacle in self.obstacles:
            #         i = (constants.GRID_LENGTH - constants.GRID_CELL_LENGTH - obstacle.position.x) // constants.GRID_CELL_LENGTH
            #         j = (obstacle.position.y - constants.GRID_CELL_LENGTH) // constants.GRID_CELL_LENGTH
            #         if (currentPos[0] - 2 == i) and (y == j):
            #             print(f"COLLISION!")
            #             return
            if (0 <= (currentPos[0] + yStep) * cellSize < gridSize) and (0 <= (currentPos[1] - xStep) * cellSize < gridSize):
                self.drawRobot(currentPos, cellSize, constants.GREEN,
                               constants.GREEN, constants.GREEN)
                self.bot.setCurrentPos(
                    currentPos[0] + yStep, currentPos[1] - xStep, currentPos[2])
        elif currentPos[2] == Direction.BOTTOM:
            # for y in range(currentPos[1] - 1, currentPos[1] + 2):
            #     for obstacle in self.obstacles:
            #         i = (constants.GRID_LENGTH - constants.GRID_CELL_LENGTH - obstacle.position.x) // constants.GRID_CELL_LENGTH
            #         j = (obstacle.position.y - constants.GRID_CELL_LENGTH) // constants.GRID_CELL_LENGTH
            #         if (currentPos[0] - 2 == i) and (y == j):
            #             print(f"COLLISION!")
            #             return
            if (0 <= (currentPos[0] - xStep) * cellSize < gridSize) and (0 <= (currentPos[1] - yStep) * cellSize < gridSize):
                self.drawRobot(currentPos, cellSize, constants.GREEN,
                               constants.GREEN, constants.GREEN)
                self.bot.setCurrentPos(
                    currentPos[0] - xStep, currentPos[1] - yStep, currentPos[2])
        elif currentPos[2] == Direction.LEFT:
            # for y in range(currentPos[1] - 1, currentPos[1] + 2):
            #     for obstacle in self.obstacles:
            #         i = (constants.GRID_LENGTH - constants.GRID_CELL_LENGTH - obstacle.position.x) // constants.GRID_CELL_LENGTH
            #         j = (obstacle.position.y - constants.GRID_CELL_LENGTH) // constants.GRID_CELL_LENGTH
            #         if (currentPos[0] - 2 == i) and (y == j):
            #             print(f"COLLISION!")
            #             return
            if (0 <= (currentPos[0] - yStep) * cellSize < gridSize) and (0 <= (currentPos[1] + xStep) * cellSize < gridSize):
                self.drawRobot(currentPos, cellSize, constants.GREEN,
                               constants.GREEN, constants.GREEN)
                self.bot.setCurrentPos(
                    currentPos[0] - yStep, currentPos[1] + xStep, currentPos[2])

    def moveSouthWest(self, currentPos, gridSize, cellSize):
        xStep = 4
        yStep = 1
        if currentPos[2] == Direction.TOP:
            # for y in range(currentPos[1] - 1, currentPos[1] + 2):
            #     for obstacle in self.obstacles:
            #         i = (constants.GRID_LENGTH - constants.GRID_CELL_LENGTH - obstacle.position.x) // constants.GRID_CELL_LENGTH
            #         j = (obstacle.position.y - constants.GRID_CELL_LENGTH) // constants.GRID_CELL_LENGTH
            #         if (currentPos[0] - 2 == i) and (y == j):
            #             print(f"COLLISION!")
            #             return
            if (0 <= (currentPos[0] + xStep) * cellSize < gridSize) and (0 <= (currentPos[1] - yStep) * cellSize < gridSize):
                self.drawRobot(currentPos, cellSize, constants.GREEN,
                               constants.GREEN, constants.GREEN)
                self.bot.setCurrentPos(
                    currentPos[0] + xStep, currentPos[1] - yStep, currentPos[2])
        elif currentPos[2] == Direction.RIGHT:
            # for y in range(currentPos[1] - 1, currentPos[1] + 2):
            #     for obstacle in self.obstacles:
            #         i = (constants.GRID_LENGTH - constants.GRID_CELL_LENGTH - obstacle.position.x) // constants.GRID_CELL_LENGTH
            #         j = (obstacle.position.y - constants.GRID_CELL_LENGTH) // constants.GRID_CELL_LENGTH
            #         if (currentPos[0] - 2 == i) and (y == j):
            #             print(f"COLLISION!")
            #             return
            if (0 <= (currentPos[0] - yStep) * cellSize < gridSize) and (0 <= (currentPos[1] - xStep) * cellSize < gridSize):
                self.drawRobot(currentPos, cellSize, constants.GREEN,
                               constants.GREEN, constants.GREEN)
                self.bot.setCurrentPos(
                    currentPos[0] - yStep, currentPos[1] - xStep, currentPos[2])
        elif currentPos[2] == Direction.BOTTOM:
            # for y in range(currentPos[1] - 1, currentPos[1] + 2):
            #     for obstacle in self.obstacles:
            #         i = (constants.GRID_LENGTH - constants.GRID_CELL_LENGTH - obstacle.position.x) // constants.GRID_CELL_LENGTH
            #         j = (obstacle.position.y - constants.GRID_CELL_LENGTH) // constants.GRID_CELL_LENGTH
            #         if (currentPos[0] - 2 == i) and (y == j):
            #             print(f"COLLISION!")
            #             return
            if (0 <= (currentPos[0] - xStep) * cellSize < gridSize) and (0 <= (currentPos[1] + yStep) * cellSize < gridSize):
                self.drawRobot(currentPos, cellSize, constants.GREEN,
                               constants.GREEN, constants.GREEN)
                self.bot.setCurrentPos(
                    currentPos[0] - xStep, currentPos[1] + yStep, currentPos[2])
        elif currentPos[2] == Direction.LEFT:
            # for y in range(currentPos[1] - 1, currentPos[1] + 2):
            #     for obstacle in self.obstacles:
            #         i = (constants.GRID_LENGTH - constants.GRID_CELL_LENGTH - obstacle.position.x) // constants.GRID_CELL_LENGTH
            #         j = (obstacle.position.y - constants.GRID_CELL_LENGTH) // constants.GRID_CELL_LENGTH
            #         if (currentPos[0] - 2 == i) and (y == j):
            #             print(f"COLLISION!")
            #             return
            if (0 <= (currentPos[0] + yStep) * cellSize < gridSize) and (0 <= (currentPos[1] + xStep) * cellSize < gridSize):
                self.drawRobot(currentPos, cellSize, constants.GREEN,
                               constants.GREEN, constants.GREEN)
                self.bot.setCurrentPos(
                    currentPos[0] + yStep, currentPos[1] + xStep, currentPos[2])

    def movement(self, x, y, buttonLength, buttonWidth, currentPos):
        # move North
        if (685 < x < 685 + buttonLength) and (110 < y < 110 + buttonWidth):
            self.moveForward(currentPos, constants.GRID_LENGTH * constants.SCALING_FACTOR,
                             constants.GRID_CELL_LENGTH * constants.SCALING_FACTOR)
        # move South
        elif (685 < x < 685 + buttonLength) and (180 < y < 180 + buttonWidth):
            self.moveBackward(currentPos, constants.GRID_LENGTH * constants.SCALING_FACTOR,
                              constants.GRID_CELL_LENGTH * constants.SCALING_FACTOR)
        # move Forward East
        elif (720 < x < 720 + buttonLength) and (132.5 < y < 132.5 + buttonWidth):
            self.turnRight(currentPos, constants.GRID_LENGTH * constants.SCALING_FACTOR,
                           constants.GRID_CELL_LENGTH * constants.SCALING_FACTOR)
        # move Forward West
        elif (650 < x < 650 + buttonLength) and (132.5 < y < 132.5 + buttonWidth):
            self.turnLeft(currentPos, constants.GRID_LENGTH * constants.SCALING_FACTOR,
                          constants.GRID_CELL_LENGTH * constants.SCALING_FACTOR)
        # move Backward East
        elif (720 < x < 720 + buttonLength) and (160 < y < 160 + buttonWidth):
            self.reverseTurnRight(currentPos, constants.GRID_LENGTH * constants.SCALING_FACTOR,
                                  constants.GRID_CELL_LENGTH * constants.SCALING_FACTOR)
        # move backward West
        elif (650 < x < 650 + buttonLength) and (160 < y < 160 + buttonWidth):
            self.reverseTurnLeft(currentPos, constants.GRID_LENGTH * constants.SCALING_FACTOR,
                                 constants.GRID_CELL_LENGTH * constants.SCALING_FACTOR)
        # move North East
        elif (720 < x < 720 + buttonLength) and (107.5 < y < 107.5 + buttonWidth):
            print(f"YOU CLICKED THE NORTHEAST BUTTON\T{currentPos}")
            self.moveNorthEast(currentPos, constants.GRID_LENGTH * constants.SCALING_FACTOR,
                               constants.GRID_CELL_LENGTH * constants.SCALING_FACTOR)
        # move North West
        elif (650 < x < 650 + buttonLength) and (107.5 < y < 107.5 + buttonWidth):
            print(f"YOU CLICKED THE NORTHWEST BUTTON\T{currentPos}")
            self.moveNorthWest(currentPos, constants.GRID_LENGTH * constants.SCALING_FACTOR,
                               constants.GRID_CELL_LENGTH * constants.SCALING_FACTOR)
        # move South East
        elif (720 < x < 720 + buttonLength) and (182.5 < y < 182.5 + buttonWidth):
            print(f"YOU CLICKED THE SOUTHEAST BUTTON\T{currentPos}")
            self.moveSouthEast(currentPos, constants.GRID_LENGTH * constants.SCALING_FACTOR,
                               constants.GRID_CELL_LENGTH * constants.SCALING_FACTOR)
        # move South West
        elif (650 < x < 650 + buttonLength) and (182.5 < y < 182.5 + buttonWidth):
            print(f"YOU CLICKED THE SOUTHWEST BUTTON\T{currentPos}")
            self.moveSouthWest(currentPos, constants.GRID_LENGTH * constants.SCALING_FACTOR,
                               constants.GRID_CELL_LENGTH * constants.SCALING_FACTOR)

        '''
        cls.drawImage(img, 685, 110, constants.GREY, size, size)       # Forward N
        cls.drawImage(img, 685, 180, constants.GREY, size, size)       # Backward S

        cls.drawImage(img, 720, 132.5, constants.GREY, size, size)       # Forward E
        cls.drawImage(img, 650, 132.5, constants.GREY, size, size)       # Forward W
        cls.drawImage(img, 720, 160, constants.GREY, size, size)       # Backward E
        cls.drawImage(img, 650, 160, constants.GREY, size, size)       # Backward W

        cls.drawImage(img, 720, 107.5, constants.GREY, size, size)       # Slant Forward E
        cls.drawImage(img, 650, 107.5, constants.GREY, size, size)       # Slant Forward W
        cls.drawImage(img, 720, 182.5, constants.GREY, size, size)       # Slant Backward E
        cls.drawImage(img, 650, 182.5, constants.GREY, size, size)       # Slant Backward W
        '''

    def draw(cls, x, y):
        # start button
        cls.drawButtons(650, 500, constants.GREEN, 'START!', constants.BLACK,
                        constants.BUTTON_LENGTH, constants.BUTTON_WIDTH)
        # current cursor coordinates, change to robot
        cls.drawButtons(0, 600, constants.BLACK,
                        f"({x}, {y})", constants.WHITE, constants.BUTTON_LENGTH, constants.BUTTON_WIDTH)
        # supposedly current direction object is facing
        cls.drawButtons(150, 600, constants.BLACK, f"Direction: North",
                        constants.WHITE, constants.BUTTON_LENGTH * 2, constants.BUTTON_WIDTH)
        # set obstacles, asking for input from cmd prompt
        cls.drawButtons(650, 450, constants.GREEN, 'SET', constants.BLACK,
                        constants.BUTTON_LENGTH, constants.BUTTON_WIDTH)
        # reset grid button
        cls.drawButtons(650, 400, constants.GREY, 'RESET', constants.BLACK,
                        constants.BUTTON_LENGTH, constants.BUTTON_WIDTH)

        if len(cls.obstacles) != 0:
            cls.drawObstaclesButton(cls.obstacles, constants.RED)
        else:
            cls.drawObstaclesButton([], constants.RED)

    def runSimulation(self, bot):
        self.bot = deepcopy(bot)
        self.clock = pygame.time.Clock()
        while True:
            self.drawGrid()
            # print(bot.getCurrentPos())
            # if set == 1:
            currentPosX = self.bot.get_current_pos().x
            currentPosY = self.bot.get_current_pos().y
            direction = self.bot.get_current_pos().direction
            print(f"currentPosX: {currentPosX}, currentPosY: {currentPosY}")
            # set = 1
            # currentPos = (currentPosX, currentPosY, direction)
            currentPos = ((constants.GRID_LENGTH - constants.GRID_CELL_LENGTH -
                          currentPosX) // 10, currentPosY // 10, direction)
            print(f"currentPos ======= {currentPos}")
            self.drawRobot(currentPos, constants.GRID_CELL_LENGTH *
                           constants.SCALING_FACTOR, constants.RED, constants.BLUE, constants.LIGHT_BLUE)
            self.clock.tick(10)     # 10 frames per second apparently
            # self.screen.blit(bg, (0, 0))
            x, y = pygame.mouse.get_pos()
            self.draw(x, y)
            # self.drawObstaclesButton()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if (650 < x < 650 + constants.BUTTON_LENGTH) and (500 < y < 500 + constants.BUTTON_WIDTH):
                        print(
                            "START BUTTON IS CLICKED!!! I REPEAT, START BUTTON IS CLICKED!!!")
                        '''insert run algo function'''
                        # grid, obstacles = app.initGrid()
                        # app.runAlgo(grid, obstacles)
                    elif (650 < x < 650 + constants.BUTTON_LENGTH) and (450 < y < 450 + constants.BUTTON_WIDTH):
                        # print("*****Setting obstacles*****")
                        # self.obstacles = self.createObstacles(
                        #     constants.GRID_LENGTH // constants.GRID_CELL_LENGTH)
                        self.obstacles = self.bot.hamiltonian.grid.obstacles
                        print("*****Drawing obstacles*****")
                        self.drawObstaclesButton(self.obstacles, constants.RED)
                    elif (650 < x < 650 + constants.BUTTON_LENGTH) and (400 < y < 400 + constants.BUTTON_WIDTH):
                        self.reset(bot)
                    elif (650 < x < 720 + constants.GRID_CELL_LENGTH * constants.SCALING_FACTOR) and (115 < y < 185 + constants.GRID_CELL_LENGTH * constants.SCALING_FACTOR):
                        self.movement(
                            x, y,
                            constants.GRID_CELL_LENGTH * constants.SCALING_FACTOR, 25,
                            currentPos)

                elif event.type == pygame.KEYDOWN:
                    keys = pygame.key.get_pressed()
                    # if event.key == pygame.K_UP:
                    if keys[pygame.K_UP]:
                        if keys[pygame.K_UP] and keys[pygame.K_RIGHT]:
                        # if event.key == pygame.K_UP and event.key == pygame.K_RIGHT:
                            self.turnRight(currentPos, constants.GRID_LENGTH * constants.SCALING_FACTOR,
                                           constants.GRID_CELL_LENGTH * constants.SCALING_FACTOR)
                        elif keys[pygame.K_UP] and keys[pygame.K_LEFT]:
                        # elif event.key == pygame.K_UP and event.key == pygame.K_LEFT:
                            self.turnLeft(currentPos, constants.GRID_LENGTH * constants.SCALING_FACTOR,
                                          constants.GRID_CELL_LENGTH * constants.SCALING_FACTOR)
                        else:
                            self.moveForward(currentPos, constants.GRID_LENGTH * constants.SCALING_FACTOR,
                                             constants.GRID_CELL_LENGTH * constants.SCALING_FACTOR)
                    # elif event.key == pygame.K_DOWN:
                    if keys[pygame.K_DOWN]:
                        if keys[pygame.K_DOWN] and keys[pygame.K_RIGHT]:
                        # if event.key == pygame.K_DOWN and event.key == pygame.K_RIGHT:
                            self.reverseTurnRight(currentPos, constants.GRID_LENGTH * constants.SCALING_FACTOR,
                                                  constants.GRID_CELL_LENGTH * constants.SCALING_FACTOR)
                        elif keys[pygame.K_DOWN] and keys[pygame.K_LEFT]:
                        # elif event.key == pygame.K_DOWN and event.key == pygame.K_LEFT:
                            self.reverseTurnLeft(currentPos, constants.GRID_LENGTH * constants.SCALING_FACTOR,
                                                 constants.GRID_CELL_LENGTH * constants.SCALING_FACTOR)
                        else:
                            self.moveBackward(currentPos, constants.GRID_LENGTH * constants.SCALING_FACTOR,
                                              constants.GRID_CELL_LENGTH * constants.SCALING_FACTOR)
                    elif event.key == pygame.K_e:
                        self.moveNorthEast(currentPos, constants.GRID_LENGTH * constants.SCALING_FACTOR,
                                           constants.GRID_CELL_LENGTH * constants.SCALING_FACTOR)
                    elif event.key == pygame.K_q:
                        self.moveNorthWest(currentPos, constants.GRID_LENGTH * constants.SCALING_FACTOR,
                                           constants.GRID_CELL_LENGTH * constants.SCALING_FACTOR)
                    elif event.key == pygame.K_d:
                        self.moveSouthEast(currentPos, constants.GRID_LENGTH * constants.SCALING_FACTOR,
                                           constants.GRID_CELL_LENGTH * constants.SCALING_FACTOR)
                    elif event.key == pygame.K_a:
                        self.moveSouthWest(currentPos, constants.GRID_LENGTH * constants.SCALING_FACTOR,
                                           constants.GRID_CELL_LENGTH * constants.SCALING_FACTOR)
                    
                    # elif (x < constants.GRID_LENGTH * constants.SCALING_FACTOR) and (y < constants.GRID_LENGTH * constants.SCALING_FACTOR):
                    #     ''' Each cell is 10x10 multiplied by scaling factor of 3 = 30x30px
                    #         if i want to get grid cell, take coordinate // (10 * 3) '''
                    #     self.selectObstacles(x // (10 * 3), y // ( 10 * 3), constants.GRID_CELL_LENGTH * constants.SCALING_FACTOR, constants.GREY)
            pygame.display.update()
