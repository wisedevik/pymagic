from typing import cast
from logic.avatar.logic_client_avatar import LogicClientAvatar
from logic.home.logic_client_home import LogicClientHome
from logic.messages.home.end_client_turn_message import EndClientTurnMessage
from server.mode.game_mode import GameMode
from server.config import Configuration
from logic import LogicVersion
from logic.messages.auth import LoginMessage
from logic.messages.auth import LoginOkMessage
from server.resources.resource_manager import ResourceManager
from server.util.util import Util
from titan.debug import Debugger
from titan.math import LogicLong
from titan.message import PiranhaMessage

from logic.messages.home import OwnHomeDataMessage
from server.database import AccountCrud


class MessageManager:
    def __init__(self, connection):
        self.connection = connection

    async def receive_message(self, message: PiranhaMessage):
        Debugger.print(f"Received message of type: {message.get_message_type()}")

        match message.get_message_type():
            case LoginMessage.MESSAGE_TYPE:
                await self.on_login_message(cast(LoginMessage, message))
            case EndClientTurnMessage.MESSAGE_TYPE:
                await self.on_end_client_turn_message(
                    cast(EndClientTurnMessage, message)
                )
            case _:
                ...

    async def on_end_client_turn_message(self, message: EndClientTurnMessage) -> None:
        game_mode: GameMode = self.connection.get_game_mode()

        if game_mode:
            game_mode.on_client_turn_received(
                message.sub_tick, message.checksum, message.commands
            )

    async def on_login_message(self, message: LoginMessage):
        Debugger.print(
            f"Received new login, pass_token={message.pass_token!r}, account_id={message.account_id}"
        )

        account = await AccountCrud.get_account_by_token(message.pass_token)

        if (
            not account
            and message.account_id.low_integer == 0
            and message.pass_token is None
        ):
            account = await AccountCrud.create_account(Util.random_string())
        elif not account:
            Debugger.print("Invalid login attempt")
            return

        login_ok = LoginOkMessage()
        login_ok.account_id = LogicLong(0, account.id)
        login_ok.home_id = LogicLong(0, account.id)
        login_ok.pass_token = account.pass_token
        login_ok.environment = Configuration.game.environment
        login_ok.major_version = LogicVersion.major_version
        login_ok.build = LogicVersion.build
        login_ok.minor_version = LogicVersion.content_version

        await self.connection.send_message(login_ok)

        own_home_data_message = OwnHomeDataMessage()
        home = LogicClientHome()
        home.set_home_json(ResourceManager.STARTING_HOME_JSON)
        own_home_data_message.set_seconds_since_last_save(0)
        own_home_data_message.set_home(home)
        own_home_data_message.set_avatar(LogicClientAvatar.get_default_avatar());

        await self.connection.send_message(own_home_data_message)
