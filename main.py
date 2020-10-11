from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QLabel
from PyQt5.QtGui import QPainter, QFont, QImage
from PyQt5.QtCore import Qt, QCoreApplication

from modules import gamefield as g, bomb as b
import sys
import time
from os.path import *


class Menu(QWidget):

    def __init__(self, parent):
        super().__init__()
        self.setParent(parent)
        self.is_active = False
        self.initUI()

    def initUI(self):
        self.init_labels()
        self.init_buttons()
        self.setFixedHeight(self.height())
        self.setFixedWidth(self.width())

    def init_labels(self):
        label_width = self.parent().frame_width * (len(self.parent().gamefield.gamefield[0]) - 2)
        label_height = self.parent().frame_height * 1.2
        self.slz = (label_width, label_height)
        game_over_text = "YOU " + ("WIN " if self.parent().gamefield.win else "LOST ") + \
                         "AND YOU GOT " + \
            str(self.parent().gamefield.bomberman.points) + "POINTS"
        label_pos = (self.parent().frame_width, self.parent().frame_width * 0.2)
        self.game_over = Label(label_pos, self.slz, game_over_text, self)
        lb_size = (self.parent().window_width, self.parent().window_height)
        lb_str = self.parent().gamefield.leaderboard.str_format
        self.leaderboard = Label(label_pos, lb_size, lb_str,self)
        self.close_all_labels()

    def close_all_labels(self):
        self.game_over.close()
        self.leaderboard.close()

    def show_last_menu(self, event=None):
        self.close_all_labels()
        game_over_text = "YOU " + ("WIN " if self.parent().gamefield.win else "LOST ") + \
                         "AND YOU GOT " + \
            str(self.parent().gamefield.bomberman.points) + " POINTS"
        self.game_over.setText(game_over_text)
        self.game_over.show()
        self.show_start_menu()

    def init_buttons(self):
        sbz = (self.parent().frame_width * (self.parent().gamefield.width - 2), self.parent().frame_height * 1.2)
        pos = [self.parent().frame_width, self.parent().frame_height]
        text = "New game"
        self.new_game_button = Button(self._start_game, (pos[0], pos[1] * 1.5), sbz, text, self)
        text = "Show Leaderboard"
        self.leaderboard_button = Button(self.show_leaderboard, (pos[0], pos[1] * 4.1), sbz, text, self)
        text = "Exit"
        self.exit_button = Button(self._exit_func, (pos[0], pos[1] * 5.7), sbz, text, self)
        self.setChildNoFocus(self.new_game_button)
        self.setChildNoFocus(self.leaderboard_button)
        self.setChildNoFocus(self.exit_button)
        self.close_all_buttons()

    def setChildNoFocus(self, child):
        child.setFocusPolicy(Qt.NoFocus)

    def close(self):
        super().close()

    def close_all_buttons(self):
        self.new_game_button.close()
        self.leaderboard_button.close()
        self.exit_button.close()

    def show_leaderboard(self):
        self.leaderboard.setText(
            self.parent().gamefield.leaderboard.str_format)
        self.leaderboard.mouseReleaseEvent = self.show_start_menu if not self.parent().gamefield.game_over\
            else self.show_last_menu
        self.leaderboard.setStyleSheet("background-color : black;"
                                       "color : blue;")
        self.leaderboard.show()
        self.close_all_buttons()

    def _start_game(self):
        self.parent().start()

    def _exit_func(self):
        self.parent()._close()

    def show_start_menu(self, event=None):
        self.leaderboard.close()
        self.new_game_button.show()
        self.leaderboard_button.show()
        self.exit_button.show()

    '''def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.deactivate()

    def deactivate(self):
        self.is_active = False
        if self.qb:
            self.qb.is_active = not self.is_active
            self.close()'''


class Label(QLabel):

    def __init__(self, coordinates, size, text, parent=None):
        super().__init__(parent)
        self.setText(text)
        self.setGeometry(coordinates[0], coordinates[1], size[0], size[1])
        self.setFixedHeight(self.height())
        self.setFixedWidth(self.width())


