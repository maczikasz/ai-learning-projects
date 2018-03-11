class CarAppSimulator:
    def __init__(self, game_world, save_orchestrator, score_history, game_simulator, run_condition):
        self.run_condition = run_condition
        self.game_simulator = game_simulator
        self.score_history = score_history
        self.save_orchestrator = save_orchestrator
        self.game_world = game_world

    def run(self):
        step = 0
        while self.run_condition(step):
            if step % 1000 == 0:
                print step
            if step % 10000 == 0:
                self.score_history.plot_rewards()

            step += 1
            self.game_simulator.update(step)
