import collections

import numpy as np

Point = collections.namedtuple("Point", "x y")


class GameSimulator:
    def __init__(self, game_updater):
        self.car = SimulatedCar(np.array([390, 295]), np.array([6, 0]))
        self.game_updater = game_updater

    def update(self, dt):
        self.game_updater.update(self.car)


class GameSimulatorEnv:
    def __init__(self, game_updater, counter):
        self.counter = counter
        self.car = SimulatedCar(np.array([390, 295]), np.array([6, 0]))
        self.game_updater = game_updater

    def reset(self):
        self.car = SimulatedCar(np.array([390, 295]), np.array([6, 0]))

    def get_state(self):
        return self.game_updater.get_state(self.car)

    def take_action(self, ai_action):
        self.game_updater.take_action(self.car, ai_action)
        return self.game_updater.get_reward(self.car)

    def is_done(self):
        return self.counter.counter >= 2


def _rotate(deg):
    theta = np.radians(deg)
    c, s = np.cos(theta), np.sin(theta)
    return np.array([[c, -s], [s, c]])


def _to_point(array):
    return Point(*array)


class SimulatedCar:
    angle = 0
    rotation = 0
    sensor1 = Point(0, 0)
    sensor2 = Point(0, 0)
    sensor3 = Point(0, 0)
    signal1 = 0
    signal2 = 0
    signal3 = 0

    def __init__(self, starter_center, velocity):
        self.velocity = velocity
        self._set_pos(starter_center)

    def _set_pos(self, pos):
        self.pos = pos
        self.x = pos[0]
        self.y = pos[1]

    def move(self, rotation, game_world):
        self._set_pos(self.velocity + self.pos)
        self.rotation = rotation
        self.angle = self.angle + self.rotation
        self.sensor1 = _to_point(np.matmul(_rotate(self.angle), np.array([30, 0])) + self.pos)
        self.sensor2 = _to_point(np.matmul(_rotate((self.angle + 30) % 360), np.array([30, 0])) + self.pos)
        self.sensor3 = _to_point(np.matmul(_rotate((self.angle - 30) % 360), np.array([30, 0])) + self.pos)

        self.signal1 = int(np.sum(game_world.sand[int(self.sensor1.x) - 10:int(self.sensor1.x) + 10,
                                  int(self.sensor1.y) - 10:int(self.sensor1.y) + 10])) / 400.
        self.signal2 = int(np.sum(game_world.sand[int(self.sensor2.x) - 10:int(self.sensor2.x) + 10,
                                  int(self.sensor2.y) - 10:int(self.sensor2.y) + 10])) / 400.
        self.signal3 = int(np.sum(game_world.sand[int(self.sensor3.x) - 10:int(self.sensor3.x) + 10,
                                  int(self.sensor3.y) - 10:int(self.sensor3.y) + 10])) / 400.
        if self.sensor1.x > game_world.width - 10 or self.sensor1.x < 10 or self.sensor1.y > game_world.height - 10 or self.sensor1.y < 10:
            self.signal1 = 1.
        if self.sensor2.x > game_world.width - 10 or self.sensor2.x < 10 or self.sensor2.y > game_world.height - 10 or self.sensor2.y < 10:
            self.signal2 = 1.
        if self.sensor3.x > game_world.width - 10 or self.sensor3.x < 10 or self.sensor3.y > game_world.height - 10 or self.sensor3.y < 10:
            self.signal3 = 1.

        self.reposition(game_world)

    def reposition(self, game_world):
        x = self.x
        y = self.y
        if x < 10:
            x = 10
        if y < 10:
            y = 10
        if x > game_world.width - 10:
            x = game_world.width - 10
        if y > game_world.height - 10:
            y = game_world.height - 10

        self._set_pos(Point(x, y))
