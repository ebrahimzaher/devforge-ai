import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

MODELS = {
    "fast": "openai/gpt-oss-20b",
    "reasoning": "openai/gpt-oss-120b",
    "code": "openai/gpt-oss-120b",
}

def get_llm(kind: str = "reasoning", temperature: float = 0.3) -> ChatGroq:
    model_name = MODELS.get(kind, MODELS["reasoning"])
    return ChatGroq(
        model=model_name,
        api_key=GROQ_API_KEY,
        temperature=temperature,
    )