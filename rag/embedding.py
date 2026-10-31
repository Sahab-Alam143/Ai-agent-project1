
from langchain_ollama import OllamaEmbeddings

# Initialize embedding model
embeddings = OllamaEmbeddings(
    model="all-minilm"
)

# Generate embedding
text = "Customers can return products within 7 days."

vector = embeddings.embed_query(text)

print("Embedding generated successfully!")
print("Vector dimensions:", len(vector))
print(vector[:10])
