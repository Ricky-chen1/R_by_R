# menu.py
import pygame

from rank import Leaderboard
from constants import NORMAL_FONT_SIZE, SMALL_FONT_SIZE
from constants import BUTTON_WIDTH, BUTTON_HEIGHT
from constants import WIDTH, HEIGHT, WHITE, BLACK

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont(None, NORMAL_FONT_SIZE)
        self.small_font = pygame.font.SysFont(None, SMALL_FONT_SIZE)
        self.selected_difficulty = 'easy'  # 默认选择easy
        self.background = pygame.image.load("../images/background.png")
        self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))
        self.start_button = None
        self.easy_button = None
        self.normal_button = None

        self.name_input_active = False
        self.player_name = ""

        self.leaderboard = Leaderboard()
        self.leaderboard_button = None

        self.return_button = None  # 添加返回主菜单按钮
        self.exit_button = None # 添加退出游戏按钮

    def draw_button(self, text, center, width, height):
        button_rect = pygame.Rect(0, 0, width, height)
        button_rect.center = center
        pygame.draw.rect(self.screen, WHITE, button_rect, border_radius=10)  # 白色背景
        pygame.draw.rect(self.screen, BLACK, button_rect, 2, border_radius=10)  # 黑色边框

        text_surface = self.small_font.render(text, True, BLACK)
        text_rect = text_surface.get_rect(center=center)
        self.screen.blit(text_surface, text_rect)

        return button_rect

    def draw_name_input(self):
        self.screen.blit(self.background, (0, 0))  # 绘制背景图片
        title = self.font.render("Enter Your Name", True, BLACK)
        title_rect = title.get_rect(center=(WIDTH // 2, HEIGHT // 4))
        self.screen.blit(title, title_rect)

        # 计算输入框的 y 坐标，使其位于标题文本的下方
        input_box_y = title_rect.bottom + 20

        input_box = pygame.Rect(WIDTH // 2 - 150, input_box_y, 300, 50)
        pygame.draw.rect(self.screen, WHITE, input_box, border_radius=10)
        pygame.draw.rect(self.screen, BLACK, input_box, 2, border_radius=10)

        name_surface = self.small_font.render(self.player_name, True, BLACK)
        self.screen.blit(name_surface, (input_box.x + 10, input_box.y + 10))

        self.start_button = self.draw_button("Next", (WIDTH // 2, HEIGHT // 2 + 50), BUTTON_WIDTH, BUTTON_HEIGHT)
        self.return_button = self.draw_button("Back", (WIDTH // 2, HEIGHT // 2 + 200), BUTTON_WIDTH, BUTTON_HEIGHT)

    def draw_main_menu(self):
        self.screen.blit(self.background, (0, 0))  # 绘制背景图片
        title = self.font.render("R by R", True, BLACK)
        title_rect = title.get_rect(center=(WIDTH // 2, HEIGHT // 4 - 50))
        self.screen.blit(title, title_rect)

        self.start_button = self.draw_button("Start Game", (WIDTH // 2, HEIGHT // 2 - 100), BUTTON_WIDTH, BUTTON_HEIGHT)
        self.leaderboard_button = self.draw_button("Rank", (WIDTH // 2, HEIGHT // 2 + 50), BUTTON_WIDTH, BUTTON_HEIGHT)
        self.exit_button = self.draw_button("Exit", (WIDTH // 2, HEIGHT // 2 + 200), BUTTON_WIDTH, BUTTON_HEIGHT)

        pygame.display.flip()

    def draw_leaderboard(self):
        self.screen.blit(self.background, (0, 0))  # 绘制背景图片
        title = self.font.render("Rank", True, BLACK)
        title_rect = title.get_rect(center=(WIDTH // 2, HEIGHT // 4))
        self.screen.blit(title, title_rect)

        top_entries = self.leaderboard.get_top_entries()
        for i, entry in enumerate(top_entries):
            entry_text = f"{i + 1}. {entry['name']} - {entry['time']}s - {entry['difficulty']}"
            entry_surface = self.small_font.render(entry_text, True, BLACK)
            entry_rect = entry_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 + i * 30))
            self.screen.blit(entry_surface, entry_rect)

        self.return_button = self.draw_button("Return to Main Menu", (WIDTH // 2, HEIGHT - 100), BUTTON_WIDTH,
                                              BUTTON_HEIGHT)

        pygame.display.flip()

    def draw_difficulty_menu(self):
        self.screen.blit(self.background, (0, 0))  # 绘制背景图片
        title = self.font.render("Select Difficulty", True, BLACK)
        title_rect = title.get_rect(center=(WIDTH // 2, HEIGHT // 4))
        self.screen.blit(title, title_rect)

        self.easy_button = self.draw_button("Easy", (WIDTH // 2, HEIGHT // 2), BUTTON_WIDTH, BUTTON_HEIGHT)
        self.normal_button = self.draw_button("Normal", (WIDTH // 2, HEIGHT // 2 + 150), BUTTON_WIDTH, BUTTON_HEIGHT)
        self.return_button = self.draw_button("Back", (WIDTH // 2, HEIGHT // 2 + 300), BUTTON_WIDTH, BUTTON_HEIGHT)

        pygame.display.flip()

    def handle_event(self, event, current_state):
        if current_state == 'main_menu':
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.start_button.collidepoint(event.pos):
                    return 'name_input'
                elif self.leaderboard_button.collidepoint(event.pos):
                    return 'leaderboard'
                elif self.exit_button.collidepoint(event.pos):
                    pygame.quit()
                    exit()
        elif current_state == 'name_input':
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return 'difficulty_menu'
                elif event.key == pygame.K_BACKSPACE:
                    self.player_name = self.player_name[:-1]
                else:
                    self.player_name += event.unicode
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.start_button.collidepoint(event.pos):
                    return 'difficulty_menu'
                elif self.return_button.collidepoint(event.pos):
                    return 'main_menu'
        elif current_state == 'difficulty_menu':
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.easy_button.collidepoint(event.pos):
                    self.selected_difficulty = 'easy'
                    return 'playing'
                elif self.normal_button.collidepoint(event.pos):
                    self.selected_difficulty = 'normal'
                    return 'playing'
                elif self.return_button.collidepoint(event.pos):
                    return 'name_input'
        elif current_state == 'leaderboard':
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.return_button.collidepoint(event.pos):
                    return 'main_menu'
        return current_state