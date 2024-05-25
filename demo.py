import pygame
import sys
import random

# 音频
pygame.mixer.init()
pygame.mixer.music.load('audios/c.wav')


# 设置窗口的大小
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 400

# 设置球的大小
BALL_DIAMETER = 15
BALL_RADIUS = BALL_DIAMETER // 2

# 设置障碍物的大小和速度
# OBSTACLE_WIDTH = 20
# OBSTACLE_HEIGHT = 60
OBSTACLE_WIDTH = 60
OBSTACLE_HEIGHT = 20
OBSTACLE_SPEED = 2
OBSTACLE_KNOCKBACK_SPEED_X = -5  # 障碍物被撞飞的水平速度
OBSTACLE_KNOCKBACK_SPEED_Y = -10  # 障碍物被撞飞的初始垂直速度
GRAVITY = 1  # 重力加速度

# 颜色定义
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# 初始化 Pygame
pygame.init()

# 设置窗口和标题
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Avoid Obstacles')

# 设置字体
font = pygame.font.Font(None, 36)

# 初始化球的位置和速度
ball_x = WINDOW_WIDTH // 4
ball_y = WINDOW_HEIGHT // 1.2
ball_dx = 0
ball_dy = 0


# 生成障碍物
def create_obstacle():
    #随机生成横向四个轨道的障碍物，初始化在顶部
    return pygame.Rect(random.randint(0,2)*WINDOW_WIDTH/3 + WINDOW_WIDTH/6 -OBSTACLE_WIDTH/2, (0 - OBSTACLE_HEIGHT), OBSTACLE_WIDTH,OBSTACLE_HEIGHT)
    # return pygame.Rect(WINDOW_WIDTH, random.randint(0, WINDOW_HEIGHT - OBSTACLE_HEIGHT), OBSTACLE_WIDTH,OBSTACLE_HEIGHT)


# 主函数，用于启动游戏
def main():
    global ball_x, ball_y, ball_dx, ball_dy  # 声明全局变量

    obstacles = [create_obstacle()]
    knocked_back_obstacles = []

    # 游戏主循环
    while True:
        # 事件处理
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # 键盘控制球的移动
        # keys = pygame.key.get_pressed()
        # if keys[pygame.K_LEFT]:
        #     ball_dx = -10
        # if keys[pygame.K_RIGHT]:
        #     ball_dx = 10
        # if keys[pygame.K_UP]:
        #     ball_dy = -10
        # if keys[pygame.K_DOWN]:
        #     ball_dy = 10
        #
        # 停止球的移动
        # if not keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT]:
        #     ball_dx = 0
        # if not keys[pygame.K_UP] and not keys[pygame.K_DOWN]:
        #     ball_dy = 0

        keys = pygame.key.get_pressed()
        if keys[pygame.K_1]:
            ball_x = WINDOW_WIDTH/6*1
        if keys[pygame.K_2]:
            ball_x = WINDOW_WIDTH/6*3
        if keys[pygame.K_3]:
            ball_x = WINDOW_WIDTH/6*5
        # if keys[pygame.K_4]:
        #     ball_y = 340

        # 更新球的位置
        # ball_x += ball_dx
        # ball_y += ball_dy

        # 限制球不出界
        # ball_x = max(BALL_RADIUS, min(ball_x, WINDOW_WIDTH - BALL_RADIUS))
        # ball_y = max(BALL_RADIUS, min(ball_y, WINDOW_HEIGHT - BALL_RADIUS))

        # 移动障碍物
        for obstacle in obstacles[:]:
            obstacle.y += OBSTACLE_SPEED

            # 移除已通过的障碍物
            if obstacle.x + OBSTACLE_WIDTH < 0:
                obstacles.remove(obstacle)

            # 碰撞检测
            if obstacle.colliderect(
                    pygame.Rect(ball_x - BALL_RADIUS, ball_y - BALL_RADIUS, BALL_DIAMETER, BALL_DIAMETER)):
                # 障碍物被撞飞
                pygame.mixer.music.play(0)
                knocked_back_obstacles.append([obstacle, OBSTACLE_KNOCKBACK_SPEED_X, OBSTACLE_KNOCKBACK_SPEED_Y])
                obstacles.remove(obstacle)

        # 处理被撞飞的障碍物
        for obstacle_data in knocked_back_obstacles[:]:
            obstacle, knockback_x, knockback_y = obstacle_data
            obstacle.x += knockback_x
            obstacle.y += knockback_y
            obstacle_data[2] += GRAVITY  # 更新垂直速度

            # 如果障碍物离开屏幕，则移除
            if (obstacle.x + OBSTACLE_WIDTH < 0 or obstacle.y > WINDOW_HEIGHT):
                knocked_back_obstacles.remove(obstacle_data)

        # 生成新障碍物
        if random.randint(1, 60) == 1:  # 每隔一段时间生成一个新的障碍物
            obstacles.append(create_obstacle())

        # 清屏
        screen.fill(BLACK)

        # 画球
        pygame.draw.circle(screen, WHITE, (ball_x, ball_y), BALL_RADIUS)

        # 画障碍物
        for obstacle in obstacles:
            pygame.draw.rect(screen, RED, obstacle)

        # 画被撞飞的障碍物
        for obstacle_data in knocked_back_obstacles:
            obstacle = obstacle_data[0]
            pygame.draw.rect(screen, RED, obstacle)

        # 更新屏幕
        pygame.display.flip()

        # 控制游戏刷新速度
        pygame.time.Clock().tick(60)


# 确保可以直接运行 demo.py 作为主程序
if __name__ == "__main__":
    main()
