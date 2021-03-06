from abc import ABCMeta, abstractmethod

from . ai_input_provider import AiInputProvider


class SelfDrivingCarAI:
    def __init__(self, gamma, dqn_initializator):
        self.brain = dqn_initializator(AiInputProvider.INPUT_DIM, AiActionProvider.NUMBER_OF_ACTIONS, gamma)

    def get_next_action(self, input):
        action = self.brain.update(input)
        return AiActionProvider.ACTIONS[action]

    def score(self):
        return self.brain.score()


class AiAction:
    __metaclass__ = ABCMeta

    @abstractmethod
    def apply(self, car, game_world):
        pass


class RotationAction(AiAction):
    def __init__(self, deg, index):
        self.index = index
        self.deg = deg

    def apply(self, car, game_world):
        car.move(self.deg, game_world)


class AiActionProvider:
    ACTIONS = [RotationAction(0, 0), RotationAction(-20, 1), RotationAction(-10, 2), RotationAction(10, 3),
               RotationAction(20, 4)]
    NUMBER_OF_ACTIONS = len(ACTIONS)
