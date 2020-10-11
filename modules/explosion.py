from modules import cell as c,\
    explosive as ex


class Explosion(c.Cell, ex.Explosive):

    def __init__(self, position, ex_type=ex.ExplosionType.T1, user=None, timer=0.3, bonus=None):
        self._position = position
        self.ex_type = ex_type
        self.user = user
        self.timer = timer
        self.bonus = bonus

    @property
    def position(self):
        return self._position

    def explode(self, gamefield, ex_type, user):
        gamefield[self._position.y][self._position.x] = Explosion(
            self._position, ex_type=ex_type, user=user, bonus=self.bonus)

    def should_continue_explode(self, ex_type):
        return True

    @property
    def extra_range(self):
        return 0

    @position.setter
    def set_position(self, position):
        self._position = position

    def contact(self, user):
        user.take_damage()
        from modules import bomberman as b
        if self.user and not isinstance(user, b.Bomberman):
            self.user.add_points(user.price)

    def action(self, gamefield, tick_time):
        self.timer -= tick_time
        if self.timer <= 0:
            from modules import empty_cell as ec
            gamefield[self._position.y][self._position.x] = ec.Empty(self._position) if not self.bonus\
                else self.bonus(self._position)

    def is_passable(self, user):
        return True

    @property
    def image_name(self):
        return "explosion.png"
