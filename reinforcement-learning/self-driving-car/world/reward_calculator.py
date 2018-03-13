import numpy as np


class RewardCalculator():
    def __init__(self, game_world):
        self.game_world = game_world
        self.last_distance = 0
        self.steps_since_last_goal = 0
        self.living_penalty = 0

    def calculate_reward(self, car):
        x = car.x
        y = car.y

        distance = np.sqrt((x - self.game_world.get_goal().x) ** 2 + (y - self.game_world.get_goal().y) ** 2)
        if self.game_world.sand[int(x), int(y)] > 0:
            last_reward = -2
        else:  # otherwise
            # last_reward = -1
            if distance < self.last_distance:
                last_reward = 0.3
            else:
                last_reward = -0.1

        if x < 10:
            car.x = 10
            last_reward = -1
        if x > self.game_world.width - 10:
            car.x = self.game_world.width - 10
            last_reward = -1
        if y < 10:
            car.y = 11
            last_reward = -2
        if y > self.game_world.height - 10:
            car.y = self.game_world.height - 10
            last_reward = -1

        if distance < 100:
            last_reward = 0.3
            self.steps_since_last_goal = 0
            self.living_penalty = 0

        self.steps_since_last_goal += 1
        if self.steps_since_last_goal > 500:
            self.living_penalty -= 0.03
            self.steps_since_last_goal = 0

        # last_reward += self.living_penalty
        # print steps_taken_since_last_goal, goal_x, goal_y
        # print last_reward, living_penalty
        self.last_distance = distance
        return last_reward
