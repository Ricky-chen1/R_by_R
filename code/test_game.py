# test/test_game.py
import unittest
import pygame

from game import Game
from menu import Menu
from rank import Leaderboard

class TestGame(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.game = Game(self.screen, 'easy')
        self.menu = Menu(self.screen)
        self.menu.draw_name_input()  # Initialize buttons
        self.leaderboard = Leaderboard()

    def tearDown(self):
        pygame.quit()

    def test_game_initialization(self):
        self.assertEqual(self.game.difficulty, 'easy')
        self.assertFalse(self.game.is_game_success())
        self.assertFalse(self.game.is_game_over())

    def test_menu_initialization(self):
        self.assertEqual(self.menu.selected_difficulty, 'easy')
        self.assertEqual(self.menu.player_name, "")

    def test_leaderboard_initialization(self):
        self.assertIsInstance(self.leaderboard.data, list)

    def test_add_entry_to_leaderboard(self):
        self.leaderboard.clear()
        initial_length = len(self.leaderboard.data)
        self.leaderboard.add_entry('TestPlayer', 120, 'easy')
        self.assertEqual(len(self.leaderboard.data), initial_length + 1)
        self.assertEqual(self.leaderboard.data[-1]['name'], 'TestPlayer')

    def test_menu_handle_event(self):
        event = pygame.event.Event(pygame.MOUSEBUTTONDOWN, pos=(300, 400))
        new_state = self.menu.handle_event(event, 'main_menu')
        self.assertIn(new_state, ['name_input', 'leaderboard', 'main_menu'])

if __name__ == '__main__':
    unittest.main()