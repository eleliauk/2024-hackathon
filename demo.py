import pygame
import sys
import random
import sound

# 音频
sound = sound.sound()

# pygame.mixer.init()
# pygame.mixer.music.load('audios/first.wav')
# pygame.mixer.music.play(0)

# 设置窗口的大小
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800

# 设置球的大小
BALL_DIAMETER = 30
BALL_RADIUS = BALL_DIAMETER // 1.2

# 设置障碍物的大小和速度
OBSTACLE_WIDTH = 70
OBSTACLE_HEIGHT = 60  # 增加障碍物的高度
OBSTACLE_SPEED = 4
OBSTACLE_KNOCKBACK_SPEED_X = -2  # 障碍物被撞飞的水平速度
OBSTACLE_KNOCKBACK_SPEED_Y = -5

GRAVITY = 1  # 重力加速度

# 轨道数量
TRACK_NUM = 3
TRACK_HEIGHT = 90

# 颜色定义
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 120, 255)

# 初始化 Pygame
pygame.init()

# 设置窗口和标题
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('摇滚猫')

# 设置字体
font = pygame.font.Font(None, 36)

# 加载背景图片
background_image = pygame.image.load('img/background.png').convert()
background_image = pygame.transform.scale(background_image, (WINDOW_WIDTH, WINDOW_HEIGHT))

# 初始化球的位置和速度
ball_x = WINDOW_WIDTH // 1.88
ball_y = WINDOW_HEIGHT // 2
ball_dx = 0
ball_dy = 0

# 加载障碍物图片
obstacle_image1 = pygame.image.load('img/dog_blue.png').convert_alpha()
obstacle_hit_image1 = pygame.image.load('img/dog_blue_die.png').convert_alpha()
obstacle_image1 = pygame.transform.scale(obstacle_image1, (OBSTACLE_WIDTH, OBSTACLE_HEIGHT))
obstacle_hit_image1 = pygame.transform.scale(obstacle_hit_image1, (OBSTACLE_WIDTH, OBSTACLE_HEIGHT))

obstacle_image2 = pygame.image.load('img/dog_red.png').convert_alpha()
obstacle_hit_image2 = pygame.image.load('img/dog_red_die.png').convert_alpha()
obstacle_image2 = pygame.transform.scale(obstacle_image2, (OBSTACLE_WIDTH, OBSTACLE_HEIGHT))
obstacle_hit_image2 = pygame.transform.scale(obstacle_hit_image2, (OBSTACLE_WIDTH, OBSTACLE_HEIGHT))

obstacle_image3 = pygame.image.load('img/dog_green.png').convert_alpha()
obstacle_hit_image3 = pygame.image.load('img/dog_green_die.png').convert_alpha()
obstacle_image3 = pygame.transform.scale(obstacle_image3, (OBSTACLE_WIDTH, OBSTACLE_HEIGHT))
obstacle_hit_image3 = pygame.transform.scale(obstacle_hit_image3, (OBSTACLE_WIDTH, OBSTACLE_HEIGHT))

# 两个按键状态
isKey1 = False
isKey2 = False
isKey3 = False


# 生成障碍物
def create_obstacle():
    rect = pygame.Rect(WINDOW_WIDTH, WINDOW_HEIGHT / 2 - TRACK_HEIGHT / 2, OBSTACLE_WIDTH, OBSTACLE_HEIGHT)
    note = random.randint(1, 3)
    if note == 1:
        return {'rect': rect, 'image': obstacle_image1, 'note': note}
    elif note == 2:
        return {'rect': rect, 'image': obstacle_image2, 'note': note}
    else:
        return {'rect': rect, 'image': obstacle_image3, 'note': note}


