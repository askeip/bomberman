from modules import movable as m


class Dying_bomberman(m.Movable):

    def __init__(self, pos, bomberman=None):
        super().__init__(pos, 0, 0, 0)
        self._position = pos
        if bomberman:
            self.ex_type = bomberman.ex_type
            self.bomb_range = bomberman.bomb_range
            self.points = bomberman.points
        self.timer = 1.2
        self.dead = False

    def place_bomb(self, gamefield):
        return

    def explode(self, gamefield, ex_type, user):
        return

    def action(self, gamefield, tick_time):
        self.timer -= tick_time
        if self.timer <= 0:
            self.dead = True

    @property
    def image_name(self):
        return "dying_bomberman.png"
