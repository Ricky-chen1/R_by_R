# menu.py
import pygame
from constants import BLACK, WHITE, WIDTH, HEIGHT

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 100)
        self.button_font = pygame.font.Font(None, 50)
        self.button_start_rect = None
        self.background = pygame.image.load('../images/background.png')

    def draw(self):
        # Fill the background
        self.screen.blit(self.background, (0, 0))

        # Define button properties
        button_width = 400
        button_height = 100
        self.button_start_rect = pygame.Rect(
            (WIDTH - button_width) // 2,  # Center the button horizontally
            (HEIGHT - button_height) // 2,  # Center the button vertically
            button_width,
            button_height
        )

        # Draw the button with rounded corners
        pygame.draw.rect(self.screen, WHITE, self.button_start_rect, border_radius=20)

        # Add a border to the button for better styling
        pygame.draw.rect(self.screen, BLACK, self.button_start_rect, width=3, border_radius=20)

        # Render the button text and center it
        button_text = self.button_font.render("Game Start", True, BLACK)
        text_rect = button_text.get_rect(center=self.button_start_rect.center)
        self.screen.blit(button_text, text_rect)

    def handle_event(self, event):
        # Handle mouse button click
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            # Check if the button is clicked
            if self.button_start_rect.collidepoint(mouse_x, mouse_y):
                return 'playing'  # Switch to the game state
        return 'menu'
