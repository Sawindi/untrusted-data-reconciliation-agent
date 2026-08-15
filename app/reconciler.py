from app.models import SourceUpdate
from app.trust import calculate_trust_score


def detect_conflicts(
    updates: list[SourceUpdate],
) -> list[str]:
    """
    Identify product fields that contain conflicting values.

    Only the actual structured product fields are compared.
    Metadata is not used to influence the comparison.
    """

    conflicts: list[str] = []

    if not updates:
        return conflicts

    fields = ["price", "stock"]

    for field in fields:
        values = {
            getattr(update.product, field)
            for update in updates
        }

        if len(values) > 1:
            conflicts.append(field)

    return conflicts


def choose_winner(
    updates: list[SourceUpdate],
) -> tuple[SourceUpdate, dict[str, float]]:
    """
    Select the source with the highest trust score.

    The decision is based only on the fixed trust-scoring strategy.
    """

    scores = {}

    for update in updates:
        trust_score = calculate_trust_score(update)
        scores[update.source_id] = trust_score.total_score

    winner = max(
        updates,
        key=lambda update: scores[update.source_id],
    )

    return winner, scores