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
        if (self.offset < self.length):
            return self.length

        return self.offset

    def get_offset(self) -> int:
        return self.offset

    def is_at_end(self) -> bool:
        return self.offset >= self.length

    def clear(self, capacity: int):
        self.buffer = bytearray(capacity)
        self.offset = 0

    def get_byte_array(self) -> bytearray:
        return self.buffer

    def read_roolean(self) -> bool:
        if (self.bit_index == 0):
            self.offset += 1

        value: bool = (self.buffer[self.offset - 1] & (1 << self.bit_index)) != 0
        self.bit_index = (self.bit_index + 1) & 7

        return value

    def read_byte(self):
        self.bit_index = 0
        value = self.buffer[self.offset]
        self.offset += 1
        return value

    def read_short(self):
        self.bit_index = 0

        value = (self.buffer[self.offset] << 8) | self.buffer[self.offset + 1]
        self.offset += 2

        return value

    def read_int(self):
        self.bit_index = 0

        value = (self.buffer[self.offset] << 24) | (self.buffer[self.offset + 1] << 16) | (self.buffer[self.offset + 2] << 8) | self.buffer[self.offset + 3]
        self.offset += 4

        return value

    def readLong(self) -> LogicLong:
        long: LogicLong = LogicLong()
        long.decode(self)
        return long

    def read_bytes_length(self) -> int:
        return self.read_int()

    def read_bytes(self, length: int, maxCapacity: int) -> Optional[bytearray]:
        self.bit_index = 0

        if (length <= -1):
            if (length != -1):
                Debugger.warning("Negative readBytes length encountered.")

            return None

        if (length <= maxCapacity):
            array: bytearray = self.buffer[self.offset: self.offset + length]
            self.offset += length
            return array

        Debugger.warning("readBytes too long array, max " + str(maxCapacity))
        return None

    def read_string(self, maxCapacity: int = 900001) -> Optional[str]:
        length: int = self.read_bytes_length()

        if (length == -1):
            if (length != -1):
                Debugger.warning("Too long String encountered.")

            return None
        else:
            if (length <= maxCapacity):
                byteArray: bytearray = self.buffer[self.offset: self.offset + length]
                stringValue: str = byteArray.decode("utf-8")
                self.offset += length
                return stringValue

            Debugger.warning("Too long String encountered, max " + str(maxCapacity))

        return None

    def read_string_reference(self, maxCapacity: int = 900000) -> str:
        length: int = self.read_bytes_length()

        if (length <= -1):
            Debugger.warning("Negative String length encountered.")

        else:
            if (length <= maxCapacity):
                byteArray: bytearray = self.buffer[self.offset: self.offset + length]
                stringValue: str = byteArray.decode("utf-8")
                self.offset += length
                return stringValue

            Debugger.warning("Too long String encountered, max " + str(maxCapacity))

        return ""


    def write_boolean(self, value: bool):
        super().write_boolean(value)

        if self.bit_index == 0:
            self.ensure_capacity(1)
            self.buffer[self.offset] = 0
            self.offset += 1

        if value:
            self.buffer[self.offset - 1] |= (1 << self.bit_index) & 0xFF

        self.bit_index = (self.bit_index + 1) & 7

    def write_byte(self, value: int):
        super().write_byte(value)

        self.ensure_capacity(1)

        self.bit_index = 0

        self.buffer[self.offset] = value
        self.offset += 1

    def write_short(self, value: int):
        super().write_short(value)

        self.ensure_capacity(2)

        self.bit_index = 0

        self.buffer[self.offset] = (value >> 8) & 0xFF
        self.buffer[self.offset + 1] = value & 0xFF

        self.offset += 2

    def write_int(self, value: int):
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

    def write_bytes(self, value: bytearray, length: int):
        super().write_bytes(value, length)

        if value is None:
            self.write_int(-1)
        else:
            self.ensure_capacity(length + 4)
            self.write_int(length)

            self.buffer[self.offset:self.offset + length] = value
            self.offset += length

    def write_string(self, value: str):
        super().write_string(value)

        if (value is None):
            self.write_int(-1)

        else:
            bytesValue: bytes = value.encode("utf-8")
            length: int = len(bytesValue)

            if (length <= 900001):
                self.ensure_capacity(length + 4)
                self.write_int(length)

                self.buffer[self.offset:self.offset + length] = bytesValue
                self.offset += length
            else:
                print("ByteStream::writeString invalid string length " + str(length))
                self.write_int(-1)

    def write_string_reference(self, value: str):
        super().write_string_reference(value)

        bytesValue: bytes = value.encode("utf-8")
        length: int = len(bytesValue)

        if (length <= 900001):
            self.ensure_capacity(length + 4)
            self.write_int(length)

            self.buffer[self.offset:self.offset + length] = bytesValue
            self.offset += length
        else:
            print("ByteStream::writeString invalid string length " + str(length))
            self.write_int(-1)


    def reset_offset(self):
        self.offset = 0
        self.bit_index = 0

    def set_byte_array(self, buffer: bytearray, length: int):
        self.offset = 0
        self.bit_index = 0
        self.buffer = buffer
        self.length = length

    def set_offset(self, offset: int):
        self.offset = offset
        self.bit_index = 0

    def ensure_capacity(self, capacity: int):
        bufferLength = len(self.buffer)

        if self.offset + capacity > bufferLength:
            tmpBuffer = bytearray(bufferLength + capacity + 100)
            tmpBuffer[:bufferLength] = self.buffer # copy from buffer to tmpBuffer by bufferLength
            self.buffer = tmpBuffer
