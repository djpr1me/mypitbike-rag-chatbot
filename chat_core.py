from langchain.chains import RetrievalQA
from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings
from langchain.prompts import PromptTemplate
from model_providers import ModelFactory, ModelType
import re

class MypitbikeChatBot:
    def __init__(self, model_type=ModelType.OLLAMA_LOCAL, model_config=None):
        # Store configuration for later use
        self.config = model_config or {}
        # Save current model name from config for conditional cleaning
        self.current_model_name = self.config.get("model_name", "")
        # Set flag to remove <think> blocks only if using DeepSeek R1 via Together AI
        self.use_think_clean = False
        if model_type == ModelType.TOGETHER_AI and self.current_model_name == "deepseek-ai/DeepSeek-R1-Distill-Llama-70B-free":
            self.use_think_clean = True

        # Initializing LLM with ModelFactory
        self.llm = ModelFactory(
            model_type=model_type, 
            **(model_config or {})
        ).get_llm()
        
        # Load vector store
        self.embeddings = OllamaEmbeddings(model="nomic-embed-text")
        self.vector_store = FAISS.load_local("vector_store", self.embeddings, allow_dangerous_deserialization=True)
        
        # Prompt template
        self.prompt = PromptTemplate.from_template(
            """
            Context: {context}
            
            Question: {question}
            
            Answer in English using the data from the context without introspective commentary or thoughts. 
            If there is no answer in the context, write so.
            """
        )
        
        # Initialize QA chain
        self.qa = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.vector_store.as_retriever(search_kwargs={"k": 4}),
            return_source_documents=True,
            chain_type_kwargs={"prompt": self.prompt}
        )

    def clean_response(self, response: str) -> str:
        # Remove <think>...</think> blocks from the response
        clean_response = re.sub(r'<think>.*?</think>', '', response, flags=re.DOTALL)
        return clean_response.strip()
    
    def ask(self, question: str) -> dict:
        # The primary method for questions
        result = self.qa.invoke({"query": question})
        answer = result['result']
        # Apply cleaning only if flag is set
        if self.use_think_clean:
            answer = self.clean_response(answer)
        return self._format_response(answer, result)
    
    def _format_response(self, answer: str, result: dict) -> dict:
        # Extract URLs from metadata
        sources = [doc.metadata['url'] for doc in result['source_documents']]
        return {
            "answer": answer,
            "sources": sources,
            "context": [doc.page_content for doc in result['source_documents']]
        }
