from logic.data.core.logic_data import LogicData
from logic.data.tables.logic_data_tables import LogicDataTables
from titan.datastream.byte_stream import ByteStream
from titan.datastream.checksum_encoder import ChecksumEncoder


class ByteStreamHelper:
    @staticmethod
    def write_data_reference(encoder: ChecksumEncoder, data: LogicData):
        if data:
            encoder.write_int(data.get_global_id())
        else:
            encoder.write_int(0)

    @staticmethod
    def read_data_reference(stream: ByteStream):
        data = LogicDataTables.get_data_by_id(stream.read_int())
        return data
