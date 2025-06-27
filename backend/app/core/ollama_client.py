from langchain_ollama import OllamaEmbeddings
from langchain_ollama.llms import OllamaLLM
from app.core.config import settings


def get_ollama_embeddings():
    return OllamaEmbeddings(model="llama3.2", base_url=settings.OLLAMA_URL)

def get_ollama_llm():
    return OllamaLLM(model="llama3.2", base_url=settings.OLLAMA_URL, temperature=0.1)

def check_ollama_connection():
    import requests
    try:
        response = requests.get(f"{settings.OLLAMA_URL}/api/tags")
        if response.status_code == 200:
            print("✅ Ollama está rodando e acessível.")
        else:
            print(f"⚠️ Ollama respondeu com status {response.status_code}")
    except Exception as e:
        print(f"❌ Falha ao conectar com Ollama: {e}")
