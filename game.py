import pygame


class Game():
    def __init__(self, board, screen_size):
        self.board = board
        self.screen_size = screen_size

    def run(self):
        pygame.init()
        screen = pygame.display.set_mode(self.screen_size)
        running = True
        while running:
            for event in pygame.event.get():
                if event.type is pygame.QUIT:
                    running = False
            self.draw()
            pygame.display.flip()
        pygame.quit()

    def draw(self):
        pass
