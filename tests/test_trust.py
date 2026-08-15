from datetime import datetime, timezone

from app.models import ProductData, SourceUpdate
from app.trust import calculate_trust_score


def test_supplier_has_higher_trust_than_marketplace():
    supplier_update = SourceUpdate(
        source_id="supplier_a",
        timestamp=datetime.now(timezone.utc),
        product=ProductData(
            product_id="LAPTOP-001",
            price=999.00,
            stock=12,
        ),
        metadata={"source_type": "supplier"},
    )

    marketplace_update = SourceUpdate(
        source_id="marketplace_b",
        timestamp=datetime.now(timezone.utc),
        product=ProductData(
            product_id="LAPTOP-001",
            price=799.00,
            stock=12,
        ),
        metadata={"source_type": "marketplace"},
    )

    supplier_score = calculate_trust_score(supplier_update)
    marketplace_score = calculate_trust_score(marketplace_update)

    assert supplier_score.total_score > marketplace_score.total_score