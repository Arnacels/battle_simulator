import random
from enum import Enum

from pydantic import BaseModel, Field


class Strategies(str, Enum):
    random = 'random'
    weakest = 'weakest'
    strongest = 'strongest'


class Config(BaseModel):
    armies_count: int = Field(ge=2)
    squad_count: int = Field(ge=2)
    unit_count: int = Field(ge=5, le=10)
    strategy_name: Strategies = Field(title='/'.join([s.name for s in Strategies]))


class CompositeMixin(object):
    """
    Composite mixin
    Implement all methods for work with objects where unit compose units
    """
    _composites_class: list = None

    def __init__(self):
        self.units: list = []

    def add_unit(self, unit):
        self.units.append(unit)

    def remove_unit(self, unit):
        if unit in self.units:
            self.units.remove(unit)

    @classmethod
    def create(cls, *, count=1, **kwargs):
        if not cls._composites_class:
            raise ValueError('_composite_class not set')
        composite_unit = cls()
        for _ in range(count):
            unit_class = random.choice(composite_unit._composites_class)
            unit = unit_class.create(**kwargs)
            composite_unit.add_unit(unit)
        return composite_unit

    def get_alive_units(self):
        return [unit for unit in self.units if unit.is_alive()]

    def get_active_units(self):
        return [unit for unit in self.units if unit.is_active() and unit.is_alive()]

    def get_strongest(self, skip_unit=None):
        return self._get_by_strange(strongest=True, skip_unit=skip_unit)

    def get_weakest(self, skip_unit=None):
        return self._get_by_strange(strongest=False, skip_unit=skip_unit)

    def _get_by_strange(self, strongest: bool, skip_unit):
        return next(iter(sorted(self.units, key=lambda x: all((x.get_damage_amount(),
                                                               x.is_alive(),
                                                               x != skip_unit)), reverse=strongest)))


def print_armies_status(armies):
    for army in armies:
        print(f"Army #{army.id}")
        print(str(army))
