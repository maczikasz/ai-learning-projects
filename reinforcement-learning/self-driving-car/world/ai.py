from ai_input_provider import AiInputProvider
from abc import ABCMeta, abstractmethod


class SelfDrivingCarAI:
    def __init__(self, gamma, dqn_initializator):
        self.brain = dqn_initializator(AiInputProvider.INPUT_DIM, AiActionProvider.NUMBER_OF_ACTIONS, gamma)

    def get_next_action(self, input, last_reward):
        action = self.brain.update(last_reward, input)
        return AiActionProvider.ACTIONS[action]


class AiAction:
    __metaclass__ = ABCMeta

    @abstractmethod
    def apply(self, car, game_world):
        pass


class NoOpAction(AiAction):
    def apply(self, car, game_world):
        pass


class RotationAction(AiAction):
    def __init__(self, deg):
        self.deg = deg

    def apply(self, car, game_world):
        car.move(self.deg, game_world)


class AiActionProvider:
    ACTIONS = [NoOpAction(), RotationAction(-20), RotationAction(-10), RotationAction(10), RotationAction(20)]
    NUMBER_OF_ACTIONS = len(ACTIONS)
