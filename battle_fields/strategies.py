from typing import List
from enum import Enum
import random

from units import Army
from units.base import CompositeUnit


class Strategies(str, Enum):
    random = 'random'
    weakest = 'weakest'
    strongest = 'strongest'


class Strategy(object):
    def battle(self, attack_army: Army, armies: List[Army]):
        raise NotImplementedError


class RandomStrategy(Strategy):
    name: str = Strategies.random.value

    def battle(self, attack_army: Army, armies: List[Army]):
        random_army = random.choice(armies)

        squads = [random.choice(attack_army.units), random.choice(random_army.units)]
        battle_squads(squads)


class WeakestStrategy(Strategy):
    name: str = Strategies.weakest.value

    def battle(self, attack_army: Army, armies: List[Army]):
        weakest_army = get_weakest(armies)
        weakest_army_squad = get_weakest(weakest_army.units)
        attack_army_squad = get_weakest(attack_army.units)
        squads = [weakest_army_squad, attack_army_squad]

        battle_squads(squads)


class StrongestStrategy(Strategy):
    name: str = Strategies.strongest.value

    def battle(self, attack_army: Army, armies: List[Army]):
        strongest_army = get_strongest(armies)
        strongest_army_squad = get_strongest(strongest_army.units)
        attack_army_squad = get_strongest(attack_army.units)
        squads = [strongest_army_squad, attack_army_squad]

        battle_squads(squads)


def battle_squads(squads: list):
    lucky_squad = list(sorted(squads, key=lambda x: x.get_attack_success(), reverse=True))[0]
    squads.remove(lucky_squad)
    unlucky_squad = squads[0]
    unlucky_squad.taking_damage(lucky_squad.attack())


def get_strongest(units: list) -> CompositeUnit:
    return next(sorted(units, key=lambda x: x.get_damage_amount() and x.is_active(), reverse=True))


def get_weakest(units: list) -> CompositeUnit:
    return next(sorted(units, key=lambda x: x.get_damage_amount() and x.is_active()))
