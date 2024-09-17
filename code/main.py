import pygame
from constants import WIDTH, HEIGHT
from menu import Menu
from game import Game

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("R了个R")

    # 创建 Menu 实例
    menu = Menu(screen)
    game = None
    game_state = 'main_menu'  # 初始状态

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # 处理不同状态的事件
            game_state = menu.handle_event(event, game_state)
            if game_state == 'playing' and game is None:
                game = Game(screen, menu.selected_difficulty)
            elif game_state == 'playing':
                game.handle_event(event)

        # 检查游戏状态
        if game_state == 'playing':
            if game.is_game_success():  # 如果游戏成功
                game_state = 'game_success'
            elif game.is_game_over():  # 如果游戏失败
                game_state = 'game_over'

        # 绘制当前状态
        if game_state == 'main_menu':
            menu.draw_main_menu()
        elif game_state == 'difficulty_menu':
            menu.draw_difficulty_menu()
        elif game_state == 'playing':
            game.draw()
        elif game_state == 'game_over':
            game.show_game_over_screen(win=False)
            game = None  # 重置游戏实例
            game_state = 'main_menu'  # 返回主菜单
        elif game_state == 'game_success':
            game.show_game_over_screen(win=True)
            game = None  # 重置游戏实例
            game_state = 'main_menu'  # 返回主菜单

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()