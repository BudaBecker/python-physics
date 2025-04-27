import math
import pygame

# Pygame init
pygame.init()
WIDTH = 900
HEIGHT = 800
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption("Spring Pendulum")

# Global variables
FPS = 60
GRAVITY = 0.5
AIR_FRICTION = 1
BG_COLOR = (50, 50, 50)
STATIC_POINT = (WIDTH/2, 150)

# Weight variables
WEIGHT_COLOR = (255, 0, 0)
WEIGHT_RADIUS = 20
WEIGHT_MASS = 15

# Spring variables
SPRING_COLOR = (255, 255, 255)
INITIAL_ANGLE = 0
L0 = 400
N_COILS = 10
SPRING_K = 0.2

# Weight class
class Weight:
    def __init__(self):
        self.angle = INITIAL_ANGLE
        self.angle_vel = 0
        self.angle_acc = 0
        
        self.r = L0
        self.r_vel = 0
        self.r_acc = 0
        
        self.radius = WEIGHT_RADIUS

    def draw_scheme(self):
        pygame.draw.circle(screen, (150, 150, 150), (self.x_pos, self.y_pos), self.radius)
        pygame.draw.circle(screen, WEIGHT_COLOR, (self.x_pos, self.y_pos), self.radius-2)
      
    def weight_calcs(self):
        # radius acceleration
        self.r_acc = (
            self.r * (self.angle_vel ** 2) - (SPRING_K / WEIGHT_MASS) * (self.r - L0) - GRAVITY * math.cos(self.angle)
        )
        self.r_vel += self.r_acc
        self.r_vel *= AIR_FRICTION
        self.r += self.r_vel

        # angular acceleration
        self.angle_acc = (
            -2 * self.r_vel * self.angle_vel / self.r - (GRAVITY / self.r) * math.sin(self.angle)
        )
        self.angle_vel += self.angle_acc
        self.angle_vel *= AIR_FRICTION
        self.angle += self.angle_vel

        self.x_pos = STATIC_POINT[0] + self.r * math.sin(self.angle)
        self.y_pos = STATIC_POINT[1] + self.r * math.cos(self.angle)

# Spring Class
class Spring:
    def __init__(self, n_spike: int, base: int, color, thickness, s_width: int):
        self.n_spike = n_spike
        self.base = base
        self.color = color
        self.thickness = thickness
        self.s_width = s_width
    
    def draw_spring(self, init_pos: tuple, end_pos: tuple):
        # Using pygame vectors
        init = pygame.Vector2(init_pos)
        end  = pygame.Vector2(end_pos)
        diff = end - init
        total_length = diff.length()
        # Avoiding errors
        if total_length <= 2 * self.base or self.n_spike <= 0:
            pygame.draw.line(screen, self.color, init, end, self.thickness)
            return

        # Setting unit and normal vectors
        direction   = diff.normalize()
        perpendicular = direction.rotate(90)
        wave_length = total_length - 2 * self.base
        half_seg = wave_length / (self.n_spike * 2)

        # Points list with all the spring points to draw
        points = []
        points.append(init)
        points.append(init + direction * self.base)
        # Zigzag points
        for i in range(1, self.n_spike * 2):
            t = self.base + i * half_seg
            pt_on_axis = init + direction * t
            offset = perpendicular * (self.s_width / 2) * (1 if i % 2 else -1)
            points.append(pt_on_axis + offset)
        points.append(end - direction * self.base)
        points.append(end)

        # Draw spring
        pygame.draw.lines(screen, self.color, False, points, self.thickness)
    
# Functions
def draw_static_point():
    pygame.draw.circle(screen, (150, 150, 150), STATIC_POINT, 7)
    pygame.draw.circle(screen, (0, 0, 0), STATIC_POINT, 4)

# Main loop
def main():
    timer = pygame.time.Clock()
    running = True
    weight = Weight()
    spring = Spring(
        n_spike= N_COILS,
        base= 30,
        color= SPRING_COLOR,
        thickness= 3,
        s_width= 30
    )
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
                active = True
            if event.type == pygame.MOUSEBUTTONUP:
                active = False
        if active:
            weight.angle_acc, weight.angle_vel, weight.r_acc, weight.r_vel = 0, 0, 0, 0
            if mouse_pos[1] > STATIC_POINT[1]:
                weight.x_pos, weight.y_pos = mouse_pos
                weight.angle = math.atan((mouse_pos[0]-STATIC_POINT[0])/(mouse_pos[1]-STATIC_POINT[1]))
                weight.r = math.sqrt((weight.x_pos - STATIC_POINT[0])**2 + (weight.y_pos - STATIC_POINT[1])**2)
        else:   
            weight.weight_calcs()
            
        # Draw
        spring.draw_spring(init_pos= STATIC_POINT, end_pos= (weight.x_pos, weight.y_pos))
        weight.draw_scheme()
        draw_static_point()
        
        pygame.display.update()
    pygame.quit()
    
if __name__ == "__main__":
    main()