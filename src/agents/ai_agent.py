from utils import parse_llm_json
from config import get_llm
from prompts import AI_SYSTEM_PROMPT

def run_ai(task: str) -> dict:
    llm = get_llm(kind="code", temperature=0.2)

    response = llm.invoke(
        [
            {"role": "system", "content": AI_SYSTEM_PROMPT},
            {"role": "user", "content": task},
        ]
    )

    raw = response.content.strip()

    return parse_llm_json(raw, "AI Agent")