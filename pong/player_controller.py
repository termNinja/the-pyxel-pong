from pong import config
import pyxel
from abc import ABC, abstractmethod


class PlayerController(ABC):
    def __init__(self, x):
        super().__init__()
        self.x = x
        self.y = config.WINDOW_HEIGHT_HALF
        self.score = 0
        self.bar_width = config.BAR_WIDTH
        self.bar_height = config.BAR_HEIGHT
        self.y_top = self.y - self.bar_height / 2
        self.y_bottom = self.y + self.bar_height / 2

    def move_up(self):
        new_y = self.move_up_in_future()
        new_y_top = new_y - self.bar_height / 2
        new_y_bottom = new_y + self.bar_height / 2

        # Check if movement is available
        # and perform it if possible
        up_edge = 0
        if new_y_top >= (up_edge - config.BAR_MAX_VERTICAL_OFFSET):
            self.y = new_y
            self.y_top = new_y_top
            self.y_bottom = new_y_bottom

    def move_down(self):
        new_y = self.move_down_in_future()
        new_y_top = new_y - self.bar_height / 2
        new_y_bottom = new_y + self.bar_height / 2

        # Check if movement is available
        # and perform it if possible
        down_edge = config.WINDOW_HEIGHT
        if new_y_bottom <= down_edge + config.BAR_MAX_VERTICAL_OFFSET:
            self.y = new_y
            self.y_top = new_y_top
            self.y_bottom = new_y_bottom

    def move_up_in_future(self):
        return self.y - config.BAR_MOVEMENT_SPEED

    def move_down_in_future(self):
        return self.y + config.BAR_MOVEMENT_SPEED

    def record_score(self):
        self.score += 1

    @abstractmethod
    def draw(self): pass

    def __str__(self):
        return f'player at ({self.x, self.y}) bar_width={self.bar_width} bar_height={self.bar_height} y_top={self.y_top} y_bottom={self.y_bottom}'

    def __repr__(self):
        return str(self)


class LeftPlayerController(PlayerController):
    def __init__(self):
        super().__init__(0)

    def __str__(self):
        return 'left ' + super().__str__()

    def draw(self):
        pyxel.rect(self.x, self.y - config.BAR_HALF_HEIGHT, config.BAR_WIDTH, config.BAR_HEIGHT, config.COLOR_LEFT_BAR)


class RightPlayerController(PlayerController):
    def __init__(self):
        super().__init__(config.WINDOW_WIDTH - config.BAR_WIDTH)

    def __str__(self):
        return 'right ' + super().__str__()

    def draw(self):
        pyxel.rect(self.x, self.y - config.BAR_HALF_HEIGHT, config.BAR_WIDTH, config.BAR_HEIGHT, config.COLOR_RIGHT_BAR)
