import random
import time

from pydantic import ValidationError

from battle_fields import BattleField
from builder import BattleBuilder
from utils import Config, filter_alive_units, filter_active_units, print_armies_status


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
            print('\n'.join([', '.join(er.get('loc')) + ': ' + er.get('msg') for er in exc.errors()]))

    battle_field: BattleField = BattleBuilder(**config.dict()).get_result()
    alive_armies = list(filter_alive_units(battle_field.armies))
    while len(alive_armies) > 1:
        active_armies = list(filter_active_units(alive_armies))
        if len(active_armies) > 1:
            army = random.choice(active_armies)
            battle_field.battle(army)
            alive_armies = list(filter_alive_units(battle_field.armies))
            time.sleep(1/5)

    print(print_armies_status(battle_field.armies))
    print(f'Winner is {next(filter_alive_units(battle_field.armies)).id}')


if __name__ == '__main__':
    main()

