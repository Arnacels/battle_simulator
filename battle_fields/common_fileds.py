from typing import List

from units import Army
from utils import CompositeMixin
from .strategies import RandomStrategy, StrongestStrategy, WeakestStrategy, Strategy


class BaseBattleField(object):
    def battle(self, attack_army):
        raise NotImplementedError


class BattleField(BaseBattleField, CompositeMixin):
    """
    Battlefield
    Is class have context strategy for battle and composite Armies in units
    """
    __strategies_variable: dict
    __strategy: Strategy = None
    _composites_class: List[Army] = [Army]

    def __init__(self):
        super().__init__()
        self.__strategies_variable = dict()
        for strategy in [RandomStrategy, StrongestStrategy, WeakestStrategy]:
            self.__strategies_variable[strategy.name] = strategy()

    @property
    def strategy(self):
        return self.__strategy

    @strategy.setter
    def strategy(self, name):
        self.__strategy = self.__strategies_variable[name]

    def add_unit(self, unit: Army):
        self.units.append(unit)

    @classmethod
    def create(cls, *, count=1, **kwargs):
        return super().create(count=kwargs.get('armies_count', 0), **kwargs)

    def battle(self, attack_army):
        if self.__strategy:
            self.__strategy.battle(attack_army, self)
