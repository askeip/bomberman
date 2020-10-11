from modules import bomb as b,\
    explosive as ex,\
    movable as m


class Bomberman(m.Movable):

    def __init__(self, pos, max_speed, tick_time, acceleration=0):
        super().__init__(pos, max_speed, tick_time, acceleration)
        self.bombs_count = 1
        self._max_bombs_count = self.bombs_count
        self.ex_type = ex.ExplosionType.T1
        self.bomb_range = 1
        self.bomb_timer = 2.5

    def place_bomb(self, gamefield):
        y = self.rounded_pos.y
        x = self.rounded_pos.x
        bcount = self.bombs_count
        if not isinstance(gamefield.gamefield[y][x], b.Bomb) and bcount > 0:
            self.bombs_count -= 1
            gamefield.place_bomb(
                self.rounded_pos, self.bomb_timer, self)

    def new_lvl(self):
        self.bombs_count = self._max_bombs_count

    def add_bomb(self):
        self.bombs_count += 1
        self._max_bombs_count += 1

    def change_type(self):
        self.ex_type = ex.ExplosionType(
            (self.ex_type.value + 1) % len(ex.ExplosionType))

    @property
    def image_name(self):
        return "Bomberman.png"

    def __str__(self):
        return "Bomberman"
