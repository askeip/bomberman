from modules import movable as m
import random


class Bot(m.Movable):

    def __init__(self, pos, max_speed, tick_time, acceleration=0):
        super().__init__(pos, max_speed, tick_time, acceleration, 1)

    def action(self, gamefield, tick_time):
        if not self.x_direct and not self.y_direct:
            self.choose_direction(gamefield)
        super().action(gamefield, tick_time)
        if self.x_speed == 0 and self.y_speed == 0:
            self.choose_direction(gamefield)

    def choose_direction(self, gamefield):
        x_directions = self.check_directions(
            gamefield, self.x_mv_vls, m.Direction.Right, m.Direction.Left)
        self.x_direct = None if len(x_directions) == 0 else x_directions[
            random.randint(0, len(x_directions) - 1)]
        y_directions = self.check_directions(
            gamefield, self.y_mv_vls, m.Direction.Down, m.Direction.Up)
        self.y_direct = None if len(y_directions) == 0 else y_directions[
            random.randint(0, len(y_directions) - 1)]
        if self.x_direct and self.y_direct:
            directions = [self.x_direct, self.y_direct]
            directions[random.randint(0, len(directions) - 1)] = 0
            self.x_direct = directions[0]
            self.y_direct = directions[1]

    def check_directions(self, gamefield, move_values, dir1, dir2):
        directions = []
        self.check_direction(gamefield, move_values,
                             self.positive_move, dir1, directions)
        self.check_direction(gamefield, move_values,
                             self.negative_move, dir2, directions)
        return directions

    def check_direction(self, gamefield, move_values, func, dir, directions):
        if func(self.position, gamefield, move_values[0], move_values[1], 0) != 0:
            directions.append(dir)

    @property
    def image_name(self):
        return "bot.png"

    def str(self):
        return "bot"
