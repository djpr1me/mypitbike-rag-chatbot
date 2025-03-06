from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings

# Initialize embeddings and load the vector store
embeddings = OllamaEmbeddings(model="nomic-embed-text")
vector_store = FAISS.load_local("vector_store", embeddings, allow_dangerous_deserialization=True)

# Prompt the user for a question
query = input("Please enter your question: ")

# Perform a similarity search
results = vector_store.similarity_search(query, k=3)

# Print the results
print(f"Found {len(results)} results:")
for doc in results:
    print(f"\nSource: {doc.metadata['source']}")
    print(f"Content:\n{doc.page_content[:300]}...")