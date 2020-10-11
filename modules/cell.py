from abc import ABCMeta, abstractmethod, abstractproperty


class Position():

    def __init__(self, x, y):
        self._position = (x, y)
        self._x = x
        self._y = y

    def __eq__(self, other):
        return self._x == other.x and self._y == other.y

    @property
    def position(self):
        return self._position

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y


class Cell():
    __metaclass__ = ABCMeta

    @abstractproperty
    def position(self):
        pass

    @abstractmethod
    def action(self, gamefield, tick_time):
        pass

    @abstractmethod
    def contact(self, user):
        pass

    @abstractmethod
    def is_passable(self, user):
        pass

    @abstractproperty
    def image_name(self):
        pass
