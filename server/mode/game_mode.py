import asyncio
from operator import imod

from sqlalchemy.sql.elements import conv
from logic.command.logic_command import LogicCommand
from logic.mode import logic_game_mode
from logic.mode.logic_game_mode import LogicGameMode
from server.database.crud.account_crud import AccountCrud
from titan.debug.debugger import Debugger
from titan.util.logic_array_list import LogicArrayList
from titan.json.logic_json_object import LogicJSONObject

class GameMode:
    def __init__(self, connection) -> None:
        self.logic_game_mode = LogicGameMode()
        self.connection = connection

    def on_client_turn_received(
        self, sub_tick: int, checksum: int, commands: LogicArrayList[LogicCommand]
    ):
        if (
            self.logic_game_mode.get_state() == 4
            or self.logic_game_mode.get_state() == 5
        ):
            return

        if commands:
            for i in range(commands.count):
                self.logic_game_mode.get_command_manager().add_command(commands[i])

        prev_sub_tick = self.logic_game_mode.get_level().get_logic_time().get_tick()

        for i in range(cnt := sub_tick - prev_sub_tick):
            self.logic_game_mode.update_one_sub_tick()

        self.save_state()

    def save_state(self):
        if (self.logic_game_mode.get_state() == 1):
            jsonObject = LogicJSONObject()
            self.logic_game_mode.save_to_json(jsonObject)
