import pygame
from pygame import RESIZABLE, VIDEORESIZE, QUIT
from pygame.constants import K_ESCAPE, KEYDOWN, MOUSEBUTTONDOWN, K_c, K_g, K_m, K_r
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
        self.board = Board()
        self.set_piece_size()
        self.screen_size = (self.board.size[0]*self.piece_size,
                            self.board.size[1]*self.piece_size)
        self.game_ended = False

    def run(self):
        self.screen = set_display(self.screen_size, RESIZABLE)
        pygame.display.set_caption('Minesweeper')

        running = True
        self.on_menu = True
        self.on_game = False
        self.on_controls = False
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
                            self.controls_rect.left,
                        )
                        right_boundary = max(
                            self.beginner_rect.right,
                            self.intermediary_rect.right,
                            self.advanced_rect.right,
                            self.controls_rect.right,
                        )

                        if left_boundary < x < right_boundary:
                            if self.beginner_rect.top < y < self.beginner_rect.bottom:
                                # begginer
                                self.board = Board((9, 9), 10)
                                self.on_menu = False
                                self.on_game = True
                                self.game_ended = False
                                self.draw_board()
                            if self.intermediary_rect.top < y < self.intermediary_rect.bottom:
                                # intermediary
                                self.board = Board((16, 16), 40)
                                self.on_menu = False
                                self.on_game = True
                                self.game_ended = False
                                self.draw_board()
                            if self.advanced_rect.top < y < self.advanced_rect.bottom:
                                # advanced
                                self.board = Board((30, 16), 99)
                                self.on_menu = False
                                self.on_game = True
                                self.game_ended = False
                                self.update_screen()
                                self.draw_board()
                            if self.controls_rect.top < y < self.controls_rect.bottom:
                                # draw controls
                                self.on_controls = True
                                self.on_menu = False
                                self.on_game = False
                                self.game_ended = False
                                self.draw_controls()

                # Game Controls
                elif self.on_game and not self.game_ended:
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

                # Global Controls
                if self.on_game or self.on_menu or self.on_controls:
                    # M key pressed: Show Main Menu
                    if event.type == KEYDOWN and pygame.key.get_pressed()[K_m]:
                        self.on_game = False
                        self.on_menu = True
                        self.draw_menu()
                    # C key pressed: Show Controls
                    elif event.type == KEYDOWN and pygame.key.get_pressed()[K_c]:
                        self.on_controls = True
                        self.on_game = False
                        self.on_menu = False
                        self.draw_controls()
                    # G key pressed: go to back to active game
                    elif event.type == KEYDOWN and pygame.key.get_pressed()[K_g]:
                        self.on_game = True
                        self.on_menu = False
                        if hasattr(self, 'board'):
                            self.draw_board()
                        else:
                            self.draw_menu()
                    # ESC key pressed: close the game
                    elif event.type == KEYDOWN and pygame.key.get_pressed()[K_ESCAPE]:
                        running = False

        pygame.quit()

    def draw_controls(self):
        self.screen.fill(LIGHT_GRAY)

        controls_text = self.font_50.render('Controls', True, BLACK)
        controls_rect = controls_text.get_rect()
        controls_rect.center = (self.screen_size[0]//2, 50)
        self.screen.blit(controls_text, controls_rect)

        mouse_lb_text = self.font_c.render(
            'Left Mouse Button > Reveal Piece', True, BLACK)
        mouse_lb_rect = mouse_lb_text.get_rect()
        mouse_lb_rect.center = (self.screen_size[0]//2, 150)
        self.screen.blit(mouse_lb_text, mouse_lb_rect)

        mouse_rb_text = self.font_c.render(
            'Right Mouse Button > Flag Piece', True, BLACK)
        mouse_rb_rect = mouse_rb_text.get_rect()
        mouse_rb_rect.center = (self.screen_size[0]//2, 200)
        self.screen.blit(mouse_rb_text, mouse_rb_rect)

        key_m_text = self.font_c.render(
            'Press "M" to go to Main Menu', True, BLACK)
        key_m_rect = key_m_text.get_rect()
        key_m_rect.center = (self.screen_size[0]//2, 250)
        self.screen.blit(key_m_text, key_m_rect)

        key_c_text = self.font_c.render(
            'Press "C" to go to Controls', True, BLACK)
        key_c_rect = key_c_text.get_rect()
        key_c_rect.center = (self.screen_size[0]//2, 300)
        self.screen.blit(key_c_text, key_c_rect)

        key_g_text = self.font_c.render(
            'Press "G" to go to current game', True, BLACK)
        key_g_rect = key_g_text.get_rect()
        key_g_rect.center = (self.screen_size[0]//2, 350)
        self.screen.blit(key_g_text, key_g_rect)

        key_esc_text = self.font_c.render('ESC to close the game', True, BLACK)
        key_esc_rect = key_esc_text.get_rect()
        key_esc_rect.center = (self.screen_size[0]//2, 400)
        self.screen.blit(key_esc_text, key_esc_rect)

        pygame.display.flip()

    def draw_menu(self):
        self.screen.fill(LIGHT_GRAY)
        self.font = pygame.font.Font('font/game_plan_dker.ttf', 32)
        self.font_c = pygame.font.Font('font/prussian_brew_gemfonts.ttf', 32)
        self.font_50 = pygame.font.Font('font/game_plan_dker.ttf', 50)

        minesweeper_text = self.font_50.render('MINESWEEPER', True, BLACK)
        self.minesweeper_rect = minesweeper_text.get_rect()
        self.minesweeper_rect.center = (self.screen_size[0]//2, 50)
        self.screen.blit(minesweeper_text, self.minesweeper_rect)

        beginner_text = self.font.render('Beginner', True, BLACK)
        self.beginner_rect = beginner_text.get_rect()
        self.beginner_rect.center = (self.screen_size[0]//2, 150)
        self.screen.blit(beginner_text, self.beginner_rect)

        intermediary_text = self.font.render('Intermediary', True, BLACK)
        self.intermediary_rect = intermediary_text.get_rect()
        self.intermediary_rect.center = (self.screen_size[0]//2, 200)
        self.screen.blit(intermediary_text, self.intermediary_rect)

        advanced_text = self.font.render('Advanced', True, BLACK)
        self.advanced_rect = advanced_text.get_rect()
        self.advanced_rect.center = (self.screen_size[0]//2, 250)
        self.screen.blit(advanced_text, self.advanced_rect)

        controls_text = self.font.render('Controls', True, BLACK)
        self.controls_rect = controls_text.get_rect()
        self.controls_rect.center = (self.screen_size[0]//2, 300)
        self.screen.blit(controls_text, self.controls_rect)

        pygame.display.flip()

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
        elif self.on_controls:
            self.draw_controls()

    def draw_board(self):
        # TODO: Break check board state for wining from draw board
        drawing_pos = (0, 0)
        self.set_piece_size()
        for col in range(self.board.size[1]):
            for row in range(self.board.size[0]):
                piece = self.board.get_piece(col, row)
                if piece.is_flagged:
                    image = Piece('flag').image
                elif piece.is_hidden:
                    image = Piece('blank').image
                elif piece.name == 'bomb' and not piece.is_hidden and not self.game_ended:
                    self.on_game = False
                    self.end_game(GAME_OVER)
                    break
                elif self.board.pieces_revealed >= self.board.size[0]*self.board.size[1] - self.board.bombs and not self.game_ended:
                    self.on_game = False
                    self.end_game(GAME_WON)
                    break
                else:
                    image = piece.image
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
        if end_status == GAME_OVER:
            self.board.reveal_board()
            self.draw_board()
            pygame.display.flip()
        self.screen.fill(
            LIGHT_GRAY,
            pygame.Rect(0, 0,
                        self.screen_size[0], min(125, self.screen_size[1]))
        )
        end_text = self.font_50.render(END_STATUS[end_status], True, BLACK)
        text_rect = end_text.get_rect()
        text_rect.center = (self.screen_size[0]//2, 50)
        self.screen.blit(end_text, text_rect)
        pygame.display.flip()
