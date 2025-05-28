from abc import ABC, abstractmethod


class LogicMessageFactory(ABC):
    @abstractmethod
    def create_message_by_type(self, type: int): ...
