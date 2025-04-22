import pygame

# Pygame init
pygame.init()
WIDTH = 1000
HEIGHT = 800
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption("Animated Spring")

# Global variables
FPS = 60
BG_COLOR = (50, 50, 50)

# Spring variable
SPRING_COLOR = (255, 255, 255)

# Spring Class
class Spring:
    def __init__(self, n_spike: int, base: int, color, thickness, s_width: int):
        self.n_spike = n_spike
        self.base = base
        self.color = color
        self.thickness = thickness
        self.s_width = s_width
    
    def draw_spring(self, init_pos: tuple, end_pos: tuple):
        init = pygame.Vector2(init_pos)
        end  = pygame.Vector2(end_pos)
        diff = end - init
        total_length = diff.length()
        if total_length <= 2 * self.base or self.n_spike <= 0:
            pygame.draw.line(screen, self.color, init, end, self.thickness)
            return

        direction   = diff.normalize()
        perpendicular = direction.rotate(90)
        wave_length = total_length - 2 * self.base
        half_seg = wave_length / (self.n_spike * 2)

        # Points list with all the spring points to draw
        points = []
        points.append(init)
        points.append(init + direction * self.base)
        for i in range(1, self.n_spike * 2):
            t = self.base + i * half_seg
            pt_on_axis = init + direction * t
            offset = perpendicular * (self.s_width / 2) * (1 if i % 2 else -1)
            points.append(pt_on_axis + offset)
        points.append(end - direction * self.base)
        points.append(end)

        # Draw spring
        pygame.draw.lines(screen, self.color, False, points, self.thickness)

# Main game loop
def main():
    timer = pygame.time.Clock()
    running = True
    spring = Spring(
        n_spike= 20,
        base= 20,
        color= (255, 255, 255),
        thickness= 3,
        s_width= 30
    )
    while running:
        timer.tick(FPS)
        screen.fill(BG_COLOR)
        
        # Pygame events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        mouse_pos = pygame.mouse.get_pos()
        spring.draw_spring(init_pos= (0, HEIGHT/2), end_pos= mouse_pos)
        pygame.display.update()
    pygame.quit()
        
if __name__ == "__main__":
    main()