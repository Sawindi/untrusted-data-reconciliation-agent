from app.models import SourceUpdate


def validate_update(update: SourceUpdate) -> tuple[bool, list[str]]:
    """
    Validate an update before it enters the reconciliation process.

    Validation checks the structure and basic values of the data.
    It does not attempt to interpret instructions contained in the data.
    """

    errors: list[str] = []

    if not update.source_id:
        errors.append("Missing source ID.")

    if not update.product.product_id:
        errors.append("Missing product ID.")

    if update.product.price < 0:
        errors.append("Price cannot be negative.")

    if update.product.stock < 0:
        errors.append("Stock cannot be negative.")

    if not update.metadata:
        errors.append("Missing source metadata.")

    return len(errors) == 0, errors