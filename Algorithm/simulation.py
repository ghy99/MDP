import pygame
import sys
from copy import deepcopy
import settings
import app

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
        self.screen.fill(settings.BLACK)

    def reset(cls, bot):
        cls.screen.fill(settings.BLACK)
        cls.bot.setCurrentPos(bot.getCurrentPos()[0], bot.getCurrentPos()[
                              1], bot.getCurrentPos()[2])
        cls.obstacles.clear()

    def selectObstacles(cls, y, x, cellSize, color):
        newRect = pygame.Rect(y * cellSize, x * cellSize, cellSize, cellSize)
        cls.screen.fill(color, newRect)
        pygame.draw.rect(cls.screen, color, newRect, 2)

    def drawRobot(cls, robotPos, cellSize, directionColor, botColor, botAreaColor):
        for x in range(robotPos[0] - 1, robotPos[0] + 2):
            for y in range(robotPos[1] - 1, robotPos[1] + 2):
                if (0 <= x * cellSize < settings.GRID_LENGTH * settings.SCALING_FACTOR) and (0 <= y * cellSize < settings.GRID_LENGTH * settings.SCALING_FACTOR):
                    if robotPos[0] == x and robotPos[1] == y:
                        cls.selectObstacles(
                            robotPos[1], robotPos[0], cellSize, botColor)
                        if robotPos[2] == 'N':
                            imageSide = pygame.Rect(
                                robotPos[1] * cellSize, robotPos[0] * cellSize, cellSize, 5)
                            cls.screen.fill(directionColor, imageSide)
                            pygame.draw.rect(
                                cls.screen, directionColor, imageSide, 5)
                        elif robotPos[2] == 'E':
                            imageSide = pygame.Rect(
                                (robotPos[1] * cellSize) + cellSize - 5, (robotPos[0] * cellSize), 5, cellSize)
                            cls.screen.fill(directionColor, imageSide)
                            pygame.draw.rect(
                                cls.screen, directionColor, imageSide, 5)
                        elif robotPos[2] == 'S':
                            imageSide = pygame.Rect(
                                robotPos[1] * cellSize, (robotPos[0] * cellSize) + cellSize - 5, cellSize, 5)
                            cls.screen.fill(directionColor, imageSide)
                            pygame.draw.rect(
                                cls.screen, directionColor, imageSide, 5)
                        elif robotPos[2] == 'W':
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
        for x in range(0, settings.GRID_LENGTH * settings.SCALING_FACTOR, settings.GRID_CELL_LENGTH * settings.SCALING_FACTOR):
            for y in range(0, settings.GRID_LENGTH * settings.SCALING_FACTOR, settings.GRID_CELL_LENGTH * settings.SCALING_FACTOR):
                rect = pygame.Rect(y, x, settings.GRID_CELL_LENGTH * settings.SCALING_FACTOR,
                                   settings.GRID_CELL_LENGTH * settings.SCALING_FACTOR)
                pygame.draw.rect(cls.screen, settings.WHITE, rect, 2)

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
        size = settings.GRID_CELL_LENGTH * settings.SCALING_FACTOR
        turningSize = ((settings.GRID_CELL_LENGTH *
                       settings.SCALING_FACTOR * 3) + 10) // 4
        # self.selectObstacles(x // (10 * 3), y // ( 10 * 3),
        # settings.GRID_CELL_LENGTH * settings.SCALING_FACTOR,
        # settings.GREY)
        for i in obstacles:
            cls.selectObstacles(
                i[1], i[0], settings.GRID_CELL_LENGTH * settings.SCALING_FACTOR, settings.YELLOW)
            if i[2] == 'N':
                imageSide = pygame.Rect(i[1] * size, i[0] * size, size, 5)
                cls.screen.fill(color, imageSide)
                pygame.draw.rect(cls.screen, color, imageSide, 5)
            elif i[2] == 'E':
                imageSide = pygame.Rect(
                    (i[1] * size) + size - 5, (i[0] * size), 5, size)
                cls.screen.fill(color, imageSide)
                pygame.draw.rect(cls.screen, color, imageSide, 5)
            elif i[2] == 'S':
                imageSide = pygame.Rect(
                    i[1] * size, (i[0] * size) + size - 5, size, 5)
                cls.screen.fill(color, imageSide)
                pygame.draw.rect(cls.screen, color, imageSide, 5)
            elif i[2] == 'W':
                imageSide = pygame.Rect(i[1] * size, i[0] * size, 5, size)
                cls.screen.fill(color, imageSide)
                pygame.draw.rect(cls.screen, color, imageSide, 5)

        img = pygame.image.load("images/MoveForward.png").convert()
        cls.drawImage(img, 685, 110, settings.GREY,
                      size, size)       # Forward N
        img = pygame.image.load("images/MoveBackward.png").convert()
        cls.drawImage(img, 685, 180, settings.GREY,
                      size, size)       # Backward S

        img = pygame.image.load("images/TurnForwardRight.png").convert()
        cls.drawImage(img, 720, 132.5, settings.GREY,
                      size, size)       # Forward E
        img = pygame.image.load("images/TurnForwardLeft.png").convert()
        cls.drawImage(img, 650, 132.5, settings.GREY,
                      size, size)       # Forward W
        img = pygame.image.load("images/TurnReverseRight.png").convert()
        cls.drawImage(img, 720, 160, settings.GREY,
                      size, size)       # Backward E
        img = pygame.image.load("images/TurnReverseLeft.png").convert()
        cls.drawImage(img, 650, 160, settings.GREY,
                      size, size)       # Backward W

        img = pygame.image.load("images/slantForwardRight.png").convert()
        cls.drawImage(img, 720, 107.5, settings.GREY,
                      size, size)       # Slant Forward E
        img = pygame.image.load("images/slantForwardLeft.png").convert()
        cls.drawImage(img, 650, 107.5, settings.GREY,
                      size, size)       # Slant Forward W
        img = pygame.image.load("images/slantBackwardsRight.png").convert()
        cls.drawImage(img, 720, 182.5, settings.GREY,
                      size, size)       # Slant Backward E
        img = pygame.image.load("images/slantBackwardsLeft.png").convert()
        cls.drawImage(img, 650, 182.5, settings.GREY,
                      size, size)       # Slant Backward W

    def moveForward(self, currentPos, gridSize, cellSize):
        if currentPos[2] == 'N':
            for y in range(currentPos[1] - 1, currentPos[1] + 2):
                for obstacle in self.obstacles:
                    if (currentPos[0] - 2 == obstacle[0]) and (y == obstacle[1]):
                        print(f"COLLISION!")
                        return
            if (0 <= (currentPos[0] - 1) * cellSize < gridSize) and (0 <= currentPos[1] * cellSize < gridSize):
                self.drawRobot(currentPos, cellSize, settings.GREEN,
                               settings.GREEN, settings.GREEN)
                self.bot.setCurrentPos(
                    currentPos[0] - 1, currentPos[1], currentPos[2])
        elif currentPos[2] == 'E':
            for x in range(currentPos[0] - 1, currentPos[0] + 2):
                for obstacle in self.obstacles:
                    if (x == obstacle[0]) and (currentPos[1] + 2 == obstacle[1]):
                        print(f"COLLISION!")
                        return
            if (0 <= currentPos[0] * cellSize < gridSize) and (0 <= (currentPos[1] + 1) * cellSize < gridSize):
                self.drawRobot(currentPos, cellSize, settings.GREEN,
                               settings.GREEN, settings.GREEN)
                self.bot.setCurrentPos(
                    currentPos[0], currentPos[1] + 1, currentPos[2])
        elif currentPos[2] == 'S':
            for y in range(currentPos[1] - 1, currentPos[1] + 2):
                for obstacle in self.obstacles:
                    if (currentPos[0] + 2 == obstacle[0]) and (y == obstacle[1]):
                        print(f"COLLISION!")
                        return
            if (0 <= (currentPos[0] + 1) * cellSize < gridSize) and (0 <= currentPos[1] * cellSize < gridSize):
                self.drawRobot(currentPos, cellSize, settings.GREEN,
                               settings.GREEN, settings.GREEN)
                self.bot.setCurrentPos(
                    currentPos[0] + 1, currentPos[1], currentPos[2])
        elif currentPos[2] == 'W':
            for x in range(currentPos[0] - 1, currentPos[0] + 2):
                for obstacle in self.obstacles:
                    if (x == obstacle[0]) and (currentPos[1] - 2 == obstacle[1]):
                        print(f"COLLISION!")
                        return
            if (0 <= currentPos[0] * cellSize < gridSize) and (0 <= (currentPos[1] - 1) * cellSize < gridSize):
                self.drawRobot(currentPos, cellSize, settings.GREEN,
                               settings.GREEN, settings.GREEN)
                self.bot.setCurrentPos(
                    currentPos[0], currentPos[1] - 1, currentPos[2])

    def moveBackward(self, currentPos, gridSize, cellSize):
        if currentPos[2] == 'N':
            for y in range(currentPos[1] - 1, currentPos[1] + 2):
                for obstacle in self.obstacles:
                    if (currentPos[0] + 2 == obstacle[0]) and (y == obstacle[1]):
                        print(f"COLLISION!")
                        return
            if (0 <= (currentPos[0] + 1) * cellSize < gridSize) and (0 <= currentPos[1] * cellSize < gridSize):
                self.drawRobot(currentPos, cellSize, settings.GREEN,
                               settings.GREEN, settings.GREEN)
                self.bot.setCurrentPos(
                    currentPos[0] + 1, currentPos[1], currentPos[2])
        elif currentPos[2] == 'E':
            for x in range(currentPos[0] - 1, currentPos[0] + 2):
                for obstacle in self.obstacles:
                    if (x == obstacle[0]) and (currentPos[1] - 2 == obstacle[1]):
                        print(f"COLLISION!")
                        return
            if (0 <= currentPos[0] * cellSize < gridSize) and (0 <= (currentPos[1] - 1) * cellSize < gridSize):
                self.drawRobot(currentPos, cellSize, settings.GREEN,
                               settings.GREEN, settings.GREEN)
                self.bot.setCurrentPos(
                    currentPos[0], currentPos[1] - 1, currentPos[2])
        elif currentPos[2] == 'S':
            for y in range(currentPos[1] - 1, currentPos[1] + 2):
                for obstacle in self.obstacles:
                    if (currentPos[0] - 2 == obstacle[0]) and (y == obstacle[1]):
                        print(f"COLLISION!")
                        return
            if (0 <= (currentPos[0] - 1) * cellSize < gridSize) and (0 <= currentPos[1] * cellSize < gridSize):
                self.drawRobot(currentPos, cellSize, settings.GREEN,
                               settings.GREEN, settings.GREEN)
                self.bot.setCurrentPos(
                    currentPos[0] - 1, currentPos[1], currentPos[2])
        elif currentPos[2] == 'W':
            for x in range(currentPos[0] - 1, currentPos[0] + 2):
                for obstacle in self.obstacles:
                    if (x == obstacle[0]) and (currentPos[1] + 2 == obstacle[1]):
                        print(f"COLLISION!")
                        return
            if (0 <= currentPos[0] * cellSize < gridSize) and (0 <= (currentPos[1] + 1) * cellSize < gridSize):
                self.drawRobot(currentPos, cellSize, settings.GREEN,
                               settings.GREEN, settings.GREEN)
                self.bot.setCurrentPos(
                    currentPos[0], currentPos[1] + 1, currentPos[2])

    def turnRight(self, currentPos, gridSize, cellSize):
        if currentPos[2] == 'N':
            if (0 <= (currentPos[0] - 4) * cellSize < gridSize) and (0 <= (currentPos[1] + 3) * cellSize < gridSize):
                for x in range(currentPos[0] - 5, currentPos[0] + 2):
                    for y in range(currentPos[1] - 1, currentPos[1] + 5):
                        if (x > currentPos[0] - 3) and (y > currentPos[1] + 1):
                            continue
                        else:
                            for obstacle in self.obstacles:
                                if (x == obstacle[0]) and (y == obstacle[1]):
                                    print(f"COLLISION!")
                                    return
                        if (0 <= x * cellSize < gridSize) and (0 <= y * cellSize < gridSize):
                            newRect = pygame.Rect(
                                y * cellSize, x * cellSize, cellSize, cellSize)
                            self.screen.fill(settings.GREEN, newRect)
                            pygame.draw.rect(
                                self.screen, settings.GREEN, newRect, 2)
                # if (0 <= (currentPos[0] - 4) * cellSize < gridSize) and (0 <= (currentPos[1] + 3) * cellSize < gridSize):
                print(f"TURNING RIGHT\t{currentPos}")
                self.drawRobot(currentPos, cellSize, settings.GREEN,
                               settings.GREEN, settings.GREEN)
                self.bot.setCurrentPos(
                    currentPos[0] - 4, currentPos[1] + 3, 'E')
        elif currentPos[2] == 'E':
            if (0 <= (currentPos[0] + 3) * cellSize < gridSize) and (0 <= (currentPos[1] + 4) * cellSize < gridSize):
                for x in range(currentPos[0] - 1, currentPos[0] + 5):
                    for y in range(currentPos[1] - 1, currentPos[1] + 6):
                        if (x > currentPos[0] + 1) and (y < currentPos[1] + 3):
                            continue
                        else:
                            for obstacle in self.obstacles:
                                if (x == obstacle[0]) and (y == obstacle[1]):
                                    print(f"COLLISION!")
                                    return
                            if (0 <= x * cellSize < gridSize) and (0 <= y * cellSize < gridSize):
                                newRect = pygame.Rect(
                                    y * cellSize, x * cellSize, cellSize, cellSize)
                                self.screen.fill(settings.GREEN, newRect)
                                pygame.draw.rect(
                                    self.screen, settings.GREEN, newRect, 2)
                # if (0 <= (currentPos[0] + 3) * cellSize < gridSize) and (0 <= (currentPos[1] + 4) * cellSize < gridSize):
                print(f"TURNING RIGHT\t{currentPos}")
                self.drawRobot(currentPos, cellSize, settings.GREEN,
                               settings.GREEN, settings.GREEN)
                self.bot.setCurrentPos(
                    currentPos[0] + 3, currentPos[1] + 4, 'S')
        elif currentPos[2] == 'S':
            if (0 <= (currentPos[0] + 4) * cellSize < gridSize) and (0 <= (currentPos[1] - 3) * cellSize < gridSize):
                for x in range(currentPos[0] - 1, currentPos[0] + 6):
                    for y in range(currentPos[1] - 4, currentPos[1] + 2):
                        if (x < currentPos[0] + 3) and (y < currentPos[1] - 1):
                            continue
                        else:
                            for obstacle in self.obstacles:
                                if (x == obstacle[0]) and (y == obstacle[1]):
                                    print(f"COLLISION!")
                                    return
                            if (0 <= x * cellSize < gridSize) and (0 <= y * cellSize < gridSize):
                                newRect = pygame.Rect(
                                    y * cellSize, x * cellSize, cellSize, cellSize)
                                self.screen.fill(settings.GREEN, newRect)
                                pygame.draw.rect(
                                    self.screen, settings.GREEN, newRect, 2)
                # if (0 <= (currentPos[0] + 4) * cellSize < gridSize) and (0 <= (currentPos[1] - 3) * cellSize < gridSize):
                print(f"TURNING RIGHT\t{currentPos}")
                self.drawRobot(currentPos, cellSize, settings.GREEN,
                               settings.GREEN, settings.GREEN)
                self.bot.setCurrentPos(
                    currentPos[0] + 4, currentPos[1] - 3, 'W')
        elif currentPos[2] == 'W':
            if (0 <= (currentPos[0] - 3) * cellSize < gridSize) and (0 <= (currentPos[1] - 4) * cellSize < gridSize):
                for x in range(currentPos[0] - 4, currentPos[0] + 2):
                    for y in range(currentPos[1] - 5, currentPos[1] + 2):
                        if (x < currentPos[0] - 1) and (y > currentPos[1] - 3):
                            continue
                        else:
                            for obstacle in self.obstacles:
                                if (x == obstacle[0]) and (y == obstacle[1]):
                                    print(f"COLLISION!")
                                    return
                            if (0 <= x * cellSize < gridSize) and (0 <= y * cellSize < gridSize):
                                newRect = pygame.Rect(
                                    y * cellSize, x * cellSize, cellSize, cellSize)
                                self.screen.fill(settings.GREEN, newRect)
                                pygame.draw.rect(
                                    self.screen, settings.GREEN, newRect, 2)
                # if (0 <= (currentPos[0] - 4) * cellSize < gridSize) and (0 <= (currentPos[1] - 3) * cellSize < gridSize):
                print(f"TURNING RIGHT\t{currentPos}")
                self.drawRobot(currentPos, cellSize, settings.GREEN,
                               settings.GREEN, settings.GREEN)
                self.bot.setCurrentPos(
                    currentPos[0] - 3, currentPos[1] - 4, 'N')

    def turnLeft(self, currentPos, gridSize, cellSize):
        if currentPos[2] == 'N':
            if (0 <= (currentPos[0] - 4) * cellSize < gridSize) and (0 <= (currentPos[1] - 3) * cellSize < gridSize):
                for x in range(currentPos[0] - 5, currentPos[0] + 2):
                    for y in range(currentPos[1] - 4, currentPos[1] + 2):
                        if (x > currentPos[0] - 3) and (y < currentPos[1] - 1):
                            continue
                        else:
                            for obstacle in self.obstacles:
                                if (x == obstacle[0]) and (y == obstacle[1]):
                                    print(f"COLLISION!")
                                    return
                            if (0 <= x * cellSize < gridSize) and (0 <= y * cellSize < gridSize):
                                newRect = pygame.Rect(
                                    y * cellSize, x * cellSize, cellSize, cellSize)
                                self.screen.fill(settings.GREEN, newRect)
                                pygame.draw.rect(
                                    self.screen, settings.GREEN, newRect, 2)
                # if (0 <= (currentPos[0] - 4) * cellSize < gridSize) and (0 <= (currentPos[1] - 3) * cellSize < gridSize):
                print(f"TURNING LEFT\t{currentPos}")
                self.drawRobot(currentPos, cellSize, settings.GREEN,
                               settings.GREEN, settings.GREEN)
                self.bot.setCurrentPos(
                    currentPos[0] - 4, currentPos[1] - 3, 'W')
        elif currentPos[2] == 'E':
            if (0 <= (currentPos[0] - 3) * cellSize < gridSize) and (0 <= (currentPos[1] + 4) * cellSize < gridSize):
                for x in range(currentPos[0] - 4, currentPos[0] + 2):
                    for y in range(currentPos[1] - 1, currentPos[1] + 6):
                        if (x < currentPos[0] - 1) and (y < currentPos[1] + 3):
                            continue
                        else:
                            for obstacle in self.obstacles:
                                if (x == obstacle[0]) and (y == obstacle[1]):
                                    print(f"COLLISION!")
                                    return
                            if (0 <= x * cellSize < gridSize) and (0 <= y * cellSize < gridSize):
                                newRect = pygame.Rect(
                                    y * cellSize, x * cellSize, cellSize, cellSize)
                                self.screen.fill(settings.GREEN, newRect)
                                pygame.draw.rect(
                                    self.screen, settings.GREEN, newRect, 2)
                # if (0 <= (currentPos[0] - 3) * cellSize < gridSize) and (0 <= (currentPos[1] + 4) * cellSize < gridSize):
                print(f"TURNING LEFT\t{currentPos}")
                self.drawRobot(currentPos, cellSize, settings.GREEN,
                               settings.GREEN, settings.GREEN)
                self.bot.setCurrentPos(
                    currentPos[0] - 3, currentPos[1] + 4, 'N')
        elif currentPos[2] == 'S':
            if (0 <= (currentPos[0] + 4) * cellSize < gridSize) and (0 <= (currentPos[1] + 3) * cellSize < gridSize):
                for x in range(currentPos[0] - 1, currentPos[0] + 6):
                    for y in range(currentPos[1] - 1, currentPos[1] + 5):
                        if (x < currentPos[0] + 3) and (y > currentPos[1] + 1):
                            continue
                        else:
                            for obstacle in self.obstacles:
                                if (x == obstacle[0]) and (y == obstacle[1]):
                                    print(f"COLLISION!")
                                    return
                            if (0 <= x * cellSize < gridSize) and (0 <= y * cellSize < gridSize):
                                newRect = pygame.Rect(
                                    y * cellSize, x * cellSize, cellSize, cellSize)
                                self.screen.fill(settings.GREEN, newRect)
                                pygame.draw.rect(
                                    self.screen, settings.GREEN, newRect, 2)
                # if (0 <= (currentPos[0] + 4) * cellSize < gridSize) and (0 <= (currentPos[1] + 3) * cellSize < gridSize):
                print(f"TURNING LEFT\t{currentPos}")
                self.drawRobot(currentPos, cellSize, settings.GREEN,
                               settings.GREEN, settings.GREEN)
                self.bot.setCurrentPos(
                    currentPos[0] + 4, currentPos[1] + 3, 'E')
        elif currentPos[2] == 'W':
            if (0 <= (currentPos[0] + 3) * cellSize < gridSize) and (0 <= (currentPos[1] - 4) * cellSize < gridSize):
                for x in range(currentPos[0] - 1, currentPos[0] + 5):
                    for y in range(currentPos[1] - 5, currentPos[1] + 2):
                        if (x > currentPos[0] + 1) and (y > currentPos[1] - 3):
                            continue
                        else:
                            for obstacle in self.obstacles:
                                if (x == obstacle[0]) and (y == obstacle[1]):
                                    print(f"COLLISION!")
                                    return
                            if (0 <= x * cellSize < gridSize) and (0 <= y * cellSize < gridSize):
                                newRect = pygame.Rect(
                                    y * cellSize, x * cellSize, cellSize, cellSize)
                                self.screen.fill(settings.GREEN, newRect)
                                pygame.draw.rect(
                                    self.screen, settings.GREEN, newRect, 2)
                # if (0 <= (currentPos[0] + 3) * cellSize < gridSize) and (0 <= (currentPos[1] - 4) * cellSize < gridSize):
                print(f"TURNING LEFT\t{currentPos}")
                self.drawRobot(currentPos, cellSize, settings.GREEN,
                               settings.GREEN, settings.GREEN)
                self.bot.setCurrentPos(
                    currentPos[0] + 3, currentPos[1] - 4, 'S')

    def reverseTurnRight(self, currentPos, gridSize, cellSize):
        if currentPos[2] == 'N':
            if (0 <= (currentPos[0] - 4) * cellSize < gridSize) and (0 <= (currentPos[1] + 3) * cellSize < gridSize):
                for x in range(currentPos[0] - 1, currentPos[0] + 5):
                    for y in range(currentPos[1] - 1, currentPos[1] + 6):
                        if (x < currentPos[0] + 2) and (y > currentPos[1] + 1):
                            continue
                        else:
                            for obstacle in self.obstacles:
                                if (x == obstacle[0]) and (y == obstacle[1]):
                                    print(f"COLLISION!")
                                    return
                        if (0 <= x * cellSize < gridSize) and (0 <= y * cellSize < gridSize):
                            newRect = pygame.Rect(
                                y * cellSize, x * cellSize, cellSize, cellSize)
                            self.screen.fill(settings.GREEN, newRect)
                            pygame.draw.rect(self.screen, settings.GREEN, newRect, 2)
                # if (0 <= (currentPos[0] - 4) * cellSize < gridSize) and (0 <= (currentPos[1] + 3) * cellSize < gridSize):
                print(f"REVERSE RIGHT\t{currentPos}")
                self.drawRobot(currentPos, cellSize, settings.GREEN,
                               settings.GREEN, settings.GREEN)
                self.bot.setCurrentPos(
                    currentPos[0] + 3, currentPos[1] + 4, 'W')
        elif currentPos[2] == 'E':
            if (0 <= (currentPos[0] + 3) * cellSize < gridSize) and (0 <= (currentPos[1] + 4) * cellSize < gridSize):
                for x in range(currentPos[0] - 1, currentPos[0] + 5):
                    for y in range(currentPos[1] - 1, currentPos[1] + 6):
                        if (x > currentPos[0] + 1) and (y < currentPos[1] + 3):
                            continue
                        else:
                            for obstacle in self.obstacles:
                                if (x == obstacle[0]) and (y == obstacle[1]):
                                    print(f"COLLISION!")
                                    return
                            if (0 <= x * cellSize < gridSize) and (0 <= y * cellSize < gridSize):
                                newRect = pygame.Rect(
                                    y * cellSize, x * cellSize, cellSize, cellSize)
                                self.screen.fill(settings.GREEN, newRect)
                                pygame.draw.rect(
                                    self.screen, settings.GREEN, newRect, 2)
                # if (0 <= (currentPos[0] + 3) * cellSize < gridSize) and (0 <= (currentPos[1] + 4) * cellSize < gridSize):
                print(f"TURNING RIGHT\t{currentPos}")
                self.drawRobot(currentPos, cellSize, settings.GREEN,
                               settings.GREEN, settings.GREEN)
                self.bot.setCurrentPos(
                    currentPos[0] + 3, currentPos[1] + 4, 'S')
        elif currentPos[2] == 'S':
            if (0 <= (currentPos[0] + 4) * cellSize < gridSize) and (0 <= (currentPos[1] - 3) * cellSize < gridSize):
                for x in range(currentPos[0] - 1, currentPos[0] + 6):
                    for y in range(currentPos[1] - 4, currentPos[1] + 2):
                        if (x < currentPos[0] + 3) and (y < currentPos[1] - 1):
                            continue
                        else:
                            for obstacle in self.obstacles:
                                if (x == obstacle[0]) and (y == obstacle[1]):
                                    print(f"COLLISION!")
                                    return
                            if (0 <= x * cellSize < gridSize) and (0 <= y * cellSize < gridSize):
                                newRect = pygame.Rect(
                                    y * cellSize, x * cellSize, cellSize, cellSize)
                                self.screen.fill(settings.PINK, newRect)
                                pygame.draw.rect(
                                    self.screen, settings.PINK, newRect, 2)
                # if (0 <= (currentPos[0] + 4) * cellSize < gridSize) and (0 <= (currentPos[1] - 3) * cellSize < gridSize):
                print(f"TURNING RIGHT\t{currentPos}")
                self.drawRobot(currentPos, cellSize, settings.GREEN,
                               settings.GREEN, settings.GREEN)
                self.bot.setCurrentPos(
                    currentPos[0] + 4, currentPos[1] - 3, 'W')
        elif currentPos[2] == 'W':
            if (0 <= (currentPos[0] - 3) * cellSize < gridSize) and (0 <= (currentPos[1] - 4) * cellSize < gridSize):
                for x in range(currentPos[0] - 4, currentPos[0] + 2):
                    for y in range(currentPos[1] - 5, currentPos[1] + 2):
                        if (x < currentPos[0] - 1) and (y > currentPos[1] - 3):
                            continue
                        else:
                            for obstacle in self.obstacles:
                                if (x == obstacle[0]) and (y == obstacle[1]):
                                    print(f"COLLISION!")
                                    return
                            if (0 <= x * cellSize < gridSize) and (0 <= y * cellSize < gridSize):
                                newRect = pygame.Rect(
                                    y * cellSize, x * cellSize, cellSize, cellSize)
                                self.screen.fill(settings.PINK, newRect)
                                pygame.draw.rect(
                                    self.screen, settings.PINK, newRect, 2)
                # if (0 <= (currentPos[0] - 4) * cellSize < gridSize) and (0 <= (currentPos[1] - 3) * cellSize < gridSize):
                print(f"TURNING RIGHT\t{currentPos}")
                self.drawRobot(currentPos, cellSize, settings.GREEN,
                               settings.GREEN, settings.GREEN)
                self.bot.setCurrentPos(
                    currentPos[0] - 3, currentPos[1] - 4, 'N')

    def reverseTurnLeft(self, currentPos, gridSize, cellSize):
        if currentPos[2] == 'N':
            if (0 <= (currentPos[0] - 4) * cellSize < gridSize) and (0 <= (currentPos[1] - 3) * cellSize < gridSize):
                for x in range(currentPos[0] - 5, currentPos[0] + 2):
                    for y in range(currentPos[1] - 4, currentPos[1] + 2):
                        if (x > currentPos[0] - 3) and (y < currentPos[1] - 1):
                            continue
                        else:
                            for obstacle in self.obstacles:
                                if (x == obstacle[0]) and (y == obstacle[1]):
                                    print(f"COLLISION!")
                                    return
                            if (0 <= x * cellSize < gridSize) and (0 <= y * cellSize < gridSize):
                                newRect = pygame.Rect(
                                    y * cellSize, x * cellSize, cellSize, cellSize)
                                self.screen.fill(settings.GREEN, newRect)
                                pygame.draw.rect(
                                    self.screen, settings.GREEN, newRect, 2)
                # if (0 <= (currentPos[0] - 4) * cellSize < gridSize) and (0 <= (currentPos[1] - 3) * cellSize < gridSize):
                print(f"TURNING LEFT\t{currentPos}")
                self.drawRobot(currentPos, cellSize, settings.GREEN,
                               settings.GREEN, settings.GREEN)
                self.bot.setCurrentPos(
                    currentPos[0] - 4, currentPos[1] - 3, 'W')
        elif currentPos[2] == 'E':
            if (0 <= (currentPos[0] - 3) * cellSize < gridSize) and (0 <= (currentPos[1] + 4) * cellSize < gridSize):
                for x in range(currentPos[0] - 4, currentPos[0] + 2):
                    for y in range(currentPos[1] - 1, currentPos[1] + 6):
                        if (x < currentPos[0] - 1) and (y < currentPos[1] + 3):
                            continue
                        else:
                            for obstacle in self.obstacles:
                                if (x == obstacle[0]) and (y == obstacle[1]):
                                    print(f"COLLISION!")
                                    return
                            if (0 <= x * cellSize < gridSize) and (0 <= y * cellSize < gridSize):
                                newRect = pygame.Rect(
                                    y * cellSize, x * cellSize, cellSize, cellSize)
                                self.screen.fill(settings.GREEN, newRect)
                                pygame.draw.rect(
                                    self.screen, settings.GREEN, newRect, 2)
                # if (0 <= (currentPos[0] - 3) * cellSize < gridSize) and (0 <= (currentPos[1] + 4) * cellSize < gridSize):
                print(f"TURNING LEFT\t{currentPos}")
                self.drawRobot(currentPos, cellSize, settings.GREEN,
                               settings.GREEN, settings.GREEN)
                self.bot.setCurrentPos(
                    currentPos[0] - 3, currentPos[1] + 4, 'N')
        elif currentPos[2] == 'S':
            if (0 <= (currentPos[0] + 4) * cellSize < gridSize) and (0 <= (currentPos[1] + 3) * cellSize < gridSize):
                for x in range(currentPos[0] - 1, currentPos[0] + 6):
                    for y in range(currentPos[1] - 1, currentPos[1] + 5):
                        if (x < currentPos[0] + 3) and (y > currentPos[1] + 1):
                            continue
                        else:
                            for obstacle in self.obstacles:
                                if (x == obstacle[0]) and (y == obstacle[1]):
                                    print(f"COLLISION!")
                                    return
                            if (0 <= x * cellSize < gridSize) and (0 <= y * cellSize < gridSize):
                                newRect = pygame.Rect(
                                    y * cellSize, x * cellSize, cellSize, cellSize)
                                self.screen.fill(settings.GREEN, newRect)
                                pygame.draw.rect(
                                    self.screen, settings.GREEN, newRect, 2)
                # if (0 <= (currentPos[0] + 4) * cellSize < gridSize) and (0 <= (currentPos[1] + 3) * cellSize < gridSize):
                print(f"TURNING LEFT\t{currentPos}")
                self.drawRobot(currentPos, cellSize, settings.GREEN,
                               settings.GREEN, settings.GREEN)
                self.bot.setCurrentPos(
                    currentPos[0] + 4, currentPos[1] + 3, 'E')
        elif currentPos[2] == 'W':
            if (0 <= (currentPos[0] + 3) * cellSize < gridSize) and (0 <= (currentPos[1] - 4) * cellSize < gridSize):
                for x in range(currentPos[0] - 1, currentPos[0] + 5):
                    for y in range(currentPos[1] - 5, currentPos[1] + 2):
                        if (x > currentPos[0] + 1) and (y > currentPos[1] - 3):
                            continue
                        else:
                            for obstacle in self.obstacles:
                                if (x == obstacle[0]) and (y == obstacle[1]):
                                    print(f"COLLISION!")
                                    return
                            if (0 <= x * cellSize < gridSize) and (0 <= y * cellSize < gridSize):
                                newRect = pygame.Rect(
                                    y * cellSize, x * cellSize, cellSize, cellSize)
                                self.screen.fill(settings.GREEN, newRect)
                                pygame.draw.rect(
                                    self.screen, settings.GREEN, newRect, 2)
                # if (0 <= (currentPos[0] + 3) * cellSize < gridSize) and (0 <= (currentPos[1] - 4) * cellSize < gridSize):
                print(f"TURNING LEFT\t{currentPos}")
                self.drawRobot(currentPos, cellSize, settings.GREEN,
                               settings.GREEN, settings.GREEN)
                self.bot.setCurrentPos(
                    currentPos[0] + 3, currentPos[1] - 4, 'S')

    def moveNorthEast(self, currentPos, gridSize, cellSize):
        for y in range(currentPos[1] - 1, currentPos[1] + 2):
            for obstacle in self.obstacles:
                if (currentPos[0] - 2 == obstacle[0]) and (y == obstacle[1]):
                    print(f"COLLISION!")
                    return
        if (0 <= (currentPos[0] - 1) * cellSize < gridSize) and (0 <= currentPos[1] * cellSize < gridSize):
            print(f"YOU CLICKED THE NORTH BUTTON\t{currentPos}")
            self.bot.setCurrentPos(
                currentPos[0] - 1, currentPos[1], currentPos[2])
            print(self.bot.getCurrentPos())

    def movement(self, x, y, buttonLength, buttonWidth, currentPos):
        # move North
        if (685 < x < 685 + buttonLength) and (110 < y < 110 + buttonWidth):
            self.moveForward(currentPos, settings.GRID_LENGTH * settings.SCALING_FACTOR,
                             settings.GRID_CELL_LENGTH * settings.SCALING_FACTOR)
        # move South
        elif (685 < x < 685 + buttonLength) and (180 < y < 180 + buttonWidth):
            self.moveBackward(currentPos, settings.GRID_LENGTH * settings.SCALING_FACTOR,
                              settings.GRID_CELL_LENGTH * settings.SCALING_FACTOR)
        # move Forward East
        elif (720 < x < 720 + buttonLength) and (132.5 < y < 132.5 + buttonWidth):
            self.turnRight(currentPos, settings.GRID_LENGTH * settings.SCALING_FACTOR,
                           settings.GRID_CELL_LENGTH * settings.SCALING_FACTOR)
        # move Forward West
        elif (650 < x < 650 + buttonLength) and (132.5 < y < 132.5 + buttonWidth):
            self.turnLeft(currentPos, settings.GRID_LENGTH * settings.SCALING_FACTOR,
                          settings.GRID_CELL_LENGTH * settings.SCALING_FACTOR)
        # move Backward East
        elif (720 < x < 720 + buttonLength) and (160 < y < 160 + buttonWidth):
            self.reverseTurnRight(currentPos, settings.GRID_LENGTH * settings.SCALING_FACTOR,
                           settings.GRID_CELL_LENGTH * settings.SCALING_FACTOR)
        # move backward West
        elif (650 < x < 650 + buttonLength) and (160 < y < 160 + buttonWidth):
            self.reverseTurnLeft(currentPos, settings.GRID_LENGTH * settings.SCALING_FACTOR,
                          settings.GRID_CELL_LENGTH * settings.SCALING_FACTOR)
        # move North East
        elif (720 < x < 720 + buttonLength) and (107.5 < y < 107.5 + buttonWidth):
            print(f"YOU CLICKED THE NORTHEAST BUTTON\T{currentPos}")
            self.moveNorthEast(currentPos, settings.GRID_LENGTH * settings.SCALING_FACTOR,
                               settings.GRID_CELL_LENGTH * settings.SCALING_FACTOR)
        # move North West
        elif (650 < x < 650 + buttonLength) and (107.5 < y < 107.5 + buttonWidth):
            print(f"YOU CLICKED THE NORTHWEST BUTTON\T{currentPos}")
            self.moveNorthWest(currentPos, settings.GRID_LENGTH * settings.SCALING_FACTOR,
                               settings.GRID_CELL_LENGTH * settings.SCALING_FACTOR)
        # move South East
        elif (720 < x < 720 + buttonLength) and (182.5 < y < 182.5 + buttonWidth):
            print(f"YOU CLICKED THE SOUTHEAST BUTTON\T{currentPos}")
            self.moveSouthEast(currentPos, settings.GRID_LENGTH * settings.SCALING_FACTOR,
                               settings.GRID_CELL_LENGTH * settings.SCALING_FACTOR)
        # move South West
        elif (650 < x < 650 + buttonLength) and (182.5 < y < 182.5 + buttonWidth):
            print(f"YOU CLICKED THE SOUTHWEST BUTTON\T{currentPos}")
            self.moveSouthWest(currentPos, settings.GRID_LENGTH * settings.SCALING_FACTOR,
                               settings.GRID_CELL_LENGTH * settings.SCALING_FACTOR)

        '''
        cls.drawImage(img, 685, 110, settings.GREY, size, size)       # Forward N
        cls.drawImage(img, 685, 180, settings.GREY, size, size)       # Backward S

        cls.drawImage(img, 720, 132.5, settings.GREY, size, size)       # Forward E
        cls.drawImage(img, 650, 132.5, settings.GREY, size, size)       # Forward W
        cls.drawImage(img, 720, 160, settings.GREY, size, size)       # Backward E
        cls.drawImage(img, 650, 160, settings.GREY, size, size)       # Backward W

        cls.drawImage(img, 720, 107.5, settings.GREY, size, size)       # Slant Forward E
        cls.drawImage(img, 650, 107.5, settings.GREY, size, size)       # Slant Forward W
        cls.drawImage(img, 720, 182.5, settings.GREY, size, size)       # Slant Backward E
        cls.drawImage(img, 650, 182.5, settings.GREY, size, size)       # Slant Backward W
        '''

    def draw(cls, x, y):
        # start button
        cls.drawButtons(650, 500, settings.GREEN, 'START!', settings.BLACK,
                        settings.BUTTON_LENGTH, settings.BUTTON_WIDTH)
        # current cursor coordinates, change to robot
        cls.drawButtons(0, 600, settings.BLACK,
                        f"({x}, {y})", settings.WHITE, settings.BUTTON_LENGTH, settings.BUTTON_WIDTH)
        # supposedly current direction object is facing
        cls.drawButtons(150, 600, settings.BLACK, f"Direction: North",
                        settings.WHITE, settings.BUTTON_LENGTH * 2, settings.BUTTON_WIDTH)
        # set obstacles, asking for input from cmd prompt
        cls.drawButtons(650, 450, settings.GREEN, 'SET', settings.BLACK,
                        settings.BUTTON_LENGTH, settings.BUTTON_WIDTH)
        # reset grid button
        cls.drawButtons(650, 400, settings.GREY, 'RESET', settings.BLACK,
                        settings.BUTTON_LENGTH, settings.BUTTON_WIDTH)

        if len(cls.obstacles) != 0:
            cls.drawObstaclesButton(cls.obstacles, settings.RED)
        else:
            cls.drawObstaclesButton([], settings.RED)

    def runSimulation(self, bot):
        self.bot = deepcopy(bot)
        # bg = pygame.image.load(os.path.join("./images/", "white.png"))
        self.clock = pygame.time.Clock()
        # startingPosX = 0
        # startingPosY = (settings.GRID_LENGTH - settings.GRID_CELL_LENGTH) * settings.SCALING_FACTOR
        while True:
            self.drawGrid()
            # print(bot.getCurrentPos())
            currentPos = self.bot.getCurrentPos()
            self.drawRobot(currentPos, settings.GRID_CELL_LENGTH *
                           settings.SCALING_FACTOR, settings.RED, settings.BLUE, settings.LIGHT_BLUE)
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
                    if (650 < x < 650 + settings.BUTTON_LENGTH) and (500 < y < 500 + settings.BUTTON_WIDTH):
                        print(
                            "START BUTTON IS CLICKED!!! I REPEAT, START BUTTON IS CLICKED!!!")
                        grid, obstacles = app.initGrid()
                        app.runAlgo(grid, obstacles)
                    elif (650 < x < 650 + settings.BUTTON_LENGTH) and (450 < y < 450 + settings.BUTTON_WIDTH):
                        print("*****Setting obstacles*****")
                        self.obstacles = app.createObstacles(
                            settings.GRID_LENGTH // settings.GRID_CELL_LENGTH)
                        print("*****Drawing obstacles*****")
                        self.drawObstaclesButton(self.obstacles, settings.RED)
                    elif (650 < x < 650 + settings.BUTTON_LENGTH) and (400 < y < 400 + settings.BUTTON_WIDTH):
                        self.reset(bot)
                    elif (650 < x < 720 + settings.GRID_CELL_LENGTH * settings.SCALING_FACTOR) and (115 < y < 185 + settings.GRID_CELL_LENGTH * settings.SCALING_FACTOR):
                        self.movement(
                            x, y, 
                            settings.GRID_CELL_LENGTH * settings.SCALING_FACTOR, 25, 
                            currentPos)

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.moveForward(currentPos, settings.GRID_LENGTH * settings.SCALING_FACTOR,
                                         settings.GRID_CELL_LENGTH * settings.SCALING_FACTOR)
                    elif event.key == pygame.K_RIGHT:
                        self.turnRight(currentPos, settings.GRID_LENGTH * settings.SCALING_FACTOR,
                                       settings.GRID_CELL_LENGTH * settings.SCALING_FACTOR)
                    elif event.key == pygame.K_DOWN:
                        self.moveBackward(currentPos, settings.GRID_LENGTH * settings.SCALING_FACTOR,
                                          settings.GRID_CELL_LENGTH * settings.SCALING_FACTOR)
                    elif event.key == pygame.K_LEFT:
                        self.turnLeft(currentPos, settings.GRID_LENGTH * settings.SCALING_FACTOR,
                                      settings.GRID_CELL_LENGTH * settings.SCALING_FACTOR)

                    # elif (x < settings.GRID_LENGTH * settings.SCALING_FACTOR) and (y < settings.GRID_LENGTH * settings.SCALING_FACTOR):
                    #     ''' Each cell is 10x10 multiplied by scaling factor of 3 = 30x30px
                    #         if i want to get grid cell, take coordinate // (10 * 3) '''
                    #     self.selectObstacles(x // (10 * 3), y // ( 10 * 3), settings.GRID_CELL_LENGTH * settings.SCALING_FACTOR, settings.GREY)
            pygame.display.update()
