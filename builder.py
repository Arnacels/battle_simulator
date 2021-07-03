from battle_fields import BattleField


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

    def get_battle_field(self) -> BattleField:
        raise NotImplementedError

    def _create_battle_field(self) -> BattleField:
        raise NotImplementedError


class BattleBuilder(BattleBuilderBase):

    def get_battle_field(self) -> BattleField:
        return self._create_battle_field()

    def _create_battle_field(self) -> BattleField:
        battle_field = BattleField.create(squad_count=self._squad_count,
                                          unit_count=self._unit_count,
                                          armies_count=self._armies_count)
        battle_field.strategy = self._strategy_name
        return battle_field
