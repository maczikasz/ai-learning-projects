import matplotlib.pyplot as pyplot


class ScoreHistory:
    def __init__(self):
        self.scores = []

    def append(self, score):
        self.scores.append(score)

    def plot_rewards(self):
        pyplot.plot(self.scores)
        pyplot.show()
