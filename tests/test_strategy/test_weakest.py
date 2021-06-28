from battle_fields import BattleField
from units import Army
from utils import Strategies
from tests.test_strategy.base import StrategyBase


class TestWeakest(StrategyBase):

    def test_strategy(self, battle_field: BattleField, army1: Army, army2: Army, army: Army):
        battle_field.strategy = Strategies.weakest.value
        before_health = army1.health
        battle_field.armies = [army1, army2, army]
        self.make_strongest(army1)
        battle_field.battle(army2)
        assert army2.health < before_health