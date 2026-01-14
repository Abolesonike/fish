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
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
FISHING_AREA_WIDTH = 120
FISHING_AREA_HEIGHT = 400
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
        self.x = FISHING_AREA_X + 10
        self.y = random.randint(FISHING_AREA_Y + 20, FISHING_AREA_Y + FISHING_AREA_HEIGHT - 20)
        self.width = 30
        self.height = 20
        self.speed = random.uniform(1.0, 3.0)
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
                                          (self.x + self.width + 10, self.y),
                                          (self.x + self.width + 10, self.y + self.height // 2)])
        pygame.draw.polygon(screen, BLUE, [(self.x + self.width, self.y + self.height * 3 // 4),
                                          (self.x + self.width + 10, self.y + self.height),
                                          (self.x + self.width + 10, self.y + self.height // 2)])
        # 绘制眼睛
        pygame.draw.circle(screen, WHITE, (self.x + 20, self.y + self.height // 2), 3)
        pygame.draw.circle(screen, BLACK, (self.x + 21, self.y + self.height // 2), 1)

class FishingBar:
    def __init__(self):
        self.x = FISHING_AREA_X + 50
        self.y = FISHING_AREA_Y + FISHING_AREA_HEIGHT - 50
        self.width = 40
        self.height = 40
        self.speed = 2.0
        self.target_y = self.y
        self.max_height = 60  # 最大高度，随技能等级提升
        self.min_height = 20   # 最小高度
    
    def update(self, mouse_y):
        # 计算目标位置
        self.target_y = mouse_y - self.height // 2
        
        # 限制目标位置在钓鱼区域内
        if self.target_y < FISHING_AREA_Y:
            self.target_y = FISHING_AREA_Y
        elif self.target_y > FISHING_AREA_Y + FISHING_AREA_HEIGHT - self.height:
            self.target_y = FISHING_AREA_Y + FISHING_AREA_HEIGHT - self.height
        
        # 平滑移动到目标位置
        if self.y < self.target_y:
            self.y += min(self.speed, self.target_y - self.y)
        elif self.y > self.target_y:
            self.y -= min(self.speed, self.y - self.target_y)
    
    def draw(self, screen):
        # 绘制钓鱼条
        pygame.draw.rect(screen, GREEN, (self.x, self.y, self.width, self.height))
        # 绘制边框
        pygame.draw.rect(screen, DARK_GRAY, (self.x, self.y, self.width, self.height), 2)

class ProgressBar:
    def __init__(self):
        self.x = FISHING_AREA_X - 30
        self.y = FISHING_AREA_Y
        self.width = 20
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
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
    
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
                    if 350 <= mouse_x <= 450 and 400 <= mouse_y <= 450:
                        self.start_fishing()
                elif self.state in [GameState.SUCCESS, GameState.FAILURE]:
                    # 点击重新开始
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if 350 <= mouse_x <= 450 and 400 <= mouse_y <= 450:
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
            
            # 获取鼠标位置并更新钓鱼条
            mouse_x, mouse_y = pygame.mouse.get_pos()
            self.fishing_bar.update(mouse_y)
            
            # 检测重叠
            is_overlapping = self.check_overlap()
            
            # 更新进度条
            self.progress_bar.update(is_overlapping)
            
            # 检查游戏状态
            if self.progress_bar.progress >= self.progress_bar.max_progress:
                self.state = GameState.SUCCESS
            # 这里可以添加失败条件，例如进度条为0时
    
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
            self.screen.blit(title_text, (WINDOW_WIDTH // 2 - title_text.get_width() // 2, 200))
            
            start_text = self.font.render("开始钓鱼", True, WHITE)
            pygame.draw.rect(self.screen, GREEN, (350, 400, 100, 50))
            self.screen.blit(start_text, (350 + 50 - start_text.get_width() // 2, 400 + 25 - start_text.get_height() // 2))
            
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
            self.screen.blit(success_text, (WINDOW_WIDTH // 2 - success_text.get_width() // 2, 200))
            
            restart_text = self.font.render("再钓一次", True, WHITE)
            pygame.draw.rect(self.screen, GREEN, (350, 400, 100, 50))
            self.screen.blit(restart_text, (350 + 50 - restart_text.get_width() // 2, 400 + 25 - restart_text.get_height() // 2))
            
        elif self.state == GameState.FAILURE:
            # 绘制失败界面
            failure_text = self.font.render("钓鱼失败！", True, BLACK)
            self.screen.blit(failure_text, (WINDOW_WIDTH // 2 - failure_text.get_width() // 2, 200))
            
            restart_text = self.font.render("再试一次", True, WHITE)
            pygame.draw.rect(self.screen, GREEN, (350, 400, 100, 50))
            self.screen.blit(restart_text, (350 + 50 - restart_text.get_width() // 2, 400 + 25 - restart_text.get_height() // 2))
        
        # 更新显示
        pygame.display.flip()

if __name__ == "__main__":
    # 导入math模块（在Fish类中使用）
    import math
    game = FishingGame()
    game.run()
