from minio import Minio
from minio.error import S3Error
from ..core.config import settings
import os

client = Minio(
    settings.MINIO_ENDPOINT,
    access_key=settings.MINIO_ACCESS_KEY,
    secret_key=settings.MINIO_SECRET_KEY,
    secure=settings.MINIO_USE_SSL
)

async def save_file_to_storage(local_file_path: str, object_name: str, content_type: str = "application/octet-stream") -> str:
    """
    Uploads a file to MinIO object storage.
    Returns the path (object_name) of the file in storage.
    """
    bucket_name = settings.MINIO_BUCKET_NAME

    # Make sure bucket exists
    found = client.bucket_exists(bucket_name)
    if not found:
        client.make_bucket(bucket_name)
    # else:
    #     print(f"Bucket 	ható{bucket_name}" already exists")

    try:
        client.fput_object(
            bucket_name, object_name, local_file_path, content_type=content_type
        )
        # print(f" 	ható{local_file_path}" is successfully uploaded as object 	ható{object_name}" to bucket 	ható{bucket_name}".")
        return object_name # Or f"/{bucket_name}/{object_name}" if you want full path
    except S3Error as exc:
        print(f"Error occurred: {exc}")
        raise

async def get_file_from_storage(object_name: str, destination_path: str):
    """
    Downloads a file from MinIO to a local path.
    """
    bucket_name = settings.MINIO_BUCKET_NAME
    try:
        client.fget_object(bucket_name, object_name, destination_path)
        return destination_path
    except S3Error as exc:
        print(f"Error occurred: {exc}")
        raise

