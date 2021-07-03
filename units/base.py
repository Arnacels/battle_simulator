import statistics
from abc import ABC, abstractmethod

from utils import CompositeMixin


class Unit(ABC):
    """
    Base Unit class
    """
    _health: float  # health unit
    _recharge: int  # time when unit is sleep

    @property
    def health(self):
        return self._health if self._health > 0 else 0

    @health.setter
    def health(self, value):
        self._health = value

    @property
    def recharge(self):
        return self._recharge

    @recharge.setter
    def recharge(self, value):
        self._recharge = value

    @abstractmethod
    def get_attack_success(self) -> float:
        """
        Count chance of success attack
        :return: float chance of success attack
        """
        raise NotImplementedError

    @abstractmethod
    def get_damage_amount(self) -> float:
        """
        Calculate the amount of damage that the squad can do
        :return: float damage of unit
        """
        raise NotImplementedError

    @abstractmethod
    def is_active(self) -> bool:
        """
        :return: bool Unit is sleep
        """
        raise NotImplementedError

    @abstractmethod
    def is_alive(self) -> bool:
        """
        :return: bool Unit is alive
        """
        raise NotImplementedError

    @abstractmethod
    def taking_damage(self, amount: float) -> None:
        """
        :param amount: How damage taking unit
        :return: None
        """
        raise NotImplementedError

    @abstractmethod
    def attack(self) -> float:
        """
        When a unit attacks, it calls several methods but returns
        the amount of damage it can deal.
        :return: float count of damage amount
        """
        raise NotImplementedError


class CompositeUnit(Unit, CompositeMixin):
    """
    Base composite unit class
    I was thinking of separating the "Composite" entity with the "Unit" entity.
    Then use "Composite" as "Mixin".
    Then the "Units" methods would not be confused with "Composite" for such entities as "Army" and "Battlefield".
    """

    def __str__(self):
        info = f"Live units: {len(self.get_alive_units())} \nActive units: {len(self.get_active_units())} \n"
        info += "    ".join([str(unit) for unit in self.units]) + '\n'
        return info

    @property
    def health(self):
        return statistics.mean([unit.health for unit in self.units if unit.is_alive()])

    def is_alive(self):
        return any([unit.is_alive() for unit in self.units])
