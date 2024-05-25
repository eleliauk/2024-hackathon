import pygame
import sys
from utils import scale_background


class PassScreen:
    def __init__(self, screen):
        self.screen = screen
        self.background_image = scale_background('img/pass.png', screen.get_width(), screen.get_height())
        self.font = pygame.font.Font(None, 36)  # None indicates using the default font
        self.is_running = True

    def draw(self):
        # Draw background
        self.screen.blit(self.background_image, (0, 0))

        # Draw title
        title_text = self.font.render('启动', True, pygame.Color('white'))
        title_rect = title_text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 - 100))
        self.screen.blit(title_text, title_rect)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False

    def run(self):
        while self.is_running:
            self.handle_events()
            self.draw()
            pygame.display.flip()
            pygame.time.Clock().tick(60)