import pygame
from sys import exit
pygame.init()

main_display = pygame.display.set_mode((800, 600))

running = True

clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    main_display.fill((0, 0, 0))

    pygame.display.flip()

    clock.tick(60)

pygame.quit()

