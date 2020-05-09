import logging
import os
import uuid
from abc import ABC, abstractmethod
from typing import Any, Optional

import boto3
from boto3.exceptions import Boto3Error

logger = logging.getLogger(__name__)


class StorageClientException(Exception):
    def __init__(self, e: Exception) -> None:
        self.e = e

    def __str__(self) -> str:
        return str(self.e)


class StorageClient(ABC):
    @staticmethod
    def key_append_uuid(key: str) -> str:
        key_basename, key_ext = os.path.splitext(key)
        return f"{key_basename}_{uuid.uuid4().hex}{key_ext}"

    @abstractmethod
    def save(self, key: str, file: Any) -> None:
        pass

    @abstractmethod
    def get_url(self, key: str, *, content_type: Optional[str] = None) -> str:
        pass

    @abstractmethod
    def get_attachment_url(self, key: str, *, content_type: Optional[str] = None) -> str:
        pass


class AWSS3StorageClient(StorageClient):
    def __init__(self, bucket_name: str) -> None:
        self.bucket_name = bucket_name

    def save(self, key: str, file: Any) -> None:
        s3 = boto3.resource("s3")
        try:
            s3_obj = s3.Bucket(self.bucket_name).put_object(Key=key, Body=file)
            logger.info(f"s3 upload success: {s3_obj.bucket_name}/{s3_obj.key}")
        except Boto3Error as e:
            logger.info(f"s3 upload error: {e}")
            raise StorageClientException(e)

    def get_url(self, key: str, *, content_type: Optional[str] = None) -> str:
        params = {"Bucket": self.bucket_name, "Key": key}
        if content_type is not None:
            params["ResponseContentType"] = content_type
        try:
            return boto3.client("s3").generate_presigned_url(ClientMethod="get_object", Params=params, ExpiresIn=30)
        except Boto3Error as e:
            logger.error(f"s3 url gen error: {e}")
            raise StorageClientException(e)

    def get_attachment_url(self, key: str, *, content_type: Optional[str] = None) -> str:
        content_type = content_type or "application/octet-stream"
        try:
            return boto3.client("s3").generate_presigned_url(
                ClientMethod="get_object",
                Params={
                    "Bucket": self.bucket_name,
                    "Key": key,
                    "ResponseContentDisposition": f"attachment; filename={key}",
                    "ResponseContentType": content_type,
                },
                ExpiresIn=30,
            )
        except Boto3Error as e:
            logger.error(f"s3 url gen error: {e}")
            raise e
