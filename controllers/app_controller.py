from models.maze import Maze
from models.grid_size import GridSize

from controllers.welcome_controller import WelcomeController
from controllers.game_controller import GameController
from controllers.game_over_controller import GameOverController

import pygame
import pygame.locals

from models.player import Player


class App:
    '''Main class for the application. It interacts with Maze model and three controllers:
       WelcomeController
       GameController
       GameOverController'''

    def __init__(self, filename=None):
        """ Call the classmethod to load all students from the CSV """
        self._maze = Maze()
        self._maze._load_all_from_file(filename)
        self._maze.generate_random_spots()
        self._window = pygame.display.set_mode(
            (self._maze.row * GridSize.SIZE, self._maze.col * GridSize.SIZE + GridSize.SIZE))

    @property
    def window(self):
        return self._window

    def run(self):
        """ This is the main method for our application.

        It runs an infinite loop, unless the user decides to quit.
        The `SystemExit` exception is raised by the child controllers.

        """
        pygame.init()
        print(self._maze.locations)
        # window = pygame.display.set_mode(
        #     (self._maze.row * GridSize.SIZE, self._maze.col * GridSize.SIZE + 50))
        clock = pygame.time.Clock()

        welcome_controller = WelcomeController(
            self.window, self._maze.row * GridSize.SIZE, self._maze.col * GridSize.SIZE + GridSize.SIZE, 50)
        # welcome_controller = WelcomeController(window)

        running = False

        welcome_controller.run()
        pygame.display.update()

        # start = False

        # while not start:
        #     start_key=welcome_controller.get_input()
        #     start=(len(start_key)>0)

        # while not start:
        #     key=welcome_controller.get_input()
        #     if key=="q":
        #         pygame.quit()
        #     elif key is not None:
        #         start=True

        welcome_controller.get_input()

        running = True

        # initialize pygame elements
        self._maze.create_player()
        self._maze.create_maze_exit()
        self._maze.create_wall()
        self._maze.create_items()

        # score = 0

        while running:
            pygame.display.update()
            clock.tick(20)
            self.window.fill((0, 0, 0))

            # for event in pygame.event.get():
            #     if event.type == pygame.locals.QUIT:
            #         running = False

            game_controller = GameController(self._maze, self._window)

            game_controller.run()

            if game_controller._view._maze._time_left <= 0:
                running = False

            # if pygame.sprite.spritecollide(self._maze.player, self._maze._maze_items, dokill=True):
            #     self._maze._score += 1

            # # move these to view?
            # self.window.blit(create_text_surface(
            #     f"Score: {self._maze._score}"), (self._maze.row * GridSize.SIZE - GridSize.SIZE * 2, self._maze.col * GridSize.SIZE))
            # self.window.blit(create_text_surface(
            #     f"{pygame.time.get_ticks()} ms"), (0, self._maze.col * GridSize.SIZE))

            # # move these to view?
            # self.window.blit(self._maze.player.image, self._maze.player.rect)
            # self.window.blit(self._maze.maze_exit.image, self._maze.maze_exit.rect)
            # self._maze._wall.draw(self.window)
            # self._maze._maze_items.draw(self.window)

            if pygame.sprite.collide_rect(self._maze.player, self._maze.maze_exit):
                # game over controller will be in here
                # game_over_controller = GameOverController(self.window, self._maze)
                # game_over_controller.run()

                running = False

            #

            # if result:
            #     running = False

        # result can be win or loss

        # game_over_controller = GameOverController(self.window, self._maze)
        # game_over_controller.run()

        # game over controller will be in here
        game_over_controller = GameOverController(self.window, self._maze)
        game_over_controller.run()
        pygame.display.update()

        if game_over_controller._maze_result:
            self._maze.add_name_score()

        while True:
            key = game_over_controller.get_user_input()
            if key == "q":
                pygame.quit()


# better to put this somewhere else


# def create_text_surface(text):
#     openSans = pygame.font.SysFont('open sans', 24)
#     text_surface = openSans.render(text, True, (160, 0, 0))

#     return text_surface
