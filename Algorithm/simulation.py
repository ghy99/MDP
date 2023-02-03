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
    def drawButtons(cls, xpos, ypos, color, text):
        startButton = pygame.Rect(xpos, ypos, settings.BUTTON_LENGTH, settings.BUTTON_WIDTH)
        pygame.draw.rect(cls.screen, color, startButton)
        text = cls.font.render(text, True, (settings.BLACK))
        cls.screen.blit(text, text.get_rect(center=(startButton.x + (settings.BUTTON_LENGTH//2), startButton.y + (settings.BUTTON_WIDTH//2))))

    def runSimulation(self):
        # bg = pygame.image.load(os.path.join("./images/", "white.png"))
        self.clock = pygame.time.Clock()
        
        while True:
            self.drawGrid()
            self.drawButtons(650, 500, settings.GREEN, 'START!')    # start button
            self.clock.tick(10)     # 10 frames per second apparently
            # self.screen.blit(bg, (0, 0))
            x, y = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if (650 < x < x + settings.BUTTON_LENGTH) and (500 < y < y + settings.BUTTON_WIDTH):
                        print("START BUTTON IS CLICKED!!! I REPEAT, START BUTTON IS CLICKED!!!")
                        grid, obstacles = app.initGrid()
                        app.runAlgo(grid, obstacles)
                    elif (x < settings.GRID_LENGTH * settings.SCALING_FACTOR) and (y < settings.GRID_LENGTH * settings.SCALING_FACTOR):
                        ''' Each cell is 10x10 multiplied by scaling factor of 3 = 30x30px
                            if i want to get grid cell, take coordinate // (10 * 3) '''
                        cellCoord = (x // (10 * 3), y // (10 * 3))
                        print(f"Coordinates: {cellCoord}")
                        
                        newRect = pygame.Rect((x // (10 * 3)) * settings.GRID_CELL_LENGTH * settings.SCALING_FACTOR, (y // (10 * 3)) * settings.GRID_CELL_LENGTH * settings.SCALING_FACTOR, settings.GRID_CELL_LENGTH * settings.SCALING_FACTOR, settings.GRID_CELL_LENGTH * settings.SCALING_FACTOR)
                        self.screen.fill(settings.GREY, newRect)
                        pygame.draw.rect(self.screen, settings.GREY, newRect, 2)
            pygame.display.update()

