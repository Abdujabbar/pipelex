from abc import ABC, abstractmethod
from typing import Any


class StorageProviderAbstract(ABC):
    @abstractmethod
    def load(self, uri: str) -> bytes:
        pass

    @abstractmethod
    def store(self, data: bytes) -> str:
        pass

    @abstractmethod
    def get_client(self) -> Any:
        pass
