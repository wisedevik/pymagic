from titan.datastream.byte_stream import ByteStream


class PiranhaMessage:
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

    def get_message_bytes(self) -> bytearray:
        return self.stream.get_byte_array()

    def get_encoding_length(self) -> int:
        return self.stream.get_length()

    def get_byte_stream(self) -> ByteStream:
        return self.stream
