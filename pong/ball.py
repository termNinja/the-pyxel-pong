import time

from pong import config
import random
import pyxel
from enum import Enum


class BallState(Enum):
    FLYING = 1
    HIT_LEFT_PLAYER_BAR = 2
    HIT_RIGHT_PLAYER_BAR = 3
    HIT_LEFT_PLAYER_GOAL = 4
    HIT_RIGHT_PLAYER_GOAL = 5


class Ball:
    def __init__(self):
        self.x = config.BALL_START_X
        self.y = random.randrange(0 + config.BALL_START_Y_OFFSET, config.WINDOW_HEIGHT - config.BALL_START_Y_OFFSET)
        self.state = BallState.FLYING
        self.direction_horizontal = random.choice([-1, 1])
        self.direction_vertical = random.choice([-1, 1])
        self.start_time = time.time()

    def draw(self):
        pyxel.circ(self.x, self.y, 1, config.COLOR_BALL)

    def _future_ball_position(self):
        new_x = self.x + self.direction_horizontal * config.BALL_SPEED
        new_y = self.y + self.direction_vertical * config.BALL_SPEED
        return new_x, new_y

    def update(self, context):
        current_time = time.time()
        delta_time = current_time - self.start_time
        if delta_time <= config.BALL_START_DELAY_SECS:
            return

        new_x, new_y = self._future_ball_position()

        # Check if top or bottom wall was hit
        if new_y <= 0 or new_y >= config.WINDOW_HEIGHT:
            self.invert_vertical_movement()
            self.state = BallState.FLYING

        if new_x == (context.player_controller_left.x + context.player_controller_left.bar_width) and context.player_controller_left.y_top <= new_y <= context.player_controller_left.y_bottom:
            self.state = BallState.HIT_LEFT_PLAYER_BAR
            self.invert_horizontal_movement()
        elif new_x == context.player_controller_right.x and context.player_controller_right.y_top <= new_y <= context.player_controller_right.y_bottom:
            self.state = BallState.HIT_RIGHT_PLAYER_BAR
            self.invert_horizontal_movement()

        # Check if window edge was hit
        elif new_x == 0:
            self.state = BallState.HIT_LEFT_PLAYER_GOAL
        elif new_x == config.WINDOW_WIDTH:
            self.state = BallState.HIT_RIGHT_PLAYER_GOAL
        else:
            self.state = BallState.FLYING

        self.x = new_x
        self.y = new_y

    def invert_horizontal_movement(self):
        self.direction_horizontal *= -1

    def invert_vertical_movement(self):
        self.direction_vertical *= -1
