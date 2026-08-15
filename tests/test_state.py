from app.models import ProductData
from app.state import ReconciledState


def test_reconciled_state_stores_product():
    state = ReconciledState()

    product = ProductData(
        product_id="LAPTOP-001",
        price=999.00,
        stock=12,
    )

    state.update(product)

    stored_product = state.get("LAPTOP-001")

    assert stored_product == product


def test_reconciled_state_returns_none_for_unknown_product():
    state = ReconciledState()

    assert state.get("UNKNOWN") is None


def test_reconciled_state_updates_existing_product():
    state = ReconciledState()

    original = ProductData(
        product_id="LAPTOP-001",
        price=999.00,
        stock=12,
    )

    updated = ProductData(
        product_id="LAPTOP-001",
        price=899.00,
        stock=10,
    )

    state.update(original)
    state.update(updated)

    stored_product = state.get("LAPTOP-001")

    assert stored_product == updated