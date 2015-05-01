import pygame


class GameHandler:
    def handle_input(self, event):
        pass

    def handle_draw(self, canvas):
        pass

    def handle_update(self, dt):
        pass

    # noinspection PyMethodMayBeStatic
    def running(self) -> bool:
        return True


class Game:
    def __init__(self, handler: GameHandler, fps=60, scr_width=960,
                 scr_height=600):
        self._handler = handler
        self._fps = fps
        self._running = False

        pygame.init()

        self._clock = pygame.time.Clock()
        self._screen = pygame.display.set_mode((scr_width, scr_height))

    def start(self):
        self.run()

    def run(self):
        while self._handler.running():
            dt = self._clock.tick(self._fps)
            self.step(dt)

        pygame.quit()

    def step(self, dt):
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
        def running(self):
            return True

        def handle_draw(self, canvas):
            canvas.fill((0, 0, 0xff))

    Game(handler=SimpleGameHandler()).start()
