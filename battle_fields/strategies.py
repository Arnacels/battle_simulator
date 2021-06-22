from typing import List

from units import Army


class Strategy(object):
    def battle(self, armies: List[Army]):
        raise NotImplementedError
