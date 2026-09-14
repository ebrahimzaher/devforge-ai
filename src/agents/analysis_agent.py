import json
from config import get_llm
from prompts import ANALYSIS_SYSTEM_PROMPT

def run_analysis(brief: str) -> dict:
    llm = get_llm(kind="reasoning", temperature=0.2)
 
    response = llm.invoke(
        [
            {"role": "system", "content": ANALYSIS_SYSTEM_PROMPT},
            {"role": "user", "content": brief},
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
            f"Analysis Agent did not return valid JSON.\nRaw output:\n{raw}"
        ) from e