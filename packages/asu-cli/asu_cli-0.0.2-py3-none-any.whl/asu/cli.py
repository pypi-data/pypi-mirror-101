import sys
from typing import List, Optional

import typer

import asu.display as display
import asu.s3 as s3

app = typer.Typer(help="AWS S3 CLI utils")


@app.command()
def create(name: str,
            kms_key_id: Optional[str] = typer.Option(default=None, help="SSE KMS master key ID"),
            tag: Optional[List[str]] = typer.Option(default=None, help="a name=value pair. Can be repeated to apply multiple tags."),
            public_access_block: bool = True) -> None:
    """Make bucket"""
    tags = {t[0]: t[1] for t in [t.split("=") for t in tag]}
    display.pretty_print(s3.create_bucket(name, kms_key_id, tags, public_access_block))


@app.command()
def ls() -> None:
    """List buckets"""
    display.pretty_print(s3.list_buckets())


@app.command()
def sse() -> None:
    """List default encryption for all buckets"""
    display.pretty_print(s3.describe_all_buckets_encryption())


@app.command()
def tags(key: str) -> None:
    """List tag for all buckets"""
    display.pretty_print(s3.describe_all_buckets_tags(key))


def main(args: List[str] = sys.argv[1:]) -> None:
    app(args)


if __name__ == "__main__":
    main()
