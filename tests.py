from modules import movable as m,\
    gamefield as g,\
    bomb as b,\
    cell as c,\
    bomb_bonus as bb,\
    range_bonus as rb,\
    speed_bonus as sb,\
    explosion as ex,\
    wall_immutable as wi,\
    wall_mutable as wm,\
    dying_bomberman as db,\
    explosive as exive
import unittest
from os.path import join


class TestMoves(unittest.TestCase):

    def setUp(self):
        self.gamefield = g.GameField([join("text files", "testlvl.txt")], 0.03)

    def test_rounded_pos(self):
        movable = m.Movable(c.Position(22.3, 34.5), 0.1, 0.03)
        self.assertEqual(movable.rounded_pos.x, round(movable.x))
        self.assertEqual(movable.rounded_pos.y, round(movable.y))

    def test_points(self):
        movable = m.Movable(c.Position(22.3, 34.5), 0.1, 0.03)
        self.assertEqual(movable.points, 0)
        movable.add_points(5)
        self.assertEqual(movable.points, 5)

    def test_position(self):
        movable = m.Movable(c.Position(22.3, 34.5), 0.1, 0.03)
        self.assertEqual(c.Position(22.3, 34.5), movable.position)
        movable.position = c.Position(12.3, 14.5)
        self.assertEqual(c.Position(12.3, 14.5), movable.position)
        self.assertEqual(c.Position(12, 14), movable.rounded_pos)

    def test_x(self):
        movable = m.Movable(c.Position(22.3, 34.5), 0.1, 0.03)
        self.assertEqual(22.3, movable.x)

    def test_y(self):
        movable = m.Movable(c.Position(22.3, 34.5), 0.1, 0.03)
        self.assertEqual(34.5, movable.y)

    def test_left_x(self):
        movable = m.Movable(c.Position(22.3, 34.5), 0.1, 0.03)
        self.assertEqual(22, movable.left_x)

    def test_right_x(self):
        movable = m.Movable(c.Position(22.3, 34.5), 0.1, 0.03)
        self.assertEqual(23, movable.right_x)

    def test_top_y(self):
        movable = m.Movable(c.Position(22.3, 34.5), 0.1, 0.03)
        self.assertEqual(34, movable.top_y)

    def test_bot_y(self):
        movable = m.Movable(c.Position(22.3, 34.5), 0.1, 0.03)
        self.assertEqual(35, movable.bot_y)

    def movable_move(self, item, position):
        self.gamefield.make_moves()
        self.assertEqual(self.gamefield.bomberman.x, position.x)
        self.assertEqual(self.gamefield.bomberman.y, position.y)

    def test_movable_right_move(self):
        self.gamefield.bomberman.move_right()
        self.movable_move(0, c.Position(
            1 + self.gamefield.bomberman.acceleration, 1))

    def test_movable_left_move(self):
        self.gamefield.bomberman.move_left()
        self.movable_move(0, c.Position(1, 1))

    def test_movable_up_move(self):
        self.gamefield.bomberman.move_up()
        self.movable_move(0, c.Position(1, 1))

    def test_movable_down_move(self):
        self.gamefield.bomberman.move_down()
        self.movable_move(0, c.Position(
            1, 1 + self.gamefield.bomberman.acceleration))

    def test_lifes(self):
        lifes = self.gamefield.bomberman.lifes
        self.gamefield.bomberman.explode(self.gamefield, None, None)
        self.assertEqual(self.gamefield.bomberman.lifes, lifes - 1)

    def test_alt_move_right(self):
        self.gamefield.bomberman.move_down()
        self.gamefield.make_moves()
        self.gamefield.bomberman.stop_moving_down()
        self.gamefield.bomberman.move_right()
        self.movable_move(0, c.Position(1, 1))

    def test_alt_move_left(self):
        self.gamefield.bomberman.position = c.Position(3, 1)
        self.gamefield.bomberman.move_down()
        self.gamefield.make_moves()
        self.gamefield.bomberman.stop_moving_down()
        self.gamefield.bomberman.move_left()
        self.movable_move(0, c.Position(3, 1))

    def test_alt_move_down(self):
        self.gamefield.bomberman.move_right()
        self.gamefield.make_moves()
        self.gamefield.bomberman.stop_moving_right()
        self.gamefield.bomberman.move_down()
        self.movable_move(0, c.Position(1, 1))

    def test_alt_move_up(self):
        self.gamefield.bomberman.position = c.Position(1, 3)
        self.gamefield.bomberman.move_right()
        self.gamefield.make_moves()
        self.gamefield.bomberman.stop_moving_right()
        self.gamefield.bomberman.move_up()
        self.movable_move(0, c.Position(1, 3))

    def test_bomb(self):
        self.gamefield.bomberman.ex_type = exive.ExplosionType.T4
        self.gamefield.bomberman.position = c.Position(4, 2)
        self.gamefield.bomberman.place_bomb(self.gamefield)
        self.gamefield.bomberman.position = c.Position(1, 1)
        cell = self.gamefield.gamefield[2][4]
        while cell.timer != 0 and isinstance(cell, b.Bomb):
            self.gamefield.make_moves()
            cell = self.gamefield.gamefield[2][4]
        self.gamefield.make_moves()
        self.assertIsInstance(self.gamefield.gamefield[1][4], ex.Explosion)
        self.assertIsInstance(self.gamefield.gamefield[2][4], ex.Explosion)
        self.assertIsInstance(self.gamefield.gamefield[2][3], ex.Explosion)
        self.assertIsInstance(self.gamefield.gamefield[3][4], ex.Explosion)
        self.assertIsInstance(self.gamefield.gamefield[4][4], ex.Explosion)
        self.assertIsInstance(self.gamefield.gamefield[5][4], ex.Explosion)
        self.assertIsInstance(self.gamefield.movable[0], db.Dying_bomberman)

    def test_bomb_bonus_picking(self):
        self.gamefield.gamefield[1][1] = bb.Bomb_bonus(c.Position(1, 1))
        self.gamefield.make_moves()
        self.assertEqual(self.gamefield.bomberman.bombs_count, 2)

    def test_range_bonus_picking(self):
        self.gamefield.gamefield[1][1] = rb.Range_bonus(c.Position(1, 1))
        self.gamefield.make_moves()
        self.assertEqual(self.gamefield.bomberman.bomb_range, 2)

    def test_speed_bonus_picking(self):
        self.gamefield.gamefield[1][1] = sb.Speed_bonus(c.Position(1, 1))
        self.gamefield.make_moves()
        self.assertEqual(self.gamefield.bomberman.max_speed, 0.12 * 1.15)

    def bonus_explosion(self, bonus_type):
        self.gamefield.bomberman.place_bomb(self.gamefield)
        self.gamefield.gamefield[1][2] = bonus_type(c.Position(2, 1))
        self.gamefield.bomberman.position = c.Position(1, 3)
        cell = self.gamefield.gamefield[1][1]
        while isinstance(cell, b.Bomb) and cell.timer != 0:
            self.gamefield.make_moves()
            cell = self.gamefield.gamefield[1][1]
        self.gamefield.make_moves()
        self.assertIsInstance(self.gamefield.gamefield[1][2], ex.Explosion)

    def test_bomb_bonus_explosion(self):
        self.bonus_explosion(bb.Bomb_bonus)

    def test_range_bonus_explosion(self):
        self.bonus_explosion(rb.Range_bonus)

    def test_speed_bonus_explosion(self):
        self.bonus_explosion(sb.Speed_bonus)

    def test_leaderboard(self):
        self.gamefield.bomberman.place_bomb(self.gamefield)
        cell = self.gamefield.gamefield[1][1]
        while isinstance(cell, b.Bomb) and cell.timer != 0:
            self.gamefield.make_moves()
            cell = self.gamefield.gamefield[2][4]
        while self.gamefield.bomberman is db.Dying_bomberman:
            self.gamefield.make_moves()
        self.gamefield.make_moves()
        lb_length = len(self.gamefield.leaderboard.results)
        self.assertGreaterEqual(self.gamefield.leaderboard.results[lb_length - 1],0)

    def image_name_exists(self, image_name):
        self.assertTrue(image_name)

    def test_bomb_bonus_image_name_exists(self):
        self.image_name_exists(bb.Bomb_bonus(c.Position(1, 1)).image_name)

    def test_bomberman_name_exists(self):
        self.image_name_exists(self.gamefield.bomberman.image_name)

    def test_bot(self):
        self.image_name_exists(self.gamefield.movable[0].image_name)

    def test_dying_bomberman_image_name_exists(self):
        self.gamefield.bomberman.take_damage()
        self.gamefield.make_moves()
        self.image_name_exists(self.gamefield.bomberman.image_name)

    def test_explosion_image_name_exists(self):
        self.image_name_exists(ex.Explosion(c.Position(1, 1)).image_name)

    def test_range_bonus_image_name_exists(self):
        self.image_name_exists(rb.Range_bonus(c.Position(1, 1)).image_name)

    def test_speed_bonus_image_name_exists(self):
        self.image_name_exists(sb.Speed_bonus(c.Position(1, 1)).image_name)

    def test_wall_immutable_image_name_exists(self):
        self.image_name_exists(wi.Wall_Immutable(c.Position(1, 1)).image_name)

    def test_wall_mutable_image_name_exists(self):
        self.image_name_exists(wm.Wall_Mutable(
            c.Position(1, 1), exive.ExplosionType.T1).image_name)

    def test_gamefield_width(self):
        self.assertEqual(self.gamefield.width, 6)

    def test_gamefield_height(self):
        self.assertEqual(self.gamefield.height, 7)

    def test_next_lvl_creating(self):
        self.gamefield.create_next_lvl()
        self.assertTrue(self.gamefield.win)

    def test_leaderboard(self):
        leaderboard = self.gamefield.leaderboard.results
        self.gamefield.leaderboard.refresh(0)
        results_len = len(self.gamefield.leaderboard.results)
        self.assertEqual(leaderboard[- 1],
                         self.gamefield.leaderboard.results[results_len - 1])


if __name__ == '__main__':
    unittest.main()
