import pygame


class GameHandler:
    def handle_input(self, event):
        raise NotImplementedError

    def handle_draw(self, canvas):
        raise NotImplementedError

    def handle_update(self, dt):
        raise NotImplementedError


class Game:
    def __init__(self, handler, fps=60, scr_width=960, scr_height=600):
        self._handler = handler
        self._fps = fps
        self._running = False

        pygame.init()

        self._clock = pygame.time.Clock()
        self._screen = pygame.display.set_mode((scr_width, scr_height))

    def start(self):
        self.run()

    def run(self):
        self._running = True
        while self._running:
            dt = self._clock.tick(self._fps)
            self.step(dt)

        pygame.quit()

    def step(self, dt):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._running = False
                return
            self._handler.handle_input(event)

        self._handler.handle_update(dt)
        self._handler.handle_draw(self._screen)

        pygame.display.flip()


if __name__ == '__main__':
    class SimpleGameHandler(GameHandler):
        def handle_update(self, dt):
            pass

        def handle_input(self, event):
            pass

        def handle_draw(self, canvas):
            canvas.fill((0, 0, 0xff))

    Game(handler=SimpleGameHandler()).start()
