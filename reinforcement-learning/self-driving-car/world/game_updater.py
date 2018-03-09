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
