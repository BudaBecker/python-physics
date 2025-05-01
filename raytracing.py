# TODO:
# 1- Refactor so can add new objects without any complications (its all hard-coded cuz it was my first try doing it)
# 2- Change all the raw math to numpy/math functions for easy understanding
# 3- Add first person view (the coding train challange #146)

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
RAY_THICK = 2
N_RAYS = 1000
SUN_SIZE = 20

# RGB
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 50)
ORANGE = (218, 160, 109)
GREY = (100, 100, 100)

# Light class
class Light:
    def __init__(self):
        self.sun_radius = SUN_SIZE
        self.n_rays = N_RAYS
        self.ray_color = YELLOW
        self.sun_pos = (float(WIDTH/2), float(HEIGHT/2))
        self.obj_pos = np.array([WIDTH/4, HEIGHT/2], dtype=float)
        self.obj_radius = float(150)
        self.obj_vel = np.array([0, 2], dtype=float)
        self.wall = (1200, 200, 50, 500)
        self.mirror = (900, 870, 200, 50)
        self.mirror_text = mirror_font.render("MIRROR", 1, WHITE)
    
    def draw_sun(self):
        pygame.draw.circle(screen, BLACK, self.sun_pos, self.sun_radius+1)
        pygame.draw.circle(screen, self.ray_color, self.sun_pos, self.sun_radius)
    
    def draw_rays(self):
        for i in range(self.n_rays):
            angle = 2 * math.pi * i / self.n_rays
            start = (self.sun_pos[0] + math.cos(angle) * self.sun_radius, self.sun_pos[1] + math.sin(angle) * self.sun_radius)
            end = (self.sun_pos[0] + math.cos(angle) * (self.sun_radius + 1900), self.sun_pos[1] + math.sin(angle) * (self.sun_radius + 1900))
            end, mirror = self.check_ray(start, end)
            pygame.draw.line(screen, self.ray_color, start, end, RAY_THICK)

            if mirror:
                sun_start = start
                start = end
                end = self.reflect_ray(sun_start, start, angle)
                end = self.check_ray_no_mirror(start, end)
                pygame.draw.line(screen, self.ray_color, start, end, RAY_THICK)
    
    def reflect_ray(self, sun_start, start, angle):
        angle = angle - math.pi
        
        # normal rays
        if (angle % math.pi == 0):
            return sun_start
        # upper mirror side
        if (self.mirror[0]) <= start[0] <= (self.mirror[0] + self.mirror[2]) and (start[1] <= self.mirror[1]):
            angle = math.pi - angle
            return (start[0] + math.cos(angle) * (1900), start[1] + math.sin(angle) * (1900))
        # right mirror side
        if (start[0] >= self.mirror[0] + self.mirror[2]) and ((self.mirror[1]) <= start[1] <= (self.mirror[1] + self.mirror[3])):
            angle = (2*math.pi) - angle
            return (start[0] + math.cos(angle) * (1900), start[1] + math.sin(angle) * (1900))
        # left mirror side
        if (start[0] <= self.mirror[0]) and ((self.mirror[1]) <= start[1] <= (self.mirror[1] + self.mirror[3])):
            angle = (2*math.pi) - angle
            return (start[0] + math.cos(angle) * (1900), start[1] + math.sin(angle) * (1900))
        return sun_start
    
    def check_ray_no_mirror(self, start, end):
        # do NOT look here, go to check_ray(), same here but without the mirror.
        sx, sy = start
        ex, ey = end
        dx, dy = ex - sx, ey - sy
        cx, cy = self.obj_pos
        r = self.obj_radius
        x_min_w, y_min_w = self.wall[0], self.wall[1]
        x_max_w, y_max_w = self.wall[0] + self.wall[2], self.wall[1] + self.wall[3]
        if ((sx - cx)**2 + (sy - cy)**2 <= r**2) or ((x_min_w <= sx <= x_max_w) and (y_min_w <= sy <= y_max_w)):
            return start
        fx, fy = sx - cx, sy - cy
        a = dx*dx + dy*dy
        b = 2 * (fx*dx + fy*dy)
        c = fx*fx + fy*fy - r*r
        discr = b*b - 4*a*c
        t_circle = None
        if discr >= 0:
            sqrt_d = math.sqrt(discr)
            for t in ((-b - sqrt_d)/(2*a), (-b + sqrt_d)/(2*a)):
                if (0 <= t <= 1):
                    if (t_circle == None) or (t < t_circle):
                        t_circle = t
        t_wall = None
        if dx != 0:
            for x_edge in (x_min_w, x_max_w):
                t = (x_edge - sx) / dx
                if (0 <= t <= 1):
                    y_int = sy + t*dy
                    if y_min_w <= y_int <= y_max_w:
                        if (t_wall == None) or (t < t_wall):
                            t_wall = t
        if dy != 0:
            for y_edge in (y_min_w, y_max_w):
                t = (y_edge - sy) / dy
                if (0 <= t <= 1):
                    x_int = sx + t*dx
                    if x_min_w <= x_int <= x_max_w:
                        if (t_wall == None) or (t < t_wall):
                            t_wall = t
        t_final = None
        if (t_circle != None) and (t_wall != None):
            t_final = min(t_circle, t_wall)
        elif t_circle == None:
            t_final = t_wall
        elif t_wall == None:
            t_final = t_circle
        if t_final == None:
            return end
        return (sx + t_final*dx, sy + t_final*dy)
    
    def check_ray(self, start, end):
        # Setting up constants
        sx, sy = start
        ex, ey = end
        dx, dy = ex - sx, ey - sy  # direction vector (dx, dy) // P(t) = start + t(dx, dy) // *P(t) is the final point
        
        # obstacles parameters
        cx, cy = self.obj_pos # circle
        r = self.obj_radius
        
        x_min_w, y_min_w = self.wall[0], self.wall[1] # wall
        x_max_w, y_max_w = self.wall[0] + self.wall[2], self.wall[1] + self.wall[3]
        
        x_min_m, y_min_m = self.mirror[0], self.mirror[1] # mirror
        x_max_m, y_max_m = self.mirror[0] + self.mirror[2], self.mirror[1] + self.mirror[3] 
        
        # If ray is inside of any object
        if ((sx - cx)**2 + (sy - cy)**2 <= r**2) or ((x_min_w <= sx <= x_max_w) and (y_min_w <= sy <= y_max_w))or ((x_min_m <= sx <= x_max_m) and (y_min_m <= sy <= y_max_m)):
            return start, False
        
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
            for x_edge in (x_min_w, x_max_w):
                t = (x_edge - sx) / dx
                if (0 <= t <= 1):
                    y_int = sy + t*dy
                    if y_min_w <= y_int <= y_max_w:
                        if (t_wall == None) or (t < t_wall):
                            t_wall = t
        if dy != 0:
            for y_edge in (y_min_w, y_max_w):
                t = (y_edge - sy) / dy
                if (0 <= t <= 1):
                    x_int = sx + t*dx
                    if x_min_w <= x_int <= x_max_w:
                        if (t_wall == None) or (t < t_wall):
                            t_wall = t
        
        # Check if ray hits mirror
        t_mirror = None
        if dx != 0:
            for x_edge in (x_min_m, x_max_m):
                t = (x_edge - sx) / dx
                if (0 <= t <= 1):
                    y_int = sy + t*dy
                    if y_min_m <= y_int <= y_max_m:
                        if (t_mirror == None) or (t < t_mirror):
                            t_mirror = t
        if dy != 0:
            for y_edge in (y_min_m, y_max_m):
                t = (y_edge - sy) / dy
                if (0 <= t <= 1):
                    x_int = sx + t*dx
                    if x_min_m <= x_int <= x_max_m:
                        if (t_mirror == None) or (t < t_mirror):
                            t_mirror = t
        
        # Find the smallest t, then return P(t)
        t_final = None
        hits_m = False
        if (t_circle != None) and (t_wall != None) and (t_mirror != None):
            if (t_mirror < min(t_circle, t_wall)):
                t_final = min(t_circle, t_wall)
                hits_m = True
            else:
                t_final = min(t_circle, t_wall)
        elif (t_circle == None) and (t_wall != None) and (t_mirror != None):
            if t_mirror < t_wall:
                t_final = t_mirror
                hits_m = True
            else:
                t_final = t_wall
        elif (t_circle != None) and (t_wall == None) and (t_mirror != None):
            if t_mirror < t_circle:
                t_final = t_mirror
                hits_m = True
            else:
                t_final = t_circle
        elif (t_circle != None) and (t_wall != None) and (t_mirror == None):
            t_final = min(t_circle, t_wall)
        elif (t_circle != None) and (t_wall == None) and (t_mirror == None):
            t_final = t_circle
        elif (t_circle == None) and (t_wall != None) and (t_mirror == None):
            t_final = t_wall
        elif (t_circle == None) and (t_wall == None) and (t_mirror != None):
            t_final = t_mirror
            hits_m = True
        
        if t_final == None: # ray goes through nothing
            return end, hits_m
        return (sx + t_final*dx, sy + t_final*dy), hits_m
    
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
        pygame.draw.rect(screen, GREY , self.mirror)
        screen.blit(self.mirror_text, (965, 875))
        pygame.draw.circle(screen, WHITE, self.obj_pos.astype(int), int(self.obj_radius))

# Main game loop
def main():
    active = False
    running = True
    clock = pygame.time.Clock()
    light = Light()
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