import random
from typing import List

from battle_fields import BattleField
import units


class BattleBuilderBase(object):

    def __init__(self,
                 armies_count: int,
                 strategy_name: str,
                 squad_count: int,
                 unit_count: int
                 ):
        self._armies_count = armies_count
        self._strategy_name = strategy_name
        self._squad_count = squad_count
        self._unit_count = unit_count

    def _create_armies(self) -> List[units.Army]:
        raise NotImplementedError

    def _create_squads(self) -> List[units.Squad]:
        raise NotImplementedError

    def _create_battle_field(self, strategy_name, armies) -> BattleField:
        raise NotImplementedError

    def get_result(self) -> BattleField:
        raise NotImplementedError


class BattleBuilder(BattleBuilderBase):

    def _create_army(self) -> units.Army:
        army = units.Army()
        for _ in range(self._squad_count):
            army.add_unit(self._create_squad())
        return army

    def _create_squad(self) -> units.Squad:
        random_unit = random.choice((self._create_vehicle, self._create_soldier))
        squad = units.Squad()
        for _ in range(self._unit_count):
            squad.add_unit(random_unit())
        return squad

    def _create_vehicle(self) -> units.Vehicle:
        vehicle = units.Vehicle()
        vehicle.recharge = random.randint(1000, 3000)
        for _ in range(random.randint(1, 3)):
            vehicle.add_unit(self._create_soldier())
        return vehicle

    def _create_soldier(self) -> units.Soldier:
        soldier = units.Soldier()
        soldier.health = 100.0
        soldier.recharge = random.randint(100, 2000)
        return soldier

    def _create_battle_field(self, strategy_name: str, armies: List[units.Army]) -> BattleField:
        battle_field = BattleField(armies)
        battle_field.strategy = strategy_name
        return battle_field

    def get_result(self) -> BattleField:
        armies = []
        for _ in range(self._armies_count):
            armies.append(self._create_army())
        return self._create_battle_field(self._strategy_name, armies)
