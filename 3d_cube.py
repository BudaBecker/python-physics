import pygame
import numpy as np
from math import cos, sin, radians

# Pygame init
pygame.init()
WIDTH, HEIGHT = 600, 700
screen = pygame.display.set_mode([WIDTH, HEIGHT])
font = pygame.font.SysFont("Arial", 20, bold= True)

# Global variables
FPS = 60
CUBE_SIZE = 300

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
        self.projected = [(0, 0)] * 8

    def get_vertices(self):
        return np.array([
            [-1,-1,-1], [1,-1,-1], [1,1,-1], [-1,1,-1],
            [-1,-1, 1], [1,-1, 1], [1,1, 1], [-1,1, 1]
        ], dtype= float)

    def rotate_cube(self):
        Ax, Ay, Az = self.angle

        # https://en.wikipedia.org/wiki/Rotation_matrix
        Rx = np.array([
            [1,       0,        0],
            [0, cos(Ax), -sin(Ax)],
            [0, sin(Ax),  cos(Ax)]
        ], dtype= float)
        Ry = np.array([
            [ cos(Ay), 0, sin(Ay)],
            [       0, 1,       0],
            [-sin(Ay), 0, cos(Ay)]
        ], dtype= float)
        Rz = np.array([
            [cos(Az), -sin(Az), 0],
            [sin(Az),  cos(Az), 0],
            [      0,        0, 1]
        ], dtype= float)
        
        # X @ Y = matrix-multiply X by Y // R.T is the transpose of the matrix R
        R = Rz @ Ry @ Rx
        self.vertices = (self.get_vertices() @ R.T)
        self.projected = [(x, y) for (x, y, z) in self.vertices] # Orthographic projection (ignoring the z-axis)
    
    def add_perspective_projection(self, d, camera_distance):
        # Adds perspective projection
        proj = []
        for (x, y, z) in self.vertices:
            z_adj = z + camera_distance
            if z_adj == 0:
                z_adj = 1e-6
            factor = d / z_adj
            proj.append((x*factor, y*factor))
            
        self.projected = proj
      
    def draw(self):
        edges = [
            (0,1),(1,2),(2,3),(3,0),   # front face
            (4,5),(5,6),(6,7),(7,4),   # back face
            (0,4),(1,5),(2,6),(3,7),   # connectors
        ]

        for (i, j) in edges:
            # Rescale and reposition to the center of the screen.
            pygame.draw.line(screen, WHITE, (self.projected[i][0]*self.size + WIDTH/2, self.projected[i][1]*self.size + HEIGHT/2), 
                                            (self.projected[j][0]*self.size + WIDTH/2, self.projected[j][1]*self.size + HEIGHT/2), 3)
        
        for (px, py) in self.projected:
            # Rescale and reposition to the center of the screen.
            pygame.draw.circle(screen, RED, (px*self.size + WIDTH/2, py*self.size + HEIGHT/2), 5)

def display_instruct():
    instructions = font.render("press             keys to move the cube or S to spin.", 1, WHITE)
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
    
    instructions = font.render("press P to change between perspective and orthographic projection.", 1, WHITE)
    screen.blit(instructions, (10, 40))
    
def main():
    cube = Cube(l= CUBE_SIZE/2)
    timer = pygame.time.Clock()
    running = True
    spinning = False
    projecting = False
    while running:
        pygame.display.set_caption(f"3D Cube, FPS: {int(timer.get_fps())}")
        timer.tick(60)
        screen.fill(BLACK)
        display_instruct()
        
        # Pygame events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if 's' ==pygame.key.name(event.key):
                    if not spinning:
                        spinning = True
                    else:
                        spinning = False
                if 'p' ==pygame.key.name(event.key):
                    if not projecting:
                        projecting = True
                    else:
                        projecting = False
                        
                        
        # Move if arrows
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            cube.angle += [radians(-2), 0, 0]
        elif keys[pygame.K_DOWN]:
            cube.angle += [radians(2), 0, 0]
        if keys[pygame.K_LEFT]:
            cube.angle += [0, radians(2), 0]
        elif keys[pygame.K_RIGHT]:
            cube.angle += [0, radians(-2), 0]
        
        if spinning:
            cube.angle += [radians(1), radians(1), radians(1)]
        
        # Cube att
        cube.rotate_cube()
        if projecting:
            cube.add_perspective_projection(d= 2, camera_distance= 3)
        cube.draw()
        
        pygame.display.update()
    pygame.quit()
if __name__ == "__main__":
    main()