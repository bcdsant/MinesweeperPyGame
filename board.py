from utils import find, array_to_matrix
import random
import pygame


class Board():
    def __init__(self, size, bombs):
        self.size = size
        self.bombs = bombs
        self.set_board()

    def set_board(self):
        board_row = []
        bombs_placed = 0
        for _ in range(self.size[0]*self.size[1]):
            if bombs_placed < self.bombs:
                piece = Piece('bomb')
                bombs_placed += 1
            else:
                piece = Piece('cleared')
            board_row.append(piece)

        random.shuffle(board_row)
        self.board = array_to_matrix(board_row, self.size[1])
        self.insert_numbers()

    def insert_numbers(self):
        for row in range(self.size[0]):
            for col in range(self.size[1]):
                number = 0
                if self.board[row][col].name == 'bomb':
                    continue
                else:
                    # FIXME: Update corners and improve this part, probably changing Piece Class
                    if ((row + 1 < self.size[0]) and (row-1) >= 0) and ((col + 1 < self.size[1]) and (col-1) >= 0):
                        if self.board[row-1][col].name == 'bomb':
                            number += 1
                        if self.board[row-1][col-1].name == 'bomb':
                            number += 1
                        if self.board[row-1][col+1].name == 'bomb':
                            number += 1
                        if self.board[row][col+1].name == 'bomb':
                            number += 1
                        if self.board[row][col-1].name == 'bomb':
                            number += 1
                        if self.board[row+1][col].name == 'bomb':
                            number += 1
                        if self.board[row+1][col-1].name == 'bomb':
                            number += 1
                        if self.board[row+1][col+1].name == 'bomb':
                            number += 1
                        if number > 0:
                            self.board[row][col] = Piece('#'+str(number))

    def is_on_board(self, row, col):
        return (row >= 0) and (row < len(self.size[0])) and (col >= 0) and (col < len(self.size[1]))

    def get_piece(self, row, col):
        return self.board[row][col]


class Piece():
    # TODO: improve Piece class to hold more information
    def __init__(self, name, img_ext='.png'):
        self.name = name
        self.img_ext = img_ext
        self.load_piece_image()

    def load_piece_image(self):
        image_path = find(self.name, 'images', self.img_ext)
        self.image = pygame.image.load(image_path)
