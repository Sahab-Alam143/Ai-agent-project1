
from langchain_core.tools import tool

from rag.retrieve_policy import retrieve_policy


@tool
def return_policy_tool(query: str) -> str:
    """
    Search the return and shipping policies to answer
    customer questions about returns, refunds, and shipping.
    """
    results = retrieve_policy(query, k=3)

    if not results:
        return "No relevant policy information found."

    policy_text = []

    for result in results:
        policy_text.append(result.page_content)

    return "\n\n".join(policy_text)
