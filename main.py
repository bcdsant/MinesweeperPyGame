from game import Game
from board import Board

BOARD_SIZE = (BOARD_WIDTH, BOARD_HIGHT) = (15, 15)
BOARD = Board(BOARD_SIZE)
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HIGHT) = (45*BOARD_WIDTH, 45*BOARD_HIGHT)

game = Game(board=BOARD, screen_size=SCREEN_SIZE)
game.run()
