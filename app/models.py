from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass
class ProductData:
    """Represents the product information received from a data source."""

    product_id: str
    price: float
    stock: int


@dataclass
class SourceUpdate:
    """Represents an update received from one external source."""

    source_id: str
    timestamp: datetime
    product: ProductData
    metadata: dict[str, Any]


@dataclass
class TrustScore:
    """Stores the reliability scores calculated for a data source."""

    source_id: str
    historical_accuracy: float
    coherence_score: float
    freshness_score: float

    @property
    def total_score(self) -> float:
        """
        Calculate the source's overall trust score.

        The weights are fixed in code so that untrusted source data
        cannot influence or modify the conflict-resolution strategy.
        """
        return (
            0.60 * self.historical_accuracy
            + 0.25 * self.coherence_score
            + 0.15 * self.freshness_score
        )