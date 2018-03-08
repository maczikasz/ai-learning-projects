# Creating the game class
from kivy.properties import ObjectProperty
from kivy.uix.widget import Widget
from kivy.vector import Vector


class Game(Widget):
    car = ObjectProperty(None)
    ball1 = ObjectProperty(None)
    ball2 = ObjectProperty(None)
    ball3 = ObjectProperty(None)

    def __init__(self, reward_calculator, ai_input_provider, ai, score_history, game_world, **kwargs):
        super(Game, self).__init__(**kwargs)
        self.last_reward = 0
        self.score_history = score_history
        self.game_world = game_world
        self.ai = ai
        self.ai_input_provider = ai_input_provider
        self.reward_calculator = reward_calculator

    def serve_car(self):
        self.car.center = self.center
        self.car.velocity = Vector(6, 0)

    def update_ui_element_positions(self):
        self.ball1.pos = self.car.sensor1
        self.ball2.pos = self.car.sensor2
        self.ball3.pos = self.car.sensor3

    def update(self, dt):
        ai_input = self.ai_input_provider.calculate_ai_input(self.car)
        reward = self.reward_calculator.calculate_reward(self.car)

        action = self.ai.get_next_action(ai_input, reward)
        # self.score_history.append_score(self.ai.score())

        self.game_world.affect_car(self.car)

        action.apply(self.car, self.game_world)
        self.update_ui_element_positions()

        # rotation = action2rotation[action]
        # self.car.move(rotation)
