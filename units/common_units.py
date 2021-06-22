from datetime import datetime, timedelta
import random
from typing import List, Union
import statistics

from .base import Unit, CompositeUnit


class Soldier(Unit):
    __exp: int = 0
    __last_attack: datetime

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
        return all((datetime.now() > self.__last_attack + timedelta(milliseconds=self._recharge),
                    self.health > 0))

    def taking_damage(self, amount):
        if self.health > 0:
            self.health -= amount

    def attack(self):
        self.set_exp()
        return self.get_damage_amount()


class Vehicle(CompositeUnit):
    units: List[Soldier] = []
    __last_attack: datetime

    @property
    def health(self):
        return statistics.mean([unit.health for unit in self.units if isinstance(unit.health, int)])

    @property
    def recharge(self):
        return self._recharge

    @recharge.setter
    def recharge(self, value):
        if value >= 1000:
            self._recharge = value

    def add_unit(self, unit: Soldier):
        if len(self.units) < 4:
            self.units.append(unit)

    def get_exp(self):
        return statistics.mean([unit.get_exp() / 100 for unit in self.units if unit.get_exp() > 0])

    def get_damage_amount(self):
        return 0.01 + self.get_exp() / 100

    def get_attack_success(self):
        return 0.5 * (1 + self.health / 100) * statistics.fmean([unit.get_attack_success() for unit in self.units])

    def is_active(self):
        return all((datetime.now() > self.__last_attack + timedelta(milliseconds=self._recharge),
                    self.health > 0))

    def taking_damage(self, amount):
        bad_luck_unit = random.choice(self.units)
        bad_luck_unit.taking_damage(amount * 0.2)
        for unit in self.units:
            unit.taking_damage(amount * 0.6)
            if unit != bad_luck_unit:
                unit.taking_damage(amount * 0.1)

    def attack(self):
        return self.get_damage_amount()


class Squad(CompositeUnit):
    units: List[Union[Soldier, Vehicle]] = []

    def add_unit(self, unit: Union[Soldier, Vehicle]):
        self.units.append(unit)

    def get_damage_amount(self):
        return sum([unit.get_attack_success() for unit in self.units if unit.is_active()])

    def get_attack_success(self):
        return statistics.fmean([unit.get_attack_success() for unit in self.units if unit.is_active()])

    def is_active(self):
        return any([unit.is_active() for unit in self.units])

    def taking_damage(self, amount):
        damage_per_unit = amount / len([unit for unit in self.units if unit.is_active()])
        for unit in self.units:
            unit.taking_damage(damage_per_unit)

    def attack(self):
        return self.get_damage_amount()


class Army(CompositeUnit):
    units: List[Squad] = []

    def add_unit(self, unit: Union[Squad]):
        self.units.append(unit)

    def get_damage_amount(self):
        return sum([unit.get_attack_success() for unit in self.units if unit.is_active()])

    def get_attack_success(self):
        return statistics.fmean([unit.get_attack_success() for unit in self.units])

    def is_active(self):
        return any([unit.is_active() for unit in self.units])
