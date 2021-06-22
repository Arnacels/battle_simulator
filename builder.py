from typing import List

from buttle_fields import BattleField
import units


class BattleBuilderBase(object):

    def __init__(self,
                 armies_count: int,
                 strategy_name: str,
                 squad_count: int,
                 unit_count: int
                 ):
        self.__armies_count = armies_count
        self.__strategy_name = strategy_name
        self.__squad_count = squad_count
        self.__unit_count = unit_count

    def _create_armies(self) -> List[units.Army]:
        raise NotImplementedError

    def _create_squads(self) -> List[units.Squad]:
        raise NotImplementedError

    def _create_battle_field(self) -> BattleField:
        raise NotImplementedError

    def get_result(self) -> BattleField:
        raise NotImplementedError


class BattleBuilder(BattleBuilderBase):
    pass
