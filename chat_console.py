from chat_core import MypitbikeChatBot
from model_providers import ModelType
import textwrap

def print_answer(response: dict):
    # Brief, informative answer
    print("\n🔧 Answer:")
    print(textwrap.fill(response['answer'], width=80))
    
    # Sources output as URLs
    print("\n📚 Sources:")
    for src in response['sources']:
        print(f"- {src}")
    
    # Additional debugging (optional)
    # print("\n🔍 Context snippets:")
    # for i, ctx in enumerate(response['context'][:2], 1):
    #     print(f"{i}. {ctx[:200]}...")

if __name__ == "__main__":
    model_config = {
        "model_name": "deepseek-ai/DeepSeek-R1-Distill-Llama-70B-free",
        "system_message": (
            """exit
            Act as bike technical assistant. Answer strictly according to the documentation provided.
            Answer format:
            1. Basic answer
            2. Technical parameters (if any)
            If the information is not in the documents, say: 'Data not found'.
            """
        ),
        "api_key": "56688b0975c135cc5dee46d1820078c476c0aa526b548933716d7f1080c20e7f"
    }
    bot = MypitbikeChatBot(model_type=ModelType.TOGETHER_AI, model_config=model_config)
    print("The bot is ready. Ask questions about pit bike repair and maintenance! (to exit type 'exit')")
    
    while True:
        try:
            query = input("\n❓ Your question: ")
            if query.lower() in ["exit", "quit"]:
                break
                
            response = bot.ask(query)
            print_answer(response)
            
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"⚠️ Error: {str(e)}")
