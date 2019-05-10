#!/usr/bin/env python3

import logging
import pyglet

from sim_jop.gui.shape import Rectangle
from sim_jop.gui.view import View
from sim_jop.gui.schema_elements import GTrack

# Coordinate system:
# * window: width, height
# * plan: plan_width, plan_height
# * box: box_width, box_height

LOG = logging.getLogger(__name__)

BASE_GUI_COLOR = [0, 180, 190]
CURSOR_COLOR = [255, 0, 0]


class Menu:

    def __init__(self, batch, group, geometry):
        self.frame = Rectangle(batch, group, geometry, BASE_GUI_COLOR)


class Grid:

    def __init__(self, width, height, box_width, box_height):

        self.batch = pyglet.graphics.Batch()

        points = []
        self.labels = []

        for w in range(0, width, box_width * 5):
            for h in range(0, height, box_height * 5):
                if w == 0:
                    label = pyglet.text.Label('{:d}'.format(
                        int(h / box_height)), font_name='Ariel', font_size=10, x=w, y=h, color=(0, 180, 190, 200))
                    self.labels.append(label)
                    points.extend([0, h, width, h])
                if h == 0:
                    label = pyglet.text.Label('{:d}'.format(
                        int(w / box_width)), font_name='Ariel', font_size=10, x=w, y=h, color=(0, 180, 190, 200))
                    self.labels.append(label)
                    points.extend([w, 0, w, height])

        number = int(len(points) / 2.0)
        color = [30, 30, 40]
        self.batch.add(number, pyglet.gl.GL_LINES, None, ('v2i', points), ('c3B', color * number))

    def draw(self):
        self.batch.draw()
        for label in self.labels:
            label.draw()


class EditorWindow(pyglet.window.Window):

    def __init__(self):
        super().__init__(fullscreen=True, visible=False, caption='sim_jop')
        self.set_mouse_visible(False)
        LOG.info('Resolution: {}x{}'.format(self.width, self.height))

        self.zoom_level = 1
        self.pos_x, self.pos_y = (0, 0)

        coefficient = (self.zoom_level + 1) * 2
        self.box_width = 2 * coefficient
        self.box_height = 3 * coefficient
        self.max_x = int(self.width / self.box_width)
        self.max_y = int(self.height / self.box_height)

        self.batch = pyglet.graphics.Batch()
        self.background = pyglet.graphics.OrderedGroup(0)
        self.middleground = pyglet.graphics.OrderedGroup(1)
        self.foreground = pyglet.graphics.OrderedGroup(2)

        menu_geometry = {
            'width_start': 1,
            'width_end': self.width,
            'height_start': self.height - (15 * self.box_height) + 1,
            'height_end': self.height,
        }

        self.menu = Menu(self.batch, self.background, menu_geometry)

        grid_position = {
            'width_start': 1,
            'width_end': self.width,
            'height_start': 0,
            'height_end': self.height - (15 * self.box_height) - 1,
        }

        self.cursor = Rectangle(
            self.batch,
            self.foreground,
            self._get_cursor_geometry(),
            CURSOR_COLOR)

        self.grid = Grid(
            self.width,
            self.height -
            15 *
            self.box_height,
            self.box_width,
            self.box_height)

        self.is_grid_on = False

    def _get_box(self, pos_x, pos_y):
        box_x = int(pos_x / self.box_width) if pos_x / self.box_width < self.max_x else self.max_x
        box_y = int(pos_y / self.box_height) if pos_y / \
            self.box_height < self.max_y - 1 else self.max_y - 1
        return (box_x, box_y)

    def _get_cursor_geometry(self):
        cursor_geometry = {
            'width_start': self.pos_x * self.box_width,
            'width_end': (self.pos_x + 1) * self.box_width,
            'height_start': self.pos_y * self.box_height,
            'height_end': (self.pos_y + 1) * self.box_height,
        }
        return cursor_geometry

    def on_mouse_motion(self, x, y, dx, dy):

        self.pos_x, self.pos_y = self._get_box(x, y)
        self.cursor.move(self._get_cursor_geometry())
        self.on_draw()

    def on_key_press(self, symbol, modifiers):
        if symbol == pyglet.window.key.Q:
            pyglet.app.exit()
        if symbol == pyglet.window.key.G:
            self.is_grid_on = False if self.is_grid_on else True

    def on_draw(self):
        self.clear()
        if self.is_grid_on:
            self.grid.draw()
        self.batch.draw()
