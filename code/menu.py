# menu.py
import pygame

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

    def draw_button(self, text, center, width, height):
        button_rect = pygame.Rect(0, 0, width, height)
        button_rect.center = center
        pygame.draw.rect(self.screen, WHITE, button_rect, border_radius=10)  # 白色背景
        pygame.draw.rect(self.screen, BLACK, button_rect, 2, border_radius=10)  # 黑色边框

        text_surface = self.small_font.render(text, True, BLACK)
        text_rect = text_surface.get_rect(center=center)
        self.screen.blit(text_surface, text_rect)

        return button_rect

    def draw_main_menu(self):
        self.screen.blit(self.background, (0, 0))  # 绘制背景图片
        title = self.font.render("R by R", True, BLACK)
        title_rect = title.get_rect(center=(WIDTH // 2, HEIGHT // 4))
        self.screen.blit(title, title_rect)

        self.start_button = self.draw_button("Start Game", (WIDTH // 2, HEIGHT // 2), BUTTON_WIDTH, BUTTON_HEIGHT)

        pygame.display.flip()

    def draw_difficulty_menu(self):
        self.screen.blit(self.background, (0, 0))  # 绘制背景图片
        title = self.font.render("Select Difficulty", True, BLACK)
        title_rect = title.get_rect(center=(WIDTH // 2, HEIGHT // 4))
        self.screen.blit(title, title_rect)

        self.easy_button = self.draw_button("Easy", (WIDTH // 2, HEIGHT // 2), BUTTON_WIDTH, BUTTON_HEIGHT)
        self.normal_button = self.draw_button("Normal", (WIDTH // 2, HEIGHT // 2 + 150), BUTTON_WIDTH, BUTTON_HEIGHT)

        pygame.display.flip()

    def handle_event(self, event, current_state):
        if current_state == 'main_menu':
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.start_button.collidepoint(event.pos):
                    return 'difficulty_menu'
        elif current_state == 'difficulty_menu':
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.easy_button.collidepoint(event.pos):
                    self.selected_difficulty = 'easy'
                    return 'playing'
                elif self.normal_button.collidepoint(event.pos):
                    self.selected_difficulty = 'normal'
                    return 'playing'
        return current_state