from typing import Dict, Type
from logic.level.logic_level import LogicLevel
from titan.datastream.byte_stream import ByteStream
from titan.datastream.checksum_encoder import ChecksumEncoder

commands_registry: Dict[int, Type["LogicCommand"]] = {}


class LogicCommandMeta(type):
    def __init__(cls, name, bases, attrs):
        super().__init__(name, bases, attrs)
        if name != "LogicCommand":
            instance = cls()
            commands_registry[instance.get_command_type()] = cls


class LogicCommand(metaclass=LogicCommandMeta):
    def __init__(self) -> None:
        self.execute_sub_tick = -1

    def destruct(self) -> None: ...

    def get_execute_sub_tick(self) -> int:
        return self.execute_sub_tick

    def set_execute_sub_tick(self, est) -> None:
        self.execute_sub_tick = est

    def execute(self, level: LogicLevel) -> int:
        return 0

    def encode(self, encoder: ChecksumEncoder) -> None:
        encoder.write_int(self.execute_sub_tick)

    def decode(self, stream: ByteStream) -> None:
        self.execute_sub_tick = stream.read_int()

    def get_command_type(self) -> int:
        return 0
