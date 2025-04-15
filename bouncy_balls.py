#TODO: Fix retention so balls stop completely after some time. (how tf do i do that)

import pygame
import numpy as np
from random import choice, randint

# Pygame init
pygame.init()
WIDTH = 900
HEIGHT = 800
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption("Bouncy Balls with Collisions")
myfont = pygame.font.SysFont("monospace", 15)

# Global variables
FPS = 60
BG_COLOR = (50, 50, 50)
GRAVITY = 0
BALLS_NUM_INIT = 15
RETENTION = 1 # smt between 0 and 1

# Ball Class
class Ball:
    def __init__(self, x_pos, y_pos, y_vel, x_vel, radius, color, mass, retention, id):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.radius = radius
        self.color = color
        self.mass = mass
        self.y_vel = y_vel
        self.x_vel = x_vel
        self.id = id
        self.retention = retention
        
    def draw_ball(self):
        pygame.draw.circle(screen, self.color, (self.x_pos, self.y_pos), self.radius)

    def check_moviment(self):
        if (self.y_pos >= HEIGHT - self.radius):
            self.y_vel *= -1 * self.retention
            self.y_pos = HEIGHT - self.radius
            
        if (self.y_pos <= self.radius):
            self.y_vel *= -1 * self.retention
            self.y_pos = self.radius
            
        if (self.x_pos >= WIDTH - self.radius):
            self.x_vel *= -1 * self.retention
            self.x_pos = WIDTH - self.radius
        
        if (self.x_pos <= self.radius):
            self.x_vel *= -1 * self.retention
            self.x_pos = self.radius
        
        #Check for gravity if enabled
        if self.y_pos < HEIGHT - self.radius:
            self.y_vel += GRAVITY
        
    def update_pos(self):
        self.y_pos += self.y_vel
        self.x_pos += self.x_vel
    
    def check_collision(self, balls): 
        for other in balls:
            if self.id == other.id:
                continue
            else:
                self_pos = np.array((self.x_pos, self.y_pos), dtype= float)
                other_pos = np.array((other.x_pos, other.y_pos), dtype= float)
                distance = np.linalg.norm(self_pos - other_pos)
                sum_radi = self.radius + other.radius
                
                if distance == 0: # Avoiding /0
                    self.x_pos += 1
                    other.x_pos -= 1
                elif distance <= sum_radi:
                    # Fix if overlap
                    if distance < sum_radi:
                        overlap = sum_radi - distance
                        normal_vec = (other_pos - self_pos)/distance
                        self_pos -= normal_vec * overlap
                        other_pos += normal_vec * overlap
                        self.x_pos, self.y_pos = self_pos
                        other.x_pos, other.y_pos = other_pos
                    
                    # Setting up velocity vectors
                    self_vel_vec = np.array((self.x_vel, self.y_vel), dtype=float)
                    other_vel_vec = np.array((other.x_vel, other.y_vel), dtype=float)
                    
                    # Elastic Collision Formula
                    rel_pos_other_self = other_pos - self_pos
                    rel_vel_other_self = other_vel_vec - self_vel_vec
                    rel_pos_self_other = self_pos - other_pos
                    rel_vel_self_other = self_vel_vec - other_vel_vec
                    dot_product_self = np.dot(rel_vel_other_self, rel_pos_other_self)
                    dot_product_other = np.dot(rel_vel_self_other, rel_pos_self_other)
                    self_num_scalar = 2 * other.mass * dot_product_self
                    other_num_scalar = 2 * self.mass * dot_product_other
                    den = (self.mass + other.mass) * np.linalg.norm(rel_pos_other_self)**2
                    self_vel_prime = self_vel_vec + (self_num_scalar / den) * rel_pos_other_self
                    other_vel_prime = other_vel_vec + (other_num_scalar / den) * rel_pos_self_other
                    
                    # Updating Velocity
                    self.x_vel, self.y_vel = self_vel_prime * self.retention
                    other.x_vel, other.y_vel = other_vel_prime * other.retention
                                   
# Functions
next_id_ball = 1
def create_balls(balls_list, num_balls):
    global next_id_ball
    colors = list(pygame.color.THECOLORS.keys())
    balls = balls_list
    for i in range(1, num_balls+1):
        radius = randint(10, 40)
        mass = (100*radius/3) + 20/3  # Weird proporsion i think is good
        ball = Ball(
            x_pos= randint(radius, WIDTH-radius), 
            y_pos= randint(radius, HEIGHT-radius), 
            x_vel= randint(1, 5), 
            y_vel= randint(1, 5), 
            radius= radius, 
            mass= mass, 
            color= choice(colors),
            retention= RETENTION,
            id= next_id_ball
            )
        next_id_ball += 1
        
        balls.append(ball)
    return balls

# Main game loop
def main():
    balls = []
    balls = create_balls(balls, BALLS_NUM_INIT)
    timer = pygame.time.Clock()
    running = True
    while running:
        timer.tick(FPS)
        screen.fill(BG_COLOR)

        # Pygame events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    balls = create_balls(balls, 1)
                elif event.button == 3:
                    if len(balls) > 0:
                        balls.pop(randint(0, len(balls)-1))
            elif event.type == pygame.KEYDOWN:
                if pygame.key.name(event.key):
                    global GRAVITY
                    if GRAVITY == 0:
                        GRAVITY = 0.5
                    else:
                        GRAVITY = 0

        # Balls interactions
        for ball in balls:
            ball.check_collision(balls)
            ball.draw_ball()
            ball.update_pos()
            ball.check_moviment()
        
        # Print Kinetic Enery
        Ec = 0
        for ball in balls:
            Ec += 0.5 * ball.mass * np.linalg.norm((ball.x_vel, ball.y_vel))**2
        energy = myfont.render(f"Ec = {Ec}", 1, (255,255,0))
        screen.blit(energy, (10, 50))
        instructions = myfont.render(f"G: Add/Remove Gravity", 1, (255,255,0))
        screen.blit(instructions, (10, 30))
        instructions = myfont.render(f"mouse1 create ball / mouse2 delete ball", 1, (255,255,0))
        screen.blit(instructions, (10, 10))
        
        pygame.display.update()
    pygame.quit()
          
if __name__ == "__main__":
    main()