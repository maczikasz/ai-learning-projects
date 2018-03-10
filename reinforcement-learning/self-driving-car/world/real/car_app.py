import functools
import os

from kivy.app import App
from kivy.clock import Clock
from kivy.uix.button import Button
from kivy.uix.popup import Popup

from kivy_setup.kivy_init import LoadDialog, SaveDialog


class CarApp(App):

    def __init__(self, game_world, save_orchestrator, score_history, game, widget, brains_dir, sands_dir,
                 **kwargs):
        super(CarApp, self).__init__(**kwargs)
        self.game = game
        self.score_history = score_history
        self.painter = widget
        self.save_orchestrator = save_orchestrator
        self.game_world = game_world
        self.brains_dir = sands_dir
        self.sand_dir = brains_dir

    def build(self):
        parent = self.game
        parent.serve_car()
        Clock.schedule_interval(parent.update, 1.0 / 60.0)
        button_width, button_height = 50, 35
        clearbtn = Button(text='CLR', size=(button_width, button_height))
        savebtn = Button(text='S B', pos=(button_width, 0), size=(button_width, button_height))
        loadbtn = Button(text='L B', pos=(2 * button_width, 0), size=(button_width, button_height))
        savesandbtn = Button(text='S S', pos=(3 * button_width, 0), size=(button_width, button_height))
        loadsandbtn = Button(text='L S', pos=(4 * button_width, 0), size=(button_width, button_height))
        graphbutton = Button(text='G', pos=(5 * button_width, 0), size=(button_width, button_height))
        savesandbtn.bind(on_release=functools.partial(self.save_dialog, self.save_sand, "Save sand", self.sand_dir))
        loadsandbtn.bind(on_release=functools.partial(self.load_dialog, self.load_sand, "Load sand", self.sand_dir))
        clearbtn.bind(on_release=self.clear_canvas)
        savebtn.bind(on_release=functools.partial(self.save_dialog, self.save, "Save brain", self.brains_dir))
        loadbtn.bind(on_release=functools.partial(self.load_dialog, self.load, "Load brain", self.brains_dir))
        graphbutton.bind(on_release=self.graph)
        parent.add_widget(self.painter)
        parent.add_widget(clearbtn)
        parent.add_widget(savebtn)
        parent.add_widget(loadbtn)
        parent.add_widget(savesandbtn)
        parent.add_widget(loadsandbtn)
        parent.add_widget(graphbutton)
        self.painter.redraw_sand()
        return parent

    def clear_canvas(self, obj):
        self.painter.canvas.clear()
        self.game_world.reset_sand()

    def save_dialog(self, callback, title, rootpath, obj):
        content = SaveDialog(rootpath=rootpath, save=callback, cancel=self.dismiss_popup)
        self._popup = Popup(title=title, content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    def load_dialog(self, callback, title, rootpath, obj):
        content = LoadDialog(rootpath=rootpath, load=callback, cancel=self.dismiss_popup)
        self._popup = Popup(title=title, content=content,
                            size_hint=(0.9, 0.9))
        self._popup.open()

    def save(self, path, filename):
        self.save_orchestrator.save_brain(self.find_filename(filename, path))
        self.dismiss_popup()

    def dismiss_popup(self):
        self._popup.dismiss()

    def load(self, path, filename):
        self.save_orchestrator.load_brain(self.find_filename(filename, path))
        self.dismiss_popup()

    def save_sand(self, path, filename):
        self.save_orchestrator.save_sand(self.find_filename(filename, path))
        self.dismiss_popup()

    def load_sand(self, path, filename):
        self.save_orchestrator.load_sand(self.find_filename(filename, path))
        self.dismiss_popup()
        self.painter.redraw_sand()

    def graph(self, obj):
        self.score_history.plot_rewards()

    @staticmethod
    def find_filename(filename, path):
        if path in filename:
            final_name = filename
        else:
            final_name = os.path.join(os.curdir, path, filename)
        return final_name
