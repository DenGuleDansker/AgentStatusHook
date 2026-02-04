from abc import ABC, abstractmethod

class StatusProvider(ABC):
    name: str

    @abstractmethod
    def fetch(self) -> dict:
        pass

    @abstractmethod
    def normalize(self, raw: dict) -> list[dict]:
        pass