# 主函数，用于启动游戏
def main():
    global ball_x, ball_y, ball_dx, ball_dy, isKey1, isKey2, isKey3  # 声明全局变量

    obstacles = [create_obstacle()]
    knocked_back_obstacles = []

    # 游戏主循环
    while True:

        isPress = False
        # 事件处理
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    isKey1 = True
                elif event.key == pygame.K_2:
                    isKey2 = True
                elif event.key == pygame.K_3:
                    isKey3 = True
                elif event.key == pygame.K_UP:
                    if isKey1 and not isKey2 and not isKey3:
                        # 移动障碍物
                        for obstacle in obstacles[:]:
                            if obstacle['note'] == 1:
                                rect = obstacle['rect']
                                # 碰撞检测
                                if rect.colliderect(
                                        pygame.Rect(ball_x - BALL_RADIUS, 0, BALL_DIAMETER * 2, WINDOW_HEIGHT)):
                                    # 障碍物被撞飞
                                    knocked_back_obstacles.append(
                                        [rect, OBSTACLE_KNOCKBACK_SPEED_X, OBSTACLE_KNOCKBACK_SPEED_Y,
                                         obstacle_hit_image1])
                                    obstacles.remove(obstacle)
                                    break
                    elif isKey2 and not isKey1 and not isKey3:
                        # 移动障碍物
                        for obstacle in obstacles[:]:
                            if obstacle['note'] == 2:
                                rect = obstacle['rect']
                                # 碰撞检测
                                if rect.colliderect(
                                        pygame.Rect(ball_x - BALL_RADIUS, 0, BALL_DIAMETER * 2, WINDOW_HEIGHT)):
                                    # 障碍物被撞飞
                                    knocked_back_obstacles.append(
                                        [rect, OBSTACLE_KNOCKBACK_SPEED_X, OBSTACLE_KNOCKBACK_SPEED_Y,
                                         obstacle_hit_image2])
                                    obstacles.remove(obstacle)
                                    break

                    elif isKey3 and not isKey2 and not isKey1:
                        # 移动障碍物
                        for obstacle in obstacles[:]:
                            if obstacle['note'] == 3:
                                rect = obstacle['rect']
                                # 碰撞检测
                                if rect.colliderect(
                                        pygame.Rect(ball_x - BALL_RADIUS, 0, BALL_DIAMETER * 2, WINDOW_HEIGHT)):
                                    # 障碍物被撞飞
                                    knocked_back_obstacles.append(
                                        [rect, OBSTACLE_KNOCKBACK_SPEED_X, OBSTACLE_KNOCKBACK_SPEED_Y,
                                         obstacle_hit_image3])
                                    obstacles.remove(obstacle)
                                    break




            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_1:
                    isKey1 = False
                elif event.key == pygame.K_2:
                    isKey2 = False
                elif event.key == pygame.K_3:
                    isKey3 = False

        # 移动障碍物
        for obstacle in obstacles[:]:
            rect = obstacle['rect']
            rect.x -= OBSTACLE_SPEED

            # 移除已通过的障碍物
            if rect.x + OBSTACLE_WIDTH < 0:
                obstacles.remove(obstacle)

        # 处理被撞飞的障碍物
        for obstacle_data in knocked_back_obstacles[:]:
            rect, knockback_x, knockback_y, image = obstacle_data
            rect.x += knockback_x
            rect.y += knockback_y
            obstacle_data[2] += GRAVITY  # 更新垂直速度

            # 如果障碍物离开屏幕，则移除
            if rect.x + OBSTACLE_WIDTH < 0 or rect.y > WINDOW_HEIGHT:
                knocked_back_obstacles.remove(obstacle_data)

        # 生成新障碍物
        if random.randint(1, 60) == 1:  # 每隔一段时间生成一个新的障碍物
            obstacles.append(create_obstacle())

        # 清屏
        screen.blit(background_image, (0, 0))

        # 画线
        # pygame.draw.line(screen, WHITE, (ball_x, 0), (ball_x, WINDOW_HEIGHT), 2)

        # 画障碍物
        for obstacle in obstacles:
            screen.blit(obstacle['image'], obstacle['rect'])

        # 画被撞飞的障碍物
        for obstacle_data in knocked_back_obstacles:
            rect = obstacle_data[0]
            image = obstacle_data[3]
            screen.blit(image, rect)

        # 更新屏幕
        pygame.display.flip()

        # 控制游戏刷新速度
        pygame.time.Clock().tick(60)


# 确保可以直接运行 demo.py 作为主程序
if __name__ == "__main__":
    main()
