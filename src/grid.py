import sys
from turtle import color

import numpy as np
import numpy.typing as npt
import pygame

pygame.init()


class Game:
    def __init__(self, rows, cols, cell_size) -> None:
        self.grid: npt.NDArray[np.int8] = np.array(
            [
                [7, 8, 0, 4, 0, 0, 1, 2, 0],
                [6, 0, 0, 0, 7, 5, 0, 0, 9],
                [0, 0, 0, 6, 0, 1, 0, 7, 8],
                [0, 0, 7, 0, 4, 0, 2, 6, 0],
                [0, 0, 1, 0, 5, 0, 9, 3, 0],
                [9, 0, 4, 0, 6, 0, 0, 0, 5],
                [0, 7, 0, 3, 0, 0, 0, 1, 2],
                [1, 2, 0, 0, 0, 7, 4, 0, 0],
                [0, 4, 9, 2, 0, 6, 0, 0, 7],
            ],
            dtype=np.int8,
        )
        self.rows = rows
        self.cols = cols
        self.cell_size = cell_size

        self.temp_grid = np.zeros((9, 9))

        self.rows = rows
        self.cols = cols
        self.cell_size = cell_size

        self.width = rows * self.cell_size
        self.height = cols * self.cell_size

        self.selected_cell = None
        self.solved = False

        self.win: pygame.surface.Surface = pygame.display.set_mode(
            (self.width, self.height)
        )
        pygame.display.set_caption("Sudoku")

        self.grid_font = pygame.font.SysFont("Arial", 40)
        self.temp_key_font = pygame.font.SysFont("Arial", 30)

    def reset(self):
        self.grid = np.array(
            [
                [7, 8, 0, 4, 0, 0, 1, 2, 0],
                [6, 0, 0, 0, 7, 5, 0, 0, 9],
                [0, 0, 0, 6, 0, 1, 0, 7, 8],
                [0, 0, 7, 0, 4, 0, 2, 6, 0],
                [0, 0, 1, 0, 5, 0, 9, 3, 0],
                [9, 0, 4, 0, 6, 0, 0, 0, 5],
                [0, 7, 0, 3, 0, 0, 0, 1, 2],
                [1, 2, 0, 0, 0, 7, 4, 0, 0],
                [0, 4, 9, 2, 0, 6, 0, 0, 7],
            ],
        )
        self.temp_grid = np.zeros((9, 9))
        self.solved = False

    def draw(self):
        self.win.fill((255, 255, 255))
        for row in range(self.rows):
            for col in range(self.cols):
                self.draw_temp((row, col))
                cell_rect = pygame.Rect(
                    col * self.cell_size,
                    row * self.cell_size,
                    self.cell_size,
                    self.cell_size,
                )

                cell_surface = self.grid_font.render(
                    str(self.grid[row, col]), True, (0, 0, 0)
                )
                cell_surface_rect = cell_surface.get_rect(center=cell_rect.center)

                pygame.draw.rect(self.win, (0, 0, 0), cell_rect, width=1)
                if self.grid[row, col] != 0:
                    self.win.blit(cell_surface, cell_surface_rect)

                if row == col and row % 3 == 0 and row != 0:
                    pygame.draw.line(
                        self.win,
                        (0, 0, 0),
                        (0, row * self.cell_size),
                        (self.width, row * self.cell_size),
                        width=5,
                    )
                    pygame.draw.line(
                        self.win,
                        (0, 0, 0),
                        (col * self.cell_size, 0),
                        (col * self.cell_size, self.height),
                        width=5,
                    )
                    self.draw_selected_cell()

    def select_cell(self, pos):
        if pos:
            x, y = pos
            if 0 <= x < self.width and 0 <= y < self.height:
                cell = (y // self.cell_size, x // self.cell_size)
                row, col = cell
                cell_rect = pygame.Rect(
                    col * self.cell_size,
                    row * self.cell_size,
                    self.cell_size,
                    self.cell_size,
                )
                pygame.draw.rect(self.win, (255, 0, 0), cell_rect, width=3)
                self.selected_cell = cell

    def draw_selected_cell(self):
        if self.selected_cell:
            row, col = self.selected_cell
            cell_rect = pygame.Rect(
                col * self.cell_size,
                row * self.cell_size,
                self.cell_size,
                self.cell_size,
            )
            pygame.draw.rect(self.win, (255, 0, 0), cell_rect, width=3)

    def check_valid(self, pos, value):
        row, col = pos
        for i in range(self.cols):
            if self.grid[row, i] == value:
                return False
        for j in range(self.rows):
            if self.grid[j, col] == value:
                return False

        y0 = (row // 3) * 3
        x0 = (col // 3) * 3

        for i in range(0, 3):
            for j in range(0, 3):
                if self.grid[y0 + i, x0 + j] == value:
                    return False
        return True

    def find_next(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.grid[i, j] == 0:
                    return i, j
        return None

    def gui_solve(self):
        pos = self.find_next()
        if pos is None:
            self.solved = True
            return True
        i, j = pos
        for num in range(1, 10):
            if self.check_valid((i, j), num):
                self.grid[i, j] = num

                text_surface = self.grid_font.render(str(num), True, (0, 255, 0))
                text_rect = text_surface.get_rect(
                    center=(
                        j * self.cell_size + self.cell_size / 2,
                        i * self.cell_size + self.cell_size / 2,
                    )
                )
                self.win.blit(text_surface, text_rect)
                pygame.display.update()
                pygame.time.delay(200)
                if self.gui_solve():
                    return True

                text_surface.fill((255, 255, 255))
                self.win.blit(text_surface, text_rect)

                text_surface = self.grid_font.render(str(num), True, (255, 0, 0))
                text_rect = text_surface.get_rect(
                    center=(
                        j * self.cell_size + self.cell_size / 2,
                        i * self.cell_size + self.cell_size / 2,
                    )
                )
                self.win.blit(text_surface, text_rect)
                pygame.display.update()
                pygame.time.delay(200)
                text_surface.fill((255, 255, 255))
                self.win.blit(text_surface, text_rect)

                self.grid[i, j] = 0
        return False

    def set_key(self, key):
        match key:
            case pygame.K_BACKSPACE:
                return 0
            case pygame.K_1 | pygame.K_KP1:
                return 1
            case pygame.K_2 | pygame.K_KP2:
                return 2
            case pygame.K_3 | pygame.K_KP3:
                return 3
            case pygame.K_4 | pygame.K_KP4:
                return 4
            case pygame.K_5 | pygame.K_KP5:
                return 5
            case pygame.K_6 | pygame.K_KP6:
                return 6
            case pygame.K_7 | pygame.K_KP7:
                return 7
            case pygame.K_8 | pygame.K_KP8:
                return 8
            case pygame.K_9 | pygame.K_KP9:
                return 9
            case _:
                return None

    def set_temp(self, key):
        if self.selected_cell is not None and not self.solved:
            row, col = self.selected_cell
            self.temp_grid[row, col] = int(key)

    def draw_temp(self, pos):
        row, col = pos
        if self.temp_grid[row, col] != 0 and self.grid[row, col] == 0:
            temp_surface = self.temp_key_font.render(
                str(int(self.temp_grid[row, col])), True, (0, 10, 90)
            )
            temp_rect = temp_surface.get_rect(
                topleft=(
                    col * self.cell_size + 10,
                    row * self.cell_size + 10,
                )
            )
            self.win.blit(temp_surface, temp_rect)

    def clear_temp(self):
        self.temp_grid = np.zeros((9, 9))


def main():
    clock: pygame.time.Clock = pygame.time.Clock()
    game = Game(9, 9, 100)
    pos = None

    while True:

        clock.tick(60)
        pygame.display.update()

        game.draw()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                game.select_cell(pos)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game.clear_temp()
                    game.gui_solve()
                if event.key == pygame.K_r:
                    game.reset()
                if event.key == pygame.K_DELETE:
                    game.clear_temp()

                key = game.set_key(event.key)
                if key is not None:
                    game.set_temp(key)


if __name__ == "__main__":
    main()
