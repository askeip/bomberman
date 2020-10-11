from modules import cell as c,\
    explosive as exive,\
    explosion as ex,\
    empty_cell as ec,\
    bomberman as b


class Bomb_bonus(c.Cell, exive.Explosive):

    def __init__(self, position):
        self._position = position
        self.collected = False

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, position):
        self._position = position

    def explode(self, gamefield, ex_type, user):
        gamefield[self._position.y][self._position.x] = ex.Explosion(
            self._position, ex_type=ex_type, user=user)

    def should_continue_explode(self, ex_type):
        return False

    @property
    def extra_range(self):
        return 0

    def action(self, gamefield, tick_time):
        if self.collected:
            gamefield[self._position.y][
                self._position.x] = ec.Empty(self._position)
        else:
            return

    def contact(self, user):
        if isinstance(user, b.Bomberman):
            user.add_bomb()
            self.collected = True

    def is_passable(self, user):
        return True

    @property
    def image_name(self):
        return "bomb_bonus.png"
