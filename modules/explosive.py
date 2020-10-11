from abc import ABCMeta, abstractmethod, abstractproperty
from enum import Enum, unique


@unique
class ExplosionType(Enum):
    T1 = 0
    T2 = 1
    T3 = 2
    T4 = 3


class ExplosiveTypes():
    explosive = {ExplosionType.T1: (ExplosionType.T1,),
                 ExplosionType.T2: (ExplosionType.T2, ExplosionType.T1),
                 ExplosionType.T3: (ExplosionType.T3, ExplosionType.T1),
                 ExplosionType.T4: (ExplosionType.T4, ExplosionType.T1)
                 }


class Explosive():
    __metaclass__ = ABCMeta

    @abstractmethod
    def explode(self, gamefield, ex_type, user):
        pass

    @abstractmethod
    def should_continue_explode(self, ex_type):
        pass

    @abstractproperty
    def extra_range(self):
        pass
