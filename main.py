from game import Game
from board import Board


BOARD_SIZE = (BOARD_WIDTH, BOARD_HIGHT) = (10, 10)
BOMBS_QTD = 50
BOARD = Board(BOARD_SIZE, BOMBS_QTD)
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HIGHT) = (45*BOARD_WIDTH, 45*BOARD_HIGHT)

game = Game(board=BOARD, screen_size=SCREEN_SIZE)
game.run()
