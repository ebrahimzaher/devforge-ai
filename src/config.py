import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

MODELS = {
    "fast": "openai/gpt-oss-20b",
    "reasoning": "openai/gpt-oss-20b",
    "code": "openai/gpt-oss-120b",
}

MAX_TOKENS = {
    "fast": 1024,
    "reasoning": 1024,
    "code": 4000,
}

def get_llm(kind: str = "reasoning", temperature: float = 0.3) -> ChatGroq:
    model_name = MODELS.get(kind, MODELS["reasoning"])
    max_tokens = MAX_TOKENS.get(kind, MAX_TOKENS["reasoning"])
    return ChatGroq(
        model=model_name,
        api_key=GROQ_API_KEY,
        temperature=temperature,
        max_tokens=max_tokens,
    )