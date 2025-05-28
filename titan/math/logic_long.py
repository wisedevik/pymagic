class LogicLong:
    def __init__(self, highInteger: int = 0, lowInteger: int = 0) -> None:
        self.highInteger = highInteger
        self.lowInteger = lowInteger

    def decode(self, stream) -> None:
        self.highInteger = stream.read_int()
        self.lowInteger = stream.read_int()

    def encode(self, encoder) -> None:
        encoder.write_int(self.highInteger)
        encoder.write_int(self.lowInteger)

    def __str__(self) -> str:
        return f"LogicLong({self.highInteger}-{self.lowInteger})"