class QtCheatWindow(QWidget):

    def __init__(self, bomberman):
        super().__init__()
        self.active = True
        self.setGeometry(150, 150, 200, 200)
        self.setWindowTitle('CHEATS')
        self.bomberman = bomberman
        self.create_buttons()
        self.show()

    def create_buttons(self):
        buttons_folder = "images"
        standart_button_size = (150, 50)
        self.lifes_button = Button(self.infinite_lifes, (25, 20), standart_button_size, "infinite lifes", self)
        self.bombs_button = Button(self.infinite_bombs, (25, 80), standart_button_size, "infinite bombs", self)
        self.range_button = Button(self.infinite_range, (25, 140), standart_button_size, "infinite range", self)

    def closeEvent(self, *args, **kwargs):
        self.active = False

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)

    def infinite_lifes(self):
        self.bomberman.lifes = sys.maxsize

    def infinite_bombs(self):
        self.bomberman.bombs_count = sys.maxsize

    def infinite_range(self):
        self.bomberman.bomb_range = sys.maxsize


class Button(QPushButton):

    def __init__(self, function, coordinates, size, text, parent=None):
        super(QPushButton, self).__init__(parent)
        self.setText(text)
        self.function = function
        self.setGeometry(coordinates[0], coordinates[1], size[0], size[1])
        self.clicked.connect(self._on_click)

    def _on_click(self):
        self.function()


