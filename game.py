import pygame
from pygame import RESIZABLE, VIDEORESIZE, QUIT
from pygame.constants import KEYDOWN, MOUSEBUTTONDOWN, K_m, K_r
from pygame.display import set_mode as set_display
from board import Board, Piece
GAME_OVER = 'lost'
GAME_WON = 'win'
END_STATUS = {
    GAME_OVER: 'You lost!',
    GAME_WON: 'You won!'
}
LIGHT_GRAY = (220, 220, 220)
BLACK = (0, 0, 0)


class Game():
    def __init__(self):
        pygame.init()
        display_info = pygame.display.Info()
        self.max_width = display_info.current_w - 100
        self.max_height = display_info.current_h - 100
        self.set_piece_size(
            min(self.max_width, self.max_height)//9
        )
        self.screen_size = (9*self.piece_size,
                            9*self.piece_size)
        self.game_ended = False

    def run(self):

        self.screen = set_display(self.screen_size, RESIZABLE)
        pygame.display.set_caption('Minesweeper')

        running = True
        self.on_menu = True
        self.on_game = False
        if self.on_menu:
            self.draw_menu()

        while running:
            events = pygame.event.get(QUIT) + pygame.event.get(VIDEORESIZE) + \
                pygame.event.get(MOUSEBUTTONDOWN) + pygame.event.get(KEYDOWN)
            for event in events:
                if event.type == QUIT:
                    running = False

                elif event.type == VIDEORESIZE:
                    self.resize_screen(event)

                # Menu controls
                elif self.on_menu:
                    # Leflt mouse button pressed
                    if event.type == MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
                        x, y = pygame.mouse.get_pos()
                        left_boundary = min(
                            self.beginner_rect.left,
                            self.intermediary_rect.left,
                            self.advanced_rect.left,
                        )
                        right_boundary = max(
                            self.beginner_rect.right,
                            self.intermediary_rect.right,
                            self.advanced_rect.right,
                        )

                        if left_boundary < x < right_boundary:
                            if self.beginner_rect.top < y < self.beginner_rect.bottom:
                                # begginer
                                self.board = Board((9, 9), 10)
                                self.on_menu = False
                                self.on_game = True
                                self.draw_board()
                            if self.intermediary_rect.top < y < self.intermediary_rect.bottom:
                                # intermediary
                                self.board = Board((16, 16), 40)
                                self.on_menu = False
                                self.on_game = True
                                self.draw_board()
                            if self.advanced_rect.top < y < self.advanced_rect.bottom:
                                # advanced
                                self.board = Board((30, 16), 99)
                                self.on_menu = False
                                self.on_game = True
                                self.update_screen()
                                self.draw_board()

                    # M key pressed: go to back to active game
                    if event.type == KEYDOWN and pygame.key.get_pressed()[K_m]:
                        self.on_game = True
                        self.on_menu = False
                        if hasattr(self, 'board'):
                            self.draw_board()

                # Game Controls
                elif self.on_game:
                    self.draw_board()
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

                    # M key pressed: go to Menu
                    if event.type == KEYDOWN and pygame.key.get_pressed()[K_m]:
                        self.on_game = False
                        self.on_menu = True
                        self.draw_menu()

        pygame.quit()

    def draw_menu(self):
        self.screen.fill(LIGHT_GRAY)
        font = pygame.font.Font('font/game_plan_dker.ttf', 32)
        font_50 = pygame.font.Font('font/game_plan_dker.ttf', 50)

        minesweeper_text = font_50.render('MINESWEEPER', True, BLACK)
        self.minesweeper_rect = minesweeper_text.get_rect()
        self.minesweeper_rect.center = (self.screen_size[0]//2, 50)
        self.screen.blit(minesweeper_text, self.minesweeper_rect)

        beginner_text = font.render('Beginner', True, BLACK)
        self.beginner_rect = beginner_text.get_rect()
        self.beginner_rect.center = (self.screen_size[0]//2, 150)
        self.screen.blit(beginner_text, self.beginner_rect)

        intermediary_text = font.render('Intermediary', True, BLACK)
        self.intermediary_rect = intermediary_text.get_rect()
        self.intermediary_rect.center = (self.screen_size[0]//2, 200)
        self.screen.blit(intermediary_text, self.intermediary_rect)

        advanced_text = font.render('Advanced', True, BLACK)
        self.advanced_rect = advanced_text.get_rect()
        self.advanced_rect.center = (self.screen_size[0]//2, 250)
        self.screen.blit(advanced_text, self.advanced_rect)
        pygame.display.flip()

    def resize_screen(self, event):
        # TODO: Improve resizing and resize the menu
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

    def update_screen(self, width=None, height=None):
        if width is None or height is None:
            width = self.max_width
            height = self.max_height
        self.screen_size = (width, height)
        self.screen = set_display(self.screen_size, RESIZABLE)
        if self.on_game:
            self.draw_board()
        elif self.on_menu:
            self.draw_menu()

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
        pygame.display.flip()

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
