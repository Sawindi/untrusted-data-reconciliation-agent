from app.agent import ReconciliationAgent
from app.sources import fetch_all_sources


def print_demo_results(agent: ReconciliationAgent) -> None:
    """
    Display the reconciled state and audit decisions.
    """

    print("\n" + "=" * 60)
    print("RECONCILIATION RESULT")
    print("=" * 60)

    product = agent.state.get("LAPTOP-001")

    if product is not None:
        print(f"Product: {product.product_id}")
        print(f"Price: £{product.price:.2f}")
        print(f"Stock: {product.stock}")

    print("\n" + "=" * 60)
    print("AUDIT LOG")
    print("=" * 60)

    for entry in agent.audit_log.entries():
        print(f"\nTimestamp: {entry.timestamp.isoformat()}")
        print(f"Product: {entry.product_id}")
        print(f"Field: {entry.field}")

        print("\nSource values:")
        for source, value in entry.source_values.items():
            print(f"  {source}: {value}")

        print("\nTrust scores:")
        for source, score in entry.source_scores.items():
            print(f"  {source}: {score:.3f}")

        print(f"\nSelected source: {entry.selected_source}")
        print(f"Selected value: {entry.selected_value}")
        print(f"Reason: {entry.reason}")

        if entry.ignored_directives:
            print("\nIgnored embedded directives:")
            for directive in entry.ignored_directives:
                print(f"  {directive}")


def main() -> None:
    """
    Run the complete reconciliation demonstration.
    """

    print("=" * 60)
    print("UNTRUSTED DATA RECONCILIATION AGENT")
    print("=" * 60)

    print("\nFetching data from independent sources...")

    updates = fetch_all_sources()

    for update in updates:
        print(
            f"\n{update.source_id}: "
            f"price=£{update.product.price:.2f}, "
            f"stock={update.product.stock}"
        )

        if update.metadata:
            print(f"Metadata: {update.metadata}")

    print("\nRunning reconciliation...")

    agent = ReconciliationAgent()
    agent.reconcile(updates)

    print_demo_results(agent)


if __name__ == "__main__":
    main()