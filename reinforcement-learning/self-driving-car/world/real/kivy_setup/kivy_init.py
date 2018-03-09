import numpy as np
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty, StringProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from kivy.vector import Vector


class Car(Widget):
    angle = NumericProperty(0)
    rotation = NumericProperty(0)
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)
    sensor1_x = NumericProperty(0)
    sensor1_y = NumericProperty(0)
    sensor1 = ReferenceListProperty(sensor1_x, sensor1_y)
    sensor2_x = NumericProperty(0)
    sensor2_y = NumericProperty(0)
    sensor2 = ReferenceListProperty(sensor2_x, sensor2_y)
    sensor3_x = NumericProperty(0)
    sensor3_y = NumericProperty(0)
    sensor3 = ReferenceListProperty(sensor3_x, sensor3_y)
    signal1 = NumericProperty(0)
    signal2 = NumericProperty(0)
    signal3 = NumericProperty(0)

    def move(self, rotation, game_world):
        self.pos = Vector(*self.velocity) + self.pos
        self.rotation = rotation
        self.angle = self.angle + self.rotation
        self.sensor1 = Vector(30, 0).rotate(self.angle) + self.pos
        self.sensor2 = Vector(30, 0).rotate((self.angle + 30) % 360) + self.pos
        self.sensor3 = Vector(30, 0).rotate((self.angle - 30) % 360) + self.pos
        self.signal1 = int(np.sum(game_world.sand[int(self.sensor1_x) - 10:int(self.sensor1_x) + 10,
                                  int(self.sensor1_y) - 10:int(self.sensor1_y) + 10])) / 400.
        self.signal2 = int(np.sum(game_world.sand[int(self.sensor2_x) - 10:int(self.sensor2_x) + 10,
                                  int(self.sensor2_y) - 10:int(self.sensor2_y) + 10])) / 400.
        self.signal3 = int(np.sum(game_world.sand[int(self.sensor3_x) - 10:int(self.sensor3_x) + 10,
                                  int(self.sensor3_y) - 10:int(self.sensor3_y) + 10])) / 400.
        if self.sensor1_x > game_world.width - 10 or self.sensor1_x < 10 or self.sensor1_y > game_world.height - 10 or self.sensor1_y < 10:
            self.signal1 = 1.
        if self.sensor2_x > game_world.width - 10 or self.sensor2_x < 10 or self.sensor2_y > game_world.height - 10 or self.sensor2_y < 10:
            self.signal2 = 1.
        if self.sensor3_x > game_world.width - 10 or self.sensor3_x < 10 or self.sensor3_y > game_world.height - 10 or self.sensor3_y < 10:
            self.signal3 = 1.


class Ball1(Widget):
    pass


class Ball2(Widget):
    pass


class Ball3(Widget):
    pass


class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)
    rootpath = StringProperty("")


class SaveDialog(FloatLayout):
    save = ObjectProperty(None)
    text_input = ObjectProperty(None)
    cancel = ObjectProperty(None)
    rootpath = StringProperty("")
