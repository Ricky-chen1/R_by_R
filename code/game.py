# game.py
import pygame
import random
from constants import BG_COLOR, ROWS, COLS, TILE_SIZE, WIDTH, HEIGHT

class Game:
    def __init__(self, screen):
        self.screen = screen
        # 加载并缩放游戏图案，消除背景
        self.patterns = [pygame.image.load(f"../images/animal_{i}.png").convert_alpha() for i in range(1, 7)]
        for pattern in self.patterns:
            pattern.set_colorkey((255, 255, 255))  # 假设白色背景需要消除
        self.patterns = [pygame.transform.scale(p, (TILE_SIZE, TILE_SIZE)) for p in self.patterns]

        # 为每个图案创建掩码
        self.masks = [pygame.mask.from_surface(pattern) for pattern in self.patterns]

        # 初始化游戏板（随机堆叠的卡片）
        self.board_layers = self.create_stacked_board()

        # 初始化卡槽（最大5个槽位）
        self.card_slot = [None] * 6  # 用于保存选中图案的卡槽列表

        # 加载并缩放背景图片以填满屏幕
        self.background = pygame.image.load("../images/background.png")
        self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))

        # 计算偏移量以居中游戏网格
        self.grid_offset_x = (WIDTH - (COLS * TILE_SIZE)) // 2
        self.grid_offset_y = (HEIGHT - (ROWS * TILE_SIZE)) // 2

        # 定义卡槽位置
        self.card_slot_rect = pygame.Rect(50, HEIGHT - 150, WIDTH - 100, 100)  # 位置在屏幕底部

        # 初始化倒计时
        self.time_limit = 120  # 倒计时时间，单位为秒
        self.start_ticks = pygame.time.get_ticks()

        # 加载成功和失败的背景图片
        self.success_background = pygame.image.load("../images/background.png")
        self.success_background = pygame.transform.scale(self.success_background, (WIDTH, HEIGHT))
        self.failure_background = pygame.image.load("../images/background.png")
        self.failure_background = pygame.transform.scale(self.failure_background, (WIDTH, HEIGHT))

    def reset(self):
        # 加载并缩放游戏图案，消除背景
        self.patterns = [pygame.image.load(f"../data/animal_{i}.png").convert_alpha() for i in range(1, 7)]
        for pattern in self.patterns:
            pattern.set_colorkey((255, 255, 255))  # 假设白色背景需要消除
        self.patterns = [pygame.transform.scale(p, (TILE_SIZE, TILE_SIZE)) for p in self.patterns]

        # 为每个图案创建掩码
        self.masks = [pygame.mask.from_surface(pattern) for pattern in self.patterns]

        # 初始化游戏板（随机堆叠的卡片）
        self.board_layers = self.create_stacked_board()

        # 初始化卡槽（最大5个槽位）
        self.card_slot = [None] * 6  # 用于保存选中图案的卡槽列表

        # 加载并缩放背景图片以填满屏幕
        self.background = pygame.image.load("../images/background.png")
        self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))

        # 计算偏移量以居中游戏网格
        self.grid_offset_x = (WIDTH - (COLS * TILE_SIZE)) // 2
        self.grid_offset_y = (HEIGHT - (ROWS * TILE_SIZE)) // 2

        # 定义卡槽位置
        self.card_slot_rect = pygame.Rect(50, HEIGHT - 150, WIDTH - 100, 100)  # 位置在屏幕底部

        # 初始化倒计时
        self.time_limit = 120  # 倒计时时间，单位为秒
        self.start_ticks = pygame.time.get_ticks()

    def create_stacked_board(self):
        num_tiles = ROWS * COLS
        available_patterns = self.patterns * (num_tiles // len(self.patterns))  # 创建足够多的卡牌图案
        random.shuffle(available_patterns)  # 打乱图案顺序

        board_layers = [[[] for _ in range(COLS)] for _ in range(ROWS)]

        for _ in range(ROWS * COLS * 2):  # 为每个格子生成图案
            row = random.randint(0, ROWS - 1)
            col = random.randint(0, COLS - 1)
            if len(board_layers[row][col]) < 3 and available_patterns:
                pattern = available_patterns.pop()  # 每次取出一个图案
                board_layers[row][col].append((pattern, random.randint(-10, 10), random.randint(-10, 10)))  # 增大偏移量

        return board_layers

    def is_tile_covered(self, row, col):
        # 获取当前图案的掩码和位置
        current_tile = self.board_layers[row][col][-1]
        current_mask = pygame.mask.from_surface(current_tile[0])
        current_pos = (self.grid_offset_x + col * TILE_SIZE + current_tile[1],
                       self.grid_offset_y + row * TILE_SIZE + current_tile[2])

        # 检查是否被上层图案遮挡
        for r in range(row + 1, ROWS):
            for c in range(COLS):
                if self.board_layers[r][c]:
                    for tile in self.board_layers[r][c]:
                        tile_mask = pygame.mask.from_surface(tile[0])
                        tile_pos = (self.grid_offset_x + c * TILE_SIZE + tile[1],
                                    self.grid_offset_y + r * TILE_SIZE + tile[2])
                        offset = (current_pos[0] - tile_pos[0], current_pos[1] - tile_pos[1])
                        if tile_mask.overlap(current_mask, offset):
                            return True
        return False

    def draw(self):
        # 填充背景并绘制游戏元素
        self.screen.blit(self.background, (0, 0))
        self.draw_game()
        self.draw_card_slot()  # 绘制卡槽
        self.draw_timer()  # 绘制倒计时

    def is_game_over(self):
        # 检查是否有卡槽已满且没有匹配项
        return all(slot is not None for slot in self.card_slot) and not self.check_three_in_a_row()

    def game_over(self, win=False):
        self.show_game_over_screen(win)  # 显示结束界面
        pygame.quit()
        exit()

    def handle_event(self, event):
        # 处理游戏相关事件
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            # 调整鼠标坐标相对于网格的位置
            col = (mouse_x - self.grid_offset_x) // TILE_SIZE
            row = (mouse_y - self.grid_offset_y) // TILE_SIZE

            # 确保点击在网格范围内
            if 0 <= row < ROWS and 0 <= col < COLS:
                # 只能选择最上层且未被遮挡的卡片
                if self.board_layers[row][col] and not self.is_tile_covered(row, col):
                    # 将点击的图案加入卡槽
                    self.add_to_card_slot(self.board_layers[row][col][-1][0])
                    # 从网格中移除选中的图案
                    self.board_layers[row][col].pop()

    def add_to_card_slot(self, tile):
        # 将图案添加到第一个可用槽位
        for i in range(len(self.card_slot)):
            if self.card_slot[i] is None:
                self.card_slot[i] = tile
                break
        else:
            # 如果卡槽已满且没有匹配项，则游戏结束
            if not self.check_three_in_a_row():
                self.game_over(win=False)
                return

        # 检查是否有三个相同的图案
        if self.check_three_in_a_row():
            if self.is_game_success():
                self.game_over(win=True)

    def is_game_success(self):
        # 检查是否赢得游戏（时间限制内并且消除完所有图案）
        elapsed_time = (pygame.time.get_ticks() - self.start_ticks) / 1000
        if elapsed_time <= self.time_limit:
            for row in range(ROWS):
                for col in range(COLS):
                    if self.board_layers[row][col]:  # 还有卡片未被清除
                        return False
            return True  # 所有卡片已被清除
        return False

    def check_three_in_a_row(self):
        # 检查卡槽中是否有三个相同的图案
        tile_count = {}
        for tile in self.card_slot:
            if tile is not None:
                if tile in tile_count:
                    tile_count[tile] += 1
                else:
                    tile_count[tile] = 1

        for tile, count in tile_count.items():
            if count >= 3:
                # 消除这三个匹配项
                removed = 0
                for i in range(len(self.card_slot)):
                    if self.card_slot[i] == tile:
                        self.card_slot[i] = None
                        removed += 1
                        if removed == 3:
                            break
                return True
        return False

    def draw_game(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        hovered_tile = None  # 用于记录当前悬停的卡牌

        for row in range(ROWS):
            for col in range(COLS):
                for tile, offset_x, offset_y in self.board_layers[row][col]:
                    x = self.grid_offset_x + col * TILE_SIZE + offset_x
                    y = self.grid_offset_y + row * TILE_SIZE + offset_y
                    tile_rect = tile.get_rect(topleft=(x, y))

                    if tile_rect.collidepoint(mouse_x, mouse_y) and not hovered_tile:
                        hovered_tile = tile_rect
                        # 悬停时给卡牌加上黄色边框
                        pygame.draw.rect(self.screen, (255, 255, 0), tile_rect, 3)

                    self.screen.blit(tile, (x, y))  # 显示卡牌

    def draw_card_slot(self):
        # 绘制卡槽背景的阴影
        shadow_offset = 5
        shadow_rect = self.card_slot_rect.copy()
        shadow_rect.x += shadow_offset
        shadow_rect.y += shadow_offset
        pygame.draw.rect(self.screen, (30, 30, 30), shadow_rect, border_radius=10)  # 深色阴影

        # 绘制带圆角的卡槽背景
        pygame.draw.rect(self.screen, (255, 255, 255), self.card_slot_rect, border_radius=10)  # 白色背景
        pygame.draw.rect(self.screen, (0, 200, 0), self.card_slot_rect, 2, border_radius=10)  # 绿色边框

        # 在卡槽区域内绘制每个单独的槽位
        slot_width = self.card_slot_rect.width // len(self.card_slot)  # 每个槽位的宽度
        slot_padding = 10
        for i in range(len(self.card_slot)):
            # 绘制每个槽位的阴影
            slot_x = self.card_slot_rect.x + i * slot_width + slot_padding
            slot_y = self.card_slot_rect.y + slot_padding
            slot_rect = pygame.Rect(slot_x, slot_y, slot_width - slot_padding * 2,
                                    self.card_slot_rect.height - slot_padding * 2)

            slot_shadow_rect = slot_rect.copy()
            slot_shadow_rect.x += shadow_offset // 2
            slot_shadow_rect.y += shadow_offset // 2
            pygame.draw.rect(self.screen, (30, 30, 30), slot_shadow_rect, border_radius=5)  # 深色阴影

            # 绘制槽位的背景
            pygame.draw.rect(self.screen, (200, 200, 200), slot_rect, border_radius=5)  # 浅灰色背景
            pygame.draw.rect(self.screen, (0, 0, 0), slot_rect, 2, border_radius=5)  # 黑色边框

            # 在槽位中绘制图案
            if self.card_slot[i] is not None:
                tile_rect = self.card_slot[i].get_rect(center=slot_rect.center)
                self.screen.blit(self.card_slot[i], tile_rect.topleft)

    def draw_timer(self):
        # 计算剩余时间
        elapsed_time = (pygame.time.get_ticks() - self.start_ticks) / 1000
        remaining_time = max(0, self.time_limit - int(elapsed_time))

        # 设置字体和大小
        font = pygame.font.SysFont(None, 48)
        timer_text = font.render(f"Time: {remaining_time}", True, (255, 0, 0))

        # 绘制计时器文本
        self.screen.blit(timer_text, (WIDTH - 200, 50))

        # 检查时间是否耗尽
        if remaining_time <= 0:
            if not self.is_game_success():
                self.game_over(win=False)

    def show_game_over_screen(self, win):
        # 显示成功或失败的背景图片
        if win:
            self.screen.blit(self.success_background, (0, 0))
            text = "You Win!"
            color = (0, 255, 0)  # 绿色
        else:
            self.screen.blit(self.failure_background, (0, 0))
            text = "Game Over"
            color = (255, 0, 0)  # 红色

        # 定义字体和颜色
        font = pygame.font.SysFont(None, 74)
        text_surface = font.render(text, True, color)

        # 计算文本位置
        text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.screen.blit(text_surface, text_rect)
        pygame.display.flip()
        pygame.time.wait(3000)  # 等待3秒