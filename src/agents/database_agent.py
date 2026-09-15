import json
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

    if raw.startswith("```"):
        raw = raw.strip("`")
        if raw.lower().startswith("json"):
            raw = raw[4:].strip()

    try:
        return json.loads(raw)
    except json.JSONDecodeError as e:
        raise ValueError(
            f"Database Agent did not return valid JSON.\nRaw output:\n{raw}"
        ) from e
