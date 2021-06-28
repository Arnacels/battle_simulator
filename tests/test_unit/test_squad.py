from tests.test_unit.base import UnitBase


class TestSquad(UnitBase):

    def test_active(self, squad):
        super().test_active(squad)

    def test_damage(self, squad):
        super().test_damage(squad)
        assert squad

    def test_attack(self, squad):
        attack_value = super().test_attack(squad)
        assert attack_value
