from pong.pong_game import ThePongGame
import argparse


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--left_ai", help="enable AI on the left",
                        action="store_true")
    parser.add_argument("--right_ai", help="enable AI on the right",
                        action="store_true")
    args = parser.parse_args()
    ThePongGame(not args.left_ai, not args.right_ai)

