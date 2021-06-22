from typing import List

from units import Army
from .strategies import RandomStrategy, StrongestStrategy, WeakestStrategy, Strategy


class BaseBattleField(object):
    def battle(self):
        raise NotImplementedError


class BattleField(BaseBattleField):
    __strategies_variable: dict = dict()
    __strategy: Strategy = None

    def __init__(self, armies: List[Army]):
        self.armies = armies
        for strategy in [RandomStrategy, StrongestStrategy, WeakestStrategy]:
            print(strategy.name)
            self.__strategies_variable[strategy.name] = strategy()

    @property
    def strategy(self):
        return self.__strategy

    @strategy.setter
    def strategy(self, name):
        self.__strategy = self.__strategies_variable[name]

    def battle(self):
        if self.__strategy:
            self.__strategy.battle()
