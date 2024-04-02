""" Manage all the features related to the compilation of the program"""

from gui import GUI
from game import Game
from player import Player

# Create players
player1 = Player(x=5, y=5)
player2 = Player(x=10, y=30)

# Create Game
game = Game(width=20, height=40, player_1=player1, player_2=player2)

gui = GUI(game)

# Initialize GUI components
gui.init_gui()
gui.get_height_widget()
gui.display()
gui.display_score()

# Display GUI
gui.window.mainloop()
