import pygame
import sys
import random
import sound

# 设置窗口的大小
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 400

# 设置球的大小
BALL_DIAMETER = 15
BALL_RADIUS = BALL_DIAMETER // 2

# 设置障碍物的大小和速度
OBSTACLE_WIDTH = 20
OBSTACLE_HEIGHT = 60
OBSTACLE_SPEED = 2

# 颜色定义
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# 初始化 Pygame
pygame.init()

# 设置窗口和标题
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Avoid Obstacles')

# 设置字体
font = pygame.font.Font(None, 36)

# 设置球的初始位置
ball_x = WINDOW_WIDTH // 4
ball_y = WINDOW_HEIGHT // 2

# 设置球的速度
ball_dy = 2

# sound设置
sound = sound.sound()

# 生成障碍物
def create_obstacle():
    return pygame.Rect(WINDOW_WIDTH, random.randint(0, WINDOW_HEIGHT - OBSTACLE_HEIGHT), OBSTACLE_WIDTH,
                       OBSTACLE_HEIGHT)


obstacles = [create_obstacle()]

# 游戏主循环
while True:
    # 事件处理
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            key = event.key
            if key in sound.keyDict:
                sound.playSoundScape(key)


    # 获取键盘状态
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        ball_y -= ball_dy
    if keys[pygame.K_DOWN]:
        ball_y += ball_dy

    # 限制球不出界
    ball_y = min(max(ball_y, BALL_RADIUS), WINDOW_HEIGHT - BALL_RADIUS)

    # 移动障碍物
    for obstacle in obstacles:
        obstacle.x -= OBSTACLE_SPEED

    # 移除已通过的障碍物
    obstacles = [obstacle for obstacle in obstacles if obstacle.x + OBSTACLE_WIDTH > 0]

    # 生成新障碍物
    if not obstacles or obstacles[-1].x < WINDOW_WIDTH - 200:
        obstacles.append(create_obstacle())

    # 碰撞检测
    for obstacle in obstacles:
        if obstacle.colliderect(pygame.Rect(ball_x - BALL_RADIUS, ball_y - BALL_RADIUS, BALL_DIAMETER, BALL_DIAMETER)):
            text = font.render("Game Over", True, WHITE)
            screen.blit(text, (WINDOW_WIDTH // 2 - text.get_width() // 2, WINDOW_HEIGHT // 2 - text.get_height() // 2))
            pygame.display.flip()
            pygame.time.wait(2000)
            pygame.quit()
            sys.exit()

    # 清屏
    screen.fill(BLACK)

    # 画球
    pygame.draw.circle(screen, WHITE, (ball_x, ball_y), BALL_RADIUS)

    # 画障碍物
    for obstacle in obstacles:
        pygame.draw.rect(screen, WHITE, obstacle)

    # 更新屏幕
    pygame.display.flip()

    # 延时
    pygame.time.wait(10)