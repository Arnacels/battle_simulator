import random

import pytest

import units
from battle_fields import BattleField
from units import Army


@pytest.fixture(scope='class')
def soldier():
    soldier_obj = soldier_builder()
    assert soldier_obj.health == 100.0
    yield soldier_obj


@pytest.fixture(scope='class')
def vehicle():
    vehicle_obj = vehicle_builder()
    assert vehicle_obj.health == 100.0
    yield vehicle_obj


@pytest.fixture(scope='class')
def squad():
    squad_obj = squad_builder()
    yield squad_obj


@pytest.fixture(scope='class')
def army():
    army_obj = Army()
    army_obj.id = 0
    army_obj.add_unit(squad_builder())
    army_obj.add_unit(squad_builder())
    yield army_obj


@pytest.fixture(scope='class')
def army1():
    army_obj = Army()
    army_obj.id = 1
    army_obj.add_unit(squad_builder())
    army_obj.add_unit(squad_builder())
    yield army_obj


@pytest.fixture(scope='class')
def army2():
    army_obj = Army()
    army_obj.id = 2
    army_obj.add_unit(squad_builder())
    army_obj.add_unit(squad_builder())
    yield army_obj


@pytest.fixture(scope='class')
def battle_field():
    yield BattleField(armies=[])


def soldier_builder():
    soldier_obj = units.Soldier()
    soldier_obj.health = 100.0
    soldier_obj.recharge = random.randint(100, 2000)
    return soldier_obj


def vehicle_builder():
    vehicle_obj = units.Vehicle()
    vehicle_obj.recharge = random.randint(1000, 3000)
    for _ in range(3):
        vehicle_obj.add_unit(soldier_builder())
    return vehicle_obj


def squad_builder():
    random_unit = random.choice((vehicle_builder, soldier_builder))
    squad_obj = units.Squad()
    for _ in range(5):
        squad_obj.add_unit(random_unit())
    return squad_obj
