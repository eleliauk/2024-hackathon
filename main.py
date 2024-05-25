import pygame
import sys
from start_screen import StartScreen


def main():
    # 初始化pygame
    pygame.init()

    # 设置窗口大小
    screen_width, screen_height = 1000, 800
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption('游戏开始界面')

    # 创建开始界面实例
    start_screen = StartScreen(screen)

    # 运行开始界面
    start_screen.run()

    # 退出pygame
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
