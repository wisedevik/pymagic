from titan.datastream.checksum_encoder import ChecksumEncoder


class LogicBase:
    def __init__(self) -> None:
        self.logic_data_version = 0

    def encode(self, encoder: ChecksumEncoder):
        encoder.write_int(self.logic_data_version)
