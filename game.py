import pygame
import os
from pygame import RESIZABLE, VIDEORESIZE, QUIT
from pygame.constants import MOUSEBUTTONDOWN, MOUSEBUTTONUP
from pygame.display import set_mode as set_display
from board import Piece


class Game():
    def __init__(self, board, screen_size):
        self.board = board
        (self.sceen_width, self.screen_height) = self.screen_size = screen_size
        self.set_piece_size()
        self.load_images()

    def run(self):
        pygame.init()
        display_info = pygame.display.Info()
        self.max_width = display_info.current_w
        self.max_height = display_info.current_h
        self.screen = set_display(self.screen_size, RESIZABLE)
        running = True
        self.draw_board()
        while running:
            for event in pygame.event.get():

                if event.type == QUIT:
                    running = False

                if event.type == VIDEORESIZE:
                    # resizing the window but keeping a square screen
                    # FIXME: change to keep the start screen ratio instead of keeping squared
                    if max(event.w, event.h) >= min(self.max_width, self.max_height):
                        new_size = min(self.max_width, self.max_height)
                    else:
                        new_size = max(event.w, event.h)
                    self.update_screen(new_size, new_size)

                # Leflt mouse button pressed
                if event.type == MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
                    x, y = pygame.mouse.get_pos()
                    self.board.reveal_piece_from_pos(x, y, self.piece_size)
                    self.draw_board()

                # Right mouse button pressed
                if event.type == MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[2]:
                    x, y = pygame.mouse.get_pos()
                    self.board.flag_piece_from_pos(x, y, self.piece_size)
                    self.draw_board()

            pygame.display.flip()
        pygame.quit()

    def update_screen(self, width, height):
        self.screen_size = (width, height)
        self.screen = set_display(self.screen_size, RESIZABLE)
        self.draw_board()

    def draw_board(self):
        drawing_pos = (0, 0)
        self.set_piece_size()

        for col in range(self.board.size[1]):
            for row in range(self.board.size[0]):
                piece = self.board.get_piece(col, row)
                if piece.is_flagged:
                    image = Piece('flag').image
                elif piece.is_hidden:
                    image = Piece('blank').image
                else:
                    image = piece.image
                image = pygame.transform.scale(image, self.piece_size)
                self.screen.blit(image, drawing_pos)
                drawing_pos = (drawing_pos[0] + self.piece_size[0],
                               drawing_pos[1])
            drawing_pos = (0, drawing_pos[1] + self.piece_size[1])

    def set_piece_size(self):
        self.piece_size = self.screen_size[0] // self.board.size[0], self.screen_size[1] // self.board.size[1]

    def load_images(self):
        self.images = {}
        for file_name in os.listdir('images'):
            if file_name.endswith('.png'):
                image = pygame.image.load(r'images/' + file_name)
                self.images[file_name.split('.')[0]] = image
