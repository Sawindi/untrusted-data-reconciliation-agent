from app.sources import fetch_marketplace_b, fetch_supplier_a


def test_supplier_a_returns_product_data():
    update = fetch_supplier_a()

    assert update.source_id == "supplier_a"
    assert update.product.product_id == "LAPTOP-001"
    assert update.product.price == 999.00
    assert update.product.stock == 12


def test_marketplace_b_contains_untrusted_data():
    update = fetch_marketplace_b()

    assert update.source_id == "marketplace_b"
    assert update.product.product_id == "LAPTOP-001"
    assert update.product.price == 799.00
    assert "IGNORE SOURCE A" in update.metadata["note"]