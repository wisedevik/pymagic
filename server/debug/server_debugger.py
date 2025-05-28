import datetime
from titan.debug.debugger_listener import DebuggerListener


class ServerDebugger(DebuggerListener):
    def __init__(self, file_name):
        self._file = open(file_name, "a")

    def _timestamp(self) -> str:
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def _log(self, level: str, message: str) -> None:
        timestamp = self._timestamp()
        formatted = f"[{level.upper()}] ({timestamp}) {message}\n"
        self._file.write(formatted)
        self._file.flush()
        print(formatted, end="")

    def print(self, message: str) -> None:
        self._log("INFO", message)

    def warning(self, message: str) -> None:
        self._log("WARNING", message)

    def error(self, message: str) -> None:
        self._log("ERROR", message)

    def hud_print(self, message: str) -> None:
        self._log("HUD", message)
