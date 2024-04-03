""" Manage all the features related to the Game for the Tron Game """

import random
import numpy as np
from player import Player


class Game:
    """
    A class for managing the Game of the Tron game.

    Attributes:
        width (int): The width of the game grid.
        height (int): The height of the game grid.
        grid (np.ndarray): A numpy array representing the game grid.
        player_1 (Player): The first player of the game.
        player_2 (Player): The second player of the game.
        winner (int): The id of the winning player, or None if the game is
         ongoing.
    """

    def __init__(self, width: int, height: int, player_1: Player,
                 player_2: Player) -> None:
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
        Initialize the Grid. The borders values are filled with 1 and 0 for the
        remaining ones
        :param x: height of the grid
        :param y: width of the grid
        :return: numpy array
        """
        grid = np.ones((x, y), dtype=np.int8)
        grid[1:-1, 1:-1] = 0

        return grid

    def get_allowed_moves(self, player: Player) -> list[tuple[int, int]]:
        """
        Assign the new allowed moves to the player according to its current
        position
        :param player: of the game
        :return: A tuple of integers (i, j) representing the random move, where:
                 - i represents the change in position along the x-axis.
                 - j represents the change in position along the y-axis.
        """
        x, y = player.x, player.y

        # Up : (0, -1), Down : (0, 1), Right : (1, 0), Left  : (-1, 0)
        possible_moves = [(0, -1), (0, 1), (1, 0), (-1, 0)]

        # Check if the coordinates match an empty case
        allowed_moves = [(dx, dy) for dx, dy in possible_moves
                         if (1 <= x + dx < self.width and
                             1 <= y + dy < self.height and
                             self.grid[x + dx, y + dy] == 0)]

        return allowed_moves

    def random_move(self, player: Player) -> tuple[int, int]:
        """
        Assign the new random moves to the player according to its current
        position
        :param player: of the game
        :return: A tuple of integers (i, j) representing the random move, where:
                 - i represents the change in position along the x-axis.
                 - j represents the change in position along the y-axis.
        """
        allowed_moves = self.get_allowed_moves(player)

        # When the player has no allowed move remaining, it means he is dead
        if len(allowed_moves) == 0:
            player.dead = True
            return 0, 0

        return random.choice(allowed_moves)

    def move_players(self, player_1: Player, player_2: Player):
        """
        Apply a movement to all the players based on their allowed moves
        :player_1: a player of the game
        :player_2: a player of the game
        """
        players = [player_1, player_2]
        for i, player in enumerate(players, start=1):
            next_move = self.random_move(player)
            print(f"Player {i} next move:", next_move)
            print(f"Player {i} current position:", player.x, player.y)
            player.apply_move(next_move)
            print(f"Player {i} next position:", player.x, player.y)
            self.grid[player.x, player.y] = i + 1

    def check_end_game(self, player_1: Player, player_2: Player):
        """
        Check if a player is dead
        :player_1: a player of the game
        :player_2: a player of the game
        """
        if player_1.dead:
            self.winner = 2
        elif player_2.dead:
            self.winner = 1
