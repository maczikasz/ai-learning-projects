from collections import namedtuple, deque

Transition = namedtuple('Step', ['state', 'action', 'reward', 'done'])


class EligibilityTraceAITrainer:
    def __init__(self, ai, env):
        self.env = env
        self.ai = ai
        self.steps = 0
        # self.memory = NStepReplayMemory()

    def train(self, condition, after_each_step):
        while condition(self.steps):
            self.play_one_epoch()
            after_each_step(self.steps)
            self.steps += 1

    def play_one_epoch(self):
        self.env.reset()
        for i in range(0, 200):
            self.do_n_steps(10)

    def do_n_steps(self, n):
        transition_tracker = NStepTransition()
        cummul_reward = 0
        for i in range(0, n):
            state = self.env.get_state()
            ai_action = self.ai.get_action(state)
            self.env.take_action(ai_action)
            reward = self.env.get_reward()
            is_done = self.env.is_done()
            transition_tracker.add_transition(Transition(state, ai_action, reward, is_done))
            cummul_reward += reward
            if is_done:
                self.env.reset()
                break

        self.ai.append_reward(cummul_reward)


class NStepTransition:
    def __init__(self):
        self.history = deque()

    def add_transition(self, transition):
        self.history.append(transition)


# class NStepReplayMemory:
