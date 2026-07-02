"""Filing fetcher — pulls documents via the DataSource layer (SEC EDGAR MCP;
MAYA feed via TASE in Phase 8), stores raw bytes in BlobStore, returns
FilingRef metadata. Phase 2."""

from investai.dataaccess.interface import DataSource
from investai.dataaccess.models import FilingRef
from investai.stores.blob_store import BlobStore


async def fetch_filing(
    symbol: str, form_type: str, *, source: DataSource, blobs: BlobStore
) -> FilingRef:
    raise NotImplementedError("Phase 2: filing fetch via EDGAR MCP")
