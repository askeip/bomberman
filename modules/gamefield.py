from modules import gamefield_creator as gc,\
    bomb as b,\
    cell as c,\
    leaderboard as lb,\
    bomberman as bman,\
    dying_bomberman as dbman


class GameField():
    def __init__(self, lvl_names, tick_time, lb_path="leaderbord.txt", lb_size=10):
        self.lvl_names = list(lvl_names)
        self.gamefield = None
        self.tick_time = tick_time
        self.leaderboard = lb.Leaderboard(lb_size, lb_path)
        self.bomberman = bman.Bomberman(c.Position(1, 1), 0.12, tick_time)
        self.game_over = False
        self.win = False
        self.create_next_lvl()

    def create_next_lvl(self):
        try:
            self.create_level(self.lvl_names.pop(0))
        except FileNotFoundError or gc.InvalidFileException:
            self.create_next_lvl()
        except IndexError:
            self.game_over = True
            self.win = True

    def create_level(self, file_path):
        try:
            self.gamefield, movable = gc.Gamefield_creator.create_gamefield(
                file_path)
        except gc.InvalidFileException:
            raise gc.InvalidFileException
        self.movable = []
        self.bomberman.new_lvl()
        for mov_obj in movable:
            self.movable.append(mov_obj[0](mov_obj[1], 0.08, self.tick_time))
        self.bomberman.position = c.Position(1, 1)

    @property
    def width(self):
        return len(self.gamefield[0])

    @property
    def height(self):
        return len(self.gamefield)

    def make_moves(self):
        for line in self.gamefield:
            for cell in line:
                cell.action(self.gamefield, self.tick_time)
        self.movables_moves()
        if self.game_over:
            pass
        else:
            self.bomberman.action(self.gamefield, self.tick_time)
            for movable in self.movable:
                if movable.rounded_pos == self.bomberman.rounded_pos:
                    self.bomberman.take_damage()
            if self.bomberman.lifes <= 0:
                self.bomberman = dbman.Dying_bomberman(
                    self.bomberman.position, self.bomberman)
            self.game_over = self.bomberman.dead
        if len(self.movable) == 0:
            self.create_next_lvl()
        if self.game_over:
            self.leaderboard.refresh(self.bomberman.points)

    def movables_moves(self):
        k = 0
        for i in range(0, len(self.movable)):
            i -= k
            self.movable[i].action(self.gamefield, self.tick_time)
            if self.movable[i].lifes <= 0:
                self.movable[i] = dbman.Dying_bomberman(
                    self.movable[i].position)
            if self.movable[i].dead:
                self.movable.pop(i)
                k += 1

    def place_bomb(self, position, timer, user):
        self.gamefield[position.y][position.x] = b.Bomb(position, timer, user)
