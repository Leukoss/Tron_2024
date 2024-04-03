""" Manage all the features related to the compilation of the program"""

import random
from gui import GUI
from game import Game
from player import Player

# Define the width and height of the grid
WIDTH, HEIGHT = 20, 40

# Initialize the (x,y) for each player
X_PLAYER1, X_PLAYER2 = 0, 0
Y_PLAYER1, Y_PLAYER2 = 0, 0

# Define the (x,y) for each player inside the boundaries and avoid the same
# spawn as it will result by an instant draw
while (X_PLAYER1, Y_PLAYER1) == (X_PLAYER2, Y_PLAYER2):
    X_PLAYER1, X_PLAYER2 = (random.randrange(1, WIDTH - 1),
                            random.randrange(1, WIDTH - 1))
    Y_PLAYER1, Y_PLAYER2 = (random.randrange(1, HEIGHT - 1),
                            random.randrange(1, HEIGHT - 1))

# Create players
PLAYER1 = Player(x=X_PLAYER1, y=Y_PLAYER1)
PLAYER2 = Player(x=X_PLAYER2, y=Y_PLAYER2)

# Create Game and GUI
GAME = Game(width=WIDTH, height=HEIGHT, player_1=PLAYER1, player_2=PLAYER2)
gui = GUI(GAME)

# Initialize GUI components, start the loop and display it
gui.init_gui()
gui.update_game()
gui.window.mainloop()
