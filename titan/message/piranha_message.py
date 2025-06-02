from titan.datastream.byte_stream import ByteStream
from typing import Dict, Type

message_registry: Dict[int, Type["PiranhaMessage"]] = {}


class PiranhaMessageMeta(type):
    def __init__(cls, name, bases, attrs):
        super().__init__(name, bases, attrs)
        if name != "PiranhaMessage":
            instance = cls()
            if instance.is_client_to_server_message():
                message_registry[instance.get_message_type()] = cls


class PiranhaMessage(metaclass=PiranhaMessageMeta):
    def __init__(self) -> None:
        self.stream = ByteStream(10)
        self.version = 0

    def decode(self): ...

    def encode(self): ...

    def get_message_type(self) -> int:
        return 0

    def get_service_node_type(self) -> int:
        return -1

    def get_message_version(self) -> int:
        return self.version

    def set_message_version(self, version: int):
        self.version = version

    def is_server_to_client_message(self) -> bool:
        return self.get_message_type() >= 20000

    def is_client_to_server_message(self) -> bool:
        return self.get_message_type() <= 20000

    def get_message_bytes(self) -> bytearray:
        return self.stream.get_byte_array()

    def get_encoding_length(self) -> int:
        return self.stream.get_length()

    def get_byte_stream(self) -> ByteStream:
        return self.stream
