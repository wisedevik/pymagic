from typing import Optional
from titan.datastream.checksum_encoder import ChecksumEncoder
from titan.debug.debugger import Debugger
from titan.math.logic_long import LogicLong


class ByteStream(ChecksumEncoder):
    def __init__(self, capacity: int) -> None:
        super().__init__()
        self.bit_index: int = 0
        self.buffer: bytearray = bytearray(capacity)
        self.length: int = 0
        self.offset: int = 0

    def get_length(self) -> int:
        if self.offset < self.length:
            return self.length
        return self.offset

    def get_offset(self) -> int:
        return self.offset

    def is_at_end(self) -> bool:
        return self.offset >= self.length

    def clear(self, capacity: int) -> None:
        self.buffer = bytearray(capacity)
        self.offset = 0

    def get_byte_array(self) -> bytearray:
        return self.buffer

    def read_boolean(self) -> bool:
        if self.bit_index == 0:
            self.offset += 1

        value: bool = (self.buffer[self.offset - 1] & (1 << self.bit_index)) != 0
        self.bit_index = (self.bit_index + 1) & 7
        return value

    def read_byte(self) -> int:
        self.bit_index = 0
        value = self.buffer[self.offset]
        self.offset += 1
        return value

    def read_short(self) -> int:
        self.bit_index = 0
        value = (self.buffer[self.offset] << 8) | self.buffer[self.offset + 1]
        self.offset += 2
        return value

    def read_int(self) -> int:
        self.bit_index = 0
        value = (
            (self.buffer[self.offset] << 24)
            | (self.buffer[self.offset + 1] << 16)
            | (self.buffer[self.offset + 2] << 8)
            | self.buffer[self.offset + 3]
        )
        self.offset += 4
        return value

    def read_long(self) -> LogicLong:
        long = LogicLong()
        long.decode(self)
        return long

    def read_bytes_length(self) -> int:
        return self.read_int()

    def read_bytes(self, length: int, max_capacity: int) -> Optional[bytearray]:
        self.bit_index = 0

        if length <= -1:
            if length != -1:
                Debugger.warning("Negative read_bytes length encountered.")
            return None

        if length <= max_capacity:
            array = self.buffer[self.offset : self.offset + length]
            self.offset += length
            return array

        Debugger.warning(f"read_bytes too long array, max {max_capacity}")
        return None

    def read_string(self, max_capacity: int = 900001) -> Optional[str]:
        length = self.read_bytes_length()

        if length == -1:
            if length != -1:
                Debugger.warning("Too long String encountered.")
            return None

        if length <= max_capacity:
            byte_array = self.buffer[self.offset : self.offset + length]
            string_value = byte_array.decode("utf-8")
            self.offset += length
            return string_value

        Debugger.warning(f"Too long String encountered, max {max_capacity}")
        return None

    def read_string_reference(self, max_capacity: int = 900000) -> str:
        length = self.read_bytes_length()

        if length <= -1:
            Debugger.warning("Negative String length encountered.")
        elif length <= max_capacity:
            byte_array = self.buffer[self.offset : self.offset + length]
            string_value = byte_array.decode("utf-8")
            self.offset += length
            return string_value
        else:
            Debugger.warning(f"Too long String encountered, max {max_capacity}")

        return ""

    def write_boolean(self, value: bool) -> None:
        super().write_boolean(value)

        if self.bit_index == 0:
            self.ensure_capacity(1)
            self.buffer[self.offset] = 0
            self.offset += 1

        if value:
            self.buffer[self.offset - 1] |= (1 << self.bit_index) & 0xFF

        self.bit_index = (self.bit_index + 1) & 7

    def write_byte(self, value: int) -> None:
        super().write_byte(value)
        self.ensure_capacity(1)
        self.bit_index = 0
        self.buffer[self.offset] = value
        self.offset += 1

    def write_short(self, value: int) -> None:
        super().write_short(value)
        self.ensure_capacity(2)
        self.bit_index = 0
        self.buffer[self.offset] = (value >> 8) & 0xFF
        self.buffer[self.offset + 1] = value & 0xFF
        self.offset += 2

    def write_int(self, value: int) -> None:
        super().write_int(value)
        self.ensure_capacity(4)
        self.bit_index = 0
        self.buffer[self.offset] = (value >> 24) & 0xFF
        self.buffer[self.offset + 1] = (value >> 16) & 0xFF
        self.buffer[self.offset + 2] = (value >> 8) & 0xFF
        self.buffer[self.offset + 3] = value & 0xFF
        self.offset += 4

    def write_int_to_byte_array(self, value: int) -> None:
        self.write_int(value)

    def write_bytes(self, value: bytearray, length: int) -> None:
        super().write_bytes(value, length)

        if value is None:
            self.write_int(-1)
        else:
            self.ensure_capacity(length + 4)
            self.write_int(length)
            self.buffer[self.offset : self.offset + length] = value
            self.offset += length

    def write_string(self, value: str) -> None:
        super().write_string(value)

        if value is None:
            self.write_int(-1)
        else:
            bytes_value = value.encode("utf-8")
            length = len(bytes_value)

            if length <= 900001:
                self.ensure_capacity(length + 4)
                self.write_int(length)
                self.buffer[self.offset : self.offset + length] = bytes_value
                self.offset += length
            else:
                print(f"ByteStream.write_string invalid string length {length}")
                self.write_int(-1)

    def write_string_reference(self, value: str) -> None:
        super().write_string_reference(value)
        bytes_value = value.encode("utf-8")
        length = len(bytes_value)

        if length <= 900001:
            self.ensure_capacity(length + 4)
            self.write_int(length)
            self.buffer[self.offset : self.offset + length] = bytes_value
            self.offset += length
        else:
            print(f"ByteStream.write_string invalid string length {length}")
            self.write_int(-1)

    def reset_offset(self) -> None:
        self.offset = 0
        self.bit_index = 0

    def set_byte_array(self, buffer: bytearray, length: int) -> None:
        self.offset = 0
        self.bit_index = 0
        self.buffer = buffer
        self.length = length

    def set_offset(self, offset: int) -> None:
        self.offset = offset
        self.bit_index = 0

    def ensure_capacity(self, capacity: int) -> None:
        buffer_length = len(self.buffer)

        if self.offset + capacity > buffer_length:
            tmp_buffer = bytearray(buffer_length + capacity + 100)
            tmp_buffer[:buffer_length] = self.buffer
            self.buffer = tmp_buffer
