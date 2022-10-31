import os

import boto3


def upload_file_to_s3(
    AWS_ACCESS_KEY_ID,
    AWS_SECRET_ACCESS_KEY,
    bucket: str,
    file_name: str,
    object_name: str | bool = None,
    manifest: str = 'manifest-s3-nasdaq-httpx.json',
) -> bool:
    """Upload a file into S3 bucket
    :param AWS_SECRET_ACCESS_KEY: Secret key to connect into bucket
    :param AWS_ACCESS_KEY_ID: Secret password for bucket s3
    :param file_name: File to upload into S3 bucket
    :param bucket: The name of the S3 bucket
    :param object_name: S3 object name. If not specified then file_name is used
    :param manifest: Manifest that contains config for QuickSight
    :return: True if file was uploaded correctly into S3 bucket, otherwise returns False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = os.path.basename(file_name)

    session = boto3.Session(
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    )

    # Upload the file
    s3_client = session.resource("s3")
    ok_data = s3_client.meta.client.put_object(
        Body=file_name, Bucket=bucket, Key=object_name
    )

    ok_manifest = s3_client.meta.client.put_object(
        Body=manifest, Bucket=bucket, Key=manifest
    )

    res_data = ok_data.get("ResponseMetadata")
    res_manifest = ok_manifest.get("ResponseMetadata")

    if res_data.get("HTTPStatusCode") == 200 and res_manifest.get("HTTPStatusCode") == 200:
        print("Files has been uploaded successfully.")
    else:
        print("Files has NOT been uploaded successfully.")
        return False

    return True
