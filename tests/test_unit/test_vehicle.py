from tests.test_unit.base import UnitBase


class TestVehicle(UnitBase):

    def test_active(self, vehicle):
        super().test_active(vehicle)

    def test_damage(self, vehicle):
        super().test_damage(vehicle)
        assert vehicle.health == 63.333333333333336

    def test_attack(self, vehicle):
        super().test_attack(vehicle)
        assert vehicle.get_exp() == 0.01
