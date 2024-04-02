""" Manage all the features related to the Graphical User Interface (GUI)"""

import tkinter as tk
from game import Game


class GUI:
    def __init__(self, game: Game, pixel_length=20) -> None:
        """
        Initialize the GUI
        :param game: instance of Game class
        :param pixel_length: length of a single pixel
        """
        self.game = game
        self.pixel_length = pixel_length
        self.width, self.height = game.width, game.height
        self.width_pixel, self.height_pixel = self.width * self.pixel_length, self.height * self.pixel_length
        self.dict_pages, self.current_page = {}, 0
        self.window = None
        self.frame = None
        self.canvas = None
        self.widget_height = None

    def create_page(self, id_page: int, frame: tk.Frame) -> tk.Frame:
        """
        Create a new page with the given id
        :param id_page: of the new page
        :param frame: among all frames
        :return: a new page
        """
        frame_page = tk.Frame(frame)
        self.dict_pages[id_page] = frame_page
        frame_page.grid(row=0, column=0, sticky="nsew")
        return frame_page

    def display_page(self, id_page: int) -> None:
        """
        Display the selected page
        :param id_page: index of the page to display
        :return: None
        """
        self.current_page = id_page
        self.dict_pages[id_page].tkraise()

    def init_gui(self) -> None:
        """
        Initialize the main window using Tkinter
        """
        # Define the attribute of the window
        self.window = tk.Tk()
        self.window.geometry(str(self.width_pixel) + "x" + str(self.height_pixel))
        self.window.title("Tron Game")

        # Creation of the frame stocking all the pages
        self.frame = tk.Frame(self.window)
        self.frame.pack(side="top", fill="both", expand=True)
        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)

        # Initialize the first page
        frame_0 = self.create_page(id_page=0, frame=self.frame)

        self.canvas = tk.Canvas(frame_0, width=self.width_pixel, height=self.height_pixel, bg="Black")
        self.canvas.place(x=0, y=0)

    def draw_case(self, x: int, y: int, color: str) -> None:
        """
        Define the case to color according to the parameters
        :param x: abs position of the case
        :param y: ord position of the case
        :param color: of the case (change according to the player, wall, ...)
        """
        x *= self.pixel_length
        y *= self.pixel_length
        self.canvas.create_rectangle(x, y, x + self.pixel_length, y + self.pixel_length, fill=color)

    def get_height_widget(self) -> None:
        """
        Assign the height of the widget in pixels
        """
        self.widget_height = self.canvas.winfo_height()

    def display(self) -> None:
        """
        Display the map with walls (from both map and players) and players motorbike
        """
        self.canvas.delete("all")

        # Display the map
        for x in range(self.width):
            for y in range(self.height):
                # Wall from the map
                if self.game.grid[x, y] == 1:
                    self.draw_case(x, y, "gray")
                # Wall from the player 1
                elif self.game.grid[x, y] == 2:
                    self.draw_case(x, y, "orange")
                # Wall from the player 2
                elif self.game.grid[x, y] == 3:
                    self.draw_case(x, y, "green")

        # Display both players
        self.draw_case(self.game.player_1.x, self.game.player_1.y, "red")
        self.draw_case(self.game.player_2.x, self.game.player_2.y, "blue")

    def display_score(self) -> None:
        """
        Display the score of both players
        """
        info_1 = f"SCORE PLAYER 1 : {self.game.player_1.score}"
        info_2 = f"SCORE PLAYER 2 : {self.game.player_2.score}"

        self.canvas.create_text(80, 13, font='Helvetica 12 bold', fill='red', text=info_1)
        self.canvas.create_text(300, 13, font='Helvetica 12 bold', fill='blue', text=info_2)
