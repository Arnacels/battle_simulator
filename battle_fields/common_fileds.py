from typing import List

from .strategies import Strategy


class BaseBattleField(object):
    def battle(self):
        raise NotImplementedError


class BattleField(BaseBattleField):
    __strategy: Strategy

    def __init__(self, armies: List[Army]):
        self.armies = armies

    @property
    def strategy(self):
        return self.strategy

    @strategy.setter
    def strategy(self, value):
        self.__strategy = value

    def battle(self):
        #  TODO
        pass
