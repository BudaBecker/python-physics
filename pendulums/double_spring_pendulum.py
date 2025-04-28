import pygame
import math
import numpy as np

# Pygame init
pygame.init()
WIDTH, HEIGHT = 1200, 900
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption("The Chaotic Double Elastic Pendulum")

# Global variables
FPS = 60
GRAVITY = 0.5
AIR_FRICTION = 0.99999
DT = 0.01
STEPS_PER_FRAME = 100

STATIC_POINT = (WIDTH/2, 75)
x = 80; BG_COLOR = (x, x, x)

# Weights visuals
W1_RADIUS = 15
W1_COLOR = (0, 0, 0)
W1_TRAIL = (50, 255, 50)

W2_RADIUS = 15
W2_COLOR = (0, 0, 0)
W2_TRAIL = (50, 50, 255)

# Weight class
class Weights:
    def __init__(self, init_angle1, m1, r1, k1, l1, init_angle2, m2, r2, k2, l2):
        # W1
        self.init_angle1 = init_angle1
        self.m1 = m1
        self.r1 = r1
        self.k1 = k1
        self.l1 = l1
        self.w1_pos = np.array([STATIC_POINT[0] + l1 * math.sin(self.init_angle1), STATIC_POINT[1] + l1 * math.cos(self.init_angle1)], dtype= float)
        self.w1_vel = np.zeros(2, dtype= float)
        # W2
        self.init_angle2 = init_angle2
        self.m2 = m2
        self.r2 = r2
        self.k2 = k2
        self.l2 = l2
        self.w2_pos = np.array([self.w1_pos[0] + l1 * math.sin(self.init_angle2), self.w1_pos[1] + l1 * math.cos(self.init_angle2)], dtype= float)
        self.w2_vel = np.zeros(2, dtype= float)
      
    def weight_calcs(self):
        # Weight points
        x0, y0 = STATIC_POINT
        x1, y1 = self.w1_pos
        x2, y2 = self.w2_pos

        # Spring 1 forces
        dx1 = x1 - x0
        dy1 = y1 - y0
        d1  = max(math.hypot(dx1, dy1), 1e-9) # To avoid 0 div.
        f1_mag = self.k1 * (d1 - self.l1)
        f1x = -f1_mag * dx1 / d1
        f1y = -f1_mag * dy1 / d1

        # Spring 2 forces
        dx12 = x2 - x1
        dy12 = y2 - y1
        d12  = max(math.hypot(dx12, dy12), 1e-9)
        f2_mag    = self.k2 * (d12 - self.l2)
        f2x_on1   =  f2_mag * dx12 / d12
        f2y_on1   =  f2_mag * dy12 / d12
        f2x_on2   = -f2x_on1
        f2y_on2   = -f2y_on1

        # Sum forces
        fx1 = f1x + f2x_on1
        fy1 = f1y + f2y_on1 + self.m1 * GRAVITY
        fx2 = f2x_on2
        fy2 = f2y_on2 + self.m2 * GRAVITY

        # Acc results (F = m.a)
        ax1, ay1 = fx1/self.m1, fy1/self.m1
        ax2, ay2 = fx2/self.m2, fy2/self.m2

        # Att vel and pos for W1 and W2
        self.w1_vel += np.array([ax1, ay1]) * DT
        self.w1_vel *= AIR_FRICTION
        self.w1_pos += self.w1_vel * DT

        self.w2_vel += np.array([ax2, ay2]) * DT
        self.w2_vel *= AIR_FRICTION
        self.w2_pos += self.w2_vel * DT
        
        return (x1, y1), (x2, y2)
    
    def draw_scheme(self):
        pygame.draw.circle(screen, W1_COLOR, self.w1_pos, self.r1)
        pygame.draw.circle(screen, W2_COLOR, self.w2_pos, self.r2)
    
class Spring:
    def __init__(self, n_spike: int, base: int, color, thickness, s_width: int):
        self.n_spike = n_spike
        self.base = base
        self.color = color
        self.thickness = thickness
        self.s_width = s_width
    
    def draw_spring(self, init_pos: tuple, end_pos: tuple):
        # Using pygame vectors
        init = pygame.Vector2(init_pos[0], init_pos[1])
        end  = pygame.Vector2(end_pos[0], end_pos[1])
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

def static_point():
    pygame.draw.circle(screen, (150, 150, 150), STATIC_POINT, 7)
    pygame.draw.circle(screen, (0, 0, 0), STATIC_POINT, 4)
      
def main():
    weight_trail = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    timer = pygame.time.Clock()
    running = True
    spring1 = Spring(n_spike= 15, base= W1_RADIUS + 3, color= (255, 255, 255), thickness= 2, s_width= 10)
    spring2 = Spring(n_spike= 15, base= W2_RADIUS + 3, color= (255, 255, 255), thickness= 2, s_width= 10)
    weights = Weights(
        # W1
        init_angle1= math.pi/2,
        m1 = 10,
        r1 = W1_RADIUS,
        k1= 0.2,
        l1 = 250,
        # W2
        init_angle2 = math.pi/2,
        m2 = 10,
        r2 = W2_RADIUS,
        k2= 0.2,
        l2 = 250,
    )
    while running:
        timer.tick(FPS)
        screen.fill(BG_COLOR)
        screen.blit(weight_trail, (0, 0))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        for _ in range(STEPS_PER_FRAME):   
            prev_w1, prev_w2 = weights.weight_calcs()
            pygame.draw.line(weight_trail, W1_TRAIL, prev_w1, weights.w1_pos, 2)
            pygame.draw.line(weight_trail, W2_TRAIL, prev_w2, weights.w2_pos, 2)
            
        spring1.draw_spring(STATIC_POINT, weights.w1_pos)
        spring2.draw_spring(weights.w1_pos, weights.w2_pos)
        static_point()
        weights.draw_scheme()
          
        pygame.display.update()
    pygame.quit()
if __name__ == "__main__":
    main()