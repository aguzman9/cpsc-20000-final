import pygame
import math
pygame.init()
win = pygame.display.set_mode((900, 900))
pygame.display.set_caption("people")

yellow = (255, 255, 0)
blue = (0, 150, 255)
red = (180, 50, 50)
gray = (150, 150, 150)
v_color = (255, 255, 200)
j_color = (165, 102, 80)
s_color = (180, 160, 80)
blue_green = (20, 231, 231)

class Planet:
    au = 149.6e9
    G = 6.67e-11
    s = 20 / au
    timestep = 86400

    def __init__(self, x, y, radius, color, mass):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass

        self.orbit = []
        self.sun = False
        self.d_to_sun = 0

        self.x_vel = 0
        self.y_vel = 0

    def draw(self, win):
        x = self.x * self.s + 450
        y = self.y * self.s + 450
        pygame.draw.circle(win, self.color, (x, y), self.radius)

    def force(self, other):
        dx = other.x - self.x
        dy = other.y - self.y
        dis = math.sqrt(dx**2 + dy**2)

        if other.sun:
            self.dis_to_sun = dis

        f = Planet.G * self.mass * other.mass / dis**2
        theta = math.atan2(dy, dx)
        f_x = math.cos(theta) * f
        f_y = math.sin(theta) * f
        return f_x, f_y

    def pos(self, planets):
        total_fx = total_fy = 0
        for planet in planets:
            if self == planet:
                continue
            fx, fy = self.force(planet)
            total_fx += fx
            total_fy += fy

        self.x_vel += total_fx / self.mass * self.timestep
        self.y_vel += total_fy / self.mass * self.timestep

        self.x += self.x_vel * self.timestep
        self.y += self.y_vel * self.timestep
        self.orbit.append((self.x, self.y))

def fun():
    run = True
    clock = pygame.time.Clock()

    sun = Planet(0, 0, 5, yellow, 1.98*10**30)
    sun.sun = True

    mercury = Planet(0.387 * Planet.au, 0, 1, gray, 3.30 * 10**23)
    mercury.y_vel = -47400

    venus = Planet(0.723 * Planet.au, 0, 1.1, v_color, 4.8685 * 10**24)
    venus.y_vel = -35060

    earth = Planet(-1 * Planet.au, 0, 1.2, blue, 5.9742 * 10**24)
    earth.y_vel = 30000

    mars = Planet(-1.524 * Planet.au, 0, 1.1, red, 6.39 * 10**23)
    mars.y_vel = 24077

    jupiter = Planet(-5.2 * Planet.au, 0, 2.1, j_color, 1.89813 * 10**27)
    jupiter.y_vel = 13070

    saturn = Planet(9.5 * Planet.au, 0, 2, s_color, 5.683 * 10**26)
    saturn.y_vel = -9690

    uranus = Planet(-19.8 * Planet.au, 0, 1.7, blue_green, 8.681 * 10**25)
    uranus.y_vel = 6810

    planets = [sun, mercury, venus, earth, mars, jupiter, saturn, uranus]

    while run:
        clock.tick(60)
        win.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        for planet in planets:
            planet.draw(win)
            planet.pos(planets)

        pygame.display.update()
    pygame.quit()
fun()
