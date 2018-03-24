from kivy.vector import Vector


class AiInputProvider:
    INPUT_DIM = 5

    def __init__(self, game_world):
        self.game_world = game_world

    def calculate_ai_input(self, car):
        x = car.x
        y = car.y
        goal = self.game_world.get_goal()
        xx = goal.x - x
        yy = goal.y - y
        orientation = Vector(*car.velocity).angle((xx, yy)) / 180.
        return [car.signal1, car.signal2, car.signal3, orientation, -orientation]
