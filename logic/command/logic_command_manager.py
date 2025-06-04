from typing import Optional
from titan.datastream.byte_stream import ByteStream
from titan.datastream.checksum_encoder import ChecksumEncoder
from titan.debug.debugger import Debugger
from titan.util.logic_array_list import LogicArrayList


class LogicCommandManager:
    def __init__(self, level) -> None:
        from logic.command.logic_command import LogicCommand

        self.level = level
        self.commands: Optional[LogicArrayList[LogicCommand]] = LogicArrayList[
            LogicCommand
        ]()

    def add_command(self, command):
        if command:
            if self.level.get_state() == 4:
                command.destruct()
                command = None
            else:
                self.commands.add(command)

    def is_command_allowed_in_current_state(self, command) -> bool:
        command_type = command.get_command_type()
        state = self.level.get_state()

        if state == 4:
            Debugger.warning(
                "Execute command failed! Commands are not allowed in visit state."
            )
            return False

        if command_type <= 1000:
            if command_type >= 500 and command_type < 600 and state != 1:
                Debugger.warning(
                    "Execute command failed! Command is only allowed in home state"
                )
                return False
            if command_type >= 600 and command_type < 700 & state != 2 and state != 5:
                Debugger.warning(
                    "Execute command failed! Command is only allowed in attack state"
                )
                return False

        return True

    def sub_tick(self):
        sub_tick = self.level.get_logic_time().get_tick()
        if self.commands is not None:
            for i in range(self.commands.count):
                command = self.commands[i]
                if command.get_execute_sub_tick() < sub_tick:
                    Debugger.error(
                        f"Execute command failed! Command should have been executed already. "
                        + f"(type={command.get_command_type()} server_tick={sub_tick} command_tick={command.get_execute_sub_tick()})"
                    )

                if command.get_execute_sub_tick() == sub_tick:
                    if self.is_command_allowed_in_current_state(command):
                        if command.execute(self.level) == 0:
                            ...  # listener.command_executed(command);

                        self.commands.remove(command)
                    else:
                        Debugger.warning(
                            f"Execute command failed! Command not allowed in current state. (type={command.get_command_type()} current_state={self.level.get_state()}"
                        )

    @staticmethod
    def create_command(command_type):
        from logic.command.logic_command import commands_registry

        command = commands_registry.get(command_type)

        if command:
            return command
        else:
            Debugger.warning(f"Unknown command type: {command_type}")

    @staticmethod
    def encode_command(encoder: ChecksumEncoder, command) -> None:
        encoder.write_int(command.get_command_type())
        command.encode(encoder)

    @staticmethod
    def decode_command(stream: ByteStream):
        cmd_type = stream.read_int()
        command = LogicCommandManager.create_command(cmd_type)

        if command is None:
            Debugger.warning(
                f"Command {cmd_type} is NONE!"
            )  # temporarily until the debugger is fixed
        else:
            command.decode(stream)

        return command
