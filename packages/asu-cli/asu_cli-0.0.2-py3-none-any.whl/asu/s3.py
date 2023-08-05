from typing import Dict, Generator, List, Optional, Sequence

import boto3
import botocore.exceptions


def create_bucket(name: str, kms_key_id: Optional[str],
                  tags: Optional[Dict[str, str]], public_access_block: bool) -> None:
    s3_client = boto3.client("s3")

    try:
        # Because CreateBucket returns 200 when a bucket already exists
        # we can't tell if the bucket already exists. Do an explicit check
        # and abort here if it exists.
        s3_client.head_bucket(Bucket=name)
        raise ValueError(f"Bucket {name} already exists")
    except botocore.exceptions.ClientError as e:
        if e.response.get('Error', {}).get('Code', None) != '404':
            raise e

    s3_client.create_bucket(Bucket=name)

    if kms_key_id:
        s3_client.put_bucket_encryption(Bucket=name, ServerSideEncryptionConfiguration={
            "Rules": [
                {"ApplyServerSideEncryptionByDefault":
                    {"SSEAlgorithm": "aws:kms",
                      "KMSMasterKeyID": kms_key_id
                     }
                 }
            ]})

    if tags:
        s3_client.put_bucket_tagging(Bucket=name, Tagging={"TagSet": [{"Key": k, "Value": v} for k, v in tags.items()]})

    if public_access_block:
        s3_client.put_public_access_block(Bucket=name, PublicAccessBlockConfiguration={
            'BlockPublicAcls': True,
            'IgnorePublicAcls': True,
            'BlockPublicPolicy': True,
            'RestrictPublicBuckets': True
        })


def list_buckets() -> Generator[Sequence[Optional[str]], None, None]:
    s3_client = boto3.client("s3")

    response = s3_client.list_buckets()

    yield ["Bucket"]
    for b in response["Buckets"]:
        yield [b["Name"]]


def describe_all_buckets_encryption() -> Generator[Sequence[Optional[str]], None, None]:

    s3_client = boto3.client("s3")

    response = s3_client.list_buckets()

    bucket_names: List[str] = [b["Name"] for b in response["Buckets"]]

    yield ["Bucket", "SSEAlgorithm", "KMSMasterKeyID"]

    for name in bucket_names:
        try:
            encryption = s3_client.get_bucket_encryption(Bucket=name)
            default_sse = encryption["ServerSideEncryptionConfiguration"]["Rules"][0]["ApplyServerSideEncryptionByDefault"]

        except botocore.exceptions.ClientError:
            default_sse = None

        if default_sse:
            yield [name, default_sse['SSEAlgorithm'], default_sse.get('KMSMasterKeyID', None)]
        else:
            yield [name, None, None]


def describe_all_buckets_tags(key: str) -> Generator[Sequence[Optional[str]], None, None]:

    s3_client = boto3.client("s3")

    response = s3_client.list_buckets()

    bucket_names: List[str] = [b["Name"] for b in response["Buckets"]]

    yield ["Bucket", f"Tag {key}"]

    for name in bucket_names:
        tagset = s3_client.get_bucket_tagging(Bucket=name)['TagSet']
        value = [tag['Value'] for tag in tagset if tag['Key'] == key]
        yield [name, value[0] if value else None]
