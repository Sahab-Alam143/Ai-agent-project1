
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

from rag.split_policy import split_policy_documents


def build_vector_store():
    """
    Build and save the policy document vector store.
    """
    documents = split_policy_documents()

    if not documents:
        raise ValueError("No policy documents found.")

    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    vector_store = Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        collection_name="return_policy",
        persist_directory="./chroma_db"
    )

    return vector_store


if __name__ == "__main__":
    store = build_vector_store()
    print("Policy vector store created successfully!")
    print("Total chunks:", store._collection.count())
