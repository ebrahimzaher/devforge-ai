from config import get_llm
from prompts import CEO_SYSTEM_PROMPT

def run_ceo(user_request: str) -> str:
    llm = get_llm(kind="fast", temperature=0.2)

    response = llm.invoke(
        [
            {"role": "system", "content": CEO_SYSTEM_PROMPT},
            {"role": "user", "content": user_request},
        ]
    )

    return response.content