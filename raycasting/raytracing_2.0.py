import math
import pygame

# Pygame init
pygame.init()
WIDTH, HEIGHT = 1440, 900
screen = pygame.display.set_mode([WIDTH, HEIGHT])

# Global variables
FPS = 60
GRID_SPACE = 0
RAY_THICK = 2
N_RAYS = 500
SUN_SIZE = 20
CAST_STEPS = 1
MAX_REFLECTIONS = 5

# RGB
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (100, 100, 100)
YELLOW = (255, 255, 50)
COLORS = {
    0: BLACK,
    1: WHITE,
    2: GREY,
}

# Light class
class Light:
    def __init__(self):
        self.sun_radius = SUN_SIZE
        self.n_rays = N_RAYS
        self.ray_color = YELLOW
        self.sun_pos = (float(WIDTH/2), float(HEIGHT/2))
    
    def draw_sun(self):
        pygame.draw.circle(screen, BLACK, self.sun_pos, self.sun_radius+1)
        pygame.draw.circle(screen, self.ray_color, self.sun_pos, self.sun_radius)
    
    def cast_rays(self):
        for i in range(self.n_rays):
            angle = 2 * math.pi * i / self.n_rays
            self.ang_cos = math.cos(angle)
            self.ang_sin = math.sin(angle)
            start = (self.sun_pos[0] + self.ang_cos * self.sun_radius, self.sun_pos[1] + self.ang_sin * self.sun_radius)
            end = start
            casting = True
            reflected = 0
            if self.check_cell(start) == 0:
                while casting:
                    # if end off the screen
                    if (end[0] > WIDTH) or (end[0] < 0) or (end[1] > HEIGHT) or (end[1] < 0):
                        pygame.draw.line(screen, self.ray_color, start, end, RAY_THICK)
                        break
                    
                    cell_num = self.check_cell(end)
                    if cell_num == 1: # hit wall
                        pygame.draw.line(screen, self.ray_color, start, end, RAY_THICK)
                        casting = False
                    elif cell_num == 2: # hit mirror
                        pygame.draw.line(screen, self.ray_color, start, end, RAY_THICK)
                        temp = end
                        end = self.reflected_angle(start, end)
                        start = temp
                        reflected += 1
                    else:
                        end = (end[0] + self.ang_cos * CAST_STEPS, end[1] + self.ang_sin * CAST_STEPS)
                    if reflected > MAX_REFLECTIONS: # avoiding infinite loops
                        break
            
            self.draw_sun()

    def check_cell(self, end):
        x, y = end
        i = int(x/cell_width)
        j = int(y/cell_height)
        
        if (0 <= j < grid_y) and (0 <= i < grid_x):
            return grid[j][i]
        return 1
    
    def reflected_angle(self, start, end):
        # Reflection formula:
        # R = V − 2(V@N)N
        
        # direction vect
        Vx = end[0] - start[0]
        Vy = end[1] - start[1]

        # normal vect
        Nx, Ny = self.get_normal(end)

        # dot product (V@N)
        dot = Vx * Nx + Vy * Ny

        # Reflection formula
        Rx = Vx - 2 * dot * Nx
        Ry = Vy - 2 * dot * Ny
        
        # normalize
        mag = math.hypot(Rx, Ry)
        Rx /= mag # adjacent/hypotenuse
        Ry /= mag # opposite/hypotenuse

        self.ang_cos = Rx
        self.ang_sin = Ry
        next_end = (end[0] + Rx * CAST_STEPS, end[1] + Ry * CAST_STEPS)

        return next_end
    
    def get_normal(self, end):
        x, y = end
        i = int(x / cell_width)
        j = int(y / cell_height)

        # boundaries
        mirror_left = i * cell_width
        mirror_right = mirror_left + cell_width
        mirror_up = j * cell_height
        mirror_bottom = mirror_up + cell_height

        imprecision = 0.1

        if abs(x - mirror_left) < imprecision:
            return (1, 0)  # left mirror side
        elif abs(x - mirror_right) < imprecision:
            return (-1, 0)  # right mirror side
        elif abs(y - mirror_up) < imprecision:
            return (0, 1)  # upper mirror side
        elif abs(y - mirror_bottom) < imprecision:
            return (0, -1)  # bottom mirror side
        else:
            # if endpoint is inside of the mirror (cuz of cast_steps)
            dx = x - (mirror_left + cell_width / 2)
            dy = y - (mirror_up + cell_height / 2)
            if abs(dx) > abs(dy):
                if (dx > 0):
                    return (-1, 0)
                return(1, 0)
            else:
                if (dy > 0):
                    return (0, -1)
                return(0, 1)

# 0- Black (void); 
# 1- White (dense surface); 
# 2- Grey (Mirror);
grid = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 2, 1, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
    [1, 0, 0, 0, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
    [1, 0, 0, 0, 2, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
    [1, 0, 0, 0, 2, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
    [1, 0, 0, 0, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 1, 1, 1, 1, 1]
]
grid_x = len(grid[0])
grid_y = len(grid)
cell_width = WIDTH / grid_x
cell_height = HEIGHT / grid_y

def draw_grid():
    for i, row in enumerate(grid):
            for j, cell in enumerate(row):
                if cell != 0:
                    rect = pygame.Rect(
                        int(j * cell_width),
                        int(i * cell_height),
                        int(cell_width) - GRID_SPACE,
                        int(cell_height) - GRID_SPACE
                    )
                    pygame.draw.rect(screen, COLORS[cell], rect)

# Main game loop
def main():
    running = True
    clock = pygame.time.Clock()
    active = False
    light = Light()
    while running:
        pygame.display.set_caption(f"Raycasting 2.0. FPS: {int(clock.get_fps())}")
        clock.tick(FPS)
        screen.fill(BLACK)
        
        # Pygame event
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                active = True
            if event.type == pygame.MOUSEBUTTONUP:
                active = False
        if active:
            light.sun_pos = mouse_pos
        
        light.cast_rays()
        draw_grid()
        
        pygame.display.update()
    pygame.quit()

if __name__ == "__main__":
    main()