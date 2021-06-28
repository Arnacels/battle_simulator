from tests.test_unit.base import UnitBase


class TestSoldier(UnitBase):

    def test_active(self, soldier):
        super().test_active(soldier)

    def test_damage(self, soldier):
        super().test_damage(soldier)
        assert soldier.health == 50.0

    def test_attack(self, soldier):
        super().test_attack(soldier)
        assert soldier.get_exp() == 1
