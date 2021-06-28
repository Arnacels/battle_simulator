from enum import Enum

from pydantic import BaseModel, Field


class Strategies(str, Enum):
    random = 'random'
    weakest = 'weakest'
    strongest = 'strongest'


class Config(BaseModel):
    armies_count: int = Field(ge=2)
    strategy_name: Strategies = Field(title='/'.join([s.name for s in Strategies]))
    squad_count: int = Field(ge=2)
    unit_count: int = Field(ge=5, le=10)


def filter_active_units(units):
    return filter(lambda x: x.is_active(), units)


def filter_alive_units(units):
    return filter(lambda x: x.is_alive(), units)


def get_strongest(units: list):
    return next(
        iter(sorted(units, key=lambda x: x.get_damage_amount() and x.is_active() and x.is_alive(), reverse=True)))


def get_weakest(units: list):
    return next(iter(sorted(units, key=lambda x: x.get_damage_amount() and x.is_active() and x.is_alive())))


def print_armies_status(armies):
    for army in armies:
        print(f"Army #{army.id}")
        print(str(army))
