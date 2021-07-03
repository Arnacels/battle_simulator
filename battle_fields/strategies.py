import random

from units import Army
from utils import Strategies


class Strategy(object):
    """
    Base strategy class
    in Strategy class implemented methods for execute battle with
    different params and tactics
    """
    def battle(self, attack_army: Army, battle_field):
        raise NotImplementedError

    @staticmethod
    def battle_squads(squads: list):
        lucky_squad = list(sorted(squads, key=lambda x: x.get_attack_success(), reverse=True))[0]
        squads.remove(lucky_squad)
        unlucky_squad = squads[0]
        unlucky_squad.taking_damage(lucky_squad.attack())


class RandomStrategy(Strategy):
    """
    Random strategy is strategy where attack army choose random squad for battle
    """
    name: str = Strategies.random.value

    def battle(self, attack_army: Army, battle_field):
        armies = battle_field.get_active_units()
        if attack_army in armies:
            armies.remove(attack_army)
        random_army = random.choice(armies)
        if random_army:
            squads = [random.choice(attack_army.units), random.choice(random_army.units)]
            self.battle_squads(squads)


class WeakestStrategy(Strategy):
    """
    Weakest strategy is strategy where attack army choose Weakest squad for battle
    """
    name: str = Strategies.weakest.value

    def battle(self, attack_army: Army, battle_field):
        weakest_army = battle_field.get_weakest(skip_unit=attack_army)
        weakest_army_squad = weakest_army.get_weakest()
        attack_army_squad = random.choice(attack_army.units)
        squads = [weakest_army_squad, attack_army_squad]

        self.battle_squads(squads)


class StrongestStrategy(Strategy):
    """
    Strongest strategy is strategy where attack army choose Strongest squad for battle
    """
    name: str = Strategies.strongest.value

    def battle(self, attack_army: Army, battle_field):
        strongest_army = battle_field.get_strongest(skip_unit=attack_army)
        strongest_army_squad = strongest_army.get_strongest()
        attack_army_squad = random.choice(attack_army.units)
        squads = [strongest_army_squad, attack_army_squad]

        self.battle_squads(squads)
