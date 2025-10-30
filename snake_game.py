#!/usr/bin/env python3
"""
贪吃蛇游戏 - Snake Game
使用pygame库实现的经典贪吃蛇游戏

控制方式:
- 方向键控制蛇的移动
- ESC键退出游戏
- 游戏结束后按任意键重新开始
"""

import pygame
import random
import sys
from enum import Enum

class Direction(Enum):
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)

class Color:
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    DARK_GREEN = (0, 200, 0)

class SnakeGame:
    def __init__(self, width=800, height=600, cell_size=20):
        """初始化游戏"""
        pygame.init()
        
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.grid_width = width // cell_size
        self.grid_height = height // cell_size
        
        # 创建游戏窗口
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("贪吃蛇游戏 - Snake Game")
        
        # 游戏时钟
        self.clock = pygame.time.Clock()
        
        # 字体
        self.font = pygame.font.Font(None, 36)
        self.big_font = pygame.font.Font(None, 72)
        
        # 初始化游戏状态
        self.reset_game()
    
    def reset_game(self):
        """重置游戏状态"""
        # 蛇的初始位置（屏幕中央）
        start_x = self.grid_width // 2
        start_y = self.grid_height // 2
        self.snake = [(start_x, start_y)]
        
        # 蛇的初始方向
        self.direction = Direction.RIGHT
        
        # 生成第一个食物
        self.generate_food()
        
        # 游戏状态
        self.score = 0
        self.game_over = False
    
    def generate_food(self):
        """生成食物"""
        while True:
            x = random.randint(0, self.grid_width - 1)
            y = random.randint(0, self.grid_height - 1)
            if (x, y) not in self.snake:
                self.food = (x, y)
                break
    
    def handle_events(self):
        """处理游戏事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                
                elif self.game_over:
                    # 游戏结束后按任意键重新开始
                    self.reset_game()
                
                else:
                    # 控制蛇的移动方向
                    if event.key == pygame.K_UP and self.direction != Direction.DOWN:
                        self.direction = Direction.UP
                    elif event.key == pygame.K_DOWN and self.direction != Direction.UP:
                        self.direction = Direction.DOWN
                    elif event.key == pygame.K_LEFT and self.direction != Direction.RIGHT:
                        self.direction = Direction.LEFT
                    elif event.key == pygame.K_RIGHT and self.direction != Direction.LEFT:
                        self.direction = Direction.RIGHT
        
        return True
    
    def update(self):
        """更新游戏逻辑"""
        if self.game_over:
            return
        
        # 计算蛇头的新位置
        head_x, head_y = self.snake[0]
        dx, dy = self.direction.value
        new_head = (head_x + dx, head_y + dy)
        
        # 检查碰撞
        if (new_head[0] < 0 or new_head[0] >= self.grid_width or
            new_head[1] < 0 or new_head[1] >= self.grid_height or
            new_head in self.snake):
            self.game_over = True
            return
        
        # 移动蛇
        self.snake.insert(0, new_head)
        
        # 检查是否吃到食物
        if new_head == self.food:
            self.score += 10
            self.generate_food()
        else:
            # 没有吃到食物，移除尾巴
            self.snake.pop()
    
    def draw(self):
        """绘制游戏画面"""
        # 清空屏幕
        self.screen.fill(Color.BLACK)
        
        if not self.game_over:
            # 绘制蛇
            for i, (x, y) in enumerate(self.snake):
                rect = pygame.Rect(x * self.cell_size, y * self.cell_size, 
                                 self.cell_size, self.cell_size)
                # 蛇头用不同颜色
                color = Color.GREEN if i == 0 else Color.DARK_GREEN
                pygame.draw.rect(self.screen, color, rect)
                pygame.draw.rect(self.screen, Color.WHITE, rect, 1)
            
            # 绘制食物
            food_rect = pygame.Rect(self.food[0] * self.cell_size, 
                                  self.food[1] * self.cell_size,
                                  self.cell_size, self.cell_size)
            pygame.draw.rect(self.screen, Color.RED, food_rect)
            
            # 显示分数
            score_text = self.font.render(f"分数: {self.score}", True, Color.WHITE)
            self.screen.blit(score_text, (10, 10))
            
            # 显示长度
            length_text = self.font.render(f"长度: {len(self.snake)}", True, Color.WHITE)
            self.screen.blit(length_text, (10, 50))
        
        else:
            # 游戏结束画面
            game_over_text = self.big_font.render("游戏结束!", True, Color.RED)
            score_text = self.font.render(f"最终分数: {self.score}", True, Color.WHITE)
            length_text = self.font.render(f"最终长度: {len(self.snake)}", True, Color.WHITE)
            restart_text = self.font.render("按任意键重新开始", True, Color.WHITE)
            
            # 居中显示
            game_over_rect = game_over_text.get_rect(center=(self.width//2, self.height//2 - 60))
            score_rect = score_text.get_rect(center=(self.width//2, self.height//2 - 20))
            length_rect = length_text.get_rect(center=(self.width//2, self.height//2 + 20))
            restart_rect = restart_text.get_rect(center=(self.width//2, self.height//2 + 60))
            
            self.screen.blit(game_over_text, game_over_rect)
            self.screen.blit(score_text, score_rect)
            self.screen.blit(length_text, length_rect)
            self.screen.blit(restart_text, restart_rect)
        
        pygame.display.flip()
    
    def run(self):
        """运行游戏主循环"""
        running = True
        
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            
            # 控制游戏速度
            self.clock.tick(10)  # 10 FPS
        
        pygame.quit()
        sys.exit()

def main():
    """主函数"""
    try:
        game = SnakeGame()
        game.run()
    except pygame.error as e:
        print(f"Pygame错误: {e}")
        print("请确保已安装pygame库: pip install pygame")
    except KeyboardInterrupt:
        print("\n游戏被用户中断")
    except Exception as e:
        print(f"游戏运行出错: {e}")

if __name__ == "__main__":
    main()