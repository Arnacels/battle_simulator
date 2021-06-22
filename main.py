from pydantic import BaseModel, Field, ValidationError

from battle_fields.strategies import Strategies
from builder import BattleBuilder
from battle_fields import BattleField


class Config(BaseModel):
    armies_count: int = Field(ge=2)
    strategy_name: Strategies = Field(title='/'.join([s.name for s in Strategies]))
    squad_count: int = Field(ge=2)
    unit_count: int = Field(ge=5, le=10)


def main():
    config = None
    while not config:
        fields_data = dict()
        for name, data in Config.schema().get('properties').items():
            data = input(f'Enter {data.get("title")}:')
            fields_data[name] = data
        try:
            config = Config(**fields_data)
        except ValidationError as exc:
            print('\n'.join([er.get('msg') for er in exc.errors()]))

    battle_field: BattleField = BattleBuilder(**config.dict()).get_result()
    active_armies = [army.is_active() for army in battle_field.armies]
    while len(active_armies) > 1:
        battle_field.battle()


if __name__ == '__main__':
    main()

