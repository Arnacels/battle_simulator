
class Unit(object):
    __health: int
    __recharge: int

    @property
    def health(self):
        return self.__health

    @health.setter
    def health(self, value):
        self.__health = value

    def get_attack_success(self):
        raise NotImplementedError

    def get_damage_amount(self):
        raise NotImplementedError

    def get_exp(self):
        raise NotImplementedError

    def is_active(self):
        raise NotImplementedError

    def damage(self):
        raise NotImplementedError


class CompositeUnit(Unit):
    units: list

    def add_unit(self, unit: Unit):
        raise NotImplementedError

    def remove_unit(self, unit: Unit):
        raise NotImplementedError
