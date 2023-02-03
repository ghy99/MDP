import pygame
import sys
import os
import settings


class Simulation():
    def __init__(self):
        pygame.init()
        self.running = True
        # window size = 800, 650
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
    
    def drawButtons(cls, xpos, ypos, color):
        startButton = pygame.Rect(xpos, ypos, settings.BUTTON_LENGTH, settings.BUTTON_WIDTH)
        pygame.draw.rect(cls.screen, color, startButton)

    def runSimulation(self):
        # bg = pygame.image.load(os.path.join("./images/", "white.png"))
        self.clock = pygame.time.Clock()
        self.drawGrid()
        self.drawButtons(50, 500, settings.PINK)
        while True:
            
            self.clock.tick(10)     # 10 frames per second apparently
            # self.screen.blit(bg, (0, 0))
            x, y = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            pygame.display.update()

