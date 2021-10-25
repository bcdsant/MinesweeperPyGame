import pygame
import os
from pygame import RESIZABLE, VIDEORESIZE, QUIT
from pygame.constants import KEYDOWN, MOUSEBUTTONDOWN, MOUSEBUTTONUP, K_r
from pygame.display import set_mode as set_display
from board import Piece
GAME_OVER = 'lost'
GAME_WON = 'win'
END_STATUS = {
    GAME_OVER: 'You lost!',
    GAME_WON: 'You won!'
}
# TODO: Implement wining the game, condition: GAME_WON when all the nom bombs pieces are revealed


class Game():
    def __init__(self, board):
        pygame.init()
        display_info = pygame.display.Info()
        self.max_width = display_info.current_w - 150
        self.max_height = display_info.current_h - 150
        self.board = board
        self.set_piece_size()
        self.screen_size = (self.board.size[0]*self.piece_size,
                            self.board.size[1]*self.piece_size)
        self.game_ended = False

    def run(self):

        self.screen = set_display(self.screen_size, RESIZABLE)
        running = True
        self.draw_board()
        while running:
            for event in pygame.event.get():

                if event.type == QUIT:
                    running = False

                if event.type == VIDEORESIZE:
                    self.resize_screen(event)

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

                # R key pressed
                if event.type == KEYDOWN and pygame.key.get_pressed()[K_r]:
                    self.board.reveal_board()
                    self.draw_board()

            pygame.display.flip()
        pygame.quit()

    def resize_screen(self, event):
        old_screen_size = self.screen_size
        new_piece_size = self.piece_size
        if event.w > old_screen_size[0]:
            new_piece_size = min(event.w, self.max_width)//self.board.size[0]
            if new_piece_size*self.board.size[1] > self.max_height:
                new_piece_size = self.max_height//self.board.size[1]
        elif event.w < old_screen_size[0]:
            new_piece_size = event.w // self.board.size[0]
        elif event.h > old_screen_size[1]:
            new_piece_size = min(event.h, self.max_height)//self.board.size[1]
            if new_piece_size*self.board.size[0] > self.max_width:
                new_piece_size = self.max_width//self.board.size[0]
        elif event.h < old_screen_size[1]:
            new_piece_size = event.h//self.board.size[1]

        self.set_piece_size(new_piece_size)
        new_size = (
            self.piece_size*self.board.size[0],
            self.piece_size*self.board.size[1]
        )
        self.update_screen(*new_size)

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
                if piece.name == 'bomb' and not piece.is_hidden and not self.game_ended:
                    self.end_game(GAME_OVER)
                if self.board.pieces_revealed >= self.board.size[0]*self.board.size[1] - self.board.bombs and not self.game_ended:
                    self.end_game(GAME_WON)
                image = pygame.transform.scale(
                    image, (self.piece_size, self.piece_size))
                self.screen.blit(image, drawing_pos)
                drawing_pos = (drawing_pos[0] + self.piece_size,
                               drawing_pos[1])
            drawing_pos = (0, drawing_pos[1] + self.piece_size)

    def set_piece_size(self, size=None):
        if size is None:
            if hasattr(self, 'screen_size'):
                self.piece_size = self.screen_size[0] // self.board.size[0]
            else:
                if min(self.max_width, self.max_height) == self.max_width:
                    self.piece_size = self.max_width // self.board.size[0]
                else:
                    self.piece_size = self.max_height // self.board.size[1]
        else:
            self.piece_size = size

    def end_game(self, end_status):
        self.game_ended = True
        self.board.reveal_board()
        self.draw_board()
        print(END_STATUS[end_status])
