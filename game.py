""" Manage all the features related to the Game for the Tron Game """

import random
import numpy as np
from queue import Queue
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
        self.player_1 = player_1
        self.player_2 = player_2
        self.grid = self.init_grid(self.width, self.height, player_1, player_2)
        self.winner = None

    @staticmethod
    def init_grid(x: int, y: int, player_1: Player, player_2: Player) -> np.ndarray:
        """
        Initialize the Grid. The borders values are filled with 1 and 0 for the
        remaining ones
        :param x: height of the grid
        :param y: width of the grid
        :return: numpy array
        """
        grid = np.ones((x, y), dtype=np.int8)*(-1)
        grid[1:-1, 1:-1] = 0
        grid[player_1.x, player_1.y] = 1
        grid[player_2.x, player_2.y] = 2

        return grid

    @staticmethod
    def is_path_between_players(grid: np.array, player_1: Player,
                                player_2: Player) -> bool:
        """
        Check if a path is available between two players through BFS algorithm
        :param grid: numpy array with obstacles and empty case
        :param player_1: of the game
        :param player_2: of the game
        :return: the truth of "there is a path between the players"
        """
        # Initialize visited array to keep track of visited cells
        visited = np.zeros_like(grid, dtype=bool)

        def dfs(x: int, y: int):
            visited[x, y] = True

            if (x, y) == (player_2.x, player_2.y):
                return True

            for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
                new_x, new_y = x + dx, y + dy
                if grid[x, y] == 0 and not visited[new_x, new_y]:
                    dfs(new_x, new_y)

            return False

        return dfs(player_1.x, player_1.y)

    @staticmethod
    def count_free_spaces(grid: np.array, player: Player) -> int:
        """
        Count the number of free spaces for a player enclosed
        :param grid: of the game
        :param player: of the game
        :return: int of free cases for the player
        """
        # Initialize visited array to keep track of visited cells
        visited = np.zeros_like(grid, dtype=bool)

        # Initialize a queue for BFS
        queue = Queue()
        queue.put((player.x, player.y))

        free_spaces = 0

        # Perform BFS
        while not queue.empty():
            x, y = queue.get()

            # If the current cell is already visited, continue to the next cell
            if visited[x, y]:
                continue

            visited[x, y] = True

            # Increment the count of free spaces
            free_spaces += 1

            # Check adjacent cells
            for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
                new_x, new_y = x + dx, y + dy
                if ((1 <= new_x < grid.shape[0] - 1 and
                    1 <= new_y < grid.shape[1] - 1 and
                    grid[new_x, new_y] == 0) and
                        not visited[new_x, new_y]):
                    queue.put((new_x, new_y))

        return free_spaces

    def evaluate_board(self, grid: np.array, player_1: Player,
                       player_2: Player) -> int:
        """
        Evaluate the board bases on the player_1 (if player 2 loses, points are
        increasing, while decreasing when player 2 wins)
        :param grid: board of the game to evaluate
        :param player_1: player evaluated
        :param player_2: player to define the scoring for player_1
        :return: score_board of the game for player_1
        """
        score_board = 0

        # If the opponent has won
        if player_1.dead and not player_2.dead:
            score_board -= 100
            # Lose even more points if the player has been killed by the other player
            if self.got_killed_by_other_player(player_1):
                score_board -= 500
            # If the player has won
        elif not player_1.dead and player_2.dead:
            score_board += 100
            # Win even more points if the player killed the other player
            if self.got_killed_by_other_player(player_2):
                score_board += 500
        # In case of a draw (both dead)
        if player_1.dead and player_2.dead:
            score_board -= 50


        # If both players have a wall to separate them
        if not self.is_path_between_players(grid, player_1, player_2):
            # We retrieve the number of cases available for each
            player_1_cases = self.count_free_spaces(grid, player_1)
            player_2_cases = self.count_free_spaces(grid, player_2)

            # If player_1 has more mobility then he earns points
            if player_1_cases > player_2_cases:
                score_board += 25 * player_1_cases
            elif player_2_cases > player_1_cases:
                score_board -= 25 * player_2_cases
            elif player_1_cases == player_2_cases:
                score_board -= 50

        return score_board

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

    def got_killed_by_other_player(self, player: Player) -> bool:
        """
        Check if the player has been killed by the other player
        :param player: of the game
        :return: the truth of "the player has been killed by the other player"
        """
        killed_by_other = False
        allowed_moves = self.get_allowed_moves(player)
        if len(allowed_moves) != 0:
            return killed_by_other

        for move in [(0, -1), (0, 1), (1, 0), (-1, 0)]:
            player.apply_move(move)
            # If one at least one of the neighbor cell is the other player's wall
            if self.grid[player.x, player.y] > 0 and self.grid[player.x, player.y] != player.number:
                killed_by_other = True
            player.undo_move(move)

        return killed_by_other


    def move_players(self, player_1: Player, player_2: Player) -> None:
        """
        Apply a movement to all the players based on their allowed moves
        :player_1: a player of the game
        :player_2: a player of the game
        """
        players = [player_1, player_2]

        for i, player in enumerate(players, start=1):
            player_max = player
            player_min = [player for player in players
                          if player != player_max][0]

            _, next_move = self.minimax(depth=7,
                                        maximizing_player=player_max,
                                        minimizing_player=player_min,
                                        alpha=float('-inf'),
                                        beta=float('inf'),
                                        maximizing_player_1=True,
                                        )

            print(f'Player {i} next move :', next_move)
            print(f'Player {i} current position :', player.x, player.y)
            player_max.apply_move(next_move)
            print(f'Player {i} next position :', player.x, player.y)
            self.grid[player_max.x, player_max.y] = i

    def check_end_game(self, player_1: Player, player_2: Player) -> None:
        """
        Check if a player is dead
        :player_1: a player of the game
        :player_2: a player of the game
        """
        if player_1.dead:
            self.winner = player_2
        elif player_2.dead:
            self.winner = player_1

    def check_alive(self, player: Player) -> None:
        """
        Check if a player is alive (in other terms, the player can still move)
        :param player: of the Game
        """
        if len(self.get_allowed_moves(player)) == 0:
            player.dead = True

    def minimax(self, depth: int, maximizing_player: Player,
                minimizing_player: Player, alpha: float, beta: float, maximizing_player_1=True) \
            -> tuple[int, tuple[int, int]]:
        """
        Use the minimax algorithm to explore a tree and select the best output
        :param depth: of the tree for the minimax algorithm
        :param maximizing_player: player to maximize the score
        :param minimizing_player: player to minimize the score
        :param maximizing_player_1: maximize the score of the player 1
        :param alpha: the best score for the maximizing player
        :param beta: the best score for the minimizing player
        :return: tuple of integer and tuple of integers (a, (i, j)) representing
         the best move, where:
                 - a represent the score_board of the current state
                 - i represents the new position along the x-axis
                 - j represents the new position along the y-axis
        """
        # We check if the players should be alive or not
        self.check_alive(maximizing_player)
        self.check_alive(minimizing_player)
        # As we use this function recursively, we need to check the end game
        # condition. It will change 'winner' attribute if the game is over
        self.check_end_game(maximizing_player, minimizing_player)

        # We define the base case when the max depth is reached/game is over
        if depth == 0 or self.winner is not None:
            return self.evaluate_board(self.grid, maximizing_player,
                                       minimizing_player), (0, 0)

        best_move = None

        # In the case we need to maximize the score of the maximizing_player
        if maximizing_player_1:
            # As we maximize, we start from -inf
            best_score = float('-inf')

            # We retrieve all the possible moves
            possible_moves = self.get_allowed_moves(maximizing_player)

            # We explore the nodes from the current state
            for move in possible_moves:
                # We assign a new position to the maximizing_player
                maximizing_player.apply_move(move)

                score, _ = self.minimax(depth - 1, maximizing_player,
                                        minimizing_player,
                                        alpha, beta,
                                        not maximizing_player_1)

                # We assign the oldest position to the maximizing_player to
                # explore the other branch
                maximizing_player.undo_move(move)

                # In case the score is superior to the best one we keep it
                if score > best_score:
                    best_score = score
                    best_move = move

                # Update alpha
                alpha = max(alpha, score)
                # Prune the branch if beta <= alpha
                if beta <= alpha:
                    break

        # In the case we need to minimize the score of the minimizing_player
        else:
            # As we minimize, we start from inf
            best_score = float('inf')

            # We retrieve all the possible moves
            possible_moves = self.get_allowed_moves(minimizing_player)

            # We explore the nodes from the current state
            for move in possible_moves:
                # We assign a new position to the minimizing_player
                minimizing_player.apply_move(move)

                # We generate the score for this new branch
                score, _ = self.minimax(depth - 1,
                                        maximizing_player,
                                        minimizing_player,
                                        alpha, beta,
                                        not maximizing_player_1)

                # We assign the oldest position to the minimizing_player to
                # explore the other branch
                minimizing_player.undo_move(move)

                # In case the score is inferior to the best one we keep it
                if score < best_score:
                    best_score = score
                    best_move = move

                # Update beta
                beta = min(beta, score)
                # Prune the branch if beta <= alpha
                if beta <= alpha:
                    break

        return best_score, best_move
