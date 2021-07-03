import random

from pydantic import ValidationError

from battle_fields import BattleField
from builder import BattleBuilder
from utils import Config, print_armies_status


def main():
    config = config_read()
    battle_field: BattleField = BattleBuilder(**config.dict()).get_battle_field()  # Build battlefield

    field_after_battle = run_battle(battle_field)

    get_battle_result(field_after_battle)


def config_read():
    """
    Read config from stdin
    Use validator pydantic and pydantic schemas data
    """
    config = None
    while not config:
        fields_data = dict()
        for name, data in Config.schema().get('properties').items():
            data = input(f'Enter {data.get("title")}:')
            fields_data[name] = data
        try:
            config = Config(**fields_data)
        except ValidationError as exc:
            msgs = []
            for er in exc.errors():
                fields_error = ', '.join(er.get('loc'))
                msg_error = er.get('msg')
                msgs.append(f"{fields_error}: {msg_error}")
            print('\n'.join(msgs))
    return config


def run_battle(battle_field: BattleField):
    """
    Battle continues as long as there is more than one army on the battlefield,
    in each iteration an army is randomly selected and this army,
    according to the strategy chosen by the client, attacks another army.
    """
    while len(battle_field.get_alive_units()) > 1:
        active_armies = battle_field.get_active_units()
        if len(active_armies) > 1:
            army = random.choice(active_armies)
            battle_field.battle(army)
    return battle_field


def get_battle_result(battle_field: BattleField):
    print(print_armies_status(battle_field.units))
    print(f'Winner is {next(iter(battle_field.get_alive_units())).id}')


if __name__ == '__main__':
    main()
