import datetime
from calltracing import CallContext
from titan.debug.debugger_listener import DebuggerListener


class ServerDebugger(DebuggerListener):
    def __init__(self, file_name: str):
        self.file = open(file_name, "a")

    def _timestamp(self) -> str:
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def _log(self, level: str, message: str, color_code: str) -> None:
        timestamp = self._timestamp()
        caller_info = CallContext.get_caller(3)
        log = f"[{level.upper()}] ({timestamp}) [{caller_info}] {message}"

        print(f"{color_code}{log}\033[0m")

        self.file.write(f"{log}\n")
        self.file.flush()

    def print(self, message: str) -> None:
        self._log("INFO", message, "\033[37m")

    def warning(self, message: str) -> None:
        self._log("WARNING", message, "\033[33m")

    def error(self, message: str) -> None:
        self._log("ERROR", message, "\033[31m")

    def hud_print(self, message: str) -> None:
        self._log("HUD", message, "\033[32m")
