"""Animation"""
# pylint: disable=no-member

# pylint: disable-msg=E0611
# this one is for the two imports below
from pygame.rect import Rect
from pygame.surface import Surface


class Animation:
    """Animation class"""
    colorkey = (0xff, 0xff, 0)

    def __init__(self, surface: Surface, rows, cols,
                 frame_time=.1):
        self.surface = surface

        self.rows = rows
        self.cols = cols

        self.frame_width = surface.get_width() / rows
        self.frame_height = surface.get_height() / cols

        self.row = 0
        self._col = 0

        self.frame_time = frame_time
        self.time = 0

        self.image = Surface((self.frame_width, self.frame_height))
        self.image.set_colorkey(Animation.colorkey)

        self.valid = False

    def update_image(self):
        """Updates image"""
        area = Rect(self.row * self.frame_width,
                    self._col * self.frame_height,
                    0, 0)
        area.x = self.row * self.frame_width
        area.y = self._col * self.frame_height
        area.width = area.x + self.frame_width
        area.height = area.y + self.frame_height

        self.image.fill(Animation.colorkey)
        self.image.blit(self.surface, (0, 0), area)

        self.valid = True

    def update(self, delta_time):
        """Updates"""
        self.time += delta_time

        old_row = self.row
        self.row = int(self.time / self.frame_time) % self.rows

        if old_row != self.row or not self.valid:
            self.update_image()

    def reset(self):
        """Resets"""
        self.row = 0
        self._col = 0
        self.time = 0
        self.valid = False

    @property
    def col(self):
        """Returns col"""
        return self._col

    @col.setter
    def col(self, value):
        """Sets column"""
        self._col = value
        self.valid = False
