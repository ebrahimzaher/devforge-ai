from utils import parse_llm_json
from config import get_llm
from prompts import DATABASE_SYSTEM_PROMPT

def run_database(task: str, previous_code: dict | None = None) -> dict:
    import json
    llm = get_llm(kind="code", temperature=0.2)

    user_message = task
    if previous_code and previous_code.get("files"):
        user_message += (
            "\n\nYour previous attempt produced the following files:\n"
            + json.dumps(previous_code, indent=2)
            + "\n\nFix the issues described above and return the complete corrected JSON."
        )

    response = llm.invoke([
        {"role": "system", "content": DATABASE_SYSTEM_PROMPT},
        {"role": "user", "content": user_message},
    ])
    raw = response.content.strip()

    return parse_llm_json(raw, "Database Agent")
