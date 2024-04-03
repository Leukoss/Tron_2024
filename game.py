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

    def get_allowed_moves(self, player: Player) -> list[tuple[int, int]]:
        """
        Assign the new allowed moves to the player according to its current position
        :param player: of the game
        :return: A tuple of integers (i, j) representing the random move, where:
                 - i represents the change in position along the x-axis.
                 - j represents the change in position along the y-axis.
        """
        allowed_moves = []

        # Up : (0, -1), Down : (0, 1), Right : (1, 0), Left  : (-1, 0)
        possible_moves = [(0, -1), (0, 1), (1, 0), (-1, 0)]

        # For each possible moves, we check the availability of the case
        for dx, dy in possible_moves:
            new_x, new_y = player.x + dx, player.y + dy
            if 1 <= new_x < self.width and 1 <= new_y < self.height and self.grid[new_x, new_y] == 0:
                allowed_moves.append((dx, dy))

        return allowed_moves

    def random_move(self, player: Player) -> tuple[int, int]:
        """
        Assign the new random moves to the player according to its current position
        :param player: of the game
        :return: A tuple of integers (i, j) representing the random move, where:
                 - i represents the change in position along the x-axis.
                 - j represents the change in position along the y-axis.
        """
        allowed_moves = self.get_allowed_moves(player)

        # In case there is no allowed move, we redefine allowed_moves with the default case
        if len(allowed_moves) == 0:
            player.dead=True
            return (0, 0)

        return allowed_moves[random.randrange(len(allowed_moves))]

    def move_players(self, player_1: Player, player_2: Player):
        """
        Apply a movement to all the players based on their allowed moves
        :player_1: a player of the game
        :player_2: a player of the game
        """
        players = [player_1, player_2]
        for i in range(len(players)):
            next_move = self.random_move(players[i])
            print(f"Player {i+1} next move:", next_move)
            print(f"Player {i+1} current position:", players[i].x, players[i].y)
            players[i].apply_move(next_move)
            print(f"Player {i+1} next position:", players[i].x, players[i].y)
            self.grid[players[i].x, players[i].y] = i + 2


    def check_end_game(self, player_1: Player, player_2: Player):
        """
        Check if a player is dead
        :player_1: a player of the game
        :player_2: a player of the game
        """
        #####################################
        #### A adapter si + de 2 joueurs (c'est juste l'idée : utiliser des listes de joueurs) ####
        # players = [player_1, player_2]
        # # number_of_players = len(players)
        # # dead_players = []
        # for player in players:
        #     if player.dead == True:
        #         self.winner=True
        #####################################
        if player_1.dead == True:
            self.winner = 2
        if player_2.dead == True:
            self.winner = 1

        # La fonction n'est pas encore utilisée mais permettra de définir le gagnant
        # Pour le moment le jeu ne s'arrete pas. Simplement les joueurs ne se déplacent plus lorsqu'ils n'ont plus d'options (voir lignes 68-70)