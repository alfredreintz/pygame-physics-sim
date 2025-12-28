import math
import time
from sys import exit

import pygame


class Planet(pygame.sprite.Sprite):
    def __init__(self, img, x, y, mass, v_x=0, v_y=0):
        super().__init__()
        self.image = pygame.image.load(img).convert_alpha()
        self.rect = self.image.get_rect(center=(x, y))
        self.mass = mass
        self.v_x = v_x
        self.v_y = v_y

    def update(self, dt):
        self.rect.x += self.v_x * dt
        self.rect.y += self.v_y * dt

    def set_velocity(self, v_x, v_y):
        self.v_x = v_x
        self.v_y = v_y

    def set_acceleration(self, a_x, a_y, dt):
        self.v_x += a_x * dt
        self.v_y += a_y * dt

    def calc_gravity(self, planets, dt):
        grav_const = 9e-17
        for planet in planets:
            if planet != self:
                dx = planet.rect.center[0] - self.rect.center[0]
                dy = planet.rect.center[1] - self.rect.center[1]
                if dx == 0: angle = 0
                else: angle = math.tanh(dy / dx)
                force = grav_const * self.mass * planet.mass / (math.hypot(dx, dy) ** 2)
                acceleration = force / self.mass
                if dx > 0:
                    a_x = math.cos(angle) * acceleration
                    a_y = math.sin(angle) * acceleration
                else:
                    a_x = -math.cos(angle) * acceleration
                    a_y = -math.sin(angle) * acceleration

                self.set_acceleration(a_x, a_y, dt)
                print(dx, dy, a_x, a_y, acceleration, angle)


pygame.init()
screen = pygame.display.set_mode((1300, 700))
background = pygame.image.load("img/background.png").convert()
pygame.display.set_caption("Gravity Simulator")

font = pygame.font.Font(None, 50)
txt_surf = font.render("FPS", False, "White")

clock = pygame.time.Clock()
prev_time = time.time()

# 0.7
# -0.7
fps = 60

planets = pygame.sprite.Group()
planets.add(Planet("img/moon.png", 650, 350, 7.34767309e22, 1, 100))
planets.add(Planet("img/moon.png", 850, 350, 7.34767309e22, 0, -100))

for planet in planets:
    print(planet.rect.center)

while True:
    dt = pygame.time.get_ticks() / 1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    now = time.time()
    dt = now - prev_time
    prev_time = now

    screen.blit(background, (0, 0))
    screen.blit(font.render(f"FPS: {round(clock.get_fps())}", True, "White"), (0, 0))


    for planet in planets:
        planet.calc_gravity(planets, dt)

    print("#" * 40)

    planets.draw(screen)
    planets.update(dt)

    pygame.display.update()

    clock.tick(fps)
