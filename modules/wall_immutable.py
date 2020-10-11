from modules import cell as c


class Wall_Immutable(c.Cell):

    def __init__(self, position):
        self._position = position

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, position):
        self._position = position

    def action(self, gamefield, tick_time):
        return

    def is_passable(self, user):
        return False

    @property
    def image_name(self):
        return "Wall_Immutable.png"
