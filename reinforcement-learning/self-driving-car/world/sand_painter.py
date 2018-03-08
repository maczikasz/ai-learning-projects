import numpy as np
from kivy.uix.widget import Widget
from kivy.graphics import Color, Line


class MyPaintWidget(Widget):

    def __init__(self, width, height, game_world, **kwargs):
        super(MyPaintWidget, self).__init__(**kwargs)
        self.game_world = game_world
        self.height = height
        self.width = width

    def on_touch_down(self, touch):
        global length, n_points, last_x, last_y
        with self.canvas:
            Color(0.8, 0.7, 0)
            d = 10.
            touch.ud['line'] = Line(points=(touch.x, touch.y), width=10)
            last_x = int(touch.x)
            last_y = int(touch.y)
            n_points = 0
            length = 0
            if touch.x < len(self.width) and touch.y < len(self.height):
                self.game_world.sand[int(touch.x), int(touch.y)] = 1

    def on_touch_move(self, touch):
        global length, n_points, last_x, last_y
        if touch.button == 'left':
            touch.ud['line'].points += [touch.x, touch.y]
            x = int(touch.x)
            y = int(touch.y)
            length += np.sqrt(max((x - last_x) ** 2 + (y - last_y) ** 2, 2))
            n_points += 1.
            # density = n_points/(length)
            # touch.ud['line'].width = int(20 * density + 1)
            self.game_world.sand[int(touch.x) - 10: int(touch.x) + 10, int(touch.y) - 10: int(touch.y) + 10] = 1
            last_x = x
            last_y = y

    def on_touch_up(self, touch):
        if 'line' in touch.ud:
            line_points = touch.ud['line'].points
            line_points.append(touch.ud['line'].width)
            self.game_world.sand_lines.append(line_points)

    def redraw_sand(self):
        self.canvas.clear()
        for line in self.game_world.sand_lines:
            with self.canvas:
                Color(0.8, 0.7, 0)
                Line(points=map(lambda a: int(a), line[:-1]), width=line[-1])
