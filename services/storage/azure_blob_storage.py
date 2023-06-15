"""Azure Storage Service."""
import os
from azure.storage.blob import BlobServiceClient
from azure.core.exceptions import ResourceNotFoundError

class AzureBlobStorage:
    """Azure Blob Storage Client."""

    def __init__(self):
        connection_string = os.environ.get("AZURE_STORAGE_CONNECTION_STRING")
        sas_token = os.environ.get("AZURE_STORAGE_SAS_TOKEN")
        container_name = os.environ.get("AZURE_STORAGE_CONTAINER_NAME")

        self._blob_service_client = BlobServiceClient(
            account_url=connection_string, credential=sas_token)
        self._container_client = self._blob_service_client.get_container_client(
            container_name)

    def upload(self, file_path, file_name):
        """Upload a file to Azure Blob Storage."""
        blob_client = self._container_client.get_blob_client(file_name)
        try:
            blob_client.get_blob_properties()
            return {
                "link": blob_client.url,
                "message": "The model already exists.",
            }
        except ResourceNotFoundError:
            with open(file_path, "rb") as data:
                blob_client.upload_blob(data)
            return {
                "link": blob_client.url,
                "message": "The model was successfully uploaded.",
            }

    def delete(self, file_name):
        """Delete a file from Azure Blob Storage."""
        blob_client = self._container_client.get_blob_client(file_name)
        blob_client.delete_blob()

    def clear(self):
        """Delete all files from Azure Blob Storage."""
        blob_list = self._container_client.list_blobs()
        for blob in blob_list:
            self.delete(blob.name)

    def download(self, file_path):
        """Download a file from Azure Blob Storage."""
        directory = os.path.dirname(file_path)
        os.makedirs(directory, exist_ok=True)
        blob_client = self._container_client.get_blob_client(file_path)
        with open(file_path, "wb") as my_blob:
            blob_data = blob_client.download_blob()
            blob_data.readinto(my_blob)
