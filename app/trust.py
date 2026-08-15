from datetime import datetime, timezone

from app.history import calculate_historical_accuracy, load_history
from app.models import SourceUpdate, TrustScore


# Fixed weights used by the reconciliation strategy.
# These values are defined by the system and cannot be changed
# by information received from the external sources.
HISTORICAL_ACCURACY_WEIGHT = 0.60
COHERENCE_WEIGHT = 0.25
FRESHNESS_WEIGHT = 0.15


def calculate_coherence(update: SourceUpdate) -> float:
    """
    Calculate a basic coherence score for an update.

    The score is based on whether the product data passes basic
    consistency checks.
    """

    score = 1.0

    if update.product.price < 0:
        score -= 0.5

    if update.product.stock < 0:
        score -= 0.5

    return max(0.0, score)


def calculate_freshness(update: SourceUpdate) -> float:
    """
    Calculate how recent an update is.

    Newer updates receive a higher freshness score.
    """

    now = datetime.now(timezone.utc)
    age_seconds = (now - update.timestamp).total_seconds()

    if age_seconds <= 60:
        return 1.0

    if age_seconds <= 300:
        return 0.8

    if age_seconds <= 900:
        return 0.5

    return 0.2


def calculate_trust_score(update: SourceUpdate) -> TrustScore:
    """
    Calculate the trust score for a source using the fixed strategy.

    Historical accuracy comes from system-maintained history.
    Coherence and freshness are calculated using fixed rules.

    The source itself cannot influence any part of the scoring process.
    """

    history = load_history()

    historical_accuracy = calculate_historical_accuracy(
        update.source_id,
        history,
    )

    coherence_score = calculate_coherence(update)
    freshness_score = calculate_freshness(update)

    return TrustScore(
        source_id=update.source_id,
        historical_accuracy=historical_accuracy,
        coherence_score=coherence_score,
        freshness_score=freshness_score,
    )