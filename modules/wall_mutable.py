from modules import cell as c,\
    explosion as ex,\
    explosive as exive


class Wall_Mutable(c.Cell, exive.Explosive):

    def __init__(self, position, ex_type):
        self._position = position
        self.ex_type = ex_type
        self.bonus = None

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, position):
        self._position = position

    def insert_bonus(self, bonus):
        self.bonus = bonus

    def action(self, gamefield, tick_time):
        return

    def contact(self, user):
        return

    def explode(self, gamefield, ex_type, user):
        if self.ex_type in exive.ExplosiveTypes.explosive[ex_type]:
            gamefield[self._position.y][self._position.x] = ex.Explosion(
                self._position, ex_type=ex_type, user=user, bonus=self.bonus)

    def should_continue_explode(self, ex_type):
        return self.ex_type in exive.ExplosiveTypes.explosive[ex_type]

    @property
    def extra_range(self):
        return self.ex_type.value

    def is_passable(self, user):
        return False

    @property
    def image_name(self):
        return str.format("Wall_Mutable{0}.png",self.ex_type.value)
