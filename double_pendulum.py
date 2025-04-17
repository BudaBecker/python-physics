import math
import pygame
import numpy as np

# Pygame init
pygame.init()
WIDTH = 1000
HEIGHT = 800
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption("Double Pendulum, Chaos Theory")
myfont = pygame.font.SysFont("monospace", 35)

# Global physics variables
FPS = 60
GRAVITY = 0.5
L_1 = 200
L_2 = 200
M_1 = 10
M_2 = 10
AIR_FRICTION = 1

# Global custom variables
WEIGHT_1_RADIUS = 15
WEIGHT_2_RADIUS = 15
STR_D_1 = 7 + WEIGHT_1_RADIUS + L_1
STR_D_2 = 2*WEIGHT_2_RADIUS + L_2
COLOR_1 = (255, 20, 20)
COLOR_2 = (20, 255, 90)
BG_COLOR = (50, 50, 50)

# Class Pendulum
class Pendulum:
    def __init__(self, color, angle_init_1, angle_init_2):
        self.mass_1 = M_1
        self.angle_1 = angle_init_1 * math.pi/180
        self.angle_vel_1 = 0
        self.angle_acc_1 = 0
        self.weight_radius_1 = WEIGHT_1_RADIUS
        
        self.mass_2 = M_2
        self.angle_2 = angle_init_2 * math.pi/180
        self.angle_vel_2 = 0
        self.angle_acc_2 = 0
        self.weight_radius_2 = WEIGHT_2_RADIUS
        
        self.color = color
        self.trajectory = np.empty((0, 2), dtype=np.float32)
        self.buffer = []

    def draw_scheme(self):
        self.x_pos_1 = STR_D_1 * math.sin(self.angle_1) + (WIDTH/2)
        self.y_pos_1 = STR_D_1 * math.cos(self.angle_1) + 275
        self.x_pos_2 = STR_D_2 * math.sin(self.angle_2) + self.x_pos_1
        self.y_pos_2 = STR_D_1 * math.cos(self.angle_2) + self.y_pos_1
        pygame.draw.lines(screen, self.color, False, [(WIDTH/2, 275), (self.x_pos_1, self.y_pos_1)], width=2)
        pygame.draw.circle(screen, self.color, (self.x_pos_1, self.y_pos_1), self.weight_radius_1)
        pygame.draw.lines(screen, self.color, False, [(self.x_pos_1, self.y_pos_1), (self.x_pos_2, self.y_pos_2)], width=2)
        pygame.draw.circle(screen, self.color, (self.x_pos_2, self.y_pos_2), self.weight_radius_2)
    
    def check_angles(self):
        # For θ1''
        num1 = -GRAVITY * (2*self.mass_1 + self.mass_2) * math.sin(self.angle_1)
        num2 = -self.mass_2 * GRAVITY * math.sin(self.angle_1 - 2*self.angle_2)
        num3 = -2 * math.sin(self.angle_1 - self.angle_2) * self.mass_2
        num4 = (self.angle_vel_2**2) * STR_D_2 + (self.angle_vel_1**2) * STR_D_1 * math.cos(self.angle_1 - self.angle_2)
        den = STR_D_1 * (2*self.mass_1 + self.mass_2 - self.mass_2 * math.cos(2*self.angle_1 - 2*self.angle_2))
        self.angle_acc_1 = (num1 + num2 + num3 * num4) / den

        
        # For θ2''
        num1 = 2 * math.sin(self.angle_1 - self.angle_2)
        num2 = (self.angle_vel_1**2) * STR_D_1 * (self.mass_1 + self.mass_2)
        num3 = GRAVITY * (self.mass_1 + self.mass_2) * math.cos(self.angle_1)
        num4 = (self.angle_vel_2**2) * STR_D_2 * self.mass_2 * math.cos(self.angle_1 - self.angle_2)
        den = STR_D_2 * (2*self.mass_1 + self.mass_2 - self.mass_2 * math.cos(2*self.angle_1 - 2*self.angle_2))
        self.angle_acc_2 = (num1 * (num2 + num3 + num4)) / den

        
        self.angle_vel_1 += self.angle_acc_1
        self.angle_vel_2 += self.angle_acc_2
        self.angle_vel_1 *= AIR_FRICTION
        self.angle_vel_2 *= AIR_FRICTION
        self.angle_1 += self.angle_vel_1
        self.angle_2 += self.angle_vel_2
    
# Functions
def create_pendulums():
    pend_list = []
    pend_list.append(
        Pendulum(color= COLOR_1, angle_init_1= 90, angle_init_2= 90)   #angle_init in degrees.
    )
    pend_list.append(
        Pendulum(color = COLOR_2, angle_init_1= 90, angle_init_2= 89)   #angle_init in degrees.
    )
    pend_list.append(
        Pendulum(color = (0, 136, 255), angle_init_1= 90, angle_init_2= 88)   #angle_init in degrees.
    )
    
    return pend_list

# Draw pin
def draw_static_point():
    pygame.draw.circle(screen, (150, 150, 150), (WIDTH/2, 275), 7)
    pygame.draw.circle(screen, (0, 0, 0), (WIDTH/2, 275), 4)

# Main game loop
def main():
    global GRAVITY
    pendulums = []
    pendulums = create_pendulums()
    timer = pygame.time.Clock()
    running = True
    temp_g = GRAVITY
    GRAVITY = 0
    while running:
        timer.tick(FPS)
        screen.fill(BG_COLOR)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if 'space' == pygame.key.name(event.key):
                    GRAVITY = temp_g
        
        for pendulum in pendulums:
            pendulum.draw_scheme()
            pendulum.check_angles()
        
            pendulum.buffer.append([pendulum.x_pos_2, pendulum.y_pos_2])
            if len(pendulum.buffer) >= 100:
                new_points = np.array(pendulum.buffer, dtype=np.float32)
                pendulum.trajectory = np.vstack((pendulum.trajectory, new_points))
                pendulum.buffer.clear()
            
            combined_points = pendulum.trajectory
            if pendulum.buffer:
                combined_points = np.vstack((combined_points, np.array(pendulum.buffer, dtype=np.float32)))
            if len(combined_points) > 1:
                
                # for i in range(5, 0, -1):
                #     alpha = int(255 * (i / 5) * 0.2)  # decrease alpha
                #     glow_color = pygame.Color(pendulum.color)
                #     glow_color.a = alpha
                #     glow_surface = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
                #     pygame.draw.lines(glow_surface, glow_color, False, combined_points.tolist(), i * 2)
                #     screen.blit(glow_surface, (0, 0))

                pygame.draw.lines(screen, pendulum.color, False, combined_points.tolist(), 2)
        
        if GRAVITY == 0:
            instructions = myfont.render("Press 'space' to start", 25, (255,255,255))
            screen.blit(instructions, (WIDTH/2 - 260, 200))
        
        draw_static_point()
        pygame.display.update()
    pygame.quit()

if __name__ == "__main__":
    main()