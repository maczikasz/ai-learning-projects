from kivy.app import App
from kivy.clock import Clock
from kivy.uix.button import Button


class CarApp(App):

    def __init__(self, game_world, save_orchestrator, score_history, game, widget, **kwargs):
        super(CarApp, self).__init__(**kwargs)
        self.game = game
        self.score_history = score_history
        self.painter = widget
        self.save_orchestrator = save_orchestrator
        self.game_world = game_world

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
        savesandbtn.bind(on_release=self.save_sand)
        loadsandbtn.bind(on_release=self.load_sand)
        clearbtn.bind(on_release=self.clear_canvas)
        savebtn.bind(on_release=self.save)
        loadbtn.bind(on_release=self.load)
        graphbutton.bind(on_release=self.graph)
        parent.add_widget(self.painter)
        parent.add_widget(clearbtn)
        parent.add_widget(savebtn)
        parent.add_widget(loadbtn)
        parent.add_widget(savesandbtn)
        parent.add_widget(loadsandbtn)
        parent.add_widget(graphbutton)
        return parent

    def clear_canvas(self, obj):
        self.painter.canvas.clear()
        self.game_world.reset_sand()

    def save(self, obj):
        print("saving brain...")
        self.save_orchestrator.save_brain()

    def load(self, obj):
        self.save_orchestrator.load_brain()

    def save_sand(self, obj):
        self.save_orchestrator.save_sand()

    # os.remove("sand.npy")
    # os.remove("sand_lines.npy")
    # np.save("sand", sand)
    # np.save("sand_lines", sand_lines)

    def load_sand(self, obj):
        self.save_orchestrator.load_sand()

    def graph(self, obj):
        self.score_history.plot_rewards()
