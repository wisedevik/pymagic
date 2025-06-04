from logic.command.logic_command import LogicCommand
from logic.command.logic_command_manager import LogicCommandManager
from titan.debug.debugger import Debugger
from titan.message.piranha_message import PiranhaMessage
from titan.util.logic_array_list import LogicArrayList


MESSAGE_TYPE = 14102


class EndClientTurnMessage(PiranhaMessage):
    def __init__(self) -> None:
        super().__init__()
        self.sub_tick = 0
        self.checksum = 0
        self.commands: LogicArrayList[LogicCommand] = None

    def decode(self):
        super().decode()

        self.sub_tick = self.stream.read_int()
        self.checksum = self.stream.read_int()

        cnt = self.stream.read_int()
        if cnt <= 512:
            if cnt > 0:
                self.commands = LogicArrayList[LogicCommand](cnt)

                while cnt != 0:
                    command = LogicCommandManager.decode_command(self.stream)
                    if command is None:
                        break

                    self.commands.add(command)
                    cnt -= 1
        else:
            Debugger.warning(
                f"EndClientTurn.decode() command count is too high! ({cnt})"
            )

    def get_message_type(self) -> int:
        return MESSAGE_TYPE
