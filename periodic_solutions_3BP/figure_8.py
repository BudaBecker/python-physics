import pygame
import numpy as np

# Pygame init
pygame.init()
WIDTH, HEIGHT = 900, 800
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption("Figure-8 Solution")
trail = pygame.Surface((WIDTH, HEIGHT), flags=pygame.SRCALPHA)

# Global variables
FPS = 60
DT = 0.001
STEPS_PER_FRAME = 25
BODY_RADIUS = 15
G = 1
SCALE = 380

# RGB
x = 50; BG_COLOR = (x, x, x)
RED = (255, 50, 50)
GREEN = (50, 255, 50)
BLUE = (50, 50, 255)

# Bodies Class
class Body:
    def __init__(self, init_pos, init_vel, mass, color, id):
        self.id = id
        self.color = color
        self.mass = mass
        self.acc = np.zeros(2, dtype=float)
        self.vel = np.array(init_vel, dtype=float)
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
        # As we're using Cris Moore's solution (center in (0, 0)), we need to re-size the schema to our canvas.
        x = int(WIDTH/2 + SCALE * self.pos[0])
        y = int(HEIGHT/2 - SCALE * self.pos[1])
        pygame.draw.circle(trail, self.color, (x,y), 2)
        pygame.draw.circle(screen, self.color, (x, y), BODY_RADIUS)     
   
# Main game loop
def main():
    bodies = [
        # These values are already already determined by Cris Moore's solution, including mass = 1 and G = 1.
        Body(init_pos= (0.97000436, -0.24308753), init_vel= (0.466203685, 0.43236573), mass= 1, color= RED, id= 0),
        Body(init_pos= (-0.97000436, 0.24308753), init_vel= (0.466203685, 0.43236573), mass= 1, color= GREEN, id= 1),
        Body(init_pos= (0, 0), init_vel= (-0.93240737 , -0.86473146), mass= 1, color= BLUE, id= 2)
    ]
    timer = pygame.time.Clock()
    running = True
    while running:
        timer.tick(FPS)
        screen.fill(BG_COLOR)
        trail.fill((0,0,0,3), special_flags=pygame.BLEND_RGBA_SUB)
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