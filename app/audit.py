from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass
class AuditEntry:
    """
    Represents one auditable reconciliation decision.
    """

    timestamp: datetime
    product_id: str
    field: str
    source_values: dict[str, object]
    source_scores: dict[str, float]
    selected_source: str
    selected_value: object
    reason: str
    ignored_directives: list[str] = field(default_factory=list)


class AuditLog:
    """
    Stores reconciliation decisions in memory.

    The audit log records what the agent decided and why,
    making each conflict resolution explainable.
    """

    def __init__(self) -> None:
        self._entries: list[AuditEntry] = []

    def record(
        self,
        product_id: str,
        field: str,
        source_values: dict[str, object],
        source_scores: dict[str, float],
        selected_source: str,
        selected_value: object,
        reason: str,
        ignored_directives: list[str] | None = None,
    ) -> None:
        """
        Record a reconciliation decision.
        """

        entry = AuditEntry(
            timestamp=datetime.now(timezone.utc),
            product_id=product_id,
            field=field,
            source_values=source_values,
            source_scores=source_scores,
            selected_source=selected_source,
            selected_value=selected_value,
            reason=reason,
            ignored_directives=ignored_directives or [],
        )

        self._entries.append(entry)

    def entries(self) -> list[AuditEntry]:
        """
        Return all recorded audit entries.
        """

        return self._entries.copy()