from modules import cell as c, explosion as ex, explosive as exive


class Empty(c.Cell, exive.Explosive):

    def __init__(self, position):
        self._position = position

    @property
    def position(self):
        return self._position

    @position.setter
    def set_position(self, position):
        self._position = position

    def explode(self, gamefield, ex_type, user):
        gamefield[self._position.y][self._position.x] = ex.Explosion(
            self._position, ex_type=ex_type, user=user)

    def should_continue_explode(self, ex_type):
        return True

    @property
    def extra_range(self):
        return 0

    def action(self, gamefield, tick_time):
        return

    def contact(self, user):
        return

    def is_passable(self, user):
        return True

    @property
    def image_name(self):
        return None
