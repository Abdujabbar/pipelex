from abc import ABC, abstractmethod

from botocore.client import BaseClient


class StorageProviderAbstract(ABC):
    @abstractmethod
    def get_object(self, bucket_name: str, object_key: str) -> bytes:
        pass

    @abstractmethod
    def get_client(self) -> BaseClient:
        pass
