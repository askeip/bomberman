from modules import cell as c,\
    wall_immutable as wi,\
    empty_cell as ec,\
    wall_mutable as wm,\
    bomb_bonus as bb,\
    range_bonus as rb,\
    speed_bonus as sb,\
    explosive as ex,\
    bot,\
    movable as m
import random

cells = {'#': wi.Wall_Immutable, ' ': ec.Empty,\
         None: ec.Empty, '0': wm.Wall_Mutable,
         '1': wm.Wall_Mutable, '2': wm.Wall_Mutable,
         '3': wm.Wall_Mutable, 'B': bot.Bot}


class InvalidFileException(Exception):
    pass


class Gamefield_creator():

    @staticmethod
    def create_wall_line(gamefield, width):
        field_line = []
        for i in range(width):
            field_line.append(wi.Wall_Immutable(c.Position(i, len(gamefield))))
        gamefield.append(field_line)

    @staticmethod
    def create_gamefield(file_path):
        with open(file_path) as f:
            str_field = f.read().split('\n')
        f.close()
        game_info = str_field.pop(0).split()
        width = int(game_info[0]) + 2
        bonuses_count = int(game_info[1])
        mutable_walls = []
        movable = []
        gamefield = []
        Gamefield_creator.create_wall_line(gamefield, width)
        for i in range(len(str_field)):
            string = str_field[i]
            string = string[0:width]
            field_line = []
            field_line.append(wi.Wall_Immutable(c.Position(0, i + 1)))
            for j in range(len(string)):
                game_object = cells.get(string[j])
                if not game_object:
                    raise InvalidFileException
                position = c.Position(j + 1, i + 1)
                if issubclass(game_object, m.Movable):
                    field_line.append(ec.Empty(position))
                    movable.append((game_object, position))
                else:
                    if game_object is wm.Wall_Mutable:
                        field_line.append(game_object(
                            position, ex.ExplosionType(int(string[j]))))
                    else:
                        field_line.append(game_object(position))
                    if isinstance(field_line[- 1], wm.Wall_Mutable):
                        mutable_walls.append(field_line[len(field_line) - 1])
            while len(field_line) < width - 1:
                field_line.append(ec.Empty(c.Position(len(field_line), i + 1)))
            field_line.append(wi.Wall_Immutable(
                c.Position(len(field_line), i + 1)))
            gamefield.append(field_line)
        Gamefield_creator.create_wall_line(gamefield, width)
        gamefield[1][1] = ec.Empty(c.Position(1, 1))
        Gamefield_creator.randomize_bonuses(mutable_walls, bonuses_count)
        return gamefield, movable

    @staticmethod
    def randomize_bonuses(mutable_walls, bonuses_count):
        bonuses = bb.Bomb_bonus, rb.Range_bonus, sb.Speed_bonus
        walls_count = len(mutable_walls)
        while bonuses_count != 0 and walls_count > 0:
            bonus = bonuses[random.randint(0, len(bonuses) - 1)]
            mutable_walls.pop(random.randint(
                0, walls_count - 1)).insert_bonus(bonus)
            walls_count -= 1
            bonuses_count -= 1
