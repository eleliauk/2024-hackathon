import pygame


def scale_background(image_path, screen_width, screen_height):
    # 加载原始图像
    original_image = pygame.image.load(image_path)
    # 调整图像大小以适应屏幕
    scaled_image = pygame.transform.scale(original_image, (screen_width, screen_height))
    return scaled_image
