from datetime import datetime, timedelta
import random
from typing import List, Union, Type
import statistics

from .base import Unit, CompositeUnit


class Soldier(Unit):
    """
    Common Soldier
    """
    __exp: int = 0
    __last_attack: datetime = None

    def __str__(self):
        return f"Health: {self.health}     Exp: {self.get_exp()} \n \n"

    @classmethod
    def create(cls, **kwargs):
        """
        :param kwargs: health float; recharge int
        :return: Soldier object
        """
        unit = cls()
        unit.health = kwargs.get('health', 0)
        unit.recharge = kwargs.get('recharge', 1200)
        return unit

    def set_exp(self):
        if self.__exp < 50:
            self.__exp += 1

    def get_exp(self):
        return self.__exp

    def get_damage_amount(self):
        exp = self.get_exp() if self.get_exp() > 0 else 1
        return 0.05 + exp / 100

    def get_attack_success(self):
        return 0.5 * (1 + 100 / 100) * random.randint(50 + self.__exp, 100) / 100

    def is_active(self):
        return not self.__last_attack or datetime.now() > self.__last_attack + timedelta(milliseconds=self._recharge)

    def is_alive(self):
        return self.health > 0

    def taking_damage(self, amount):
        if self.is_alive():
            self.health -= amount

    def attack(self):
        self.set_exp()
        self.__last_attack = datetime.now()
        return self.get_damage_amount()


class Vehicle(CompositeUnit):
    """
    Common Vehicle
    Composite Soldier in units 1-3
    """
    units: List[Soldier]
    _composites_class: List[Type[Soldier]] = [Soldier]
    __last_attack: datetime = None

    def __str__(self):
        return f"Vehicle: " + super().__str__()

    @property
    def recharge(self):
        return self._recharge

    @recharge.setter
    def recharge(self, value):
        if value >= 0:
            self._recharge = value

    def add_unit(self, unit: Soldier):
        if len(self.units) < 4:
            self.units.append(unit)

    @classmethod
    def create(cls, **kwargs):
        """
        :param kwargs: health float; recharge int for soldier in Vehicle
        :return: Vehicle object
        """
        kwargs.update(dict(
            health=1.0,
            recharge=random.randint(0, 1)
        ))
        unit = super().create(count=random.randint(1, 3), **kwargs)
        unit.recharge = random.randint(0, 1)
        return unit

    def get_exp(self):
        exps = []
        for unit in self.get_alive_units():
            exps.append(unit.get_exp() / 100 if unit.get_exp() > 0 else 0)
        return statistics.mean(exps)

    def get_damage_amount(self):
        return 0.01 + self.get_exp() / 100

    def get_attack_success(self):
        return 0.5 * (1 + self.health / 100) * statistics.fmean(
            [unit.get_attack_success() for unit in self.get_alive_units()])

    def is_active(self):
        return not self.__last_attack or datetime.now() > self.__last_attack + timedelta(milliseconds=self._recharge)

    def taking_damage(self, amount):
        alive_units = self.get_alive_units()
        bad_luck_unit = random.choice(alive_units)
        bad_luck_unit.taking_damage(amount * 0.2)
        for unit in alive_units:
            unit.taking_damage(amount * 0.6)
            if unit != bad_luck_unit:
                unit.taking_damage(amount * 0.1)

    def attack(self):
        self.__last_attack = datetime.now()
        [soldier.attack() for soldier in self.units]
        return self.get_damage_amount()


class Squad(CompositeUnit):
    """
    Common Squad
    Composite Soldier or Vehicle in units
    amount of units 5-10
    """
    units: List[Union[Soldier, Vehicle]]
    _composites_class: List[Union[Type[Soldier], Type[Vehicle]]] = [Soldier, Vehicle]

    def __str__(self):
        return f"Squad: " + super().__str__()

    def add_unit(self, unit: Union[Soldier, Vehicle]):
        self.units.append(unit)

    @classmethod
    def create(cls, *, count=1, **kwargs):
        """
        :param kwargs: health float; recharge int for soldier in Vehicle; unit_count for count units in squad
        :return: Squad object
        """
        return super().create(count=kwargs.get('unit_count', 0), **kwargs)

    def get_damage_amount(self):
        return sum([unit.get_damage_amount() for unit in self.get_alive_units() if unit.is_active()])

    def get_attack_success(self):
        successes = [unit.get_attack_success() for unit in self.get_alive_units() if unit.is_active()]
        if successes:
            return statistics.fmean(successes)
        return 0

    def is_active(self):
        return any([unit.is_active() for unit in self.units])

    def taking_damage(self, amount):
        alive_units = self.get_alive_units()
        if alive_units:
            damage_per_unit = amount / len([unit for unit in alive_units])
            for unit in alive_units:
                unit.taking_damage(damage_per_unit)

    def attack(self):
        damage = self.get_damage_amount()
        [unit.attack() for unit in self.get_alive_units()]
        return damage


class Army(CompositeUnit):
    """
    Common Army
    Composite Squad in units
    """
    units: List[Squad]
    _composites_class: List[Squad] = [Squad]
    id: int = 0

    def __str__(self):
        return f"Army {self.id}:" + super().__str__()

    def add_unit(self, unit: Union[Squad]):
        self.units.append(unit)

    @classmethod
    def create(cls, *, count=1, **kwargs):
        """
        :param kwargs: health float; recharge int for soldier in Vehicle; squad_count for count squad in army
        :return: Squad object
        """
        return super().create(count=kwargs.get('squad_count', 0), **kwargs)

    def get_damage_amount(self):
        return sum([unit.get_damage_amount() for unit in self.get_alive_units() if unit.is_active()])

    def get_attack_success(self):
        return statistics.fmean([unit.get_attack_success() for unit in self.get_alive_units() if unit.is_active()])

    def is_active(self):
        return any([unit.is_active() for unit in self.units])

    def attack(self) -> float:
        return self.get_damage_amount()

    def taking_damage(self, amount):
        pass
