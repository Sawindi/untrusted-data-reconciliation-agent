from turtle import update

from app.audit import AuditLog
from app.history import record_outcome
from app.models import SourceUpdate
from app.reconciler import choose_winner, detect_conflicts
from app.state import ReconciledState
from app.trust import (
    HISTORICAL_ACCURACY_WEIGHT,
    COHERENCE_WEIGHT,
    FRESHNESS_WEIGHT,
    calculate_trust_score,
)
from app.validator import validate_update


class ReconciliationAgent:
    """
    Coordinates the complete reconciliation workflow.

    The agent treats all source data as untrusted. Source content is used only as data and never as instructions.
    """

    def __init__(self) -> None:
        self.state = ReconciledState()
        self.audit_log = AuditLog()

    def reconcile(
        self,
        updates: list[SourceUpdate],
    ) -> None:
        """
        Validate, compare, score, decide, store, and audit updates.
        """

        # 1. Validate incoming updates.
        valid_updates = [
            update
            for update in updates
            if validate_update(update)
        ]

        if not valid_updates:
            return

        # 2. Detect conflicts between valid updates.
        conflicts = detect_conflicts(valid_updates)

        # 3. If there are no conflicts, use the only/consistent value.
        if not conflicts:
            self._store_consistent_state(valid_updates)
            return

        # 4. Calculate trust scores using fixed system rules.
        winner, scores = choose_winner(valid_updates)

        trust_breakdown = {}

        for update in valid_updates:
            trust_score = calculate_trust_score(update)

            trust_breakdown[update.source_id] = {
                "historical_accuracy": trust_score.historical_accuracy,
                "coherence": trust_score.coherence_score,
                "freshness": trust_score.freshness_score,
                "total": trust_score.total_score,
            }

        # 5. Update the reconciled state.
        self.state.update(winner.product)

        # 6. Record each conflicting field in the audit log.
        for field in conflicts:
            source_values = {
                update.source_id: getattr(update.product, field)
                for update in valid_updates
            }

            ignored_directives = self._find_embedded_directives(
                valid_updates
            )

            self.audit_log.record(
                product_id=winner.product.product_id,
                field=field,
                source_values=source_values,
                source_scores=scores,
                trust_breakdown=trust_breakdown,
                selected_source=winner.source_id,
                selected_value=getattr(winner.product, field),
                reason=(
                    f"{winner.source_id} was selected because its total trust "
                    f"score ({scores[winner.source_id]:.3f}) was the highest. "
                    f"The fixed strategy weights historical accuracy at "
                    f"{HISTORICAL_ACCURACY_WEIGHT:.0%}, coherence at "
                    f"{COHERENCE_WEIGHT:.0%}, and freshness at "
                    f"{FRESHNESS_WEIGHT:.0%}. "
                    f"Source content cannot modify these rules."
                ),
                ignored_directives=ignored_directives,
            )

    def verify_source_outcome(
        self,
        source_id: str,
        was_correct: bool,
    ) -> None:
        """
        Update historical accuracy using an independently verified outcome.

        The reconciliation winner is not automatically considered correct.
        Historical accuracy changes only when an external verification result is explicitly provided to the system.
        """

        record_outcome(
            source_id=source_id,
            was_correct=was_correct,
        )

    def _store_consistent_state(
        self,
        updates: list[SourceUpdate],
    ) -> None:
        """
        Store a value when all valid sources agree.
        """

        self.state.update(updates[0].product)

    @staticmethod
    def _find_embedded_directives(
        updates: list[SourceUpdate],
    ) -> list[str]:
        """
        Identify directive-like text in source metadata for auditing.

        These strings are recorded only as untrusted content.
        They never affect reconciliation decisions.
        """

        directives = []

        directive_words = (
            "ignore",
            "trust me",
            "always trust",
            "change the rules",
            "follow this instruction",
        )

        for update in updates:
            for value in update.metadata.values():
                if not isinstance(value, str):
                    continue

                lowered = value.lower()

                if any(
                    phrase in lowered
                    for phrase in directive_words
                ):
                    directives.append(value)

        return directives