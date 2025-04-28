import pygame
import numpy as np

# Pygame init
pygame.init()
WIDTH = 900
HEIGHT = 800
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption("Black Hole Slingshot Effect")
myfont = pygame.font.SysFont("Verdana", 20)

# Global variables
FPS = 60
x = 100; BG_COLOR = (x, x, x)
BLACK_HOLE_MASS = 1000
BLACK_HOLE_RADIUS = 70
PARTICLE_MASS = 5
PARTCLE_RADIUS = 8
VELOCITY_SCALE = 75
G = 5

# Particle Class
class Particle:
    def __init__(self, x_pos, y_pos, x_vel, y_vel, mass):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.x_vel = x_vel
        self.y_vel = y_vel
        self.mass = mass
        self.trajectory = np.empty((0, 2), dtype=np.float32)
        self.buffer = []
    
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
        instructions = myfont.render("click once to create a body, aim, then click again to launch", 1, (0, 0, 0))
        screen.blit(instructions, (0, 0))
        instructions = myfont.render("(the launch speed is proportional to the white line)", 1, (0, 0, 0))
        screen.blit(instructions, (0, 22))
        
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
                
            # Print trajectory line with numpy array (for more memory efficiency)
            part.buffer.append([part.x_pos, part.y_pos])
            if len(part.buffer) >= 100:
                new_points = np.array(part.buffer, dtype=np.float32)
                part.trajectory = np.vstack((part.trajectory, new_points))
                part.buffer.clear()
            
            combined_points = part.trajectory
            if part.buffer:
                combined_points = np.vstack((combined_points, np.array(part.buffer, dtype=np.float32)))
            if len(combined_points) > 1:
                pygame.draw.lines(screen, "blue", False, combined_points.tolist())
            
            part.draw_particle()
        draw_black_hole()
        pygame.display.update()
    pygame.quit()
if __name__ == "__main__":
    main()