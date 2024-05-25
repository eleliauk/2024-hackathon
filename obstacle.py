import pygame
import random

# 设置障碍物的大小和速度
OBSTACLE_WIDTH = 70
OBSTACLE_HEIGHT = 60
OBSTACLE_SPEED = 5
OBSTACLE_KNOCKBACK_SPEED_X = -2
OBSTACLE_KNOCKBACK_SPEED_Y = -5
GRAVITY = 1

# 轨道数量
TRACK_NUM = 3
TRACK_HEIGHT = 90


class ObstacleManager:
    def __init__(self, window_width, window_height, obstacle_image, obstacle_hit_image):
        self.window_width = window_width
        self.window_height = window_height
        self.obstacle_image = obstacle_image
        self.obstacle_hit_image = obstacle_hit_image
        self.obstacles = []
        self.knocked_back_obstacles = []

    def create_obstacle(self):
        rect = pygame.Rect(
            self.window_width,
            10 + self.window_height / 2 - (TRACK_NUM * TRACK_HEIGHT) / 2 + random.randint(0,
                                                                                          TRACK_NUM - 1) * TRACK_HEIGHT,
            OBSTACLE_WIDTH,
            OBSTACLE_HEIGHT
        )
        self.obstacles.append({'rect': rect, 'image': self.obstacle_image})

    def update_obstacles(self):
        isMiss = False
        for obstacle in self.obstacles[:]:
            rect = obstacle['rect']
            rect.x -= OBSTACLE_SPEED
            if rect.x + OBSTACLE_WIDTH < 0:#左侧漏击
                self.obstacles.remove(obstacle)
                isMiss = True

        for obstacle_data in self.knocked_back_obstacles[:]:
            rect, knockback_x, knockback_y, image = obstacle_data
            rect.x += knockback_x
            rect.y += knockback_y
            obstacle_data[2] += GRAVITY
            if rect.x + OBSTACLE_WIDTH < 0 or rect.y > self.window_height:
                self.knocked_back_obstacles.remove(obstacle_data)

        if random.randint(1, 30) == 1:
            self.create_obstacle()

        return isMiss

    def draw_obstacles(self, screen):
        for obstacle in self.obstacles:
            screen.blit(obstacle['image'], obstacle['rect'])

        for obstacle_data in self.knocked_back_obstacles:
            rect = obstacle_data[0]
            image = obstacle_data[3]
            screen.blit(image, rect)

    def check_collision(self, ball_rect, key):
        for obstacle in self.obstacles[:]:
            rect = obstacle['rect']
            if rect.colliderect(ball_rect):
                self.knocked_back_obstacles.append(
                    [rect, OBSTACLE_KNOCKBACK_SPEED_X, OBSTACLE_KNOCKBACK_SPEED_Y, self.obstacle_hit_image]
                )
                self.obstacles.remove(obstacle)
                return True
        return False
