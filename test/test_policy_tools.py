
from unittest.mock import patch

from langchain_core.documents import Document

from tools.return_policy_tools import return_policy_tool


def test_return_policy_tool_returns_relevant_policy():
    mock_documents = [
        Document(
            page_content="Products can be returned within 7 days.",
            metadata={"policy_type": "return_policy"},
        )
    ]

    with patch(
        "tools.return_policy_tools.retrieve_policy",
        return_value=mock_documents,
    ):
        result = return_policy_tool.invoke(
            {"query": "How many days do I have to return a product?"}
        )

    assert "7 days" in result
