class UnitBase(object):

    def test_active(self, unit):
        assert unit.is_active()

    def test_damage(self, unit):
        unit.taking_damage(50)

    def test_attack(self, unit):
        attack_value = unit.attack()
        assert not unit.is_active()
        return attack_value
