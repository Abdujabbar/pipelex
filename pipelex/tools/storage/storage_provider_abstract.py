from abc import ABC, abstractmethod



class StorageProviderAbstract(ABC):
    @abstractmethod
    def get_object(self, bucket_name: str, object_key: str) -> bytes:
        """Retrieve an object from the storage."""
        pass