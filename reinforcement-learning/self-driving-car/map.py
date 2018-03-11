# Based on the original for udemy course https://www.udemy.com/artificial-intelligence-az/


import argparse
# Self Driving Car
import os

from kivy import Config
from kivy.lang import Builder

# from ai.ai_self_keras import Dqn
from ai.ai_self_tf import Dqn
# from ai.ai_self import Dqn
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

UI = "ui"
SIMULATION = "simulation"

parser = argparse.ArgumentParser(description='Run self driving car AI.')
parser.add_argument('--mode', help='Run in simulation mode', choices=[SIMULATION, UI])
parser.add_argument('--start_brain', help='Name of brain to start with, from saves/brains')
parser.add_argument('--end_brain', help='Name of brain to write to after the iterations are done, from saves/brains')
parser.add_argument('--sand', help='Name of sand file to load from saves/sands')
parser.add_argument('--iterations', type=int, help='How many iterations to run in simulation mode')

args = parser.parse_args()

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
game_world = SelfDrivingCarGameWorld(HEIGHT, WIDTH)
reward_calculator = RewardCalculator(game_world)
ai_input_provider = AiInputProvider(game_world)
ai = SelfDrivingCarAI(0.9, Dqn)
score_history = ScoreHistory()
save_orchestrator = SaveOrchestrator("saves/", ai.brain, game_world)
game_updater = GameUpdater(reward_calculator, ai_input_provider, ai, score_history, game_world)
sand_painter = MyPaintWidget(HEIGHT, WIDTH, game_world)

if args.sand:
    save_orchestrator.load_sand(os.path.join(SAVES_SANDS, args.sand))

if args.start_brain:
    save_orchestrator.load_brain(os.path.join(SAVES_BRAINS, args.start_brain))

if args.mode == SIMULATION:
    if not args.iterations:
        raise AssertionError("Iterations must be defined for simulation")

    game_simulator = GameSimulator(game_updater)
    car_app_simulator = CarAppSimulator(game_world, save_orchestrator, score_history, game_simulator,
                                        lambda step: step < args.iterations)
    car_app_simulator.run()
    if args.end_brain:
        save_orchestrator.save_brain(os.path.join(SAVES_BRAINS, args.end_brain))
    score_history.plot_rewards()
    print "Finished %i iterations brain saved to %s" % (args.iterations, args.end_brain)
elif args.mode == UI:
    Builder.load_file("world/real/kivy_setup/car.kv")
    game = Game(game_updater)
    CarApp(game_world, save_orchestrator, score_history, game, sand_painter, SAVES_SANDS, SAVES_BRAINS).run()
else:
    raise AssertionError("Must be either ui or simulation")
