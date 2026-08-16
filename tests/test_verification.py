from datetime import datetime, timezone

from app.agent import ReconciliationAgent
from app.history import load_history
from app.models import ProductData, SourceUpdate


def test_verified_outcome_updates_history(tmp_path, monkeypatch):
    import app.history as history_module

    history_file = tmp_path / "source_history.json"

    history_file.write_text(
        """
        {
            "supplier_a": {
                "correct": 9,
                "incorrect": 1
            }
        }
        """,
        encoding="utf-8",
    )

    monkeypatch.setattr(
        history_module,
        "HISTORY_FILE",
        history_file,
    )

    agent = ReconciliationAgent()

    agent.verify_source_outcome(
        source_id="supplier_a",
        was_correct=True,
    )

    history = load_history()

    assert history["supplier_a"]["correct"] == 10
    assert history["supplier_a"]["incorrect"] == 1


def test_verified_incorrect_outcome_updates_history(
    tmp_path,
    monkeypatch,
):
    import app.history as history_module

    history_file = tmp_path / "source_history.json"

    history_file.write_text(
        """
        {
            "marketplace_b": {
                "correct": 7,
                "incorrect": 3
            }
        }
        """,
        encoding="utf-8",
    )

    monkeypatch.setattr(
        history_module,
        "HISTORY_FILE",
        history_file,
    )

    agent = ReconciliationAgent()

    agent.verify_source_outcome(
        source_id="marketplace_b",
        was_correct=False,
    )

    history = load_history()

    assert history["marketplace_b"]["correct"] == 7
    assert history["marketplace_b"]["incorrect"] == 4

def test_reconciliation_does_not_automatically_update_history(
    tmp_path,
    monkeypatch,
):
    import app.history as history_module

    history_file = tmp_path / "source_history.json"

    history_file.write_text(
        """
        {
            "supplier_a": {
                "correct": 9,
                "incorrect": 1
            },
            "marketplace_b": {
                "correct": 7,
                "incorrect": 3
            }
        }
        """,
        encoding="utf-8",
    )

    monkeypatch.setattr(
        history_module,
        "HISTORY_FILE",
        history_file,
    )

    supplier = SourceUpdate(
        source_id="supplier_a",
        timestamp=datetime.now(timezone.utc),
        product=ProductData(
            product_id="LAPTOP-005",
            price=999.00,
            stock=12,
        ),
        metadata={"source_type": "supplier"},
    )

    marketplace = SourceUpdate(
        source_id="marketplace_b",
        timestamp=datetime.now(timezone.utc),
        product=ProductData(
            product_id="LAPTOP-005",
            price=799.00,
            stock=12,
        ),
        metadata={"source_type": "marketplace"},
    )

    agent = ReconciliationAgent()

    agent.reconcile([
        supplier,
        marketplace,
    ])

    history = load_history()

    assert history["supplier_a"]["correct"] == 9
    assert history["supplier_a"]["incorrect"] == 1

    assert history["marketplace_b"]["correct"] == 7
    assert history["marketplace_b"]["incorrect"] == 3