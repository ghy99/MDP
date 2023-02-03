import pygame
import sys
import os
import settings


class Simulation():
    def __init__(self):
        pygame.init()
        self.running = True

        self.screen = pygame.display.set_mode((800, 650), pygame.HWSURFACE | pygame.DOUBLEBUF)
        self.clock = None
        pygame.mouse.set_visible(1)
        pygame.display.set_caption("Vroom Vroom Simulation")

    def drawGrid(cls):
        for x in range(0, settings.GRID_LENGTH, settings.GRID_CELL_LENGTH):
            for y in range(0, settings.GRID_LENGTH, settings.GRID_CELL_LENGTH):
                rect = pygame.Rect(x, y, settings.GRID_CELL_LENGTH)
                pygame.draw.rect(cls.screen, settings.WHITE, rect, 1)
    
    def runSimulation(self):
        bg = pygame.image.load(os.path.join("./images/", "white.png"))
        while True:
            self.drawGrid()
            self.clock = pygame.time.Clock()
            self.clock.tick(60)
            self.screen.blit(bg, (0, 0))
            x, y = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            pygame.display.update()