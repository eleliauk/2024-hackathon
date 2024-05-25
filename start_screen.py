import subprocess

import pygame
import sys
from utils import scale_background


class StartScreen:
    def __init__(self, screen):
        self.screen = screen
        self.background_image = scale_background('img/start_screen.jpg', screen.get_width(), screen.get_height())
        self.font = pygame.font.Font(None, 36)  # None indicates using the default font
        # Center the button
        button_width, button_height = 200, 50
        self.button_rect = pygame.Rect(
            (screen.get_width() // 2) - (button_width // 2),
            (screen.get_height() // 2) + 50,
            button_width, button_height
        )
        self.is_running = True

    def draw(self):
        # Draw background
        self.screen.blit(self.background_image, (0, 0))

        # Draw title
        title_text = self.font.render('启动', True, pygame.Color('white'))
        title_rect = title_text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 - 100))
        self.screen.blit(title_text, title_rect)

        # Draw button
        self.draw_button('Start', pygame.Color('#D9D8FF'), self.button_rect)

    def draw_button(self, text, color, rect):
        mouse = pygame.mouse.get_pos()
        if rect.collidepoint(mouse):
            pygame.draw.rect(self.screen, pygame.Color('#C4FAFF'), rect)
            if pygame.mouse.get_pressed()[0]:
                self.is_running = False  # Button clicked, stop the start screen
        else:
            pygame.draw.rect(self.screen, color, rect)

        font_text = self.font.render(text, True, pygame.Color('black'))
        text_rect = font_text.get_rect(center=rect.center)
        self.screen.blit(font_text, text_rect)

    def start_demo(self):
        # 导入 demo 模块并调用其 main 函数
        from demo import main
        main()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.button_rect.collidepoint(event.pos):
                    self.start_demo()  # 调用开始demo的方法

    def run(self):
        while self.is_running:
            self.handle_events()
            self.draw()
            pygame.display.flip()
            pygame.time.Clock().tick(60)
