from datetime import datetime, timezone

from app.models import ProductData, SourceUpdate
from app.validator import validate_update


def test_valid_update_passes_validation():
    update = SourceUpdate(
        source_id="supplier_a",
        timestamp=datetime.now(timezone.utc),
        product=ProductData(
            product_id="LAPTOP-001",
            price=999.00,
            stock=12,
        ),
        metadata={"source_type": "supplier"},
    )

    is_valid, errors = validate_update(update)

    assert is_valid is True
    assert errors == []


def test_negative_price_fails_validation():
    update = SourceUpdate(
        source_id="supplier_a",
        timestamp=datetime.now(timezone.utc),
        product=ProductData(
            product_id="LAPTOP-001",
            price=-100.00,
            stock=12,
        ),
        metadata={"source_type": "supplier"},
    )

    is_valid, errors = validate_update(update)

    assert is_valid is False
    assert "Price cannot be negative." in errors