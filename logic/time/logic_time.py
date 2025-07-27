class LogicTime:
    def __init__(self) -> None:
        self.tick = 0
        self.full_tick = 0

    def is_full_tick(self) -> bool:
        return ((self.tick + 1) & 3) == 0

    def increase_sub_tick(self):
        self.tick += 1

        if ((self.tick + 1) & 3) == 0:
            self.full_tick += 1

    def get_tick(self) -> int:
        return self.tick

    def get_full_tick(self) -> int:
        return self.full_tick
