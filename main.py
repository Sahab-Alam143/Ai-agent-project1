from langchain.agents import create_agent
from langchain_ollama import ChatOllama

from tools.product_tools import (
    search_products,
    compare_seller_prices,
    recommend_products,
    compare_products,
)

from tools.warranty_tools import warranty_checker

from tools.return_policy_tools import return_policy_tool


model = ChatOllama(
    model="qwen3:0.6b",
    temperature=0
)


tools = [
    search_products,
    compare_seller_prices,
    recommend_products,
    compare_products,
    warranty_checker,
    return_policy_tool,
]


system_prompt = """
You are ShopSmart, an AI e-commerce shopping assistant.

Your responsibilities:

1. Search products using search_products.
2. Recommend products using recommend_products.
3. Compare seller prices using compare_seller_prices.
4. Compare product specifications using compare_products.
5. Answer warranty questions using warranty_checker.
6. Answer return, refund and shipping questions using return_policy_tool.

Rules:

- Always use tools for product prices, ratings and warranty details.
- Never invent product prices, seller names, ratings or warranty terms.
- Recommend products based on the customer's budget and requirements.
- Explain why a product is recommended.
- When comparing products, explain differences in specifications.
- If information is missing, clearly say it is unavailable.
- The catalogue contains demo data, not verified live marketplace listings.
- Reply in the language used by the customer.
- Keep answers clear and helpful.
"""


agent = create_agent(
    model=model,
    tools=tools,
    system_prompt=system_prompt,
)


def run_assistant():
    print("=" * 55)
    print("       SHOPSMART - AI E-COMMERCE ASSISTANT")
    print("=" * 55)

    print("Ask about products, prices, warranty or policies.")
    print("Type 'exit' to close.\n")

    while True:
        query = input("You: ").strip()

        if query.lower() in ["exit", "quit", "bye"]:
            print("ShopSmart: Thank you for shopping with us!")
            break

        if not query:
            continue

        try:
            response = agent.invoke({
                "messages": [
                    {"role": "user", "content": query}
                ]
            })

            last_message = response["messages"][-1]
            answer = last_message.content

            if isinstance(answer, list):
                answer = "\n".join(
                    item.get("text", "")
                    for item in answer
                    if isinstance(item, dict)
                )

            print("\nShopSmart:", answer, "\n")

        except Exception as error:
            print("\nError:", str(error))
            print("Please try again.\n")


if __name__ == "__main__":
    run_assistant()