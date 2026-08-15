from app.models import ProductData


class ReconciledState:
    """
    Maintains the single source of truth produced by the agent.

    Only reconciled values are stored here. Raw source updates are
    never treated as the final state automatically.
    """

    def __init__(self) -> None:
        self._products: dict[str, ProductData] = {}

    def update(self, product: ProductData) -> None:
        """
        Store or replace the reconciled product state.
        """

        self._products[product.product_id] = product

    def get(self, product_id: str) -> ProductData | None:
        """
        Retrieve the current reconciled state for a product.
        """

        return self._products.get(product_id)

    def all_products(self) -> dict[str, ProductData]:
        """
        Return the complete reconciled state.
        """

        return self._products.copy()