import math

class LogicGamePlayUtil:
    @staticmethod
    def dps_to_single_hit(dps: int, ms: int):
        tmp = (27487790700 * dps * ms) >> 32
        return int((tmp >> 6) + (tmp >> 31))

    @staticmethod
    def time_to_xp(time: int):
        return math.sqrt(time)
