"""BlobStore seam — raw filings + large intermediate artifacts.

RunState stays under Step Functions' 256KB payload cap by keeping big things
here and carrying refs. Local: filesystem. AWS: S3.
"""

from typing import Protocol


class BlobStore(Protocol):
    async def put(self, key: str, data: bytes) -> str:
        """Store data, return a stable ref (the key)."""
        ...

    async def get(self, ref: str) -> bytes: ...


class LocalBlobStore:
    def __init__(self, base_dir: str) -> None:
        self._base_dir = base_dir

    async def put(self, key: str, data: bytes) -> str:
        raise NotImplementedError("Phase 1: filesystem blob store")

    async def get(self, ref: str) -> bytes:
        raise NotImplementedError("Phase 1: filesystem blob store")


class S3BlobStore:
    def __init__(self, bucket: str) -> None:
        self._bucket = bucket

    async def put(self, key: str, data: bytes) -> str:
        raise NotImplementedError("Phase 5: S3 blob store")

    async def get(self, ref: str) -> bytes:
        raise NotImplementedError("Phase 5: S3 blob store")
