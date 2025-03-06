from enum import Enum
from langchain_ollama import OllamaLLM
from langchain_together import ChatTogether

class ModelType(Enum):
    OLLAMA_LOCAL = "ollama_local"
    TOGETHER_AI = "together_ai"

class ModelFactory:
    def __init__(self, model_type: ModelType, **kwargs):
        self.model_type = model_type
        self.config = kwargs

    def get_llm(self):
        if self.model_type == ModelType.OLLAMA_LOCAL:
            return OllamaLLM(
                model=self.config["model_name"],
                base_url="http://localhost:11434",
                temperature=0.3,
                system_message=self.config.get("system_message", "")
            )
        
        elif self.model_type == ModelType.TOGETHER_AI:
            return ChatTogether(
                model="deepseek-ai/DeepSeek-R1-Distill-Llama-70B-free",
                together_api_key=self.config["api_key"],
                temperature=self.config.get("temperature", 0.7)
            )

        raise ValueError("Unsupported model type")
