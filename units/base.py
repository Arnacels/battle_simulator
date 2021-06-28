import statistics


class Unit(object):
    _health: float
    _recharge: int

    @property
    def health(self):
        return self._health if self._health > 0 else 0

    @health.setter
    def health(self, value):
        self._health = value

    @property
    def recharge(self):
        return self._recharge

    @recharge.setter
    def recharge(self, value):
        self._recharge = value

    def get_attack_success(self):
        raise NotImplementedError

    def get_damage_amount(self):
        raise NotImplementedError

    def get_exp(self):
        raise NotImplementedError

    def is_active(self):
        raise NotImplementedError

    def is_alive(self):
        raise NotImplementedError

    def taking_damage(self, amount):
        raise NotImplementedError

    def attack(self):
        raise NotImplementedError


class CompositeUnit(Unit):

    def __init__(self):
        self.units: list = []

    def __str__(self):
        info = f"Live units: {len(self.get_alive_units())} \nActive units: {len(self.get_active_units())} \n"
        info += "    ".join([str(unit) for unit in self.units]) + '\n'
        return info

    @property
    def health(self):
        return statistics.mean([unit.health for unit in self.units if unit.is_alive()])

    def add_unit(self, unit: Unit):
        raise NotImplementedError

    def remove_unit(self, unit: Unit):
        if unit in self.units:
            self.units.remove(unit)

    def is_alive(self):
        return any([unit.is_alive() for unit in self.units])

    def get_alive_units(self):
        return [unit for unit in self.units if unit.is_alive()]

    def get_active_units(self):
        return [unit for unit in self.units if unit.is_active()]
