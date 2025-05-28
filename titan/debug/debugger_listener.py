from abc import ABC, abstractmethod


class DebuggerListener(ABC):
    @abstractmethod
    def hud_print(self, message: str) -> None:
        pass

    @abstractmethod
    def print(self, message: str) -> None:
        pass

    @abstractmethod
    def warning(self, message: str) -> None:
        pass

    @abstractmethod
    def error(self, message: str) -> None:
        pass
