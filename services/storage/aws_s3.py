"""AWS S3 Storage Service"""
import os
import boto3

class AmazonS3:
    """AWS S3 Storage Client."""
    def __init__(self):
        self.bucket_name = os.environ.get("AWS_S3_BUCKET_NAME")
        self.client = boto3.client(
            "s3",
            aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
            region_name=os.environ.get("AWS_REGION_NAME")
        )

    def upload(self, file_path, file_name):
        """Upload a file to S3."""
        self.client.upload_file(file_path, self.bucket_name, file_name)
        return {
            "url": self.get_url(file_name)
        }

    def download(self, file_name, file_path):
        """Download a file from S3."""
        self.client.download_file(self.bucket_name, file_name, file_path)

    def delete(self, file_name):
        """Delete a file from S3."""
        self.client.delete_object(Bucket=self.bucket_name, Key=file_name)

    def list(self):
        """List all files in S3."""
        return self.client.list_objects(Bucket=self.bucket_name)

    def get_url(self, file_name):
        """Get a file URL from S3."""
        return self.client.generate_presigned_url(
            ClientMethod="get_object",
            Params={
                "Bucket": self.bucket_name,
                "Key": file_name
            }
        )