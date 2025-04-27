import pygame
import numpy as np

# Pygame init
pygame.init()
WIDTH, HEIGHT = 900, 800
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption("Lagrange's Equilateral Triangle Solution")
trail = pygame.Surface((WIDTH, HEIGHT), flags=pygame.SRCALPHA)
T = 2

# Global variables
FPS = 60
DT = 0.0001
STEPS_PER_FRAME = 250
BODY_RADIUS = 15
G = 1
MASS = 1
A = 1.2
SCALE = 350
W = np.sqrt(((G*MASS)/(A**3))*np.sqrt(3))

# RGB
x = 50; BG_COLOR = (x, x, x)
RED = (255, 50, 50)
GREEN = (50, 255, 50)
BLUE = (50, 50, 255)

# Bodies class
class Body:
    def __init__(self, init_pos, init_vel, mass, color, id):
        self.id = id
        self.color = color
        self.mass = mass
        self.acc = np.zeros(2, dtype=float)
        self.vel = np.array(init_vel, dtype=float) * W
        self.pos = np.array(init_pos, dtype=float)

    def dynamic_calculations(self, body_list):
        acc = np.zeros(2, dtype=float)
        for other in body_list:
            if other is self:
                continue
            
            diff_vect = self.pos - other.pos
            dist = np.linalg.norm(diff_vect) 
            
            if dist > 0:
                acc -= (G*other.mass*diff_vect) / (dist)**3
        
        self.acc = acc
    
    def att_pos(self):
        self.vel += self.acc * DT
        self.pos += self.vel * DT
                            
    def draw_body(self):
        # As we're using Lagrange's solution (center in (0, 0)), we need to re-size the schema to our canvas.
        x = WIDTH/2 + SCALE * self.pos[0]
        y = HEIGHT/2 - SCALE * self.pos[1]
        pygame.draw.circle(trail, self.color, (x, y), T)
        pygame.draw.circle(screen, self.color, (x, y), BODY_RADIUS)
        
def main():
    bodies = [
        # These values are determined by calculating the vertices of a equilateral triangle.
        # Fun fact: with three equal masses, Lagrange’s solution is actually unstable. For it to be stable, try changin
        # one of the three masses to be below about 4% of the sum of the other two masses (< 0.06, in this example).
        # If you change one of the masses to be <= 0.06, the program will change it's scale and the body's radius for a better view.
        Body(init_pos= (-A/2, -A*np.sqrt(3)/6), init_vel= (A*np.sqrt(3)/6, -A/2), mass= MASS, color= RED, id= 0),
        Body(init_pos= (A/2, -A*np.sqrt(3)/6), init_vel= (A*np.sqrt(3)/6, A/2), mass= MASS, color= GREEN, id= 1),
        Body(init_pos= (0, A*np.sqrt(3)/3), init_vel= (-A*np.sqrt(3)/3, 0), mass= MASS, color= BLUE, id= 2)
    ]
    for body in bodies:
        if body.mass <= 0.06:
            global BODY_RADIUS, SCALE, T
            BODY_RADIUS = 7
            SCALE = 50
            T = 1
    timer = pygame.time.Clock()
    running = True
    while running:
        timer.tick(FPS)
        screen.fill(BG_COLOR)
        trail.fill((0,0,0,1), special_flags=pygame.BLEND_RGBA_SUB)
        screen.blit(trail, (0,0))
        
        # Pygame events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Calculate and Draw bodies.
        for _ in range(STEPS_PER_FRAME):
            for body in bodies:
                body.dynamic_calculations(bodies)
            for body in bodies:
                body.att_pos()
                body.draw_body()
                
        pygame.display.update()
    pygame.quit()
if __name__ == "__main__":
    main()