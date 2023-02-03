import pygame
import sys
import os

pygame.init()
clock = pygame.time.Clock()
# screen = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
screen = pygame.display.set_mode((600, 600), pygame.HWSURFACE | pygame.DOUBLEBUF)
bg = pygame.image.load(os.path.join("./images/", "white.png"))
pygame.mouse.set_visible(0)
pygame.display.set_caption("Vroom Vroom Simulation")
while True:
    clock.tick(60)
    screen.blit(bg, (0, 0)) # copy background image onto canvas in display
    x, y = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    pygame.display.update()