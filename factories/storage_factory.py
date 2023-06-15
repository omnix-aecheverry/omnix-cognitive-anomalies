"""Storage factory module."""
import os
from services.storage.azure_blob_storage import AzureBlobStorage
from services.storage.aws_s3 import AmazonS3


storage = {
    "azure": AzureBlobStorage,
    "aws": AmazonS3
}

class StorageFactory:
    """Storage factory class."""
    def create_storage(self):
        """Create storage."""
        storage_type = os.environ.get("STORAGE_IMPL", "azure")
        return storage[storage_type]()