class QtBomberman(QWidget):

    def __init__(self, lvlname, lvlnum=1, file_ext=".txt", lb_path="leaderbord.txt", lb_size=10):
        super().__init__()
        self.menu = None
        self.lb_path = join("text files", lb_path)
        self.lb_size = lb_size
        self.lvl_names = []
        self.generate_lvl_names(join("text files", lvlname), file_ext, lvlnum)
        self.is_active = True
        self.start()
        self.menu = Menu(self)
        self.menu.setFocusPolicy(Qt.NoFocus)
        self.initUI()

    def start(self):
        self.activate()
        self.frame_width = 32
        self.frame_height = 32
        self.tick_time = 0.05
        self.images = {}
        self.qc = None
        self.cheat = [Qt.Key_H, Qt.Key_E, Qt.Key_S,
                      Qt.Key_O, Qt.Key_Y, Qt.Key_A, Qt.Key_M]
        self.cheats_detector = []
        self.gamefield = g.GameField(
            self.lvl_names, self.tick_time, self.lb_path, self.lb_size)
        if not self.gamefield.gamefield:
            self._close()
        self.key_moves = {
            Qt.Key_D: self.gamefield.bomberman.move_right,
            Qt.Key_A: self.gamefield.bomberman.move_left,
            Qt.Key_W: self.gamefield.bomberman.move_up,
            Qt.Key_S: self.gamefield.bomberman.move_down,
            Qt.Key_Right: self.gamefield.bomberman.move_right,
            Qt.Key_Left: self.gamefield.bomberman.move_left,
            Qt.Key_Up: self.gamefield.bomberman.move_up,
            Qt.Key_Down: self.gamefield.bomberman.move_down
        }
        self.key_stop_moves = {
            Qt.Key_D: self.gamefield.bomberman.stop_moving_right,
            Qt.Key_A: self.gamefield.bomberman.stop_moving_left,
            Qt.Key_W: self.gamefield.bomberman.stop_moving_up,
            Qt.Key_S: self.gamefield.bomberman.stop_moving_down,
            Qt.Key_Right: self.gamefield.bomberman.stop_moving_right,
            Qt.Key_Left: self.gamefield.bomberman.stop_moving_left,
            Qt.Key_Up: self.gamefield.bomberman.stop_moving_up,
            Qt.Key_Down: self.gamefield.bomberman.stop_moving_down
        }

    def activate(self):
        self.is_active = True
        if self.menu:
            self.menu.is_active = not self.is_active
            self.menu.close()

    def generate_lvl_names(self, lvlname, file_ext, lvls_count):
        for lvlnum in range(lvls_count):
            num = str(lvlnum) if lvlnum != 0 else ""
            file_path = lvlname + num + file_ext
            self.lvl_names.append(file_path)

    def initUI(self):
        self.setGeometry(100, 100, self.frame_width *
                         self.game_width, self.frame_height * self.game_height)
        self.setFixedHeight(self.height())
        self.setFixedWidth(self.width())
        self.setWindowTitle('Bomberman')
        self.show()
        self.game_loop()

    def closeEvent(self, e):
        self._close()

    def _close(self):
        exit()

    @property
    def game_width(self):
        return self.gamefield.width

    @property
    def game_height(self):
        return self.gamefield.height

    @property
    def window_width(self):
        return self.gamefield.width * self.frame_width

    @property
    def window_height(self):
        return self.gamefield.height * self.frame_height

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        for raw in range(self.game_height):
            for column in range(self.game_width):
                image_name = self.gamefield.gamefield[raw][column].image_name
                if image_name:
                    image = self.find_image(image_name).scaled(
                        self.frame_width, self.frame_height)
                    qp.drawImage(column * self.frame_width,
                                 raw * self.frame_height, image)
        for movable in self.gamefield.movable:
            image_name = movable.image_name
            if image_name:
                image = self.find_image(image_name).scaled(
                    self.frame_width, self.frame_height)
                qp.drawImage(movable.x * self.frame_width,
                             movable.y * self.frame_height, image)
        image = self.find_image(self.gamefield.bomberman.image_name).scaled(
            self.frame_width, self.frame_height)
        qp.drawImage(self.gamefield.bomberman.x * self.frame_width,
                     self.gamefield.bomberman.y * self.frame_height, image)
        bomb_image_name = b.Bomb(None, None, self.gamefield.bomberman).image_name
        image = self.find_image(bomb_image_name)
        image_width = (len(self.gamefield.gamefield[0]) - 1.2) * self.frame_width
        image_height = (len(self.gamefield.gamefield) - 1.2) * self.frame_height
        qp.drawImage(image_width,image_height, image)
        font = QFont()
        font.setPointSize(font.pointSize() * 3)
        qp.setFont(font)
        text_width = (len(self.gamefield.gamefield[0]) - 5.8) * self.frame_width
        text_height = (len(self.gamefield.gamefield) - 1.2) * self.frame_height
        text = str.format("POINTS: {0}", str(self.gamefield.bomberman.points))
        qp.drawText(text_width,text_height,self.frame_width * 5, self.frame_height, Qt.AlignLeft, text)
        self.show()

    def find_image(self, image_name):
        if not (image_name in self.images):
            self.images[image_name] = QImage(join("images", image_name))
        image = self.images[image_name]
        return image

    def game_loop(self):
        while True:
            try:
                QCoreApplication.processEvents()
                self.make_moves()
                time.sleep(self.tick_time)
                if self.qc and self.qc.active or not self.is_active:
                    continue
                if self.gamefield.game_over:
                    self.change_activity_menu(self.menu.show_last_menu)
            except KeyboardInterrupt:
                self._close()

    def make_moves(self):
        self.gamefield.make_moves()
        self.repaint()

    def change_activity_menu(self, *funcs):
        self.is_active = not self.is_active
        self.menu.is_active = not self.is_active
        if self.is_active:
            self.menu.close()
        else:
            self.menu.show()
            for func in funcs:
                func()
        self.repaint()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape and not self.gamefield.game_over:
            self.change_activity_menu(self.menu.show_start_menu)
        if self.gamefield.game_over or not self.is_active:
            return
        if e.key() == Qt.Key_Space:
            self.gamefield.bomberman.place_bomb(self.gamefield)
        if e.key() == Qt.Key_Tab:
            self.gamefield.bomberman.change_type()
        else:
            try:
                self.key_moves[e.key()]()
            except KeyError:
                pass

    def detect_cheat(self, key):
        self.cheats_detector.append(key)
        if self.cheat[len(self.cheats_detector) - 1] != self.cheats_detector[- 1]:
            self.cheats_detector = []
            return
        if len(self.cheat) == len(self.cheats_detector):
            self.qc = QtCheatWindow(self.gamefield.bomberman)
            self.cheats_detector = []

    def keyReleaseEvent(self, e):
        if e.isAutoRepeat():
            return
        self.detect_cheat(e.key())
        try:
            self.key_stop_moves[e.key()]()
        except KeyError:
            pass
        self.repaint()


def main():
    app = QApplication(sys.argv)
    lvl_name, lvl_count, file_ext = enter_info()
    qb = QtBomberman(lvl_name, lvl_count, file_ext)
    sys.exit(app.exec_())


def enter_info():
    print("Enter lvl names dividing by space:")
    print("general lvl name, amount of lvls with this name, general file extension")
    info = input().split(' ')
    try:
        lvl_name = info[0]
        lvl_count = int(info[1])
        file_ext = info[2]
        return lvl_name, lvl_count, file_ext
    except:
        print("Wrong arguments, please try again")
        enter_info()

if __name__ == "__main__":
    main()
