"""Currency-aware market-data models.

The Israeli-market gotchas live HERE, explicitly, so nothing downstream guesses:
TASE quotes equities in agorot (1/100 ILS, currency code ILA) and feeds are
delayed. Every Quote carries currency + as_of + is_delayed.
"""

from datetime import date, datetime
from decimal import Decimal
from enum import StrEnum

from pydantic import BaseModel, Field


class Currency(StrEnum):
    USD = "USD"
    ILS = "ILS"
    ILA = "ILA"  # agorot = 1/100 ILS — how TASE/Yahoo quote Israeli equities


class Quote(BaseModel):
    symbol: str
    price: Decimal
    currency: Currency
    as_of: datetime
    is_delayed: bool = True  # assume delayed unless the source proves otherwise
    source: str

    def price_normalized(self) -> tuple[Decimal, Currency]:
        """Collapse agorot to ILS so downstream math never mixes scales."""
        if self.currency is Currency.ILA:
            return self.price / Decimal(100), Currency.ILS
        return self.price, self.currency


class Holding(BaseModel):
    symbol: str
    name: str | None = None
    weight: Decimal = Field(..., ge=0, le=1, description="Portfolio weight as a fraction")


class ExpenseRatio(BaseModel):
    symbol: str
    ratio: Decimal = Field(..., ge=0, description="Annual expense ratio as a fraction (0.0035)")
    as_of: date | None = None
    source: str


class FilingRef(BaseModel):
    doc_id: str
    symbol: str
    form_type: str  # "10-K", "10-Q", "prospectus", "maya_announcement", ...
    filed_at: date
    url: str
    language: str = "en"  # "he" for MAYA documents (Phase 8)
