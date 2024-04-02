""" Manage all the features related to the Game """

import random
import numpy as np
from player import Player


class Game:
    def __init__(self, width: int, height: int, player_1: Player, player_2: Player) -> None:
        """
        :param width: to define the width of the grid
        :param height: to define the height of the grid
        :param player_1: play the game as player 1
        :param player_2: play the game as player 2
        """
        self.width, self.height = width, height
        self.grid = self.init_grid(self.width, self.height)
        self.player_1 = player_1
        self.player_2 = player_2
        self.winner = None

    @staticmethod
    def init_grid(x: int, y: int) -> np.ndarray:
        """
        Initialize the Grid. The borders values are filled with 1 and 0 for the remaining ones
        :param x: height of the grid
        :param y: width of the grid
        :return: numpy array
        """
        grid = [[1 if i == 0 or i == y - 1 or j == 0 or j == x - 1 else 0 for j in range(x)] for i in range(y)]
        grid = np.array(grid, dtype=np.int8)
        grid = np.flip(grid, axis=0).transpose()

        return grid

    def allowed_move(self, player: Player) -> list[tuple[int, int]]:
        """
        Assign the new allowed moves to the player according to its current position
        :param player: of the game
        :return: A tuple of integers (i, j) representing the random move, where:
                 - i represents the change in position along the x-axis.
                 - j represents the change in position along the y-axis.
        """
        allowed_move = []

        # Up : (0, -1), Down : (0, 1), Right : (1, 0), Left  : (-1, 0)
        possible_moves = [(0, -1), (0, 1), (1, 0), (-1, 0)]

        # For each possible moves, we check the availability of the case
        for dx, dy in possible_moves:
            new_x, new_y = player.x + dx, player.y + dy
            if self.grid[new_x][new_y] == 0:
                allowed_move.append((new_x, new_y))

        return allowed_move

    def random_move(self, player: Player) -> tuple[int, int]:
        """
        Assign the new random moves to the player according to its current position
        :param player: of the game
        :return: A tuple of integers (i, j) representing the random move, where:
                 - i represents the change in position along the x-axis.
                 - j represents the change in position along the y-axis.
        """
        allowed_move = self.allowed_move(player)

        # In case there is no allowed move, we redefine allowed_move with the default case
        if len(allowed_move) == 0:
            allowed_move = [(0, -1), (0, 1), (1, 0), (-1, 0)]

        return allowed_move[random.randrange(len(allowed_move))]
