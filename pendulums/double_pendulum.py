import math
import pygame
import random

# Pygame init
pygame.init()
WIDTH = 1000
HEIGHT = 800
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption("Double Pendulum, Chaos Theory")

# Global physics variables
FPS = 60
L_1 = 200
L_2 = 200
M_1 = 10
M_2 = 10
AIR_FRICTION = 1
STATIC_POINT = (WIDTH/2, 275)

# Global custom variables
WEIGHT_1_RADIUS = 15
WEIGHT_2_RADIUS = 15
STR_D_1 = 7 + WEIGHT_1_RADIUS + L_1
STR_D_2 = 2*WEIGHT_2_RADIUS + L_2
BG_COLOR = (50, 50, 50)

# Class Pendulum
class Pendulum:
    def __init__(self, color, angle_init_1, angle_init_2):
        # initial state
        self.angle_1 = math.radians(angle_init_1)
        self.angle_2 = math.radians(angle_init_2)
        self.angle_vel_1 = 0
        self.angle_vel_2 = 0
        self.angle_acc_1 = 0
        self.angle_acc_2 = 0
        self.x_pos_1 = STR_D_1 * math.sin(self.angle_1) + STATIC_POINT[0]
        self.y_pos_1 = STR_D_1 * math.cos(self.angle_1) + STATIC_POINT[1]
        self.x_pos_2 = STR_D_2 * math.sin(self.angle_2) + self.x_pos_1
        self.y_pos_2 = STR_D_1 * math.cos(self.angle_2) + self.y_pos_1

        # constants
        self.mass_1 = M_1
        self.mass_2 = M_2
        self.weight_radius_1 = WEIGHT_1_RADIUS
        self.weight_radius_2 = WEIGHT_2_RADIUS
        self.color = color

    def draw_scheme(self):
        pygame.draw.line(screen, self.color, STATIC_POINT, (self.x_pos_1, self.y_pos_1), 2)
        pygame.draw.circle(screen, self.color, (self.x_pos_1, self.y_pos_1), self.weight_radius_1)
        pygame.draw.line(screen, self.color, (self.x_pos_1, self.y_pos_1), (self.x_pos_2, self.y_pos_2), 2)
        pygame.draw.circle(screen, self.color, (self.x_pos_2, self.y_pos_2), self.weight_radius_2)
    
    def check_angles(self):
        prev = (self.x_pos_2, self.y_pos_2)
        # For θ1''
        num1 = -GRAVITY * (2*self.mass_1 + self.mass_2) * math.sin(self.angle_1)
        num2 = -self.mass_2 * GRAVITY * math.sin(self.angle_1 - 2*self.angle_2)
        num3 = 2 * math.sin(self.angle_1 - self.angle_2)
        num4 = (self.angle_vel_2**2) * STR_D_2 + (self.angle_vel_1**2) * STR_D_1 * math.cos(self.angle_1 - self.angle_2)
        den = (2*self.mass_1 + self.mass_2 - self.mass_2 * math.cos(2*self.angle_1 - 2*self.angle_2))
        self.angle_acc_1 = (num1 + num2 + (num3 * -1 * self.mass_2) * num4) / (den * STR_D_1)
        
        # For θ2''
        num1 = num3
        num2 = (self.angle_vel_1**2) * STR_D_1 * (self.mass_1 + self.mass_2)
        num3 = GRAVITY * (self.mass_1 + self.mass_2) * math.cos(self.angle_1)
        num4 = (self.angle_vel_2**2) * STR_D_2 * self.mass_2 * math.cos(self.angle_1 - self.angle_2)
        self.angle_acc_2 = (num1 * (num2 + num3 + num4)) / (den * STR_D_2)

        # Updating angles
        self.angle_vel_1 += self.angle_acc_1
        self.angle_vel_2 += self.angle_acc_2
        self.angle_vel_1 *= AIR_FRICTION
        self.angle_vel_2 *= AIR_FRICTION
        self.angle_1 += self.angle_vel_1
        self.angle_2 += self.angle_vel_2
        
        # Updating positions
        self.x_pos_1 = STR_D_1 * math.sin(self.angle_1) + STATIC_POINT[0]
        self.y_pos_1 = STR_D_1 * math.cos(self.angle_1) + STATIC_POINT[1]
        self.x_pos_2 = STR_D_2 * math.sin(self.angle_2) + self.x_pos_1
        self.y_pos_2 = STR_D_1 * math.cos(self.angle_2) + self.y_pos_1
        
        return prev

# Draw pin
def draw_static_point():
    pygame.draw.circle(screen, (150, 150, 150), STATIC_POINT, 7)
    pygame.draw.circle(screen, (0, 0, 0), STATIC_POINT, 4)

# Main game loop
def main():
    global GRAVITY
    GRAVITY = 0
    pend_tj = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    pendulums = [
        Pendulum(color= (255, 20, 20), angle_init_1= 90, angle_init_2= 90),
        Pendulum(color= (20, 255, 90), angle_init_1= 90, angle_init_2= 89.9),  # only .1° difference!
        Pendulum(color= (0, 136, 255), angle_init_1= 90, angle_init_2= 89.8),
    ]
    timer = pygame.time.Clock()
    running = True
    while running:
        timer.tick(FPS)
        screen.fill(BG_COLOR)
        screen.blit(pend_tj, (0, 0))
        
        # Pygame events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                GRAVITY = 0.5
        
        # Pendulum iterations
        for pendulum in random.sample(pendulums, len(pendulums)): # Using random.sample for a better trajectory so that blue isn't always on top
            prev = pendulum.check_angles()
            pygame.draw.line(pend_tj, pendulum.color + (100,), prev, (pendulum.x_pos_2, pendulum.y_pos_2), width= 2)
        for pendulum in pendulums:
            pendulum.draw_scheme()
        
        # Screen instructions
        if GRAVITY == 0:
            myfont = pygame.font.SysFont("Verdana", 35)
            instructions = myfont.render("press SPACE to start", 10, (255,255,255))
            screen.blit(instructions, (STATIC_POINT[0] - 180, 150))
            myfont = pygame.font.SysFont("Verdana", 17)
            instructions = myfont.render("note: all pendulums have only 0.1° start difference!", 10, (255,255,255))
            screen.blit(instructions, (STATIC_POINT[0] - 220, 200))
        
        draw_static_point()
        pygame.display.update()
    pygame.quit()

if __name__ == "__main__":
    main()