from typing import cast
from config import Config
from logic import LogicVersion
from logic.messages.auth import LoginMessage
from logic.messages.auth import LoginOkMessage
from titan.debug import Debugger
from titan.math import LogicLong
from titan.message import PiranhaMessage

from logic.messages.home import OwnHomeDataMessage


class MessageManager:
    def __init__(self, connection):
        self._connection = connection

    async def receive_message(self, message: PiranhaMessage):
        Debugger.print(
            f"[MessageManager.receive_message] message_type={message.get_message_type()}"
        )
        match message.get_message_type():
            case 10101:
                await self.on_login_message(cast(LoginMessage, message))
            case _:
                ...

    async def on_login_message(self, message: LoginMessage):
        Debugger.print(
            f"Tryna log in id={message._account_id} token={message.pass_token} v={message.get_version()}"
        )

        loginOk = LoginOkMessage()
        loginOk.account_id = LogicLong(0, 1)
        loginOk.home_id = LogicLong(0, 1)
        loginOk.pass_token = "secret@token"
        loginOk.environment = Config.get("environment")
        loginOk.major_version = LogicVersion.major_version()
        loginOk.build = LogicVersion.build()
        loginOk.minor_version = LogicVersion.content_version()

        Debugger.print(
            f"s_v: {LogicVersion.major_version()}.{LogicVersion.build()}.{LogicVersion.content_version()}"
        )

        await self._connection.send_message(loginOk)
