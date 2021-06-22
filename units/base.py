
class Unit(object):
    _health: float
    _recharge: int

    @property
    def health(self):
        return self._health

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

    def taking_damage(self, amount):
        raise NotImplementedError

    def attack(self):
        raise NotImplementedError


class CompositeUnit(Unit):
    units: list = []

    def add_unit(self, unit: Unit):
        raise NotImplementedError

    def remove_unit(self, unit: Unit):
        if unit in self.units:
            self.units.remove(unit)
