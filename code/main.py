# main.py
import pygame
from constants import WIDTH, HEIGHT
from menu import Menu
from game import Game
from rank import Leaderboard

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("R了个R")

    # 创建 Menu 实例
    menu = Menu(screen)
    game = None
    rank = Leaderboard()
    game_state = 'main_menu'  # 初始状态

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            game_state = menu.handle_event(event, game_state)
            if game_state == 'playing' and game is None:
                game = Game(screen, menu.selected_difficulty)
            elif game_state == 'playing':
                game.handle_event(event)

        if game_state == 'playing':
            if game.is_game_success():
                rank.add_entry(menu.player_name, game.get_elapsed_time(), menu.selected_difficulty)
                game_state = 'game_success'
            elif game.is_game_over():
                game_state = 'game_over'

        if game_state == 'main_menu':
            menu.draw_main_menu()
        elif game_state == 'name_input':
            menu.draw_name_input()
        elif game_state == 'difficulty_menu':
            menu.draw_difficulty_menu()
        elif game_state == 'playing':
            game.draw()
        elif game_state == 'game_over':
            game.show_game_over_screen(win=False)
            game = None
            game_state = 'main_menu'
        elif game_state == 'game_success':
            game.show_game_over_screen(win=True)
            game = None
            game_state = 'main_menu'
        elif game_state == 'leaderboard':
            menu.draw_leaderboard()

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()