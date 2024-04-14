import boto3

from app.core.config import settings


class S3:
    def __init__(self):
        self.client = boto3.client(
            "s3",
            aws_access_key_id=settings.AWS_S3_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_S3_SECRET_ACCESS_KEY,
        )

    def upload_file(self, file, key):
        self.client.upload_fileobj(
            file.file,
            settings.AWS_S3_BUCKET,
            key,
            ExtraArgs={"ContentType": file.content_type},
        )
        return f"{settings.AWS_S3_BUCKET}.s3.amazonaws.com/{key}"

    def delete_file(self, key):
        self.client.delete_object(Bucket=settings.AWS_S3_BUCKET, Key=key)

    def get_file(self, key):
        return self.client.get_object(Bucket=settings.AWS_S3_BUCKET, Key=key)[
            "Body"
        ].read()

    def get_file_url(self, key):
        return f"https://{settings.AWS_S3_BUCKET}.s3.amazonaws.com/{key}"


s3_service = S3()
