import datetime
import inspect
from titan.debug.debugger_listener import DebuggerListener


class ServerDebugger(DebuggerListener):
    def __init__(self, file_name: str):
        self._file = open(file_name, "a")

    def _timestamp(self) -> str:
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def _get_caller_info(self) -> str:
        frame = inspect.currentframe()
        try:
            caller_frame = frame
            for _ in range(4):
                if caller_frame.f_back is None:
                    break
                caller_frame = caller_frame.f_back

            frame_info = inspect.getframeinfo(caller_frame)
            class_name = ""

            if "self" in caller_frame.f_locals:
                instance = caller_frame.f_locals["self"]
                class_name = instance.__class__.__name__ + "."

            return f"{class_name}{frame_info.function}"
        finally:
            del frame

    def _log(self, level: str, message: str, color_code: str) -> None:
        timestamp = self._timestamp()
        caller_info = self._get_caller_info()
        log_message = f"[{level.upper()}] ({timestamp}) [{caller_info}] {message}"

        print(f"{color_code}{log_message}\033[0m")

        self._file.write(f"{log_message}\n")
        self._file.flush()

    def print(self, message: str) -> None:
        self._log("INFO", message, "\033[37m")

    def warning(self, message: str) -> None:
        self._log("WARNING", message, "\033[33m")

    def error(self, message: str) -> None:
        self._log("ERROR", message, "\033[31m")

    def hud_print(self, message: str) -> None:
        self._log("HUD", message, "\033[32m")
