""" Manage all the features related to the Player """


class Player:
    def __init__(self, x: int, y: int, score=0):
        """
        Initialize the Player object
        :param x: position of the player in abs
        :param y: position of the player in ord
        :param score: score of the player to make decision
        """
        self.x = x
        self.y = y
        self.score = score
