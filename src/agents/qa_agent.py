import json
from utils import parse_llm_json
from config import get_llm
from prompts import QA_SYSTEM_PROMPT

def run_qa(agent_type: str, task: str, code: dict) -> dict:
    llm = get_llm(kind="reasoning", temperature=0.1)

    payload = {
        "agent_type": agent_type,
        "task": task,
        "files": (code or {}).get("files", []),
    }

    response = llm.invoke(
        [
            {"role": "system", "content": QA_SYSTEM_PROMPT},
            {"role": "user", "content": json.dumps(payload)},
        ]
    )

    raw = response.content.strip()

    return parse_llm_json(raw, f"QA Agent ({agent_type})")