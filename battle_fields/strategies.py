import random
from typing import List

from units import Army
from utils import Strategies, get_strongest, get_weakest


class Strategy(object):
    def battle(self, attack_army: Army, armies: List[Army]):
        raise NotImplementedError

    @staticmethod
    def battle_squads(squads: list):
        lucky_squad = list(sorted(squads, key=lambda x: x.get_attack_success(), reverse=True))[0]
        squads.remove(lucky_squad)
        unlucky_squad = squads[0]
        unlucky_squad.taking_damage(lucky_squad.attack())


class RandomStrategy(Strategy):
    name: str = Strategies.random.value

    def battle(self, attack_army: Army, armies: List[Army]):
        random_army = random.choice(armies)
        if random_army:
            squads = [random.choice(attack_army.units), random.choice(random_army.units)]
            self.battle_squads(squads)


class WeakestStrategy(Strategy):
    name: str = Strategies.weakest.value

    def battle(self, attack_army: Army, armies: List[Army]):
        weakest_army = get_weakest(armies)
        weakest_army_squad = get_weakest(weakest_army.units)
        attack_army_squad = random.choice(attack_army.units)
        squads = [weakest_army_squad, attack_army_squad]

        self.battle_squads(squads)


class StrongestStrategy(Strategy):
    name: str = Strategies.strongest.value

    def battle(self, attack_army: Army, armies: List[Army]):
        strongest_army = get_strongest(armies)
        strongest_army_squad = get_strongest(strongest_army.units)
        attack_army_squad = random.choice(attack_army.units)
        squads = [strongest_army_squad, attack_army_squad]

        self.battle_squads(squads)
