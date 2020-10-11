from abc import abstractproperty
from enum import Enum
import math
from  modules import cell as c,\
    explosive as ex


class Direction(Enum):
    Left = -2
    Up = -1
    Right = 1
    Down = 2


class Movable(ex.Explosive):

    def __init__(self, pos, max_speed, tick_time, acceleration=0, price=1):
        self.x_direct = None
        self.y_direct = None
        self.x_move_funcs = [(math.floor, math.floor), (math.ceil, math.floor),
                             (math.floor, math.ceil), (math.ceil, math.ceil)]
        self.y_move_funcs = [(math.floor, math.floor), (math.floor, math.ceil),
                             (math.ceil, math.floor), (math.ceil, math.ceil)]
        self.x_mv_vls = (0, self.x_move_funcs)
        self.y_mv_vls = (1, self.y_move_funcs)
        self._position = pos
        self.rounded_pos = c.Position(
            round(self._position.x), round(self._position.y))
        self.max_speed = max_speed
        self.tick_time = tick_time
        self.x_speed = 0
        self.y_speed = 0
        self.lifes = 1
        self.damage_standart_cd = 2
        self.damage_cd = 0
        self.dead = False
        self.max_speed = round(max_speed, 2)
        if acceleration == 0:
            self.acceleration = self.max_speed / 2
        else:
            self.acceleration = acceleration
        self.points = 0
        self.price = price

    def add_points(self, points):
        self.points += points

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, position):
        self._position = position
        self.rounded_pos = c.Position(
            round(self._position.x), round(self._position.y))

    @property
    def x(self):
        return self._position.x

    @property
    def y(self):
        return self._position.y

    @property
    def left_x(self):
        return math.floor(self._position.x)

    @property
    def right_x(self):
        return math.ceil(self._position.x)

    @property
    def top_y(self):
        return math.floor(self._position.y)

    @property
    def bot_y(self):
        return math.ceil(self._position.y)

    def try_move(self, gamefield, direction, speed):
        searched_item, funcs = self.funcs_for_move(direction)
        pos = self._position
        if not direction:
            return 0
        if direction is Direction.Left or direction is Direction.Up:
            possible_speed = self.negative_move(
                pos, gamefield, searched_item, funcs, speed)
        else:
            possible_speed = self.positive_move(
                pos, gamefield, searched_item, funcs, speed)
        return possible_speed

    def positive_move(self, pos, gamefield, searched_item, funcs, speed):
        speed = speed if speed >= 0 else 0
        psbl_spd = speed + self.acceleration
        psbl_spd = psbl_spd if psbl_spd <= self.max_speed else self.max_speed
        next_pos = [pos.x, pos.y]
        next_pos[searched_item] += psbl_spd
        pos = c.Position(next_pos[0], next_pos[1])
        y1 = funcs[2][0](pos.y)
        x1 = funcs[2][1](pos.x)
        y2 = funcs[3][0](pos.y)
        x2 = funcs[3][1](pos.x)
        if not (gamefield[y1][x1].is_passable(self)
                and gamefield[y2][x2].is_passable(self)):
            pos = self._position.position
            psbl_spd = math.ceil(pos[searched_item]) - pos[searched_item]
        return psbl_spd

    def negative_move(self, pos, gamefield, searched_item, funcs, speed):
        speed = speed if speed <= 0 else 0
        possible_speed = speed - self.acceleration
        possible_speed = possible_speed if possible_speed >= - \
            self.max_speed else - self.max_speed
        next_pos = [pos.x, pos.y]
        next_pos[searched_item] += possible_speed
        pos = c.Position(next_pos[0], next_pos[1])
        y1 = funcs[0][0](pos.y)
        x1 = funcs[0][1](pos.x)
        y2 = funcs[1][0](pos.y)
        x2 = funcs[1][1](pos.x)
        if not (gamefield[y1][x1].is_passable(self)
                and gamefield[y2][x2].is_passable(self)):
            pos = self.position.position
            possible_speed = math.floor(pos[searched_item]) - pos[searched_item]
        return possible_speed

    def funcs_for_move(self, direction):
        if direction is Direction.Left or direction is Direction.Right:
            searched_item = 0
            funcs = self.x_move_funcs
        else:
            searched_item = 1
            funcs = self.y_move_funcs
        return searched_item, funcs

    def explode(self, gamefield, ex_type, user):
        self.take_damage()

    def take_damage(self):
        if self.damage_cd == 0:
            self.lifes -= 1
            self.damage_cd = self.damage_standart_cd

    def should_continue_explode(self, ex_type):
        return True

    @property
    def extra_range(self):
        return 0

    def action(self, gamefield, tick_time):
        if self.damage_cd != 0:
            self.damage_cd -= tick_time
        psbl_x_spd = 0 if not self.x_direct else self.try_move(
            gamefield, self.x_direct, self.x_speed)
        if psbl_x_spd == 0 and self.x_direct and not self.y_direct:
            values = [[self.top_y, self.left_x], [self.bot_y, self.left_x]]
            psbl_y_spd = self.alt_move(self.x_direct, self.y, gamefield, values, self.y_mv_vls, self.y_speed)
        else:
            psbl_y_spd = 0 if psbl_x_spd != 0 else self.try_move(
                gamefield, self.y_direct, self.y_speed)
            if psbl_y_spd == 0 and psbl_x_spd == 0 and self.y_direct:
                values = [[self.top_y, self.left_x], [self.top_y, self.right_x]]
                psbl_x_spd = self.alt_move(self.y_direct, self.x, gamefield, values, self.x_mv_vls, self.x_speed)
        self.x_speed = psbl_x_spd
        self.y_speed = psbl_y_spd
        self.rounded_pos = c.Position(
            round(self._position.x), round(self._position.y))
        gamefield[self.rounded_pos.y][
            self.rounded_pos.x].contact(self)
        self._position = c.Position(
            round(self.x + self.x_speed, 2), round(self.y + self.y_speed, 2))

    def alt_move(self, direction, value, gamefield, values, mv_vls, spd):
        possible_speed = round(value) - value
        int_dir = int(direction.value / abs(direction.value))
        values[0][mv_vls[0]] += int_dir
        values[1][mv_vls[0]] += int_dir
        cell1 = gamefield[values[0][0]][values[0][1]]
        cell2 = gamefield[values[1][0]][values[1][1]]
        if possible_speed < 0 and cell1.is_passable(self):
            possible_speed = self.negative_move(self.position, gamefield, mv_vls[0], mv_vls[1], spd)
            func = math.floor
        elif possible_speed > 0 and cell2.is_passable(self):
            possible_speed = self.positive_move(self.position, gamefield, mv_vls[0], mv_vls[1], spd)
            func = math.ceil
        else:
            func = math.ceil
            possible_speed = 0
        if func(value) != func(value + possible_speed):
            pos = self._position.position
            possible_speed = func(pos[mv_vls[0]]) - pos[mv_vls[0]]
        return possible_speed

    def stop_moving_x(self, direction):
        if self.x_direct == direction:
            self.x_direct = None
            self.x_speed = 0

    def move_left(self):
        self.x_direct = Direction.Left

    def stop_moving_left(self):
        self.stop_moving_x(Direction.Left)

    def move_right(self):
        self.x_direct = Direction.Right

    def stop_moving_right(self):
        self.stop_moving_x(Direction.Right)

    def stop_moving_y(self, direction):
        if self.y_direct == direction:
            self.y_direct = None
            self.y_speed = 0

    def move_up(self):
        self.y_direct = Direction.Up

    def stop_moving_up(self):
        self.stop_moving_y(Direction.Up)

    def move_down(self):
        self.y_direct = Direction.Down

    def stop_moving_down(self):
        self.stop_moving_y(Direction.Down)

    @abstractproperty
    def image_name(self):
        pass
