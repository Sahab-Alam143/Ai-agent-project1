
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings


PERSIST_DIRECTORY = "./rag/vectorstore"
COLLECTION_NAME = "return_policy"


def retrieve_policy(query: str, k: int = 3):
    """Retrieve relevant policy sections for a user query."""

    embeddings = OllamaEmbeddings(
        model="all-minilm"
    )

    vectorstore = Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=embeddings,
        persist_directory=PERSIST_DIRECTORY,
    )

    results = vectorstore.similarity_search(
        query=query,
        k=k,
    )

    return results


if __name__ == "__main__":
    query = "How many days do I have to return a product?"

    results = retrieve_policy(query)

    for result in results:
        print("\nRetrieved Policy:")
        print(result.page_content)
        print("Metadata:", result.metadata)
