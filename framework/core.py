"""
This module encapsulates simple input-update-draw logic in its Game
class. It is responsible for implementing game window and invoking
handle_input, handle_draw and handle_update methods of provided GameHandler
object in initializer.
"""

# pygame modules are loaded dynamically, thus, supress no name/members errors
# pylint: disable=no-name-in-module
# pylint: disable=no-member
import pygame


class GameHandler:
    """Sort of an abstract class"""

    def handle_input(self, event):
        """Pseudo-abstract method for input"""
        pass

    def handle_draw(self, canvas):
        """Pseudo-abstract method for drawing"""
        pass

    def handle_update(self, delta_time):
        """Pseudo-abstract method for updating"""
        pass

    # noinspection PyMethodMayBeStatic
    # pylint: disable=no-self-use
    def running(self) -> bool:
        """Checks if the game is running"""
        return True


class Game:
    """A class called Game. Enough said."""

    def __init__(self, handler: GameHandler, fps=60, scr_width=960,
                 scr_height=600):
        self._handler = handler
        self._fps = fps
        self._running = False

        pygame.init()

        self._clock = pygame.time.Clock()
        self._screen = pygame.display.set_mode((scr_width, scr_height))

    def start(self):
        """Method responsible for starting the game."""
        self.run()

    def run(self):
        """Method responsible for keeping the game alive"""
        while self._handler.running():
            delta_time = self._clock.tick(self._fps) * 1e-3
            self.step(delta_time)

        pygame.quit()

    def step(self, delta_time):
        """Using handler methods"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                import sys

                sys.exit()

            self._handler.handle_input(event)

        self._handler.handle_update(delta_time)
        self._handler.handle_draw(self._screen)

        pygame.display.flip()


if __name__ == '__main__':
    class SimpleGameHandler(GameHandler):
        """A test handler"""

        def running(self):
            """Checks if the game is running."""
            return True

        def handle_draw(self, canvas):
            """Fills the screen with green (it rhymes)."""
            canvas.fill((0, 0, 0xff))

    Game(handler=SimpleGameHandler()).start()
