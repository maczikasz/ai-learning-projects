import os
import pickle


class SaveOrchestrator:
    def __init__(self, save_dir, brain, game_world):
        self.game_world = game_world
        self.brain = brain
        if not os.path.exists(save_dir):
            os.mkdir(save_dir)

    def save_brain(self, filename):
        self.brain.save(filename)

    def save_sand(self, filename):
        with open(filename, 'w+') as filehandle:
            pickle.dump({'lines': self.game_world.sand_lines, 'sand': self.game_world.sand}, filehandle)

    def load_brain(self, filename):
        self.brain.load(filename)

    def load_sand(self, filename):
        with open(filename, 'r') as filehandle:
            sand_dict = pickle.load(filehandle)
            self.game_world.sand = sand_dict['sand']
            self.game_world.sand_lines = sand_dict['lines']
