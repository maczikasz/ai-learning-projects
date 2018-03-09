# Based on the original for udemy course https://www.udemy.com/artificial-intelligence-az/


# Self Driving Car
import os

from kivy import Config
from kivy.lang import Builder

from ai.ai_self import Dqn
from infra.save_orchestrator import SaveOrchestrator
from infra.score_history import ScoreHistory
from world.ai import SelfDrivingCarAI
from world.ai_input_provider import AiInputProvider
from world.game_updater import GameUpdater
from world.game_world import SelfDrivingCarGameWorld
from world.real.car_app import CarApp
from world.real.game import Game
from world.reward_calculator import RewardCalculator
from world.sand_painter import MyPaintWidget
from world.simulator.car_app_simulator import CarAppSimulator
from world.simulator.game_simulator import GameSimulator

# Adding this line if we don't want the right click to put a red point
SAVES = "./saves"
SAVES_SANDS = "%s/sands" % SAVES
SAVES_BRAINS = "%s/brains" % SAVES
WIDTH = 600
HEIGHT = 800
Config.set('graphics', 'width', HEIGHT)
Config.set('graphics', 'height', WIDTH)
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')


def ensure_dir(path):
    if not os.path.exists(path):
        os.mkdir(path)


ensure_dir(SAVES)
ensure_dir(SAVES_BRAINS)
ensure_dir(SAVES_SANDS)

# Running the whole thing
if __name__ == '__main__':
    game_world = SelfDrivingCarGameWorld(HEIGHT, WIDTH)
    reward_calculator = RewardCalculator(game_world)
    ai_input_provider = AiInputProvider(game_world)
    ai = SelfDrivingCarAI(0.9, Dqn)
    score_history = ScoreHistory()
    save_orchestrator = SaveOrchestrator("saves/", ai.brain, game_world)
    game_updater = GameUpdater(reward_calculator, ai_input_provider, ai, score_history, game_world)
    sand_painter = MyPaintWidget(HEIGHT, WIDTH, game_world)

    if False:
        game_simulator = GameSimulator(game_updater)
        car_app_simulator = CarAppSimulator(game_world, save_orchestrator, score_history, game_simulator,
                                            lambda step: step < 100000)
        car_app_simulator.run()

    Builder.load_file("world/real/kivy_setup/car.kv")
    game = Game(game_updater)
    CarApp(game_world, save_orchestrator, score_history, game, sand_painter, SAVES_SANDS, SAVES_BRAINS).run()
