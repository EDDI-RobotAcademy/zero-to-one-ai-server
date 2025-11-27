import boto3
from botocore.client import Config
from review.application.port.pdf_port import StoragePort
from config.cloud_config import (
    AWS_ACCESS_KEY_ID,
    AWS_SECRET_ACCESS_KEY,
    AWS_REGION,
    AWS_S3_BUCKET
)

# S3에 파일 업로드하고 접근 가능한 URL 반환
class S3UploaderAdapter(StoragePort):

    def __init__(self):
        self.s3 = boto3.client(
            "s3",
            region_name=AWS_REGION,
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            config=Config(signature_version="s3v4")
        )
        self.bucket = AWS_S3_BUCKET

    # 파일명과 바이트 데이터를 받아 S3에 저장 후 URL 생성
    def upload(self, filename: str, file_bytes: bytes) -> str:
        self.s3.put_object(
            Bucket=self.bucket,
            Key=filename,
            Body=file_bytes,
            ContentType="application/pdf"
        )

        static_url = f"https://{self.bucket}.s3.{AWS_REGION}.amazonaws.com/{filename}"

        return static_url