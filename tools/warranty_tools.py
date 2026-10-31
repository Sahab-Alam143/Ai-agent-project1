import json

from langchain_core.tools import tool

from tools.product_tools import load_products


@tool
def warranty_checker(product_name: str) -> str:
    """Check warranty duration, coverage, exclusions and claim process for a product."""

    products = load_products()

    for product in products:
        if product_name.lower() in product["name"].lower():
            return json.dumps({
                "product": product["name"],
                "warranty": product["warranty"],
                "coverage": product["warranty_coverage"],
                "exclusions": product["warranty_exclusions"],
                "claim_steps": product["warranty_claim_steps"]
            }, indent=2)

    return "Warranty information not found for this product."