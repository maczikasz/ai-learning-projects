import collections

import numpy as np
from kivy.vector import Vector

Point = collections.namedtuple("Point", "x y")


class SelfDrivingCarGameWorld:
    def __init__(self, width, height):
        self.sand = np.zeros((width, height))
        self.sand_lines = []
        self.width = width
        self.height = height
        self.goal = Point(20, height - 20)

    def affect_car(self, car):
        x = car.x
        y = car.y
        distance = np.sqrt((x - self.goal.x) ** 2 + (y - self.goal.y) ** 2)
        if self.sand[int(x), int(y)] > 0:
            car.velocity = Vector(1, 0).rotate(car.angle)
        else:  # otherwise
            car.velocity = Vector(6, 0).rotate(car.angle)

        if distance < 100:
            self.goal = Point(self.width - self.goal.x, self.height - self.goal.y)
            print self.goal

    def get_goal(self):
        return self.goal

    def reset_sand(self):
        self.sand = np.zeros((self.width, self.height))
        self.sand_lines = []
