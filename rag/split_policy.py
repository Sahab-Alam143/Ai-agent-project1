
import re

from langchain_core.documents import Document
from rag.load_policy import load_policy_documents


SECTION_PATTERN = re.compile(
    r"(?m)^\s*(\d+)\.\s+([^\n]+)\s*$"
)


def split_policy_documents() -> list[Document]:
    """
    Split policy documents into numbered sections.
    Preserve the document heading and original metadata.
    """
    source_documents = load_policy_documents()
    chunks: list[Document] = []

    for document in source_documents:
        text = document.page_content.strip()
        source = document.metadata.get("source", "Unknown source")

        if not text:
            raise ValueError(f"Empty policy document: {source}")

        matches = list(SECTION_PATTERN.finditer(text))

        if not matches:
            raise ValueError(
                f"No numbered sections found in {source}"
            )

        # Preserve the policy heading as context.
        heading = text[:matches[0].start()].strip()

        for index, match in enumerate(matches):
            start = match.start()
            end = (
                matches[index + 1].start()
                if index + 1 < len(matches)
                else len(text)
            )

            section_text = text[start:end].strip()
            section_number = int(match.group(1))
            section_title = match.group(2).strip()

            chunk_text = (
                f"{heading}\n\n{section_text}"
                if heading
                else section_text
            )

            policy_type = document.metadata.get(
                "policy_type", "policy"
            )

            chunks.append(
                Document(
                    page_content=chunk_text,
                    metadata={
                        **document.metadata,
                        "section_number": section_number,
                        "section_title": section_title,
                        "chunk_id": (
                            f"{policy_type}_{section_number}"
                        ),
                    },
                )
            )

    print(f"\nTotal policy chunks created: {len(chunks)}")

    for chunk in chunks:
        print(
            f"{chunk.metadata['chunk_id']}: "
            f"{chunk.metadata['section_title']}"
        )

    return chunks


if __name__ == "__main__":
    split_policy_documents()
