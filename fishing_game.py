#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
《星露谷物语》钓鱼小游戏复刻
使用Pygame实现
"""

import pygame
import random
import sys

# 初始化Pygame
pygame.init()

# 游戏常量
WINDOW_WIDTH = 267  # 缩小到原来的1/3
WINDOW_HEIGHT = 200  # 缩小到原来的1/3
FISHING_AREA_WIDTH = 40  # 缩小到原来的1/3
FISHING_AREA_HEIGHT = 133  # 缩小到原来的1/3
FISHING_AREA_X = (WINDOW_WIDTH - FISHING_AREA_WIDTH) // 2
FISHING_AREA_Y = (WINDOW_HEIGHT - FISHING_AREA_HEIGHT) // 2

# 颜色定义
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
LIGHT_GREEN = (100, 255, 100)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
LIGHT_BLUE = (100, 100, 255)
GRAY = (150, 150, 150)
DARK_GRAY = (100, 100, 100)

# 游戏状态
class GameState:
    READY = 0
    FISHING = 1
    SUCCESS = 2
    FAILURE = 3

class Fish:
    def __init__(self):
        self.x = FISHING_AREA_X + 3
        self.y = random.randint(FISHING_AREA_Y + 7, FISHING_AREA_Y + FISHING_AREA_HEIGHT - 7)
        self.width = 10
        self.height = 7
        self.speed = random.uniform(0.3, 1.0)
        self.direction = random.choice([-1, 1])
        self.pattern = random.choice(["random", "sprint", "periodic"])
        self.sprint_timer = 0
        self.sprint_duration = 60
        self.periodic_timer = 0
        self.periodic_duration = 120
    
    def update(self):
        # 根据模式更新鱼的位置
        if self.pattern == "random":
            # 随机改变方向
            if random.random() < 0.02:
                self.direction *= -1
            self.y += self.speed * self.direction
        
        elif self.pattern == "sprint":
            # 冲刺模式
            if self.sprint_timer <= 0:
                self.direction = random.choice([-1, 1])
                self.sprint_timer = self.sprint_duration
                self.speed = random.uniform(3.0, 5.0)
            else:
                self.sprint_timer -= 1
                if self.sprint_timer < self.sprint_duration * 0.7:
                    self.speed = max(1.0, self.speed * 0.98)
                self.y += self.speed * self.direction
        
        elif self.pattern == "periodic":
            # 周期性移动
            self.periodic_timer = (self.periodic_timer + 1) % self.periodic_duration
            # 使用正弦函数创建周期性移动
            self.y = FISHING_AREA_Y + FISHING_AREA_HEIGHT // 2 + \
                    int(math.sin(self.periodic_timer / self.periodic_duration * 2 * math.pi) * FISHING_AREA_HEIGHT // 3)
        
        # 边界检查
        if self.y < FISHING_AREA_Y:
            self.y = FISHING_AREA_Y
            self.direction = 1
        elif self.y > FISHING_AREA_Y + FISHING_AREA_HEIGHT - self.height:
            self.y = FISHING_AREA_Y + FISHING_AREA_HEIGHT - self.height
            self.direction = -1
    
    def draw(self, screen):
        # 绘制鱼的身体
        pygame.draw.ellipse(screen, BLUE, (self.x, self.y, self.width, self.height))
        # 绘制鱼鳍
        pygame.draw.polygon(screen, BLUE, [(self.x + self.width, self.y + self.height // 4),
                                          (self.x + self.width + 3, self.y),
                                          (self.x + self.width + 3, self.y + self.height // 2)])
        pygame.draw.polygon(screen, BLUE, [(self.x + self.width, self.y + self.height * 3 // 4),
                                          (self.x + self.width + 3, self.y + self.height),
                                          (self.x + self.width + 3, self.y + self.height // 2)])
        # 绘制眼睛
        pygame.draw.circle(screen, WHITE, (self.x + 7, self.y + self.height // 2), 1)
        pygame.draw.circle(screen, BLACK, (self.x + 8, self.y + self.height // 2), 1)

class FishingBar:
    def __init__(self):
        self.x = FISHING_AREA_X + 13
        self.y = FISHING_AREA_Y + FISHING_AREA_HEIGHT - 13
        self.width = 13
        self.height = 13
        # 物理参数（参考location.py）
        self.m = 1.0           # 质量
        self.g = 10           # 重力加速度
        self.f = 50.0          # 瞬时力大小
        self.s = 0.05          # 力作用时间
        self.dt = 1/60         # 60 FPS
        self.v = 0.0           # 速度
        self.max_height = 20  # 最大高度，随技能等级提升
        self.min_height = 7   # 最小高度
    
    def apply_force(self):
        # 施加向上的瞬时力
        dv = (self.f * self.s) / self.m
        self.v += dv
    
    def update(self):
        # 应用重力
        self.v -= self.g * self.dt
        # 更新位置
        self.y += self.v * self.dt
        
        # 边界检查
        if self.y <= FISHING_AREA_Y:
            self.y = FISHING_AREA_Y
            self.v = 0
        elif self.y >= FISHING_AREA_Y + FISHING_AREA_HEIGHT - self.height:
            self.y = FISHING_AREA_Y + FISHING_AREA_HEIGHT - self.height
            self.v = 0
    
    def draw(self, screen):
        # 绘制钓鱼条
        pygame.draw.rect(screen, GREEN, (self.x, self.y, self.width, self.height))
        # 绘制边框
        pygame.draw.rect(screen, DARK_GRAY, (self.x, self.y, self.width, self.height), 2)

class ProgressBar:
    def __init__(self):
        self.x = FISHING_AREA_X - 10
        self.y = FISHING_AREA_Y
        self.width = 7
        self.height = FISHING_AREA_HEIGHT
        self.progress = 0
        self.max_progress = 100
    
    def update(self, is_overlapping):
        # 根据是否重叠更新进度
        if is_overlapping:
            self.progress += 0.5
        else:
            self.progress = max(0, self.progress - 0.2)
        
        # 限制进度范围
        self.progress = min(self.max_progress, self.progress)
    
    def draw(self, screen):
        # 绘制进度条背景
        pygame.draw.rect(screen, GRAY, (self.x, self.y, self.width, self.height))
        # 绘制进度
        progress_height = int(self.progress / self.max_progress * self.height)
        pygame.draw.rect(screen, LIGHT_GREEN, (self.x, self.y + self.height - progress_height, self.width, progress_height))
        # 绘制边框
        pygame.draw.rect(screen, DARK_GRAY, (self.x, self.y, self.width, self.height), 2)

class FishingGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("星露谷物语钓鱼小游戏")
        self.clock = pygame.time.Clock()
        self.state = GameState.READY
        self.fish = None
        self.fishing_bar = None
        self.progress_bar = None
        # 尝试使用系统字体，确保支持中文
        try:
            # 对于Windows系统，使用微软雅黑字体
            self.font = pygame.font.SysFont("Microsoft YaHei", 12)
            self.small_font = pygame.font.SysFont("Microsoft YaHei", 8)
        except:
            # 如果失败，使用默认字体
            self.font = pygame.font.Font(None, 12)
            self.small_font = pygame.font.Font(None, 8)
    
    def run(self):
        running = True
        while running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)
        pygame.quit()
        sys.exit()
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.state == GameState.READY:
                    # 点击开始按钮
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if 117 <= mouse_x <= 150 and 133 <= mouse_y <= 150:
                        self.start_fishing()
                elif self.state == GameState.FISHING:
                    # 点击鼠标施加向上的力
                    self.fishing_bar.apply_force()
                elif self.state in [GameState.SUCCESS, GameState.FAILURE]:
                    # 点击重新开始
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if 117 <= mouse_x <= 150 and 133 <= mouse_y <= 150:
                        self.state = GameState.READY
    
    def start_fishing(self):
        self.state = GameState.FISHING
        self.fish = Fish()
        self.fishing_bar = FishingBar()
        self.progress_bar = ProgressBar()
    
    def update(self):
        if self.state == GameState.FISHING:
            # 更新鱼的位置
            self.fish.update()
            
            # 更新钓鱼条（使用物理引擎）
            self.fishing_bar.update()
            
            # 检测重叠
            is_overlapping = self.check_overlap()
            
            # 更新进度条
            self.progress_bar.update(is_overlapping)
            
            # 检查游戏状态
            if self.progress_bar.progress >= self.progress_bar.max_progress:
                self.state = GameState.SUCCESS
            # 只有当进度条从正值下降到0时才失败，初始值为0不触发失败
            elif self.progress_bar.progress <= 0 and hasattr(self, 'progress_was_positive') and self.progress_was_positive:
                self.state = GameState.FAILURE
            
            # 记录进度是否曾经为正值
            if not hasattr(self, 'progress_was_positive'):
                self.progress_was_positive = False
            if self.progress_bar.progress > 0:
                self.progress_was_positive = True
    
    def check_overlap(self):
        # 检测钓鱼条与鱼是否重叠
        fish_rect = pygame.Rect(self.fish.x, self.fish.y, self.fish.width, self.fish.height)
        bar_rect = pygame.Rect(self.fishing_bar.x, self.fishing_bar.y, self.fishing_bar.width, self.fishing_bar.height)
        return fish_rect.colliderect(bar_rect)
    
    def draw(self):
        # 绘制背景
        self.screen.fill(LIGHT_BLUE)
        
        if self.state == GameState.READY:
            # 绘制准备界面
            title_text = self.font.render("星露谷物语钓鱼小游戏", True, BLACK)
            self.screen.blit(title_text, (WINDOW_WIDTH // 2 - title_text.get_width() // 2, 67))
            
            start_text = self.font.render("开始钓鱼", True, WHITE)
            pygame.draw.rect(self.screen, GREEN, (117, 133, 33, 17))
            self.screen.blit(start_text, (117 + 16 - start_text.get_width() // 2, 133 + 8 - start_text.get_height() // 2))
            
        elif self.state == GameState.FISHING:
            # 绘制钓鱼区域
            pygame.draw.rect(self.screen, WHITE, (FISHING_AREA_X, FISHING_AREA_Y, FISHING_AREA_WIDTH, FISHING_AREA_HEIGHT))
            pygame.draw.rect(self.screen, GRAY, (FISHING_AREA_X, FISHING_AREA_Y, FISHING_AREA_WIDTH, FISHING_AREA_HEIGHT), 2)
            
            # 绘制鱼
            self.fish.draw(self.screen)
            
            # 绘制钓鱼条
            self.fishing_bar.draw(self.screen)
            
            # 绘制进度条
            self.progress_bar.draw(self.screen)
            
        elif self.state == GameState.SUCCESS:
            # 绘制成功界面
            success_text = self.font.render("钓鱼成功！", True, BLACK)
            self.screen.blit(success_text, (WINDOW_WIDTH // 2 - success_text.get_width() // 2, 67))
            
            restart_text = self.font.render("再钓一次", True, WHITE)
            pygame.draw.rect(self.screen, GREEN, (117, 133, 33, 17))
            self.screen.blit(restart_text, (117 + 16 - restart_text.get_width() // 2, 133 + 8 - restart_text.get_height() // 2))
            
        elif self.state == GameState.FAILURE:
            # 绘制失败界面
            failure_text = self.font.render("钓鱼失败！", True, BLACK)
            self.screen.blit(failure_text, (WINDOW_WIDTH // 2 - failure_text.get_width() // 2, 67))
            
            restart_text = self.font.render("再试一次", True, WHITE)
            pygame.draw.rect(self.screen, GREEN, (117, 133, 33, 17))
            self.screen.blit(restart_text, (117 + 16 - restart_text.get_width() // 2, 133 + 8 - restart_text.get_height() // 2))
        
        # 更新显示
        pygame.display.flip()

if __name__ == "__main__":
    # 导入math模块（在Fish类中使用）
    import math
    game = FishingGame()
    game.run()
