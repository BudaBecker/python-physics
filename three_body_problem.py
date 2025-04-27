import pygame
import numpy as np

# Pygame init
pygame.init()
WIDTH = 900
HEIGHT = 800
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption("The Chaotic Three-Body Problem")

# Global variables
FPS = 60
DT = 0.005
STEPS_PER_FRAME = 100
x = 120; BG_COLOR = (x, x, x)
BODY_RADIUS = 7
G = 5
MASSES = {
    0: 1200,
    1: 1200,
    2: 1200
}

# RGB
BLACK = (0, 0, 0)
TJ_COLORS = {
    0: (255, 50, 50),
    1: (50, 255, 50),
    2: (50, 50, 255)
}

# Bodies Class
class Body:
    def __init__(self, init_pos, color, mass, tj_color, id):
        self.id = id
        self.mass = mass
        # init vel and acc = Vect(0)
        self.acc = np.zeros(2, dtype=float)
        self.vel = np.zeros(2, dtype=float)
        self.pos = np.array(init_pos, dtype=float)
        # Colors
        self.tj_color = tj_color
        self.color = color 

    def dynamic_calculations(self, body_list):
        acc = np.zeros(2, dtype=float)
        for other in body_list:
            if other is self:
                continue
            
            diff_vect = self.pos - other.pos
            dist = np.linalg.norm(diff_vect) 
            
            if dist >= BODY_RADIUS*2:
                acc -= (G*other.mass*diff_vect) / (dist)**3
        
        self.acc = acc
    
    def att_pos(self):
        prev = self.pos.copy()
        self.vel += self.acc * DT
        self.pos += self.vel * DT
        return prev
                            
    def draw_body(self):
        pygame.draw.circle(screen, self.color, self.pos, BODY_RADIUS)
           
# Main game loop
def main():
    bodies_tj = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    bodies = []
    timer = pygame.time.Clock()
    running = True
    while running:
        timer.tick(FPS)
        screen.fill(BG_COLOR)
        screen.blit(bodies_tj, (0, 0))
        
        # Pygame events
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # Create new body
            if (event.type == pygame.MOUSEBUTTONDOWN) and (len(bodies) < 3): 
                bodies.append(Body(
                    init_pos= mouse_pos,
                    color= BLACK, 
                    mass= MASSES[len(bodies)],
                    tj_color= TJ_COLORS[len(bodies)],
                    id= len(bodies)
                    ))
        
        # Calculate physics with multiple small steps per frame to avoid very large accelerations, occurring multiples slingshots.
        for _ in range(STEPS_PER_FRAME):
            if len(bodies) == 3:
                for body in bodies:
                    body.dynamic_calculations(bodies)
            for body in bodies:
                if len(bodies) == 3:
                    prev = body.att_pos()
                    pygame.draw.line(bodies_tj, body.tj_color, prev, body.pos, width= 2)
                body.draw_body()
                
        pygame.display.update()
    pygame.quit()
if __name__ == "__main__":
    main()