
from pathlib import Path

from langchain_core.documents import Document


# Project ke root folder ka absolute path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"

POLICY_FILES = {
    "return_policy": DATA_DIR / "return_policy.txt",
    "shipping_policy": DATA_DIR / "shipping_policy.txt",
}


def load_policy_documents() -> list[Document]:
    """
    Load return and shipping policy documents.

    Returns:
        A list of LangChain Document objects.

    Raises:
        FileNotFoundError: If a required policy file is missing.
        ValueError: If a policy file is empty.
    """
    documents: list[Document] = []

    for policy_type, file_path in POLICY_FILES.items():
        if not file_path.is_file():
            raise FileNotFoundError(
                f"Policy file not found: {file_path}\n"
                "Please create the file inside the data/ directory."
            )

        content = file_path.read_text(encoding="utf-8").strip()

        if not content:
            raise ValueError(
                f"Policy file is empty: {file_path}"
            )

        document = Document(
            page_content=content,
            metadata={
                "source": file_path.name,
                "policy_type": policy_type,
            },
        )

        documents.append(document)

        print(
            f"Loaded {file_path.name} "
            f"({len(content)} characters)"
        )

    print(f"\nTotal policy documents loaded: {len(documents)}")

    return documents


if __name__ == "__main__":
    loaded_documents = load_policy_documents()

    for document in loaded_documents:
        print("\n" + "=" * 50)
        print("Source:", document.metadata["source"])
        print("Policy type:", document.metadata["policy_type"])
        print("Preview:", document.page_content[:200])
