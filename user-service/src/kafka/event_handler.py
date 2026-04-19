from abc import ABC, abstractmethod


class EventHandler(ABC):

    @abstractmethod
    def run(self, message: bytes) -> None:
        pass
