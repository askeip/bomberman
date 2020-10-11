from modules import cell as c,\
    explosive as exive,\
    explosion as ex,\
    wall_mutable as wm


class Bomb(c.Cell, exive.Explosive):

    def __init__(self, position, timer, user):
        self.timer = timer
        self.ex_type = user.ex_type
        self._position = position
        self.user = user
        self.range = user.bomb_range

    @property
    def position(self):
        return self._position

    def action(self, gamefield, tick_time):
        self.timer -= tick_time
        if self.is_explode_time:
            self.explode(gamefield, self.ex_type, self.user)

    @position.setter
    def position(self, position):
        self._position = position

    def contact(self, user):
        return

    def explode(self, gamefield, ex_type, user):
        gamefield[self._position.y][self._position.x] = ex.Explosion(
            self._position, self.ex_type, self.user)
        if self.user:
            self.user.bombs_count += 1
        directions = [(-1, 0), (0, -1), (1, 0), (0, 1)]
        for direction in directions:
            boom_range = self.range
            i = 0
            while i < boom_range:
                y = self._position.y + direction[0] * (i + 1)
                x = self._position.x + direction[1] * (i + 1)
                if isinstance(gamefield[y][x], exive.Explosive):
                    cell = gamefield[y][x]
                    gamefield[y][x].explode(gamefield, self.ex_type, user)
                    if not cell.should_continue_explode(self.ex_type):
                        break
                    if isinstance(cell, wm.Wall_Mutable):
                        boom_range = i + 1 + cell.extra_range
                else:
                    break
                i += 1

    @property
    def is_explode_time(self):
        return self.timer <= 0

    def should_continue_explode(self, ex_type):
        return False

    @property
    def extra_range(self):
        return 0

    def is_passable(self, user):
        return (user.left_x == self.position.x or user.right_x == self.position.x)\
            and (user.top_y == self.position.y or user.bot_y == self.position.y)

    @property
    def image_name(self):
        return str.format("bomb{0}.png", self.ex_type.value)
