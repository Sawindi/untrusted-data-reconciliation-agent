from app.history import calculate_historical_accuracy, load_history


def test_supplier_historical_accuracy():
    history = load_history()

    accuracy = calculate_historical_accuracy(
        "supplier_a",
        history,
    )

    assert accuracy == 0.90


def test_marketplace_historical_accuracy():
    history = load_history()

    accuracy = calculate_historical_accuracy(
        "marketplace_b",
        history,
    )

    assert accuracy == 0.70


def test_unknown_source_has_neutral_accuracy():
    history = load_history()

    accuracy = calculate_historical_accuracy(
        "unknown_source",
        history,
    )

    assert accuracy == 0.50