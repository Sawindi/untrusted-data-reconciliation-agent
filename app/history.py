import json
from pathlib import Path


HISTORY_FILE = Path(__file__).parent.parent / "data" / "source_history.json"


def load_history() -> dict:
    """
    Load historical source outcomes from the local history file.

    The history is maintained by the reconciliation system and is
    never taken from the untrusted source data.
    """

    with HISTORY_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)


def calculate_historical_accuracy(
    source_id: str,
    history: dict,
) -> float:
    """
    Calculate historical accuracy from previous outcomes.

    Accuracy = correct outcomes / total outcomes.

    Unknown sources receive a neutral starting accuracy of 0.50.
    """

    source_history = history.get(source_id)

    if source_history is None:
        return 0.50

    correct = source_history.get("correct", 0)
    incorrect = source_history.get("incorrect", 0)

    total = correct + incorrect

    if total == 0:
        return 0.50

    return correct / total


def record_outcome(
    source_id: str,
    was_correct: bool,
) -> None:
    """
    Record the outcome of a reconciliation decision.

    Only the reconciliation system should call this function.
    """

    history = load_history()

    if source_id not in history:
        history[source_id] = {
            "correct": 0,
            "incorrect": 0,
        }

    if was_correct:
        history[source_id]["correct"] += 1
    else:
        history[source_id]["incorrect"] += 1

    with HISTORY_FILE.open("w", encoding="utf-8") as file:
        json.dump(history, file, indent=4)