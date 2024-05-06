import boto3
from typing import List, Optional

from app.core.config import settings


class S3:
    def __init__(
        self,
        aws_access_key_id: str,
        aws_secret_access_key: str,
        bucket_name: str,
        client: Optional[boto3.client] = None,
    ):
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key
        self.bucket_name = bucket_name
        self.client = client or boto3.client(
            "s3",
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key,
        )

    def upload_file(self, file, key):
        self.client.upload_fileobj(
            file.file,
            self.bucket_name,
            key,
            ExtraArgs={"ContentType": file.content_type},
        )
        return f"{settings.AWS_S3_BUCKET}.s3.amazonaws.com/{key}"

    def delete_file(self, key):
        self.client.delete_object(Bucket=self.bucket_name, Key=key)

    def get_file(self, key):
        return self.client.get_object(Bucket=self.bucket_name, Key=key)["Body"].read()

    def get_file_url(self, key):
        return f"https://{self.bucket_name}.s3.amazonaws.com/{key}"


s3_service = S3(
    aws_access_key_id=settings.AWS_S3_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_S3_SECRET_ACCESS_KEY,
    bucket_name=settings.AWS_S3_BUCKET,
)
