# Based on the original for udemy course https://www.udemy.com/artificial-intelligence-az/


# Self Driving Car
from kivy.lang import Builder

from ai.ai_self import Dqn
from world.game import Game
from world.ai import SelfDrivingCarAI
from world.reward_calculator import RewardCalculator
from world.game_world import SelfDrivingCarGameWorld
from world.ai_input_provider import AiInputProvider
from world.sand_painter import MyPaintWidget
from world.car_app import CarApp
from kivy.config import Config
from kivy_setup.kivy_init import Car, Ball1, Ball2, Ball3

# Adding this line if we don't want the right click to put a red point
Config.set('graphics', 'width', '800')
Config.set('graphics', 'height', '600')
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')

# Running the whole thing
if __name__ == '__main__':
    Builder.load_file("kivy_setup/car.kv")
    game_world = SelfDrivingCarGameWorld(800, 600)
    score_history = None
    reward_calculator = RewardCalculator(game_world)
    ai_input_provider = AiInputProvider(game_world)
    ai = SelfDrivingCarAI(0.9, Dqn)
    game = Game(reward_calculator, ai_input_provider, ai, score_history, game_world)
    save_orchestrator = None
    sand_painter = MyPaintWidget(800, 600, game_world)
    CarApp(game_world, save_orchestrator, score_history, game, sand_painter).run()
