from game import Game
from board import Board


# Beginner: 9x9 Board with 10 bombs
# Intermediary: 16x16 with 40 bombs
# Advanced: 30x16 with 99 bombs
BOARD_SIZE = (BOARD_WIDTH, BOARD_HIGHT) = (9, 9)
BOMBS_QTD = 10
BOARD = Board(BOARD_SIZE, BOMBS_QTD)

game = Game(board=BOARD)
game.run()
