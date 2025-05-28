from titan.math.logic_long import LogicLong


class ChecksumEncoder:
    def __init__(self) -> None:
        self.checksum: int = 0
        self.snapshot_checksum: int = 0

        self.enabled: bool = True

    def enable_check_sum(self, enable: bool):
        if not self.enabled or enable:
            if not self.enabled and enable:
                self.checksum = self.snapshot_checksum

            self.enabled = enable
        else:
            self.snapshot_checksum = self.checksum
            self.enabled = False

    def reset_checksum(self):
        self.checksum = 0

    def write_boolean(self, value: bool):
        self.checksum = (13 if value else 7) + self.rotate_right(self.checksum, 31)

    def write_byte(self, value: int):
        self.checksum = value + self.rotate_right(self.checksum, 31) + 11

    def write_short(self, value: int):
        self.checksum = value + self.rotate_right(self.checksum, 31) + 19

    def write_int(self, value: int):
        self.checksum = value + self.rotate_right(self.checksum, 31) + 9

    def write_long(self, value: LogicLong):
        value.encode(self)

    def write_bytes(self, value: bytearray, length: int):
        self.checksum = (
            (length + 28 if value is not None else 27) + (self.checksum >> 31)
        ) | (self.checksum << (32 - 31))

    def write_string(self, value: str):
        self.checksum = (
            len(value) + 28 if value is not None else 27
        ) + self.rotate_right(self.checksum, 31)

    def write_string_reference(self, value: str):
        self.checksum = len(value) + self.rotate_right(self.checksum, 31) + 38

    def is_check_sum_enabled(self) -> bool:
        return self.enabled

    def is_check_sum_only_mode(self) -> bool:
        return True

    @staticmethod
    def rotate_right(value: int, count: int):
        return (value >> count) | (value << (32 - count))
