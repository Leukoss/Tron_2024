""" Manage all the features related to the Game """

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

