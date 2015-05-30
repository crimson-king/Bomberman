import pygame


class GameHandler:
    """Sort of an abstract class"""
    def handle_input(self, event):
        """Pseudo-abstract method for input"""
        pass

    def handle_draw(self, canvas):
        """Pseudo-abstract method for drawing"""
        pass

    def handle_update(self, dt):
        """Pseudo-abstract method for updating"""
        pass

    # noinspection PyMethodMayBeStatic
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
            dt = self._clock.tick(self._fps) * 1e-3
            self.step(dt)

        pygame.quit()

    def step(self, dt):
        """Using handler methods"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                import sys
                sys.exit()

            self._handler.handle_input(event)

        self._handler.handle_update(dt)
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
