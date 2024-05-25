import time
import Decoder
import pygame
import sys
import random
import sound
import pass_screen

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
OBSTACLE_KNOCKBACK_SPEED_Y = -5  # 障碍物被撞飞的初始垂直速度
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
obstacle_image1 = pygame.image.load('img/dog_red.png').convert_alpha()
obstacle_hit_image1 = pygame.image.load('img/dog_red_die.png').convert_alpha()
obstacle_image1 = pygame.transform.scale(obstacle_image1, (OBSTACLE_WIDTH, OBSTACLE_HEIGHT))
obstacle_hit_image1 = pygame.transform.scale(obstacle_hit_image1, (OBSTACLE_WIDTH, OBSTACLE_HEIGHT))

obstacle_image2 = pygame.image.load('img/dog_blue.png').convert_alpha()
obstacle_hit_image2 = pygame.image.load('img/dog_blue_die.png').convert_alpha()
obstacle_image2 = pygame.transform.scale(obstacle_image2, (OBSTACLE_WIDTH, OBSTACLE_HEIGHT))
obstacle_hit_image2 = pygame.transform.scale(obstacle_hit_image2, (OBSTACLE_WIDTH, OBSTACLE_HEIGHT))

obstacle_image3 = pygame.image.load('img/dog_green.png').convert_alpha()
obstacle_hit_image3 = pygame.image.load('img/dog_green_die.png').convert_alpha()
obstacle_image3 = pygame.transform.scale(obstacle_image3, (OBSTACLE_WIDTH, OBSTACLE_HEIGHT))
obstacle_hit_image3 = pygame.transform.scale(obstacle_hit_image3, (OBSTACLE_WIDTH, OBSTACLE_HEIGHT))

# 加载提示按钮图片
button1Up_image = pygame.image.load('img/button1_up.png').convert_alpha()
button1Down_image = pygame.image.load('img/button1_down.png').convert_alpha()
button2Up_image = pygame.image.load('img/button2_up.png').convert_alpha()
button2Down_image = pygame.image.load('img/button2_down.png').convert_alpha()
button3Up_image = pygame.image.load('img/button3_up.png').convert_alpha()
button3Down_image = pygame.image.load('img/button3_down.png').convert_alpha()

# 加载提示按钮的大小
BUTTON_WIDTH = 50
BUTTON_HEIGHT = 80

# 加载提示按钮图片
button1Up_image = pygame.transform.scale(button1Up_image, (BUTTON_WIDTH, BUTTON_HEIGHT))
button1Down_image = pygame.transform.scale(button1Down_image, (BUTTON_WIDTH, BUTTON_HEIGHT))
button2Up_image = pygame.transform.scale(button2Up_image, (BUTTON_WIDTH, BUTTON_HEIGHT))
button2Down_image = pygame.transform.scale(button2Down_image, (BUTTON_WIDTH, BUTTON_HEIGHT))
button3Up_image = pygame.transform.scale(button3Up_image, (BUTTON_WIDTH, BUTTON_HEIGHT))
button3Down_image = pygame.transform.scale(button3Down_image, (BUTTON_WIDTH, BUTTON_HEIGHT))

button1X = 35+WINDOW_WIDTH/2 - BUTTON_WIDTH/2*4
button2X = 35+WINDOW_WIDTH/2 - BUTTON_WIDTH/2
button3X = 35+WINDOW_WIDTH/2 + BUTTON_WIDTH/2 * 2
buttonY = WINDOW_HEIGHT/2+100

# 两个按键状态
isKey1 = False
isKey2 = False
isKey3 = False

# 按键队列
keyQueue = Decoder.Decoder("./scores/in.info").get_beat()
# keyQueue = Decoder.Decoder("./scores/0-27-31_SongScore.txt").get_beat()
1
TIMER_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(TIMER_EVENT, 150)  # 200毫秒

# 生成障碍物
def create_obstacle(num):
    notes = keyQueue[num]
    rect = pygame.Rect(WINDOW_WIDTH, WINDOW_HEIGHT / 2 - TRACK_HEIGHT / 2, OBSTACLE_WIDTH, OBSTACLE_HEIGHT)
    level = 0
    for note in notes:
        lev = note[0] + 12 * note[1]
        lev //= 12
        lev += 1
        if lev > level:
            level = lev

    print(level)
    if level == 1:
        return {'rect': rect, 'image': obstacle_image1, 'level': level,'notes':notes}
    elif level == 2:
        return {'rect': rect, 'image': obstacle_image2, 'level': level,'notes':notes}
    else:
        return {'rect': rect, 'image': obstacle_image3, 'level': level,'notes':notes}


# 主函数，用于启动游戏
def main():
    global ball_x, ball_y, ball_dx, ball_dy, isKey1, isKey2, isKey3  # 声明全局变量

    obstacles = []
    knocked_back_obstacles = []

    #时间戳
    numOfNote = 0


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
                elif event.key == pygame.K_SPACE:
                    for obstacle in obstacles[:]:
                        if (obstacle['level'] == 1 and isKey1) or (obstacle['level'] == 2 and isKey2) or (obstacle['level'] == 3 and isKey3):
                            rect = obstacle['rect']
                            # 碰撞检测
                            if rect.colliderect(pygame.Rect(ball_x - BALL_RADIUS, 0, BALL_DIAMETER * 2, WINDOW_HEIGHT)):
                                # 障碍物被撞飞
                                imgDie = obstacle_hit_image1
                                if obstacle['level'] == 2:
                                    imgDie = obstacle_hit_image2
                                elif obstacle['level'] == 3:
                                    imgDie = obstacle_hit_image3
                                knocked_back_obstacles.append( [rect, OBSTACLE_KNOCKBACK_SPEED_X, OBSTACLE_KNOCKBACK_SPEED_Y, imgDie])
                                obstacles.remove(obstacle)
                                for note in obstacle['notes']:
                                    sound.playSoundScapebyName(note[0], note[1])
                                break

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_1:
                    isKey1 = False
                elif event.key == pygame.K_2:
                    isKey2 = False
                elif event.key == pygame.K_3:
                    isKey3 = False
            elif event.type == TIMER_EVENT:
                if numOfNote < len(keyQueue):
                    if (len(keyQueue[numOfNote]) != 0):
                        obstacles.append(create_obstacle(numOfNote))
                    numOfNote += 1


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



        # 清屏
        screen.blit(background_image, (0, 0))

        # 画按钮
        if isKey1:
            screen.blit(button1Down_image, (button1X, buttonY))
        else:
            screen.blit(button1Up_image, (button1X, buttonY))

        if isKey2:
            screen.blit(button2Down_image, (button2X, buttonY))
        else:
            screen.blit(button2Up_image, (button2X, buttonY))

        if isKey3:
            screen.blit(button3Down_image, (button3X, buttonY))
        else:
            screen.blit(button3Up_image, (button3X, buttonY))

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

        if len(obstacles) == 0 and numOfNote >= len(keyQueue):
            print("Game Over")
            pass_screen.PassScreen(screen).run()
            pygame.quit()
            sys.exit()


# 确保可以直接运行 demo.py 作为主程序
if __name__ == "__main__":
    main()
