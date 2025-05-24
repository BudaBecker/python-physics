import pygame
import numpy as np
from math import sin, cos, radians

# Pygame init
pygame.init()
WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode([WIDTH, HEIGHT])
font = pygame.font.SysFont("Arial", 20, bold= True)

# Global variables
FPS = 60
CUBE_SIZE = 250

# RGB
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 50, 50)

# Class tesseract
class Tesseract:
    def __init__(self):
        pass
    
    def get_vertices(self):
        return np.array([
            [-1, -1, -1, -1],
            [-1, -1, -1,  1],
            [-1, -1,  1, -1],
            [-1, -1,  1,  1],
            [-1,  1, -1, -1],
            [-1,  1, -1,  1],
            [-1,  1,  1, -1],
            [-1,  1,  1,  1],
            [ 1, -1, -1, -1],
            [ 1, -1, -1,  1],
            [ 1, -1,  1, -1],
            [ 1, -1,  1,  1],
            [ 1,  1, -1, -1],
            [ 1,  1, -1,  1],
            [ 1,  1,  1, -1],
            [ 1,  1,  1,  1]
        ], dtype= float)

# Main game loop
def main():
    timer = pygame.time.Clock()
    running = True
    while running:
        screen.fill(BLACK)
        timer.tick(FPS)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
        pygame.display.update()
    pygame.quit()
if __name__ == "__main__":
    main()