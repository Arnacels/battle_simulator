from typing import List

from units import Army
from utils import filter_active_units, filter_alive_units
from .strategies import RandomStrategy, StrongestStrategy, WeakestStrategy, Strategy


class BaseBattleField(object):
    def battle(self):
        raise NotImplementedError


class BattleField(BaseBattleField):
    __strategies_variable: dict
    __strategy: Strategy = None

    def __init__(self, armies: List[Army]):
        self.__strategies_variable = dict()
        self.armies = armies
        for strategy in [RandomStrategy, StrongestStrategy, WeakestStrategy]:
            self.__strategies_variable[strategy.name] = strategy()

    @property
    def strategy(self):
        return self.__strategy

    @strategy.setter
    def strategy(self, name):
        self.__strategy = self.__strategies_variable[name]

    def battle(self, attack_army):
        if self.__strategy:
            armies = list(filter_active_units(filter_alive_units(self.armies)))
            armies.remove(attack_army)
            self.__strategy.battle(attack_army, armies)
