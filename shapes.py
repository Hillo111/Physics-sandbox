import pygame as pg
import numpy as np
from globals import *


class Shape:
    def __init__(self, x, y, weight, bounce_factor, friction, color=(0, 0, 0), unmovable=False, edges=None):
        self.x = x
        self.y = y
        self.mass = weight
        if unmovable:
            self.mass = 9999999999
        self.bounce = bounce_factor
        self.vel_x = 0
        self.vel_y = 0
        self.color = color
        self.f = unmovable
        self.friction = friction

        self.edges = edges

    def check(self):
        print(self.bounce)

    def calc_vel(self, obj2):

        force1 = self.mass * (abs(self.vel_x) + abs(self.vel_y)) ** 1
        force2 = obj2.mass * (abs(obj2.vel_x) + abs(obj2.vel_y)) ** 1

        sum_vel = (force1 + force2) / (self.mass + obj2.mass)

        my_vel = self.mass / (self.mass + obj2.mass) * sum_vel

        return my_vel


class Circle(Shape):
    def __init__(self, x, y, weight, bounce_factor, radius, friction, color=(0, 0, 0), unmovable=False, edges=None):
        super().__init__(x, y, weight, bounce_factor, friction, color, unmovable, edges)
        self.r = radius

    def collision(self, shape):
        if isinstance(shape, Circle):
            s = shape.r + self.r
            dist = np.sqrt((shape.x - self.x) ** 2 + (shape.y - self.y) ** 2)
            if dist <= s:
                return True

        return False

    def colliding(self, shapes):
        for shape in shapes:
            if self.collision(shape):
                return shape

        return None

    def hitting_wall(self):
        if self.edges is None:
            return False

        if self.edges[0] + self.r > self.x or self.edges[1] - self.r < self.x:
            return True

        if self.edges[2] + self.r > self.y or self.edges[3] - self.r < self.y:
            return True

        return False

    def update(self, shapes):
        if self.f:
            return
        old_x, old_y = self.x - self.vel_x, self.y - self.vel_y
        self.vel_y -= gravity

        for shape in shapes:
            if shape != self:
                if self.collision(shape):
                    check_x, check_y = self.vel_x / 60, self.vel_y / 60
                    _old_x, _old_y = old_x, old_y
                    for i in range(60):
                        _old_x += check_x
                        _old_y += check_y

                        self.x = _old_x
                        self.y = _old_y

                        if self.collision(shape):
                            self.x = _old_x - check_x
                            self.y = _old_y - check_y
                            break

                    new_vel = self.calc_vel(shape)

                    x_travel, y_travel = self.x - shape.x, self.y - shape.y

                    d = abs(x_travel) + abs(y_travel)
                    d = d if d != 0 else 1e-9

                    new_x = x_travel / d * new_vel
                    new_y = y_travel / d * new_vel

                    self.vel_x = new_x
                    self.vel_y = new_y

        if self.edges is not None:
            if self.x - self.r < self.edges[0] or self.x + self.r > self.edges[1]:
                self.vel_x *= -self.bounce
                self.vel_x *= (1 - self.friction)

            if self.y - self.r < self.edges[2] or self.y + self.r > self.edges[3]:
                self.vel_y *= -self.bounce
                self.vel_y *= (1 - self.friction)

        self.y += self.vel_y
        self.x += self.vel_x

        if self.edges is not None:
            if self.x - self.r < self.edges[0]:
                self.x = self.edges[0] + self.r - 1

            if self.x + self.r > self.edges[1]:
                self.x = self.edges[1] - self.r + 1

            if self.y - self.r < self.edges[2]:
                self.y = self.edges[2] + self.r - 1

            if self.y + self.r > self.edges[3]:
                self.y = self.edges[3] - self.r + 1

    def draw(self, screen):
        pg.draw.circle(screen, self.color, [int(self.x), int(self.y)], self.r)