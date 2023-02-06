import pygame
import sys
import os
import settings
import app


class Simulation():
    def __init__(self):
        pygame.init()
        self.running = True
        # window size = 800, 650
        self.font = pygame.font.SysFont('Arial', 25)
        self.screen = pygame.display.set_mode((800, 650), pygame.HWSURFACE | pygame.DOUBLEBUF)
        self.clock = None
        pygame.mouse.set_visible(1)
        pygame.display.set_caption("Vroom Vroom Simulation")
        self.screen.fill(settings.BLACK)

    def drawGrid(cls):
        for x in range(0, settings.GRID_LENGTH * settings.SCALING_FACTOR, settings.GRID_CELL_LENGTH * settings.SCALING_FACTOR):
            for y in range(0, settings.GRID_LENGTH * settings.SCALING_FACTOR, settings.GRID_CELL_LENGTH * settings.SCALING_FACTOR):
                rect = pygame.Rect(x, y, settings.GRID_CELL_LENGTH * settings.SCALING_FACTOR, settings.GRID_CELL_LENGTH * settings.SCALING_FACTOR)
                pygame.draw.rect(cls.screen, settings.WHITE, rect, 2)
    
    ''' How to add texts?? '''
    def drawButtons(cls, xpos, ypos, bgcolor, text, textColor, length, width):
        startButton = pygame.Rect(xpos, ypos, length, width)
        pygame.draw.rect(cls.screen, bgcolor, startButton)
        text = cls.font.render(text, True, textColor)
        cls.screen.blit(text, text.get_rect(center=(startButton.x + (length//2), startButton.y + (width//2))))

    def selectObstacles(cls, x, y, cellSize, color):
        newRect = pygame.Rect(x * cellSize, y * cellSize, cellSize, cellSize)
        cls.screen.fill(color, newRect)
        pygame.draw.rect(cls.screen, color, newRect, 2)

    def drawObstaclesButton(cls, obstacles, color):
        size = settings.GRID_CELL_LENGTH * settings.SCALING_FACTOR
        #     self.selectObstacles(x // (10 * 3), y // ( 10 * 3), 
        #     settings.GRID_CELL_LENGTH * settings.SCALING_FACTOR, 
        #     settings.GREY)
        for i in obstacles:
            print(i)
            if i[2] == 'N':
                newRect = pygame.Rect((i[0]) * size, (i[1] - 2) * size, size, 2)
                cls.screen.fill(color, newRect)
                pygame.draw.rect(cls.screen, color, newRect, 2)
            elif i[2] == 'E':
                newRect = pygame.Rect((i[0]) * size, (i[1] - 2) * size, size, 2)
                cls.screen.fill(color, newRect)
                pygame.draw.rect(cls.screen, color, newRect, 2)
            elif i[2] == 'S':
                pass
            elif i[2] == 'W':
                pass
        # cls.drawButtons(685, 120, settings.GREY, 'N', settings.BLACK, size, size)    # N
        # cls.drawButtons(655, 150, settings.GREY, 'E', settings.BLACK, size, size)    # E
        # cls.drawButtons(685, 180, settings.GREY, 'S', settings.BLACK, size, size)    # S
        # cls.drawButtons(715, 150, settings.GREY, 'W', settings.BLACK, size, size)    # W

    def draw(cls, x, y):
        # start button
        cls.drawButtons(650, 500, settings.GREEN, 'START!', settings.BLACK, settings.BUTTON_LENGTH, settings.BUTTON_WIDTH)    
        # current cursor coordinates, change to robot
        cls.drawButtons(0, 600, settings.BLACK, f"({x}, {y})", settings.WHITE, settings.BUTTON_LENGTH, settings.BUTTON_WIDTH)
        # supposedly current direction object is facing
        cls.drawButtons(150, 600, settings.BLACK, f"Direction: North", settings.WHITE, settings.BUTTON_LENGTH * 2, settings.BUTTON_WIDTH)
        # set obstacles, asking for input from cmd prompt
        cls.drawButtons(650, 400, settings.GREEN, 'SET', settings.BLACK, settings.BUTTON_LENGTH, settings.BUTTON_WIDTH)

    def runSimulation(self):
        # bg = pygame.image.load(os.path.join("./images/", "white.png"))
        self.clock = pygame.time.Clock()
        startingPosX = 0
        startingPosY = (settings.GRID_LENGTH - settings.GRID_CELL_LENGTH) * settings.SCALING_FACTOR
        while True:
            self.drawGrid()
            
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
                    if (650 < x < x + settings.BUTTON_LENGTH) and (500 < y < y + settings.BUTTON_WIDTH):
                        print("START BUTTON IS CLICKED!!! I REPEAT, START BUTTON IS CLICKED!!!")
                        grid, obstacles = app.initGrid()
                        app.runAlgo(grid, obstacles)
                    elif (650 < x < x + settings.BUTTON_LENGTH) and (400 < y < y + settings.BUTTON_WIDTH):
                        print("*****Setting obstacles*****")
                        obstacles = app.createObstacles(settings.GRID_LENGTH // settings.GRID_CELL_LENGTH)
                        print("*****Drawing obstacles*****")
                        self.drawObstaclesButton(obstacles, settings.RED)
                    # elif (x < settings.GRID_LENGTH * settings.SCALING_FACTOR) and (y < settings.GRID_LENGTH * settings.SCALING_FACTOR):
                    #     ''' Each cell is 10x10 multiplied by scaling factor of 3 = 30x30px
                    #         if i want to get grid cell, take coordinate // (10 * 3) '''
                    #     self.selectObstacles(x // (10 * 3), y // ( 10 * 3), settings.GRID_CELL_LENGTH * settings.SCALING_FACTOR, settings.GREY)
            pygame.display.update()

