from logic.command.logic_command import LogicCommand
from logic.level.logic_level import LogicLevel
from titan.datastream.byte_stream import ByteStream
from titan.debug.debugger import Debugger


class LogicNewsSeenCommand(LogicCommand):
    def __init__(self) -> None:
        super().__init__()
        self.news_seen = 0

    def decode(self, stream: ByteStream) -> None:
        self.news_seen = stream.read_int()
        super().decode(stream)

    def execute(self, level: LogicLevel) -> int:
        Debugger.print(f"news_seen={self.news_seen}")
        level.set_last_seen_news(self.news_seen)
        return 0

    def get_command_type(self) -> int:
        return 539
