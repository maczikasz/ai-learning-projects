from collections import deque

from . memory.n_step_replay_memory import NStepReplayMemory, Transition, NStepTransition


class GameUpdater:
    def __init__(self, reward_calculator, ai_input_provider, ai, score_history, game_world, n_steps):
        self.n_steps = n_steps
        self.game_world = game_world
        self.score_history = score_history
        self.ai = ai
        self.ai_input_provider = ai_input_provider
        self.reward_calculator = reward_calculator
        self.memory = NStepReplayMemory(10000, n_steps)
        self.last_transitions = deque()

    def update(self, car):
        state = self.ai_input_provider.calculate_ai_input(car)

        action = self.ai.get_next_action(state)
        reward = self.reward_calculator.calculate_reward(car)
        self.ai.brain.append_reward(reward)

        self.score_history.append(self.ai.score())

        self.game_world.affect_car(car)

        action.apply(car, self.game_world)
        next_state = self.ai_input_provider.calculate_ai_input(car)
        self.last_transitions.append(Transition(state, action, reward, next_state))

        if len(self.last_transitions) == self.n_steps:
            n_step_transition = NStepTransition(self.last_transitions)
            self.memory.push(n_step_transition)
            if len(self.memory.memory) > 900:
                transition_samples = self.memory.sample(300)
                self.ai.brain.learn_from_transitions(transition_samples)
            self.last_transitions = deque()
