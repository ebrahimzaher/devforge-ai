from utils import parse_llm_json
from config import get_llm
from prompts import DATABASE_SYSTEM_PROMPT

def run_database(task: str) -> dict:
    llm = get_llm(kind="code", temperature=0.2)

    response = llm.invoke(
        [
            {"role": "system", "content": DATABASE_SYSTEM_PROMPT},
            {"role": "user", "content": task},
        ]
    )

    raw = response.content.strip()

    return parse_llm_json(raw, "Database Agent")
