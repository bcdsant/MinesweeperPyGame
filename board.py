from utils import find
import random
import pygame


class Board():
    def __init__(self, size, bombs):
        self.size = size
        self.bombs = bombs
        self.set_board()

    def set_board(self):
        self.board = []
        for row in range(self.size[0]):
            row = []
            for col in range(self.size[1]):
                piece = Piece('cleared')
                row.append(piece)
            self.board.append(row)
        self.insert_bombs()
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

    def insert_bombs(self):
        # FIXME: It is not inserting the correct number of bombs
        random.seed()
        bomb_coords = [
            (random.randrange(0, self.size[0]-1),
             random.randrange(0, self.size[1]-1)) for _ in range(self.bombs)
        ]

        for coord in bomb_coords:
            self.board[coord[0]][coord[1]] = Piece('bomb')

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
