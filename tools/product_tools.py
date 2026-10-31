import json
from pathlib import Path

from langchain_core.tools import tool


PROJECT_ROOT = Path(__file__).resolve().parents[1]
PRODUCT_FILE = PROJECT_ROOT / "data" / "products.json"


def load_products():
    with PRODUCT_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)


@tool
def search_products(query: str, max_price: int = 0) -> str:
    """Search products by name, category or brand. Optionally filter by maximum price."""

    products = load_products()
    query = query.lower()

    results = []

    for product in products:
        searchable = (
            product["name"] + " " +
            product["category"] + " " +
            product["brand"]
        ).lower()

        lowest_price = min(
            offer["price"]
            for offer in product["offers"]
            if offer["stock"]
        )

        if (query in searchable or query in ["all", "any", "products"]):
            if max_price == 0 or lowest_price <= max_price:
                results.append({
                    "name": product["name"],
                    "category": product["category"],
                    "lowest_price": lowest_price,
                    "rating": product["rating"],
                    "specs": product["specs"]
                })

    return json.dumps(
        results if results else {"message": "No matching products found."},
        indent=2
    )


@tool
def compare_seller_prices(product_name: str) -> str:
    """Compare prices and delivery times from different sellers for a product."""

    products = load_products()

    for product in products:
        if product_name.lower() in product["name"].lower():
            offers = sorted(
                product["offers"],
                key=lambda item: item["price"]
            )

            return json.dumps({
                "product": product["name"],
                "seller_offers": offers,
                "cheapest_seller": offers[0]["seller"],
                "lowest_price": offers[0]["price"]
            }, indent=2)

    return "Product not found."


@tool
def recommend_products(budget: int, category: str = "") -> str:
    """Recommend the best products within a budget, using rating and price."""

    products = load_products()
    recommendations = []

    for product in products:
        if category and category.lower() not in product["category"].lower():
            continue

        available_offers = [
            offer for offer in product["offers"]
            if offer["stock"]
        ]

        if not available_offers:
            continue

        cheapest = min(
            available_offers,
            key=lambda offer: offer["price"]
        )

        if cheapest["price"] <= budget:
            recommendations.append({
                "name": product["name"],
                "price": cheapest["price"],
                "seller": cheapest["seller"],
                "rating": product["rating"],
                "warranty": product["warranty"],
                "specs": product["specs"]
            })

    recommendations.sort(
        key=lambda item: item["rating"],
        reverse=True
    )

    return json.dumps(
        recommendations if recommendations else {
            "message": "No products found within this budget."
        },
        indent=2
    )


@tool
def compare_products(product_names: list[str]) -> str:
    """Compare the specifications, rating, warranty and lowest price of selected products."""

    products = load_products()
    comparison = []

    for name in product_names:
        for product in products:
            if name.lower() in product["name"].lower():
                available_offers = [
                    offer for offer in product["offers"]
                    if offer["stock"]
                ]

                if available_offers:
                    cheapest = min(
                        available_offers,
                        key=lambda offer: offer["price"]
                    )

                    comparison.append({
                        "name": product["name"],
                        "price": cheapest["price"],
                        "seller": cheapest["seller"],
                        "rating": product["rating"],
                        "warranty": product["warranty"],
                        "specs": product["specs"]
                    })

                break

    return json.dumps(
        comparison if comparison else {
            "message": "No matching products found."
        },
        indent=2
    )