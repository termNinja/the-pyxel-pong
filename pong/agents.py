import pyxel

from pong import config
from pong.player_controller import PlayerController
from abc import ABC, abstractmethod


class Agent(ABC):
    @abstractmethod
    def update(self, context = None): pass


class HumanAgent(Agent):
    def __init__(self, up_key_map, down_key_map, controller: PlayerController):
        super().__init__()
        self.up_key_map = up_key_map
        self.down_key_map = down_key_map
        self.controller = controller

    def update(self, context = None):
        if pyxel.btn(self.up_key_map):
            self.controller.move_up()
        if pyxel.btn(self.down_key_map):
            self.controller.move_down()


class DummyAgent(Agent):
    def __init__(self, controller: PlayerController):
        super().__init__()
        self.controller = controller
        self.movement_horizontal_threshold = config.WINDOW_WIDTH_HALF

    def update(self, context = None):
        new_y_down = self.controller.move_down_in_future()
        new_y_up = self.controller.move_up_in_future()

        vertical_dist_down = abs(context.ball.y - new_y_down)
        vertical_dist_up = abs(context.ball.y - new_y_up)
        horizontal_distance_to_ball = abs(self.controller.x - context.ball.x)

        if horizontal_distance_to_ball < self.movement_horizontal_threshold:
            if vertical_dist_down < vertical_dist_up:
                self.controller.move_down()
            elif vertical_dist_up < vertical_dist_down:
                self.controller.move_up()

