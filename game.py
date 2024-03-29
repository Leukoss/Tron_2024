""" Manage all the features related to the Game """


class Game:
    def __init__(self, Width, Height, Player1, Player2):
        self.Grid = self.init_grid(Width, Height)
        self.player1 = Player1
        self.player2 = Player2

    def init_grid(self, x, y) -> list:
        """
        Initialize the Grid
        :param x: height of the grid (int)
        :param y: width of the grid (int)
        :return: list of 0 except for the borders (width * height)
        """
        self.Grid = [[1 if i == 0 or i == y - 1 or j == 0 or j == x - 1
                      else 0 for j in range(x)] for i in range(y)]
