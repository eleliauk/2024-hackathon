import pygame
import sys
import random
from obstacle import ObstacleManager

# 设置窗口的大小
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800

# 设置球的大小
BALL_DIAMETER = 30
BALL_RADIUS = BALL_DIAMETER // 2

# 颜色定义
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 120, 255)

pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('摇滚猫')
font = pygame.font.Font(None, 36)

# 加载背景图片
background_image = pygame.image.load('img/background.png').convert()
background_image = pygame.transform.scale(background_image, (WINDOW_WIDTH, WINDOW_HEIGHT))

# 加载障碍物图片
obstacle_image = pygame.image.load('img/dog.png').convert_alpha()
obstacle_hit_image = pygame.image.load('img/dog-dead.png').convert_alpha()
obstacle_image = pygame.transform.scale(obstacle_image, (70, 60))
obstacle_hit_image = pygame.transform.scale(obstacle_hit_image, (70, 60))

# 加载生命值图片
life_image = pygame.image.load('img/life.png').convert_alpha()
life_image = pygame.transform.scale(life_image, (50, 50))

# 初始化障碍物管理器
obstacle_manager = ObstacleManager(WINDOW_WIDTH, WINDOW_HEIGHT, obstacle_image, obstacle_hit_image)


# 主函数，用于启动游戏
def main():
    # 初始化球的位置和速度
    ball_x = WINDOW_WIDTH // 2
    ball_y = WINDOW_HEIGHT // 2
    ball_dx = 0
    ball_dy = 0

    score = 0
    lives = 3

    # 游戏主循环
    while True:
        # 事件处理
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                key = event.key
                num = key - 48
                ball_rect = pygame.Rect(
                    ball_x - BALL_RADIUS,
                    10 + WINDOW_HEIGHT / 2 - (3 * 90) / 2 + 90 / 2 + 90 * (num - 1),
                    60,
                    10
                )
                if obstacle_manager.check_collision(ball_rect, key):
                    score += 123


        # 更新障碍物
        if obstacle_manager.update_obstacles():
            lives -= 1
            if lives == 0:
                pygame.quit()
                sys.exit()

        # 清屏
        screen.blit(background_image, (0, 0))

        # 绘制障碍物
        obstacle_manager.draw_obstacles(screen)

        # 显示生命值图片
        for i in range(lives):
            screen.blit(life_image, (10 + i * 60, 10))

        # 显示得分
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (WINDOW_WIDTH - 150, 10))

        # 更新屏幕
        pygame.display.flip()

        # 控制游戏刷新速度
        pygame.time.Clock().tick(60)


if __name__ == "__main__":
    main()
