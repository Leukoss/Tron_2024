""" Manage all the features related to the Player for the Tron Game """


class Player:
    """
    Manage all the features related to the Player.

    Attributes:
        x (int): The position of the player along the x-axis.
        y (int): The position of the player along the y-axis.
        dead (bool): Indicates whether the player is dead or alive.
        score (int): The score of the player, used for decision-making.
    """

    def __init__(self, x: int, y: int, score=0):
        """
        Initialize the Player object
        :param x: position of the player in abs
        :param y: position of the player in ord
        :param score: score of the player to make decision
        """
        self.x = x
        self.y = y
        self.dead = False
        self.score = score

    def apply_move(self, picked_move: tuple[int, int]):
        """
        Apply a movement to the Player
        :picked_move: tuple of integers (i, j) representing the new move, where:
                 - i represents the new position along the x-axis.
                 - j represents the new position along the y-axis.
        """
        self.x += picked_move[0]
        self.y += picked_move[1]
