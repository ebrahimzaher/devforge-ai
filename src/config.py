import os
from dotenv import load_dotenv
from langchain_ollama import ChatOllama

load_dotenv()

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen2.5:3b-instruct")

MODELS = {
    "fast": OLLAMA_MODEL,
    "reasoning": OLLAMA_MODEL,
    "code": OLLAMA_MODEL,
}

MAX_TOKENS = {
    "fast": 512,
    "reasoning": 768,
    "code": 1500,
}


def get_llm(kind: str = "reasoning", temperature: float = 0.3):
    model_name = MODELS.get(kind, MODELS["reasoning"])
    max_tokens = MAX_TOKENS.get(kind, MAX_TOKENS["reasoning"])

    return ChatOllama(
        model=model_name,
        base_url=OLLAMA_BASE_URL,
        temperature=temperature,
        num_predict=max_tokens,
        num_ctx=4096,
    )