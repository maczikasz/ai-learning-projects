import numpy as np


class GameUpdater:
    def __init__(self, reward_calculator, ai_input_provider, ai, score_history, game_world):
        self.game_world = game_world
        self.score_history = score_history
        self.ai = ai
        self.ai_input_provider = ai_input_provider
        self.reward_calculator = reward_calculator

    def update(self, car):
        ai_input = self.ai_input_provider.calculate_ai_input(car)
        reward = self.reward_calculator.calculate_reward(car)

        action = self.ai.get_next_action(ai_input, reward)
        self.score_history.append(self.ai.score())

        self.game_world.affect_car(car)

        action.apply(car, self.game_world)

    def update_and_compare(self, car, simulated_car):
        ai_input = self.ai_input_provider.calculate_ai_input(car)
        ai_input_sim = self.ai_input_provider.calculate_ai_input(simulated_car)

        self.compare_with_sim(ai_input, ai_input_sim)

        reward_sim = self.reward_calculator.calculate_reward_no_affect(simulated_car)
        reward = self.reward_calculator.calculate_reward(car)

        self.compare_with_sim_scalar(reward, reward_sim)

        action = self.ai.get_next_action(ai_input, reward)
        self.score_history.append(self.ai.score())

        self.game_world.affect_car(car)
        self.game_world.affect_car(simulated_car)

        action.apply(car, self.game_world)
        action.apply(simulated_car, self.game_world)

        self.compare_with_sim(car.pos, simulated_car.pos)
        self.compare_with_sim(car.sensor1, simulated_car.sensor1)
        self.compare_with_sim(car.sensor2, simulated_car.sensor2)
        self.compare_with_sim(car.sensor3, simulated_car.sensor3)
        self.compare_with_sim_scalar(car.signal1, simulated_car.signal1)
        self.compare_with_sim_scalar(car.signal2, simulated_car.signal2)
        self.compare_with_sim_scalar(car.signal3, simulated_car.signal3)

    def compare_with_sim(self, real_input, sim_input):
        if not np.array_equal(real_input, sim_input):
            print "Difference real %s : sim %s" % (real_input, sim_input)

    def compare_with_sim_scalar(self, real_input, sim_input):
        if real_input != sim_input:
            print "Difference real %s : sim %s" % (real_input, sim_input)
