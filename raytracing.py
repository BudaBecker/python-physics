# TODOS:
# 1- Refactor so can add new objects without any complications.
# 2- Add *use dramatic voice* THE MIRROR
# 3- Change all the raw math to numpy/math functions for easy understanding

import math
import pygame
import numpy as np

# Pygame init
pygame.init()
WIDTH, HEIGHT = 1400, 900
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption("Basic Raytracing")
mirror_font = pygame.font.SysFont("monospace", 20, bold= True)

# Global variables
FPS = 60

# RGB
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 50)
ORANGE = (218, 160, 109)
GREY = (100, 100, 100)

# Light class
class Light:
    def __init__(self, n_rays, color= YELLOW):
        self.sun_radius = 40
        self.n_rays = n_rays
        self.ray_color = color
        self.sun_pos = (float(WIDTH/2), float(HEIGHT/2))
        self.obj_pos = np.array([WIDTH/4, HEIGHT/2], dtype=float)
        self.obj_radius = float(150)
        self.obj_vel = np.array([0, 2], dtype=float)
        self.wall_x, self.wall_y = 1100, 200
        self.wall_width, self.wall_height = 50, 500
        self.wall = pygame.Rect(self.wall_x, self.wall_y, self.wall_width, self.wall_height)
        # self.mirror = (900, 870, 200, 50)
        # self.mirror_text = mirror_font.render("MIRROR", 1, WHITE)
    
    def draw_sun(self):
        pygame.draw.circle(screen, BLACK, self.sun_pos, self.sun_radius+1)
        pygame.draw.circle(screen, self.ray_color, self.sun_pos, self.sun_radius)
    
    def draw_rays(self):
        for i in range(self.n_rays):
            angle = 2 * math.pi * i / self.n_rays
            start = (self.sun_pos[0] + math.cos(angle) * self.sun_radius, self.sun_pos[1] + math.sin(angle) * self.sun_radius)
            end = (self.sun_pos[0] + math.cos(angle) * (self.sun_radius + 1900), self.sun_pos[1] + math.sin(angle) * (self.sun_radius + 1900))
            end = self.check_ray(start, end)
            pygame.draw.line(screen, self.ray_color, start, end, 1)
    
    def check_ray(self, start, end):
        # Setting up constants
        sx, sy = start
        ex, ey = end
        dx, dy = ex - sx, ey - sy  # direction vector (dx, dy) // P(t) = start + t(dx, dy) // *P(t) is the final point
        
        # obstacles parameters
        cx, cy = self.obj_pos
        r = self.obj_radius
        x_min, y_min = self.wall_x, self.wall_y
        x_max, y_max = self.wall_x + self.wall_width, self.wall_y + self.wall_height
        
        # If ray is inside of any object
        if ((sx - cx)**2 + (sy - cy)**2 <= r**2) or ((x_min <= sx <= x_max) and (y_min <= sy <= y_max)):
            return start
        
        # Check if ray goes through ball obj - solve for ||P(t) - (cx, cy)||^2 = r^2
        fx, fy = sx - cx, sy - cy
        a = dx*dx + dy*dy
        b = 2 * (fx*dx + fy*dy)
        c = fx*fx + fy*fy - r*r
        discr = b*b - 4*a*c
        t_circle = None
        if discr >= 0: # if delta/discriminant >= 0, the ray goes through (has solution)
            sqrt_d = math.sqrt(discr)
            for t in ((-b - sqrt_d)/(2*a), (-b + sqrt_d)/(2*a)):
                if (0 <= t <= 1): # if i has any points between start and end
                    if (t_circle == None) or (t < t_circle):
                        t_circle = t

        # Check if ray goes through wall obj
        t_wall = None
        if dx != 0:
            for x_edge in (x_min, x_max):
                t = (x_edge - sx) / dx
                if (0 <= t <= 1):
                    y_int = sy + t*dy
                    if y_min <= y_int <= y_max:
                        if (t_wall == None) or (t < t_wall):
                            t_wall = t
        if dy != 0:
            for y_edge in (y_min, y_max):
                t = (y_edge - sy) / dy
                if (0 <= t <= 1):
                    x_int = sx + t*dx
                    if x_min <= x_int <= x_max:
                        if (t_wall == None) or (t < t_wall):
                            t_wall = t # closest tangent point from circle-sun
        
        # Find the smallest t, then return P(t)
        t_final = None
        if (t_circle != None) and (t_wall != None):
            t_final = min(t_circle, t_wall)
        elif t_circle == None:
            t_final = t_wall
        elif t_wall == None:
            t_final = t_circle
        
        if t_final == None: # ray goes through nothing
            return end
        return (sx + t_final*dx, sy + t_final*dy)
    
    def draw_objects(self):
        self.obj_pos += self.obj_vel
        
        # Check obj collision, change direction and fix possible overlap
        # was lazy just ctrl+c ctrl+v from bouncy_balls.py =P
        if (self.obj_pos[1] >= HEIGHT - self.obj_radius):
            self.obj_vel[1] *= -1
            self.obj_pos[1] = HEIGHT - self.obj_radius
        if (self.obj_pos[1] <= self.obj_radius):
            self.obj_vel[1] *= -1
            self.obj_pos[1] = self.obj_radius
        if (self.obj_pos[0] >= WIDTH - self.obj_radius):
            self.obj_vel[0] *= -1
            self.obj_pos[0] = WIDTH - self.obj_radius
        if (self.obj_pos[0] <= self.obj_radius):
            self.obj_vel[0] *= -1
            self.obj_pos[0] = self.obj_radius
        
        pygame.draw.rect(screen, WHITE, self.wall)
        # pygame.draw.rect(screen, GREY , self.mirror)
        # screen.blit(self.mirror_text, (965, 875))
        pygame.draw.circle(screen, WHITE, self.obj_pos.astype(int), int(self.obj_radius))

# Main game loop
def main():
    active = False
    running = True
    clock = pygame.time.Clock()
    light = Light(n_rays= 1000)
    while running:
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

        # Lights and Objects
        light.draw_objects()
        light.draw_rays()
        light.draw_sun()
        
        pygame.display.update()
    pygame.quit()

if __name__ == "__main__":
    main()