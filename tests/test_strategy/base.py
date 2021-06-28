from units import Army


class StrategyBase(object):

    def make_strongest(self, army: Army):
        for soldier in self.armies_soldiers(army):
            for _ in range(50):
                soldier.set_exp()

    @staticmethod
    def armies_soldiers(army: Army):
        soldiers = []

        def check_unit(unit):
            if hasattr(unit, 'units'):
                for unit in unit.units:
                    check_unit(unit)
            else:
                soldiers.append(unit)

        check_unit(army)
        return soldiers
