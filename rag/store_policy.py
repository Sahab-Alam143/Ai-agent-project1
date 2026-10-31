
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings

from rag.split_policy import split_policy_documents


PERSIST_DIRECTORY = "./rag/vectorstore"
COLLECTION_NAME = "return_policy"


def store_policy():
    documents = split_policy_documents()

    embeddings = OllamaEmbeddings(
        model="all-minilm"
    )

    vectorstore = Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        collection_name=COLLECTION_NAME,
        persist_directory=PERSIST_DIRECTORY,
    )

    print("\nPolicy stored in ChromaDB successfully!")
    print("Total chunks:", len(documents))

    return vectorstore


if __name__ == "__main__":
    store_policy()
