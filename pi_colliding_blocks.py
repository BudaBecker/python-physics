import pygame

# Pygame init
pygame.init()
WIDTH, HEIGHT = 1200, 400
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption("Calculating Pi with Colliding Blocks")

# Fonts
blocks_font = pygame.font.SysFont("Arial", 25)
low_blocks_font = pygame.font.SysFont("Arial", 15, bold= True)
inst_font = pygame.font.SysFont("monospace", 25, bold= True)
low_inst_font = pygame.font.SysFont("monospace", 20, bold= True)

# Global Variables
FPS = 60
DT = 0.001
STEPS_PER_FRAME = 1800

# RGB
x = 60; BG_COLOR = (x, x, x)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
B1 = (255, 255, 50)
B2 = (50, 255, 255)

# Colliding Blocks class
class Blocks:
    def __init__(self, iterations):
        self.ite = iterations
        self.m1 = 1
        self.m2 = (100)**(iterations - 1)
        self.v1 = 0.0
        self.v2 = -1.0
        self.l1 = 50
        if self.m2 == self.m1:
            self.l2 = self.l1
        else:
            self.l2 = 100
        self.x1 = 250.0
        self.x2 = 500.0
        self.n_collisions = 0
    
    def check_collisions(self):
        overlap = (self.x1 + self.l1) >= (self.x2)
        if overlap:
            if self.v1 > self.v2:
                self.block_collision()

        if self.x1 <= 10:
            if self.v1 < 0:
               self.wall_colision()

    def wall_colision(self):
        if self.v1 < 10:
            self.v1 *= -1
            self.n_collisions += 1
            # To ensure block is off the wall
            self.x1 = 10.1
    
    def block_collision(self):
        m1, m2 = self.m1, self.m2
        v1, v2 = self.v1, self.v2 # Store constants for slightly better performance.
        sum_mass = m1 + m2

        # One-dimensional Newtonian elastic collision formula (https://en.wikipedia.org/wiki/Elastic_collision)
        self.v1 = ((m1 - m2) * v1 + 2 * m2 * v2) / sum_mass
        self.v2 = (2 * m1 * v1 + (m2 - m1) * v2) / sum_mass

        self.n_collisions += 1
    
    def update_pos(self):
        self.x1 += self.v1 * DT
        self.x2 += self.v2 * DT
    
    def draw_blocks(self): # Trash coded function just ignore :(
        x1, x2 = self.x1, self.x2
        border_thickness = 2
        
        if x2 < (x1 + self.l1) and self.m2 >= (100)**(4):
            x1 = 10
            x2 = x1 + self.l1 + 1
        
        mass = blocks_font.render(f"{self.m1}kg", 1, WHITE)
        screen.blit(mass, (x1+5, 200))
        block1 = pygame.Rect(int(x1), 300 - self.l1, self.l1, self.l1)
        border1 = pygame.Rect(block1.left - border_thickness, block1.top - border_thickness, block1.width + 2 * border_thickness, block1.height + 2 * border_thickness)
        pygame.draw.rect(screen, BLACK, border1)
        pygame.draw.rect(screen, B1, block1)
        
        if self.ite < 4:
            mass = blocks_font.render(f"{self.m2}kg", 1, WHITE)
            screen.blit(mass, (x2+5, 250-self.l2))
            block2 = pygame.Rect(int(x2), 300 - self.l2, self.l2, self.l2)
            border2 = pygame.Rect(block2.left - border_thickness, block2.top - border_thickness, block2.width + 2 * border_thickness, block2.height + 2 * border_thickness)
            pygame.draw.rect(screen, BLACK, border2)
            pygame.draw.rect(screen, B2, block2)
        else:
            mass = blocks_font.render("100  kg", 1, WHITE)
            screen.blit(mass, (x2+5, 250-self.l2))
            mass = low_blocks_font.render(f"{self.ite - 1}", 1, WHITE)
            screen.blit(mass, (x2+38, 245-self.l2))
            block2 = pygame.Rect(int(x2), 300 - self.l2, self.l2, self.l2)
            border2 = pygame.Rect(block2.left - border_thickness, block2.top - border_thickness, block2.width + 2 * border_thickness, block2.height + 2 * border_thickness)
            pygame.draw.rect(screen, BLACK, border2)
            pygame.draw.rect(screen, B2, block2)
        
# Main game loop
def main():
    timer = pygame.time.Clock()
    running = True
    start = False
    while running:
        timer.tick(FPS)
        screen.fill(BG_COLOR)
        pygame.draw.line(screen, WHITE, (10, 300), (WIDTH, 300), 2)
        pygame.draw.line(screen, WHITE, (10, 0), (10, 300), 2)
        
        # Start instructions
        if not start:
            instructions = inst_font.render("How many digits of Pi would you like to compute?", 1, WHITE)
            screen.blit(instructions, (10, 310))
            instructions = inst_font.render("Press the corresponding number.", 1, WHITE)
            screen.blit(instructions, (10, 340))
        
        # Pygame events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif (event.type == pygame.KEYDOWN) and (49 <= event.key <= 57) and (not start):
                start = True
                iter = event.key - 48
                blocks = Blocks(iterations= iter)
            elif (event.type == pygame.KEYDOWN) and (event.key == 114) and (start):
                start = False
        
        # Labels
        if start:
            instructions = inst_font.render(f"press R to restart - calculating: {iter} digits", 1, WHITE)
            instructions1 = low_inst_font.render("note: for 6+ digits it may take a while to calculate :)", 1, WHITE)
            instructions2 = low_inst_font.render("π ≈ 3.14159265...", 1, WHITE)
            screen.blit(instructions, (10, 310))
            screen.blit(instructions1, (10, 345))
            screen.blit(instructions2, (10, 370))
        
        # Blocks
        if start:
            for _ in range(STEPS_PER_FRAME):
                blocks.update_pos()
                blocks.check_collisions()
            blocks.draw_blocks()
            collisions = inst_font.render(f"Collisions: {blocks.n_collisions}", 1, WHITE)
            screen.blit(collisions, (33, 20))
                
        pygame.display.update()
    pygame.quit()
if __name__ == "__main__":
    main()