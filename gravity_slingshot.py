import pygame
import numpy as np

# Pygame init
pygame.init()
WIDTH = 900
HEIGHT = 800
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption("Black Hole Slingshot Effect")

# Global variables
FPS = 60
BG_COLOR = (80, 80, 80)
BLACK_HOLE_MASS = 1000
BLACK_HOLE_RADIUS = 70
PARTICLE_MASS = 5
PARTCLE_RADIUS = 8
VELOCITY_SCALE = 100
G = 5

# Particle Class
class Particle:
    def __init__(self, x_pos, y_pos, x_vel, y_vel, mass):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.x_vel = x_vel
        self.y_vel = y_vel
        self.mass = mass
        self.trajectory = []
    
    def draw_particle(self):
        pygame.draw.circle(screen, (0, 255, 255), (self.x_pos, self.y_pos), PARTCLE_RADIUS)

    def update_pos(self):
        # Newton's law of universal gravitation
        diff_vect = np.array((WIDTH/2, HEIGHT/2) , dtype= float) - np.array((self.x_pos, self.y_pos), dtype= float)
        distance = np.linalg.norm(diff_vect)
        acc = (G * BLACK_HOLE_MASS) / (distance**2)  # g_force = (G * self.mass * planet.mass) / (distance**2) but particle_acc = g_force /  particle_mass
        direction_vector = diff_vect / distance
        acc_vector = acc * direction_vector
        
        # Change velocity and position
        self.x_vel += acc_vector[0]
        self.y_vel += acc_vector[1]
        self.x_pos += self.x_vel
        self.y_pos += self.y_vel
    
# Functions
def draw_black_hole():
    pygame.draw.circle(screen, "black", (WIDTH/2, HEIGHT/2), BLACK_HOLE_RADIUS)

def particle_vel_vect(pos_ini, pos_end):
    pos_ini = np.array(pos_ini , dtype= float)
    pos_end = np.array(pos_end , dtype= float)
    vel_vect = pos_end - pos_ini
    return vel_vect/VELOCITY_SCALE

# Main game loop
def main():
    particles = []
    temp_part_pos = None
    timer = pygame.time.Clock()
    running = True
    while running:
        timer.tick(FPS)
        screen.fill(BG_COLOR)
        
        # Pygame events
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if temp_part_pos:
                    vel_vect = particle_vel_vect(temp_part_pos, mouse_pos)
                    particle = Particle(
                        x_pos = temp_part_pos[0],
                        y_pos = temp_part_pos[1],
                        x_vel = vel_vect[0],
                        y_vel = vel_vect[1],
                        mass = PARTICLE_MASS
                        )
                    particles.append(particle)
                    temp_part_pos = None
                else:
                    temp_part_pos = mouse_pos

        # Particles Updates
        if temp_part_pos:
            pygame.draw.line(screen, (255, 255, 255), temp_part_pos, mouse_pos, 3)
            pygame.draw.circle(screen, (0, 255, 255), temp_part_pos, PARTCLE_RADIUS) 
        for part in particles[:]:
            part.update_pos()
            in_black_hole = BLACK_HOLE_RADIUS - PARTCLE_RADIUS >= np.linalg.norm(np.array((WIDTH/2, HEIGHT/2) , dtype= float) - np.array((part.x_pos, part.y_pos), dtype= float))
            if (part.x_pos > WIDTH + PARTCLE_RADIUS) or (part.x_pos < -PARTCLE_RADIUS) or (part.y_pos > HEIGHT+PARTCLE_RADIUS) or (part.y_pos < -PARTCLE_RADIUS) or (in_black_hole):
                particles.remove(part)
                print("particle deleted")
            part.trajectory.append((int(part.x_pos), int(part.y_pos)))
            if len(part.trajectory) > 1:
                pygame.draw.lines(screen, "blue", False, part.trajectory)
            if len(part.trajectory) > 500:
                part.trajectory.pop(0)
            part.draw_particle()
        
        draw_black_hole()
        pygame.display.update()
    pygame.quit()
if __name__ == "__main__":
    main()