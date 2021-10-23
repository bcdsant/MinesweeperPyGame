import pygame
import os


class Game():
    def __init__(self, board, screen_size):
        self.board = board
        (self.sceen_width, self.screen_height) = self.screen_size = screen_size
        self.piece_size = self.sceen_width // self.board.size[1], self.screen_height // self.board.size[0]
        self.load_images()

    def run(self):
        pygame.init()
        self.screen = pygame.display.set_mode(self.screen_size)
        running = True
        self.draw()
        while running:
            for event in pygame.event.get():
                if event.type is pygame.QUIT:
                    running = False
            pygame.display.flip()
        pygame.quit()

    def draw(self):
        drawing_pos = (0, 0)
        for row in range(self.board.size[0]):
            for column in range(self.board.size[1]):
                image = self.images['blank']
                print(drawing_pos)
                self.screen.blit(image, drawing_pos)
                drawing_pos = drawing_pos[0] + \
                    self.piece_size[0], drawing_pos[1]
            drawing_pos = 0, drawing_pos[1] + self.piece_size[1]

    def load_images(self):
        self.images = {}
        for file_name in os.listdir('images'):
            if file_name.endswith('.png'):
                image = pygame.image.load(r'images/' + file_name)
                image = pygame.transform.scale(image, self.piece_size)
                self.images[file_name.split('.')[0]] = image
