from logic.data.core.logic_data import LogicData
from logic.helper import ByteStreamHelper
from titan.datastream.byte_stream import ByteStream
from titan.datastream.checksum_encoder import ChecksumEncoder


class LogicDataSlot:
    def __init__(self, data: LogicData, count: int) -> None:
        self.data = data
        self.count = count

    def encode(self, encoder: ChecksumEncoder):
        assert self.data is not None
        ByteStreamHelper.write_data_reference(encoder, self.data)
        encoder.write_int(self.count)

    def decode(self, stream: ByteStream):
        self.data = ByteStreamHelper.read_data_reference(stream)
        self.count = stream.read_int()

    def set_count(self, cnt):
        self.count = cnt
