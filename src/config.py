import os
from dotenv import load_dotenv
from langchain_ollama import ChatOllama

load_dotenv()

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen2.5-coder:7b")
OLLAMA_NUM_GPU = int(os.getenv("OLLAMA_NUM_GPU", "0"))
MAX_RETRIES = 3

MODELS = {
    "fast": OLLAMA_MODEL,
    "reasoning": OLLAMA_MODEL,
    "code": OLLAMA_MODEL,
}

MAX_TOKENS = {
    "fast": 512,
    "reasoning": 1500,
    "code": 4096,
}

REPEAT_PENALTY = {
    "fast": 1.1,
    "reasoning": 1.1,
    "code": 1.0,
}


def get_llm(kind: str = "reasoning", temperature: float = 0.3):
    model_name = MODELS.get(kind, MODELS["reasoning"])
    max_tokens = MAX_TOKENS.get(kind, MAX_TOKENS["reasoning"])
    repeat_penalty = REPEAT_PENALTY.get(kind, 1.1)

    return ChatOllama(
        model=model_name,
        base_url=OLLAMA_BASE_URL,
        temperature=temperature,
        num_predict=max_tokens,
        num_ctx=8192,
        num_gpu=OLLAMA_NUM_GPU,
        repeat_penalty=repeat_penalty,
    )