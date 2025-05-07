# sprites.py
import pygame
import math
import random
from settings import *

class Paddle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.original_width = PADDLE_WIDTH
        self.image = pygame.Surface((self.original_width, PADDLE_HEIGHT))
        self.image.fill(PADDLE_COLOR)
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT-30))
        self.speed = 8

    def reset_size(self):
        
        original_center = self.rect.center  # 获取原始位置
        self.image = pygame.Surface((self.original_width, PADDLE_HEIGHT))
        self.image.fill(PADDLE_COLOR)
        self.rect = self.image.get_rect(center=original_center)

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += self.speed

class Ball(pygame.sprite.Sprite):
    def __init__(self, speed_multiplier=1.0):
        super().__init__()
        # 图像初始化
        self.image = pygame.Surface((BALL_RADIUS*2, BALL_RADIUS*2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, BALL_COLOR, (BALL_RADIUS, BALL_RADIUS), BALL_RADIUS)
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
        
        # 速度控制
        self.base_speed = BALL_BASE_SPEED  # 基准速度
        self.speed_x = self.base_speed * speed_multiplier
        self.speed_y = -self.base_speed * speed_multiplier

    def reset_speed(self):
        self.speed_x = self.base_speed * (abs(self.speed_x)/self.speed_x if self.speed_x !=0 else 1)
        self.speed_y = self.base_speed * (abs(self.speed_y)/self.speed_y if self.speed_y !=0 else 1)

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        
        # 边界反弹
        if self.rect.left <= 0 or self.rect.right >= SCREEN_WIDTH:
            self.speed_x *= -1
        if self.rect.top <= 0:
            self.speed_y *= -1

class Brick(pygame.sprite.Sprite):
    def __init__(self, x, y, color_char):
        super().__init__()
        self.color_char = color_char
        
        # 创建透明砖块（占位符）
        if color_char == " ":
            self.image = pygame.Surface((BRICK_WIDTH, BRICK_HEIGHT), pygame.SRCALPHA)
            self.image.fill((0,0,0,0))
        # 创建可见砖块
        else:
            self.image = pygame.Surface((BRICK_WIDTH, BRICK_HEIGHT))
            self.image.fill(COLOR_MAP[color_char])
        
        self.rect = self.image.get_rect(topleft=(x, y))

class PowerUp(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # 类型配置
        self.types = ["expand", "speed", "shrink", "slow"] * 2 + ["life"]
        self.type = random.choice(self.types)
        
        # 图像特效初始化
        self.base_image = pygame.Surface((30, 15))
        self.base_image.fill(POWERUP_COLORS[self.type])
        self.image = self.base_image.copy()
        self.rect = self.image.get_rect(center=(x, y))
        self.blink_timer = 0    # 闪烁计时器
        self.scale_factor = 1.0 # 缩放系数

    def update(self):
        # 下落运动
        self.rect.y += 3
        
        # 闪烁特效（每0.5秒切换）
        self.blink_timer += 1
        if self.blink_timer % 30 == 0:
            self.image.set_alpha(100 if self.image.get_alpha() == 255 else 255)
        
        # 缩放特效（正弦波动）
        self.scale_factor = 1.0 + 0.1 * math.sin(pygame.time.get_ticks() / 200)
        scaled_image = pygame.transform.scale_by(self.base_image, (self.scale_factor, 1.0))
        self.image = scaled_image
        self.rect = scaled_image.get_rect(center=self.rect.center)