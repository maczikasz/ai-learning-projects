import argparse
# Self Driving Car
import os

from ai.async.eligibility_trace_trainer import EligibilityTraceAITrainer
from infra.save_orchestrator import SaveOrchestrator
from infra.score_history import ScoreHistory
from world.ai import SelfDrivingCarAI
from world.ai_input_provider import AiInputProvider
from world.game_updater import GameUpdater
from world.game_world import SelfDrivingCarGameWorld
from world.reward_calculator import RewardCalculator
from world.simulator.game_simulator import GameSimulatorEnv

TF, PYTORCH, KERAS, TF_DOUBLE = ("tf", "pytorch", "keras", "tf_double")

parser = argparse.ArgumentParser(description='Run self driving car AI.')
parser.add_argument('--impl', help='Select implementation to run', choices=[TF, PYTORCH, KERAS, TF_DOUBLE])
parser.add_argument('--start_brain', help='Name of brain to start with, from saves/brains')
parser.add_argument('--end_brain', help='Name of brain to write to after the epochs are done, from saves/brains')
parser.add_argument('--sand', help='Name of sand file to load from saves/sands')
parser.add_argument('--epochs', type=int, help='How many epochs to run in simulation mode')
parser.add_argument('--save_after_epochs', type=int, help='How many epochs to run in simulation mode')

args = parser.parse_args()

if args.impl == TF:
    from ai.tf.ai_self_tf import Dqn
elif args.impl == TF_DOUBLE:
    from ai.tf.ai_self_tf_dualq import Dqn
elif args.impl == KERAS:
    from ai.ai_self_keras import Dqn
elif args.impl == PYTORCH:
    from ai.ai_self import Dqn

# Adding this line if we don't want the right click to put a red point
SAVES = "./saves"
SAVES_SANDS = "%s/sands" % SAVES
SAVES_BRAINS = "%s/brains" % SAVES
WIDTH = 600
HEIGHT = 800


def ensure_dir(path):
    if not os.path.exists(path):
        os.mkdir(path)


ensure_dir(SAVES)
ensure_dir(SAVES_BRAINS)
ensure_dir(SAVES_SANDS)


class GoalChangeCounter:
    def __init__(self):
        self.counter = 0

    def register_goal_change(self):
        self.counter += 1


goal_change_counter = GoalChangeCounter()

# Running the whole thing
game_world = SelfDrivingCarGameWorld(HEIGHT, WIDTH, goal_change_listener=goal_change_counter.register_goal_change)
reward_calculator = RewardCalculator(game_world)
ai_input_provider = AiInputProvider(game_world)
ai = SelfDrivingCarAI(0.9, Dqn)
score_history = ScoreHistory()
save_orchestrator = SaveOrchestrator("saves/", ai.brain, game_world)
game_updater = GameUpdater(reward_calculator, ai_input_provider, ai, score_history, game_world)

if args.sand:
    save_orchestrator.load_sand(os.path.join(SAVES_SANDS, args.sand))

if args.start_brain:
    save_orchestrator.load_brain(os.path.join(SAVES_BRAINS, args.start_brain))

if not args.epochs and not args.save_after_epochs:
    raise AssertionError("epochs or save_after_epochs must be defined for simulation")

game_simulator = GameSimulatorEnv(game_updater, goal_change_counter)
if args.epochs:
    def condition(step):
        return step < args.epochs
else:
    def condition(step):
        return True

if args.save_after_epochs:
    def after_each_step(step):
        if step % args.save_after_epochs == 0 and step != 0:
            print "Saving brain"
            save_orchestrator.save_brain(os.path.join(SAVES_BRAINS, args.end_brain))
else:
    def after_each_step(step):
        pass

trainer = EligibilityTraceAITrainer(ai, game_simulator)

trainer.train(condition, after_each_step)

if args.end_brain:
    save_orchestrator.save_brain(os.path.join(SAVES_BRAINS, args.end_brain))
score_history.plot_rewards()
print "Finished %i epochs brain saved to %s" % (args.epochs, args.end_brain)
