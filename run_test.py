#!/usr/bin/env python3
"""
贪吃蛇游戏测试脚本
用于验证游戏是否能正常运行（无头模式测试）
"""

import sys
import os

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """测试导入模块"""
    try:
        import pygame
        print(f"✅ pygame导入成功，版本: {pygame.version.ver}")
        
        # 测试游戏模块导入
        from snake_game import SnakeGame, Direction, Color
        print("✅ 游戏模块导入成功")
        
        return True
    except ImportError as e:
        print(f"❌ 导入失败: {e}")
        return False

def test_game_logic():
    """测试游戏逻辑（无图形界面）"""
    try:
        # 设置环境变量以启用无头模式
        os.environ['SDL_VIDEODRIVER'] = 'dummy'
        
        import pygame
        pygame.init()
        
        from snake_game import SnakeGame, Direction
        
        # 创建游戏实例
        game = SnakeGame(400, 300, 20)
        print("✅ 游戏实例创建成功")
        
        # 测试初始状态
        assert len(game.snake) == 1, "初始蛇长度应为1"
        assert game.score == 0, "初始分数应为0"
        assert not game.game_over, "游戏初始不应结束"
        print("✅ 初始状态检查通过")
        
        # 测试移动逻辑
        initial_head = game.snake[0]
        game.direction = Direction.RIGHT
        game.update()
        
        new_head = game.snake[0]
        assert new_head[0] == initial_head[0] + 1, "向右移动头部x坐标应增加1"
        print("✅ 移动逻辑测试通过")
        
        # 测试边界碰撞
        game.snake = [(game.grid_width - 1, 5)]  # 设置到右边界
        game.direction = Direction.RIGHT
        game.update()
        assert game.game_over, "撞墙应该游戏结束"
        print("✅ 碰撞检测测试通过")
        
        # 测试重置功能
        game.reset_game()
        assert not game.game_over, "重置后游戏不应结束"
        assert game.score == 0, "重置后分数应为0"
        print("✅ 重置功能测试通过")
        
        pygame.quit()
        return True
        
    except Exception as e:
        print(f"❌ 游戏逻辑测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("🧪 开始贪吃蛇游戏测试...")
    print("=" * 40)
    
    # 测试导入
    if not test_imports():
        print("\n❌ 测试失败：无法导入必要模块")
        return False
    
    # 测试游戏逻辑
    if not test_game_logic():
        print("\n❌ 测试失败：游戏逻辑有问题")
        return False
    
    print("\n" + "=" * 40)
    print("🎉 所有测试通过！游戏可以正常运行")
    print("\n运行游戏命令:")
    print("source venv/bin/activate && python snake_game.py")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)