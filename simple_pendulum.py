import math
import pygame

# Pygame init
pygame.init()
WIDTH = 900
HEIGHT = 800
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption("Simple Pendulum")

# Global variables
FPS = 60
GRAVITY = 0.5
BG_COLOR = (0,0,0,)
STRING_COLOR = (255, 255, 255)
WEIGHT_COLOR = (255, 0, 0)
WEIGHT_RADIUS = 30
STRING_LENGHT = 500
STRING_DISTANCE = 7 + WEIGHT_RADIUS + STRING_LENGHT
INITIAL_ANGLE = math.pi/4
AIR_FRICTION = 0.999

# Weight class
class Weight:
    def __init__(self):
        self.angle = INITIAL_ANGLE
        self.angle_vel = 0
        self.angle_acc = 0
        self.x_pos = STRING_DISTANCE * math.sin(INITIAL_ANGLE) + (WIDTH/2)
        self.y_pos = STRING_DISTANCE * math.cos(INITIAL_ANGLE) + 100
        self.radius = WEIGHT_RADIUS

    def draw_scheme(self):
        self.x_pos = STRING_DISTANCE * math.sin(self.angle) + (WIDTH/2)
        self.y_pos = STRING_DISTANCE * math.cos(self.angle) + 100
        pygame.draw.lines(screen, STRING_COLOR, False, [(WIDTH/2, 100), (self.x_pos, self.y_pos)], width=2)
        pygame.draw.circle(screen, (150, 150, 150), (self.x_pos, self.y_pos), self.radius)
        pygame.draw.circle(screen, WEIGHT_COLOR, (self.x_pos, self.y_pos), self.radius-5)
      
    def angular_calc(self):
        self.angle_acc = (GRAVITY * math.sin(self.angle))*(-1)/STRING_LENGHT
        self.angle_vel += self.angle_acc
        self.angle_vel *= AIR_FRICTION
        self.angle += self.angle_vel 
        
# Functions
def draw_static_point():
    pygame.draw.circle(screen, (150, 150, 150), (WIDTH/2, 100), 7)
    pygame.draw.circle(screen, (0, 0, 0), (WIDTH/2, 100), 4)

# Main loop
def main():
    timer = pygame.time.Clock()
    running = True
    weight = Weight()
    active = False
    while running:
        timer.tick(FPS)
        screen.fill(BG_COLOR)
        
        # Pygame Event
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                global GRAVITY
                temp = GRAVITY
                GRAVITY = 0
                weight.angle_vel = 0
                active = True
            if event.type == pygame.MOUSEBUTTONUP:
                GRAVITY = temp
                active = False
        if active:
            if mouse_pos[1] > 100:
                weight.angle = math.atan((mouse_pos[0]-(WIDTH/2))/(mouse_pos[1]-100)) 
            if mouse_pos[1] <= 100:
                if mouse_pos[0] > WIDTH/2:
                    weight.angle = math.pi/2
                else:
                    weight.angle = 3*math.pi/2
              
        weight.angular_calc()
        weight.draw_scheme()
        draw_static_point()
        pygame.display.update()
    pygame.quit()
    
if __name__ == "__main__":
    main()