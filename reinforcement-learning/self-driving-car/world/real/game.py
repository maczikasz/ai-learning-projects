# Creating the game class
from kivy.properties import ObjectProperty
from kivy.uix.widget import Widget
from kivy.vector import Vector


class Game(Widget):
    car = ObjectProperty(None)
    ball1 = ObjectProperty(None)
    ball2 = ObjectProperty(None)
    ball3 = ObjectProperty(None)

    def __init__(self, gameUpdater, game_simulator, **kwargs):
        super(Game, self).__init__(**kwargs)
        self.game_simulator = game_simulator
        self.game_updater = gameUpdater
        self.last_reward = 0

    def serve_car(self):
        self.car.center = self.center
        self.car.velocity = Vector(6, 0)

    def update_ui_element_positions(self):
        self.ball1.pos = self.car.sensor1
        self.ball2.pos = self.car.sensor2
        self.ball3.pos = self.car.sensor3

    def update(self, dt):
        self.game_updater.update_and_compare(self.car, self.game_simulator.car)
        self.update_ui_element_positions()
