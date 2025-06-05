class LogicRandom:
    def __init__(self) -> None:
        self.iterated_random_seed = 0

    def set_iterated_random_seed(self, seed: int) -> None:
        self.iterated_random_seed = seed

    @staticmethod
    def iterate_random_seed(seed: int) -> int:
        if seed == 0:
            seed = -1

        tmp = seed ^ (seed << 13)
        tmp ^= (tmp >> 17)
        return tmp ^ (tmp * 32)
    
    def rand(self, max_value: int) -> int:
        if (max_value >= 1):
            self.iterated_random_seed = LogicRandom.iterate_random_seed(self.iterated_random_seed)

            seed: int
            if self.iterated_random_seed <= -1:
                seed = -self.iterated_random_seed
            else:
                seed = self.iterated_random_seed

            return seed % max_value

        return 0
            