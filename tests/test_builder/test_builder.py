from battle_fields import BattleField
from battle_fields.strategies import Strategies
from builder import BattleBuilder
from units import Army, Squad, Soldier, Vehicle
from utils import Config


def test_builder_battle_field():
    config = Config(
        armies_count=2,
        squad_count=5,
        unit_count=5,
        strategy_name=Strategies.random.value
    )
    battle_field: BattleField = BattleBuilder(**config.dict()).get_result()
    assert isinstance(battle_field, BattleField)
    assert isinstance(battle_field.armies[0], Army)
    assert isinstance(battle_field.armies[0].units[0], Squad)
    assert isinstance(battle_field.armies[0].units[0].units[0], Soldier) or isinstance(
        battle_field.armies[0].units[0].units[0], Vehicle)
    assert len(battle_field.armies) == config.armies_count
    assert len(battle_field.armies[0].units) == config.squad_count
    assert len(battle_field.armies[0].units[0].units) == config.unit_count
