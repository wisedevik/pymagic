from typing import cast
from titan.config import Configuration
from logic import LogicVersion
from logic.messages.auth import LoginMessage
from logic.messages.auth import LoginOkMessage
from titan.debug import Debugger
from titan.math import LogicLong
from titan.message import PiranhaMessage

from logic.messages.home import OwnHomeDataMessage


class MessageManager:
    def __init__(self, connection):
        self.connection = connection

    async def receive_message(self, message: PiranhaMessage):
        Debugger.print(f"Received message of type: {message.get_message_type()}")

        match message.get_message_type():
            case 10101:
                await self.on_login_message(cast(LoginMessage, message))
            case _:
                ...

    async def on_login_message(self, message: LoginMessage):
        Debugger.print(f"Received new login")

        login_ok = LoginOkMessage()
        login_ok.account_id = LogicLong(0, 32)
        login_ok.home_id = LogicLong(0, 32)
        login_ok.pass_token = "secret@token"
        login_ok.environment = Configuration.game.environment
        login_ok.major_version = LogicVersion.major_version
        login_ok.build = LogicVersion.build
        login_ok.minor_version = LogicVersion.content_version

        await self.connection.send_message(login_ok)
        await self.connection.send_message(OwnHomeDataMessage())
