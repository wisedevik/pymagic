from titan.debug.debugger_listener import DebuggerListener


class Debugger:
    _listener: DebuggerListener | None = None

    @classmethod
    def set_listener(cls, listener: DebuggerListener) -> None:
        cls._listener = listener

    @classmethod
    def print(cls, message: str) -> None:
        if cls._listener:
            cls._listener.print(message)

    @classmethod
    def warning(cls, message: str) -> None:
        if cls._listener:
            cls._listener.warning(message)

    @classmethod
    def error(cls, message: str) -> None:
        if cls._listener:
            cls._listener.error(message)
        raise Exception(message)

    @classmethod
    def hud_print(cls, message: str) -> None:
        if cls._listener:
            cls._listener.hud_print(message)

    @classmethod
    def do_assert(cls, condition: bool, message: str) -> bool:
        if not condition:
            cls.error(message)
        return condition
