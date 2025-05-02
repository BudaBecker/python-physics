import pygame
import numpy as np
from math import cos, sin, radians

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

#Cube class
class Cube:
    def __init__(self, l):
        self.size = l
        self.vertices = self.get_vertices()
        self.angle = np.zeros(3, dtype= float)

    def get_vertices(self):
        return np.array([
            [0,0,0], [1,0,0], [1,1,0], [0,1,0],
            [0,0,1], [1,0,1], [1,1,1], [0,1,1]
        ], dtype= float)

    def rotate_cube(self):
        Ax, Ay, Az = self.angle
        
        # keep cube centered on the screen
        center = np.array([0.5, 0.5, 0.5], dtype= float)
        V = self.get_vertices() - center

        # https://en.wikipedia.org/wiki/Rotation_matrix
        Rx = np.array([
            [1,       0,        0],
            [0, cos(Ax), -sin(Ax)],
            [0, sin(Ax),  cos(Ax)]
        ])
        Ry = np.array([
            [ cos(Ay), 0, sin(Ay)],
            [       0, 1,       0],
            [-sin(Ay), 0, cos(Ay)]
        ])
        Rz = np.array([
            [cos(Az), -sin(Az), 0],
            [sin(Az),  cos(Az), 0],
            [      0,        0, 1]
        ])
        
        # X @ Y = matrix-multiply X by Y // R.T is the transpose of the matrix R
        R = Rz @ Ry @ Rx
        self.vertices = (V @ R.T) + center
        
    def draw(self):
        edges = [
            (0,1),(1,2),(2,3),(3,0),   # front face
            (4,5),(5,6),(6,7),(7,4),   # back face
            (0,4),(1,5),(2,6),(3,7),   # connectors
        ]

        for i, j in edges:
            pygame.draw.line(screen, WHITE, 
                             (self.vertices[i][0]*self.size + (WIDTH-self.size)/2, self.vertices[i][1]*self.size + (HEIGHT-self.size)/2), 
                             (self.vertices[j][0]*self.size + (WIDTH-self.size)/2, self.vertices[j][1]*self.size + (HEIGHT-self.size)/2),
                             3)
        
        for point in self.vertices:
            pygame.draw.circle(screen, RED, (point[0]*self.size + (WIDTH-self.size)/2, point[1]*self.size + (HEIGHT-self.size)/2), 5)

def display_instruct():
    instructions = font.render("press             keys to move the cube", 1, WHITE)
    arrows = [
        font.render("↑", 1, WHITE),
        font.render("↓", 1, WHITE),
        font.render("→", 1, WHITE),
        font.render("←", 1, WHITE),
    ]
    screen.blit(instructions, (10, 10))
    screen.blit(arrows[0], (80, 0))
    screen.blit(arrows[1], (80, 19))
    screen.blit(arrows[2], (85, 10))
    screen.blit(arrows[3], (65, 10))
    
def main():
    cube = Cube(l= CUBE_SIZE)
    timer = pygame.time.Clock()
    running = True
      
    while running:
        pygame.display.set_caption(f"3D Cube, FPS: {int(timer.get_fps())}")
        timer.tick(60)
        screen.fill(BLACK)
        display_instruct()
        
        # Pygame events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            cube.angle += [radians(2), 0, 0]
        elif keys[pygame.K_DOWN]:
            cube.angle += [radians(-2), 0, 0]
        if keys[pygame.K_LEFT]:
            cube.angle += [0, radians(2), 0]
        elif keys[pygame.K_RIGHT]:
            cube.angle += [0, radians(-2), 0]
        
        # Cube att
        cube.rotate_cube()
        cube.draw()
        
        pygame.display.update()
    pygame.quit()
if __name__ == "__main__":
    main()