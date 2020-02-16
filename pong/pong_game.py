import time

import pyxel
from pong import config
from pong.agents import DummyAgent, HumanAgent
from pong.ball import Ball, BallState
from pong.player_controller import LeftPlayerController, RightPlayerController


class Context:
    """
    Object that is used to pass the context of the game (or state if you prefer)
    to whoever is interested in that. HINT: AGENTS AGENTS!!
    """
    def __init__(self, left_controller: LeftPlayerController, right_controller: RightPlayerController, ball: Ball):
        self.player_controller_left = left_controller
        self.player_controller_right = right_controller
        self.ball = ball


class ThePongGame:
    """
    A simple implementation of the legendary Pong game: https://en.wikipedia.org/wiki/Pong
    based on the `pyxel` library: https://github.com/kitao/pyxel.
    """
    def __init__(self, left_player_is_human=True, right_player_is_human=True):
        pyxel.init(config.WINDOW_WIDTH, config.WINDOW_HEIGHT, caption="The Pong!", scale=WINDOW_SCALE, fps=config.WINDOW_FPS)
        self.left_player_is_human = left_player_is_human
        self.right_player_is_human = right_player_is_human
        self._init_game()
        pyxel.run(self.update, self.draw)

    def _init_game(self):
        """
        Initializes the game to the starting state.
        """
        self.player_controller_left = LeftPlayerController()
        self.player_controller_right = RightPlayerController()
        self.ball = Ball()
        self.start_time = time.time()
        if self.left_player_is_human:
            self.agent_left = HumanAgent(pyxel.KEY_W, pyxel.KEY_S, self.player_controller_left)
        else:
            self.agent_left = DummyAgent(self.player_controller_left)

        if self.right_player_is_human:
            self.agent_right = HumanAgent(pyxel.KEY_UP, pyxel.KEY_DOWN, self.player_controller_right)
        else:
            self.agent_right = DummyAgent(self.player_controller_right)

    def reset(self):
        self._init_game()

    def context(self):
        """Converts the game state into the context object."""
        return Context(self.player_controller_left, self.player_controller_right, self.ball)

    def update(self):
        r"""
        ----------------------------------------
        Main game loop and logic.
        This is THE function.
        ----------------------------------------
         o      .   _______ _______
          \_ 0     /______//______/|   @_o
            /\_,  /______//______/     /\
           | \    |      ||      |     / |
        ----------------------------------------
        """

        if pyxel.btn(pyxel.KEY_Q): pyxel.quit()
        if pyxel.btnp(pyxel.KEY_R): self.reset()

        self.agent_left.update(self.context())
        self.agent_right.update(self.context())
        self.ball.update(self.context())

        if self.ball.state == BallState.HIT_LEFT_PLAYER_GOAL:
            self.player_controller_left.record_score()
            self.ball = Ball()
        elif self.ball.state == BallState.HIT_RIGHT_PLAYER_GOAL:
            self.player_controller_right.record_score()
            self.ball = Ball()

    def draw_score(self):
        """
        Draws the score information on the screen if the time is right!
        """
        if not time.time() - self.start_time <= config.GAME_INFO_SHOW_DURATION_SECS:
            p1 = 'p1' if self.left_player_is_human else 'ai'
            p2 = 'p2' if self.right_player_is_human else 'ai'
            score = f'({p1}) {self.player_controller_right.score}:{self.player_controller_left.score} ({p2})'
            pyxel.text(config.SCORE_X, config.SCORE_Y, score, config.COLOR_SCORE)

    def draw_game_info(self):
        """
        Draws the game information on the screen if the time is right!
        """
        if time.time() - self.start_time <= config.GAME_INFO_SHOW_DURATION_SECS:
            pyxel.text(0, 0, '(R)ESTART\n(Q)UIT\nby nmicovic', config.COLOR_SCORE)

    def draw(self):
        """
        Performs rendering of the game state.
        """
        pyxel.cls(col=config.COLOR_BACKGROUND)

        self.player_controller_left.draw()
        self.player_controller_right.draw()
        self.ball.draw()
        self.draw_score()
        self.draw_game_info()
