class LogicLong:
    def __init__(self, high_integer: int = 0, low_integer: int = 0) -> None:
        self.high_integer = high_integer
        self.low_integer = low_integer

    def decode(self, stream) -> None:
        self.high_integer = stream.read_int()
        self.low_integer = stream.read_int()

    def encode(self, encoder) -> None:
        encoder.write_int(self.high_integer)
        encoder.write_int(self.low_integer)

    def __str__(self) -> str:
        return f"LogicLong({self.high_integer},{self.low_integer})"
