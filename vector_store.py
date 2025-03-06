from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os

def create_vector_store():
    # Initialization of embeddings with new parameters
    embeddings = OllamaEmbeddings(
        model="nomic-embed-text",
        base_url="http://localhost:11434"
    )
    
    # Loading and processing documents
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    
    docs = []
    metadatas = []
    base_url = "https://docs.mypitbike.ru/docs"
    
    for root, _, files in os.walk("processed_docs"):
        for file in files:
            if file.endswith(".md"):
                path = os.path.join(root, file)
                
                # Generate URL
                relative_path = os.path.relpath(path, "processed_docs")
                url_path = os.path.splitext(relative_path)[0]  # Remove .md extension
                url = f"{base_url}/{url_path.replace(os.sep, '/')}"  # Replace separators with "/"
                
                with open(path, "r", encoding="utf-8") as f:
                    content = f.read()
                    chunks = text_splitter.split_text(content)
                    docs.extend(chunks)
                    
                    # Add metadata for each text chunk
                    for chunk in chunks:
                        metadatas.append({
                            "source": file,
                            "url": url
                        })
    
    # Create and save vector store
    vector_store = FAISS.from_texts(
        texts=docs,
        embedding=embeddings,
        metadatas=metadatas
    )
    
    vector_store.save_local("vector_store")
    print("✅ The vector base has been successfully created!")

if __name__ == "__main__":
    create_vector_store()