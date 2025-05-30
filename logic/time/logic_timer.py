from logic.time import LogicTime
from titan.math import LogicMath


class LogicTimer:
    def __init__(self) -> None:
        self.remaining_time = 0

    def get_remaining_seconds(self, time: LogicTime) -> int:
        remaining = self.remaining_time - time.get_tick()

        if remaining >= 1:
            return max((remaining + 59) // 60, 1)

        return 0

    def start_timer(self, seconds: int, time: LogicTime):
        self.remaining_time = time.get_tick() + 60 * seconds

    def get_remaining_ms(self, time: LogicTime) -> int:
        tick_diff: int = self.remaining_time - time.get_tick()
        ms: int = 1000 * (tick_diff // 60)
        remainder: int = tick_diff % 60
        if remainder >= 1:
            ms += (2133 * remainder) >> 7

        return ms
